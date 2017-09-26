## Verlet Physics system modelled after
## http://www.gamedev.net/page/resources/_/technical/math-and-physics/a-verlet-based-approach-for-2d-game-physics-r2714
## http://archive.gamedev.net/reference/programming/features/verletPhys/
##
## Geoffrey Matthews
## 2011

import numpy as N
import pygame
eulerDampingFactor = 0.98

def _getvec(a, i):
    return a[i*3:i*3+3]
def _setvec(a, i, val):
    a[i*3:i*3+3] = val

def _intervalDistance(min1, max1, min2, max2):
    if (min1 < min2):
        return min2 - max1
    else:
        return min1 - max2

class ParticleSystem():
    def __init__(self, positions, velocities, masses, time = 0.0, collisions=True):
        self.positions = N.array(positions)
        self.oldpositions = N.array(())
        self.velocities = N.array(velocities)
        self.masses = N.array(masses)
        self.n = len(masses)
        self.pins = N.array([False for i in range(self.n)])
        self.dims = self.n*3
        assert(len(self.positions) == self.dims)
        assert(len(self.velocities) == self.dims)
        self.forces = N.zeros(self.dims)
        self.computeForces = []
        self.constraints = []
        self.posderivs = N.zeros(self.dims)
        self.velderivs = N.zeros(self.dims)
        self.collisions = collisions
        self.euler = False
        self.eulerDamping = False
        self.time = time

    def ClearForces(self):
        self.forces *= 0.0;

    def mass(self, i):
        return self.masses[i]
    def setMass(self, i, val):
        self.masses[i] = val
    def pos(self, i):
        return _getvec(self.positions, i)
    def oldpos(self, i):
        return _getvec(self.oldpositions, i)
    def setPos(self, i, val):
        _setvec(self.positions, i, val)
    def incPos(self, i, val):
        _setvec(self.positions, i, val + self.pos(i))
    def dist2(self, i, j):
        v = self.pos(i) - self.pos(j)
        return N.dot(v,v)
    def dist(self, i, j):
        return N.sqrt(self.dist2(i,j))
    def vel(self, i):
        return _getvec(self.velocities, i)
    def setVel(self, i, val):
        _setvec(self.velocities, i, val)
    def force(self, i):
        return _getvec(self.forces, i)
    def setForce(self, i, val):
        _setvec(self.forces, i, val)
    def incForce(self, i, val):
        _setvec(self.forces, i, val + self.force(i))
    def posDeriv(self, i):
        return _getvec(self.posderivs, i)
    def setPosDeriv(self, i, val):
        _setvec(self.posderivs, i, val)
    def velDeriv(self, i):
        return _getvec(self.velderivs, i)
    def setVelDeriv(self, i, val):
        _setvec(self.velderivs, i, val)

    #### Forces

    def applyForce(self, force):
        if force[0] == "spring":
            f,i,j,k,d = force
            if self.pins[i]: return
            v = self.pos(i) - self.pos(j)
            actuald = N.sqrt(N.dot(v,v))
            amt = (actuald-d)/actuald
            newforce = -k*amt*v
            self.incForce(i, newforce)
            self.incForce(j, -newforce)
        elif force[0] == "gravity":
            f,i,j,k = force
            if self.pins[i]: return
            v = self.pos(j) - self.pos(i)
            mi = self.mass(i)
            mj = self.mass(j)
            dist2 = N.dot(v,v)
            newforce = (k*mi*mj)*v/dist2
            self.incForce(i, newforce)
            self.incForce(j, -newforce)
        elif force[0] == "drag":
            f,i,k = force
            if self.pins[i]: return
            self.incForce(i, -k*self.vel(i))
        elif force[0] == "constant":
            f,i,v,k = force
            if self.pins[i]: return
            self.incForce(i, k*v)
        else:
            print "Unknown force: " + force[0]

    #### Constraints

    def moveToDist(self, i, j, targetdist):
        v = self.pos(i) - self.pos(j)
        dist = N.sqrt(N.dot(v, v))
        factor = (dist-targetdist)/dist
        if not(self.pins[i]) and not(self.pins[j]):
            self.setPos(i, self.pos(i) - 0.5*v*factor)
            self.setPos(j, self.pos(j) + 0.5*v*factor)
        elif self.pins[i]:
            self.setPos(j, self.pos(j) + v*factor)
        elif self.pins[j]:
            self.setPos(i, self.pos(i) - v*factor)

    def applyConstraint(self, constr):
        if constr[0] == "stick":
            c,i,j,targetdist = constr
            self.moveToDist(i,j,targetdist)
        elif constr[0] == "triangle":
            c,i,j,k,dij,djk,dki = constr
            self.moveToDist(i,j,dij)
            self.moveToDist(j,k,djk)
            self.moveToDist(k,i,dki)
        elif constr[0] == "pin":
            c,i,x,y,z = constr
            self.setPos(i, (x,y,z))
        else:
            print "Unknown constraint: " + constr[0]          

    def makeDrag(self, i, k):
        self.computeForces.append(("drag", i, k))
    def makeConstant(self, i, v, k):
        self.computeForces.append(("constant", i, v, k))
    def makePin(self, i):
        x,y,z = self.pos(i)
        self.pins[i] = True
        self.constraints.append(("pin", i, x,y,z))
    def makeStick(self, i, j):
        self.constraints.append(("stick", i, j, self.dist(i,j)))
    def makeSpring(self, i, j, k, dist):
        self.computeForces.append(("spring", i, j, k, dist))

    def makeTriangle(self, i, j, k):
        self.constraints.append(("triangle", i, j, k,
                                 self.dist(i,j),
                                 self.dist(j,k),
                                 self.dist(k,i)))
    def makeSquare(self, i, j, k, l):
        self.makeTriangle(i,j,k)
        self.makeTriangle(j,k,l)                            

    #######  Verlet integrator

    def ParticleDeriv(self):
        self.ClearForces()
        for force in self.computeForces:
            self.applyForce(force)
        self.posderivs = self.velocities[:]
        for i in range(self.n):
            self.setVelDeriv(i, self.force(i)/self.mass(i))
        

    def Step(self, deltaT):
        if len(self.oldpositions) == 0 or self.euler:
            if self.eulerDamping:
                self.velocities *= eulerDampingFactor
            self.oldpositions = self.positions
            self.ParticleDeriv()
            self.positions = self.positions + self.posderivs*deltaT
            self.velocities = self.velocities + self.velderivs*deltaT
        else:
            posdiffs = self.positions - self.oldpositions
            self.oldpositions = self.positions
            self.ParticleDeriv()
            self.positions = self.positions + posdiffs + self.velderivs*deltaT*deltaT
            posdiffs = self.positions - self.oldpositions
            self.velocities = posdiffs/deltaT
        if self.collisions:
            for i in range(1):
                self.HandleCollisions()
        for i in range(1):
            for constr in self.constraints:
                self.applyConstraint(constr)
        self.time += deltaT

        
    ###### Collisions
        
    def Edges(self, triangle):
        c,i,j,k,dij,djk,dki = self.constraints[triangle]
        return [(i,j), (j,k), (k,i)]

    def EdgeNorm(self, edge):
        v = self.pos(edge[1]) - self.pos(edge[0])
        v /= N.sqrt(N.dot(v,v))
        return N.array((-v[1], v[0], v[2]))

    def ProjectToAxis(self, triangle, axis):
        c,i,j,k,dij,djk,dki = self.constraints[triangle]
        pi = N.dot(self.pos(i), axis)
        pj = N.dot(self.pos(j), axis)
        pk = N.dot(self.pos(k), axis)
        minp = min(pi,pj,pk)
        maxp = max(pi,pj,pk)
        return (minp, maxp)

    def ClosestPoint(self, tri1, tri2):
        c1,i1,j1,k1,dij1,djk1,dki1 = self.constraints[tri1]
        c2,i2,j2,k2,dij2,djk2,dki2 = self.constraints[tri2]
        center = (self.pos(i2)+self.pos(j2)+self.pos(k2))/3.0
        mind = N.dot(self.pos(i1), center)
        minp = i1
        d = N.dot(self.pos(j1), center)
        if d < mind:
            mind = d
            minp = j1
        d = N.dot(self.pos(k1), center)
        if d < mind:
            mind = d
            minp = j1
        return (minp, mind)

    def DetectCollision(self, tri1, tri2):
        minDistance = 1.0e20
        collisionNormal = None
        collisionEdge = None
        edgeTri = None
        pointTri = None
        if self.constraints[tri1][0] != "triangle": return False
        if self.constraints[tri2][0] != "triangle": return False
        e1 = self.Edges(tri1)
        e2 = self.Edges(tri2)
        for i,e in enumerate(e1 + e2):
            axis = self.EdgeNorm(e)
            min1,max1 = self.ProjectToAxis(tri1, axis)
            min2,max2 = self.ProjectToAxis(tri2, axis)
            dist = _intervalDistance(min1,max1, min2,max2)
            if dist > 0.0:
                return False
            if (abs(dist) < minDistance):
                minDistance = abs(dist)
                collisionNormal = axis
                collisionEdge = e
                if i < 3:
                    edgeTri = tri1
                    pointTri = tri2
                else:
                    edgeTri = tri2
                    pointTri = tri1
        point, dist = self.ClosestPoint(pointTri, edgeTri)
        c1,i1,j1,k1,dij1,djk1,dki1 = self.constraints[pointTri]
        c2,i2,j2,k2,dij2,djk2,dki2 = self.constraints[edgeTri]
        massPointTri = self.mass(i1)+self.mass(j1)+self.mass(k1)
        massEdgeTri = self.mass(i2)+self.mass(j2)+self.mass(k2)
        return (point, collisionEdge, collisionNormal, minDistance,
                massPointTri, massEdgeTri)

    def ProcessCollision(self, collision):
        point, edge, normal, dist, massPointTri, massEdgeTri = collision
        pointFactor = massEdgeTri/(massPointTri+massEdgeTri)
        edgeFactor = 1.0 - pointFactor
        self.incPos(point, -normal*dist*pointFactor)
        v1 = self.pos(point) - self.pos(edge[0])
        v2 = self.pos(edge[1]) - self.pos(edge[0])
        t = N.sqrt(N.dot(v1,v1)/N.dot(v2,v2))
        m0 = self.mass(edge[0])
        m1 = self.mass(edge[1])
        m = m0/(m0+m1)
        lmb = 1.0/(t*t*m + (1.0-t)*(1.0-t)*(1.0-m))
        self.incPos(edge[0], (1.0-t)*lmb*normal*dist*edgeFactor)
        self.incPos(edge[1], (t)*lmb*normal*dist*edgeFactor)

    def HandleCollisions(self):
        n = len(self.constraints)
        for i in range(0, n-1):
            for j in range(i+1, n):
                collision = self.DetectCollision(i,j)
                if collision:
                    self.ProcessCollision(collision)

    ##########  Drawing
                    
    def DrawLine(self, screen, i, j, a, b, color, w):
        x1 = int(self.pos(i)[a])
        y1 = int(self.pos(i)[b])
        x2 = int(self.pos(j)[a])
        y2 = int(self.pos(j)[b])
        pygame.draw.line(screen, color, (x1,y1), (x2,y2), w)
        
    def Draw(self, screen, color=(255,0,0), a=0, b=1):
        for force in self.computeForces:
            if force[0] == "spring" :
                f,i,j,k,d = force
                self.DrawLine(screen, i, j, a, b, (0,0,0), 1)
        for constr in self.constraints:
            if constr[0] == "stick":
                c,i,j,d = constr
                self.DrawLine(screen, i, j, a, b, (0,0,0), 3)
            elif constr[0] == "triangle":
                c,i,j,k,dij,djk,dki = constr
                self.DrawLine(screen, i,j,a,b, (0,0,0), 3)
                self.DrawLine(screen, j,k,a,b, (0,0,0), 3)
                self.DrawLine(screen, k,i,a,b, (0,0,0), 3)
                
        for i in range(self.n):
            s = 2 * int(N.sqrt(self.mass(i)))
            x = self.pos(i)[a]
            y = self.pos(i)[b]
            pygame.draw.circle(screen, color, (int(x), int(y)), s)
        
    
    
    
    


    
