import numpy as N
import pygame

def _getvec(a, i):
    return a[i*3:i*3+3]
def _setvec(a, i, val):
    a[i*3:i*3+3] = val

class ParticleSystem():
    def __init__(self, positions, velocities, masses, time = 0.0):
        self.positions = N.array(positions)
        self.oldpositions = None # for Verlet integration
        self.velocities = N.array(velocities)
        self.masses = N.array(masses)
        self.n = len(masses)
        self.dims = self.n*3
        assert(len(self.positions) == self.dims)
        assert(len(self.velocities) == self.dims)
        self.forces = N.zeros(self.dims)
        self.posderivs = N.zeros(self.dims)
        self.velderivs = N.zeros(self.dims)
        self.time = time

    def ClearForces(self):
        self.forces *= 0.0;

    def mass(self, i):
        return self.masses[i]
    def setMass(self, i, val):
        self.masses[i] = val
    def pos(self, i):
        return _getvec(self.positions, i)
    def setPos(self, i, val):
        _setvec(self.positions, i, val)
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

    def Draw(self, screen, color=(255,0,0), a=0, b=1, time=False, pairs=False):
        if time:
            t = self.time*10.0
        if pairs and not time:
            for i in range(0, self.n, 2):
                x1 = int(self.pos(i)[a])
                y1 = int(self.pos(i)[b])
                x2 = int(self.pos(i+1)[a])
                y2 = int(self.pos(i+1)[b])
                pygame.draw.line(screen, (0,0,0), (x1,y1), (x2,y2))
        for i in range(self.n):
            s = 2 + int(self.mass(i))
            if time:
                x = t
                y = self.pos(i)[a]
            else:
                x = self.pos(i)[a]
                y = self.pos(i)[b]
            pygame.draw.circle(screen, color, (int(x), int(y)), s)
        
def ParticleDeriv(psystem, computeForces):
    psystem.ClearForces()
    for force in computeForces:
        force(psystem)
    psystem.posderivs = psystem.velocities[:]
    for i in range(psystem.n):
        psystem.setVelDeriv(i, psystem.force(i)/psystem.mass(i))
        
def EulerStep(psystem, computeForces, deltaT):
    ParticleDeriv(psystem, computeForces)
    psystem.positions += psystem.posderivs*deltaT
    psystem.velocities += psystem.velderivs*deltaT
    psystem.time += deltaT

def MidpointStep(p1, computeForces, deltaT):
    ParticleDeriv(p1, computeForces)
    newpos = p1.positions + p1.posderivs*deltaT/2.0
    newvel = p1.velocities + p1.velderivs*deltaT/2.0
    p2 = ParticleSystem(newpos, newvel, p1.masses)
    ParticleDeriv(p2, computeForces)
    p1.positions += p2.posderivs*deltaT
    p1.velocities += p2.velderivs*deltaT
    p1.time += deltaT

def RungeKuttaStep(p1, computeForces, deltaT):
    ParticleDeriv(p1, computeForces)
    newpos = p1.positions + p1.posderivs*deltaT/2.0
    newvel = p1.velocities + p1.velderivs*deltaT/2.0
    p2 = ParticleSystem(newpos, newvel, p1.masses)
    ParticleDeriv(p1, computeForces)
    newpos = p1.positions + p2.posderivs*deltaT/2.0
    newvel = p1.velocities + p2.velderivs*deltaT/2.0
    p3 = ParticleSystem(newpos, newvel, p1.masses)
    ParticleDeriv(p3, computeForces)
    newpos = p1.positions + p3.posderivs*deltaT
    newvel = p1.velocities + p3.velderivs*deltaT
    p4 = ParticleSystem(newpos, newvel, p1.masses)
    ParticleDeriv(p4, computeForces)
    posd = p1.posderivs/6.0+p2.posderivs/3.0+p3.posderivs/3.0+p4.posderivs/6.0
    veld = p1.velderivs/6.0+p2.velderivs/3.0+p3.velderivs/3.0+p4.velderivs/6.0
    p1.positions += posd*deltaT
    p1.velocities += veld*deltaT
    p1.time += deltaT

def VerletStep(psystem, computeForces, deltaT):
    if psystem.oldpositions == None:
        psystem.oldposiions = psystem.positions
        EulerStep(psystem, computeForces, deltaT)
    else:
        ParticleDeriv(psystem, computeForces)
        posdiffs = psystem.positions - psystem.oldpositions
        psystem.oldpositions = psystem.positions
        psystem.positions += posdiffs + psystem.velderivs*deltaT*deltaT
        psystem.time += deltaT
        
        
    
    
    
    


    
