#!/usr/bin/python
# $Id: steam.py,v 1.30 2006/04/22 09:05:54 alex Exp $

import math
import md5
import os
import os.path
import pickle
import pygame
import random
import sys

from OpenGL.GL import *
from OpenGL.GLU import *

import collide
import font
import res

STEAM_TTL = 8000

class Sprite:
    def __init__(self, texture, pos=(0,0)):
        if type(texture) == str:
            texture = res.getTexture(texture)
        self.tex, self.width, self.height, self.u, self.v \
            = texture.tex, texture.width, texture.height, texture.u, texture.v
        self.hx, self.hy = self.width/2, self.height/2
        self.pos = pos
        self.list = glGenLists(1)
        glNewList(self.list, GL_COMPILE)
        glBegin(GL_QUADS)
        glTexCoord(0, 0)
        glVertex(-self.hx, -self.hy)
        glTexCoord(0, self.v)
        glVertex(-self.hx, self.hy)
        glTexCoord(self.u, self.v)
        glVertex(self.hx, self.hy)
        glTexCoord(self.u, 0)
        glVertex(self.hx, -self.hy)
        glEnd()
        glEndList()

    def draw(self, x=None, y=None):
        glBindTexture(GL_TEXTURE_2D, self.tex)
        if x == None or y == None:
            self.drawQuad(self.pos[0], self.pos[1])
        else:
            self.drawQuad(x, y)

    def drawQuad(self, x, y):
        glPushMatrix()
        glTranslate(x, y, 0)
        glCallList(self.list)
        glPopMatrix()

class MetalBehaviour(collide.Behaviour):
    def __init__(self, dropGrid, steamGrid):
        self.grids = [dropGrid, steamGrid]
    
    def respondDrop(self, collider, point):
        return self.DROP_BOUNCE

    def respondSteam(self, collider, point, ttl):
        if random.random() < 1 - ttl / float(STEAM_TTL):
            # TODO
            game.droplets.addDroplet(point[0], point[1], collider)
            return self.STEAM_CONDENSE
        else:
            return self.STEAM_BOUNCE

class WoodBehaviour(collide.Behaviour):
    def __init__(self, dropGrid, steamGrid):
        self.grids = [dropGrid, steamGrid]

    def respondDrop(self, collider, point):
        return self.DROP_BOUNCE

    def respondSteam(self, collider, point, ttl):
        return self.STEAM_BOUNCE

class VaporiseBehaviour(collide.Behaviour):
    def __init__(self, dropGrid, steamGrid):
        self.grids = [dropGrid, steamGrid]

    def respondDrop(self, collider, point):
        game.particles.addParticle(point)
        return self.DROP_REMOVE

    def respondSteam(self, collider, point, ttl):
        return self.STEAM_BOUNCE

class PlaceableObject(collide.PolygonCollider):
    DRAG_NULL = 0
    DRAG_TRANSLATE = 1
    DRAG_ROTATE = 2

    def __init__(self, width, height, texture, behaviour=None):
        collide.PolygonCollider.__init__(self, 
                                         [(0, 0), (-1, -1), (0, -1)], 
                                         behaviour)
        self.width, self.height = width, height
        # Start off-screen
        self.x, self.y = -width, -height
        if texture:
            self.sprite = Sprite(texture)
        self.rotation = 0
        self.rotationHandleSprite = Sprite('rot_handle.png')
        self.moveHandleSprite = Sprite('move_handle.png')
        self.dragOp = self.DRAG_NULL

        self.selectable = True
        self.hoverable = True
        self.rotatable = True

    def clear(self):
        collide.PolygonCollider.clear(self)

    def remove(self):
        # Need to update first because typically just moved, so grid
        # position wrt bbox is wrong
        self.updateGrids()
        self.removeGrids()

    def setPosition(self, x, y):
        self.x, self.y = x, y
        self.updateCollisionPolygon()

    def setRotation(self, rotation):
        self.rotation = rotation
        self.updateCollisionPolygon()

    def updateCollisionPolygon(self):
        # Yes this is very verbose and could be done in a couple of lines
        # but it would be really embarassing to make a mistake here!
        hx, hy = self.width/2, self.height/2
        rads = self.rotation*math.pi/180
        points = [
            [-hx, -hy], 
            [hx,  -hy],
            [hx,   hy],
            [-hx,  hy]]
        rotMatrix = (
            (math.cos(rads), -math.sin(rads)),
            (math.sin(rads), math.cos(rads)))
        for point in points:
            x, y = point
            point[0] = x*rotMatrix[0][0] + y*rotMatrix[0][1]
            point[1] = x*rotMatrix[1][0] + y*rotMatrix[1][1]
        for point in points:
            point[0] += self.x
            point[1] += self.y
        self.setPoints(points)

    def draw(self):
        #glDisable(GL_TEXTURE_2D)
        glPushMatrix()
        glTranslate(self.x, self.y, 0)
        glRotate(self.rotation, 0, 0, 1)
        self.sprite.draw(0, 0)
        glPopMatrix()
        #glColor(0.8, 1.0, 0.9, 1.0)
        #glBegin(GL_POLYGON)
        #for point in self.points:
        #    glTexCoord(point[0] / 100.0, point[1] / 100.0)
        #    glVertex(point[0], point[1], 0)
        #glEnd()
        #glEnable(GL_TEXTURE_2D)

    def drawSelection(self):
        radius = max(self.width, self.height)/2 + 10

        glPushMatrix()
        glTranslate(self.x, self.y, 0)
        """
        # Draw faint circle around object
        circlePoints = 20
        glDisable(GL_TEXTURE_2D)
        glColor(0.7,0.7,0.7,0.8)
        glBegin(GL_LINE_LOOP)
        for i in range(circlePoints):
            angle = float(i) / circlePoints * 2 * math.pi
            glVertex(math.cos(angle) * radius, math.sin(angle) * radius)
        glEnd()
        glEnable(GL_TEXTURE_2D)
        """

        # Draw rotation handles
        if self.rotatable:
            glRotate(self.rotation, 0, 0, 1)
            for i in range(4):
                angle = float(i) / 4 * 2 * math.pi + math.pi/4
                glPushMatrix()
                glTranslate(math.cos(angle) * radius, 
                            math.sin(angle) * radius, 0)
                glRotate(float(i)/4 * 360 - 45, 0, 0, 1)
                self.rotationHandleSprite.draw()
                glPopMatrix()
        else:
            self.moveHandleSprite.draw()
            
        glPopMatrix()

    def keepHover(self, x, y):
        """ There is some tolerance when mouse moves out of selection before
            dropping it """
        radius2 = (max(self.width, self.height)/2 + 25)**2
        return (x-self.x)**2 + (y-self.y)**2 < radius2

    def beginDrag(self, x, y, alternateButton):
        if self.containsPoint(x, y):
            self.dragOp = self.DRAG_TRANSLATE
            self.dragOffset = x - self.x, y - self.y
        elif self.rotatable:
            self.dragOp = self.DRAG_ROTATE
            self.dragOffsetAngle = math.atan2(y-self.y, x-self.x)*180/math.pi \
                                    - self.rotation

    def continueDrag(self, x, y):
        if self.dragOp == self.DRAG_TRANSLATE:
            self.x, self.y = x - self.dragOffset[0], y - self.dragOffset[1]
        elif self.dragOp == self.DRAG_ROTATE:
            self.rotation = math.atan2(y-self.y, x-self.x)*180/math.pi \
                                - self.dragOffsetAngle
        self.updateCollisionPolygon()

    def completeDrag(self, x, y):
        self.dragOp = self.DRAG_NULL
        self.updateGrids()

class LineStrip(collide.LineStripCollider):
    POINT_RENDER_SIZE = 4

    def __init__(self, points, texture, behaviour):
        collide.LineStripCollider.__init__(self, points, behaviour)
        self.hoverable = True
        self.selectable = True
        self.displayList = glGenLists(1)
        texture = res.getTexture(texture)
        self.tex, w, h, u, v \
            = texture.tex, texture.width, texture.height, texture.u, texture.v
        self.textureU, self.textureV = w/u, h/v
        self.triangulate()

    def triangulate(self):
        glNewList(self.displayList, GL_COMPILE)
        tess = gluNewTess()
        gluTessCallback(tess, GLU_TESS_BEGIN, self.triangulateBegin)
        gluTessCallback(tess, GLU_TESS_END, self.triangulateEnd)
        gluTessCallback(tess, GLU_TESS_VERTEX, self.triangulateVertex)
        gluTessCallback(tess, GLU_TESS_COMBINE, self.triangulateCombine)
        data = [[point[0], point[1], 0] for point in self.points]
        gluTessBeginPolygon(tess, self)
        gluTessBeginContour(tess)
        for point in data:
            gluTessVertex(tess, point, point)
        gluTessEndContour(tess)
        gluTessEndPolygon(tess)
        gluDeleteTess(tess)
        glEndList()

    def triangulateBegin(self, type):
        glBegin(type)

    def triangulateVertex(self, data):
        glTexCoord(data[0]/float(self.textureU), data[1]/float(self.textureV))
        glVertex(data)

    def triangulateEnd(self):
        glEnd()

    def triangulateCombine(self, position, vertices, weights):
        return position

    def containsPoint(self, x, y):
        if self.getNodePointAt(x, y) is not None:
            return True
        return False
    
    def getNodePointAt(self, x, y):
        sz = self.POINT_RENDER_SIZE
        for point in self.points:
            if x >= point[0]-sz and x <= point[0]+sz and \
               y >= point[1]-sz and y <= point[1]+sz:
                return point
        return None

    def draw(self, selected=False):
        glBindTexture(GL_TEXTURE_2D, self.tex)
        glCallList(self.displayList)

        if selected:
            glDisable(GL_TEXTURE_2D)
            glColor(0, 0, 1)
            glBegin(GL_LINE_STRIP)
            for point in self.points:
                glVertex(point[0], point[1], 0)
            glEnd()
            sz = self.POINT_RENDER_SIZE
            glColor(1, 0, 0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glBegin(GL_QUADS)
            for point in self.points:
                glVertex(point[0]-sz, point[1]-sz)
                glVertex(point[0]+sz, point[1]-sz)
                glVertex(point[0]+sz, point[1]+sz)
                glVertex(point[0]-sz, point[1]+sz)
            glEnd()
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glEnable(GL_TEXTURE_2D)

    def drawSelection(self):
        self.draw(True)

    def remove(self):
        self.updateGrids()
        self.removeGrids()

    def keepHover(self, x, y):
        return self.containsPoint(x, y)

    def beginDrag(self, x, y, alternateButton):
        if alternateButton or len(self.points) == 1:
            # Create new node
            self.dragPoint = [x, y]
            if self.getNodePointAt(x, y) == self.points[0]:
                # At start
                otherPoint = self.points[0]
                self.points.insert(0, self.dragPoint)
            else:
                # At end
                otherPoint = self.points[-1]
                self.points.append(self.dragPoint)
            self.colliders.append(collide.SegmentCollider(self.dragPoint, 
                                                          otherPoint, 
                                                          self.behaviour))
        else:
            self.dragPoint = self.getNodePointAt(x, y)
        self.dragOffset = x - self.dragPoint[0], y - self.dragPoint[1]

    def continueDrag(self, x, y):
        self.dragPoint[0] = x - self.dragOffset[0]
        self.dragPoint[1] = y - self.dragOffset[1]
        self.triangulate()

    def completeDrag(self, x, y):
        self.updateGrids()
        self.interactiveGrid.updateCollider(self, self.getBoundingBox())

    def addToGrid(self, grid):
        if grid is game.interactiveGrid:
            # hack override to collide with nodes, not lines
            self.interactiveGrid = grid
            grid.addCollider(self, self.getBoundingBox())
        else:
            collide.LineStripCollider.addToGrid(self, grid)

    def getBoundingBox(self):
        # Only used for interactive (realtime is segments)
        x1, y1, x2, y2 = (self.points[0][0], self.points[0][1],
                          self.points[0][0], self.points[0][1])
        for point in self.points:
            x1 = min(x1, point[0])
            y1 = min(y1, point[1])
            x2 = max(x2, point[0])
            y2 = max(y2, point[1])
        return x1, y1, x2, y2

class MetalObject(PlaceableObject):
    def __init__(self, x, y, behaviour):
        PlaceableObject.__init__(self, 90, 20, 'metal.png', behaviour)
        self.setPosition(x, y)

class WoodObject(PlaceableObject):
    def __init__(self, x, y, behaviour):
        PlaceableObject.__init__(self, 90, 20, 'wood.png', behaviour)
        self.setPosition(x, y)

class HotplateObject(PlaceableObject):
    def __init__(self, x, y, behaviour):
        PlaceableObject.__init__(self, 90, 20, 'hotplate.png', behaviour)
        self.setPosition(x, y)

class KettleObject(PlaceableObject):
    def __init__(self, x, y):
        self.sprite = Sprite('kettle.png')
        PlaceableObject.__init__(self, self.sprite.width, 
                                 self.sprite.height, None)
        self.setPosition(x, y)
        self.rotatable = False
        self.particleOffset = -25,5
        self.particleOrigin = (self.x + self.particleOffset[0], 
                               self.y + self.particleOffset[1])

    def continueDrag(self, x, y):
        PlaceableObject.continueDrag(self, x, y)
        self.particleOrigin = (self.x + self.particleOffset[0], 
                               self.y + self.particleOffset[1])

class PlantBehaviour(collide.Behaviour):
    def __init__(self, plant, dropGrid):
        self.plant = plant
        self.grids = [dropGrid]
        self.rotatable = False

    def respondDrop(self, collider, point):
        self.plant.dropCount += 1
        return self.DROP_REMOVE

class PlantObject(PlaceableObject):
    potAttachment = (0,13)
    def __init__(self, x, y, dropGrid):
        self.potSprite = Sprite('pot.png')
        PlaceableObject.__init__(self, self.potSprite.width, 20, None,
                                 PlantBehaviour(self, dropGrid))
        self.setPosition(x, y)
        self.rotatable = False
        self.plantSegmentSprite = Sprite('plant_seg.png')
        self.plantFlowerSprite = Sprite('flower.png')
        self.segments = 5
        self.clear()

    def clear(self):
        PlaceableObject.clear(self)
        self.dropCount = 0
        self.droop = 30
        self.dropCountDeriv = 0.0

    def isSatisfied(self):
        return self.droop < 0.5

    def draw(self):
        glPushMatrix()
        glTranslate(self.x, self.y, 0)
        glColor(1, 1, 1, 1)     # XXX or turn off modulate for this tex?
        self.potSprite.draw()
        glBindTexture(GL_TEXTURE_2D, self.plantSegmentSprite.tex)
        glTranslate(self.potSprite.pos[0] + self.potAttachment[0],
                    self.potSprite.pos[1] + self.potAttachment[1], 0)
        advance = self.plantSegmentSprite.hy-2
        for i in range(self.segments):
            glRotate(self.droop, 0, 0, 1)
            glTranslate(0, advance, 0)
            self.plantSegmentSprite.drawQuad(0, 0)
            glTranslate(0, advance, 0)
        self.plantFlowerSprite.draw()
        glPopMatrix()

    def update(self, millis):
        if millis == 0:
            return
        # Some kind of derivative fall-off function which jumped into my head
        # and I can't really explain now.
        self.dropCountDeriv = self.dropCountDeriv * 0.8 \
                                    + self.dropCount / float(millis) * 0.1

        # LERP from 0 to 30 degrees for 2 drips/sec to 0 drips/sec
        targetDroop = max(min(30 - self.dropCountDeriv*1000/2*30, 30), 0)

        # Constant velocity to target droop
        e = 0.5
        if self.droop < targetDroop - e:
            self.droop += 0.003 * millis
        elif self.droop > targetDroop + e:
            self.droop -= 0.003 * millis
        self.dropCount = 0


        
class Droplets:
    X=0
    Y=1
    DX=2
    DY=3
    COLLIDER=4
    COMMITTED=5
    DEBUG=6
    def __init__(self, filename, acceleration, 
                 tangentAcceleration, drag, count):
        texture = res.getTexture(filename)
        self.tex, self.width, self.height, self.u, self.v \
            = texture.tex, texture.width, texture.height, texture.u, texture.v
        self.acceleration = acceleration
        self.tangentAcceleration = tangentAcceleration
        self.drag = drag
        self.count = count
        self.droplets = []
        self.radius = max(self.width/2, self.height/2)

        self.list = glGenLists(1)
        glNewList(self.list,  GL_COMPILE)
        glBegin(GL_QUADS)
        glTexCoord(0, 0)
        glVertex(-self.radius, -self.radius)
        glTexCoord(0, self.v)
        glVertex(-self.radius, self.radius)
        glTexCoord(self.u, self.v)
        glVertex(self.radius, self.radius)
        glTexCoord(self.u, 0)
        glVertex(self.radius, -self.radius)
        glEnd()
        glEndList()

    def addDroplet(self, x, y, collider):
        if len(self.droplets) < self.count:
            self.droplets.append([x, y, 0, 0, collider, False, None])

    def clear(self):
        self.droplets = []

    def draw(self):
        glBindTexture(GL_TEXTURE_2D, self.tex)
        lastx, lasty = 0, 0
        glPushMatrix()
        for x, y, dx, dy, collider, committed, debug in self.droplets:
            glTranslate(x-lastx, y-lasty, 0)
            lastx, lasty = x, y
            glCallList(self.list) 
        glPopMatrix()
        
    def update(self, millis, grid):
        for drop in self.droplets:
            collided = False
            # If the drop is sliding along a collider, do collision with that
            # collider first to make sure that
            #  a) it's still nearby (haven't fallen off the edge)
            #  b) the drop velocity is tangent to the collider's edge
            if drop[self.COLLIDER]:
                collision = drop[self.COLLIDER].collideSphere(drop[self.X], 
                                                   drop[self.Y], 
                                                   self.radius)
                if collision:
                    penetration, tangent, nearest, collider = collision
                    tx, ty = tangent
                    # Find direction of tangent closest to acceleration
                    dot = tx*self.acceleration[0] + \
                          ty*self.acceleration[1]
                    if dot < 0:
                        tx, ty = -tx, -ty
                    # Normalize tangent
                    mag = math.sqrt(tx**2 + ty**2)
                    tx, ty = tx/mag, ty/mag
                    if ty == 0:
                        # Tangent is horizontal, just drop the particle
                        drop[self.DX] = 0
                        drop[self.DY] = 0
                        drop[self.COLLIDER] = None
                    else:
                        # Velocity along tangent. randomness prevents clumping
                        a = random.random() * 0.5 + 0.5  
                        ddy = self.tangentAcceleration * ty * millis * a
                        ddx = self.tangentAcceleration * tx * millis * a
                        dx = drop[self.DX] + ddx
                        dy = drop[self.DY] + ddy
                        drop[self.DX] = dx
                        drop[self.DY] = dy

                        # Ray-test the new trajectory with other colliders and
                        # possibly transfer the drop to another collider.
                        # Don't do this if we just switched to a new collider
                        # (committed)
                        if not drop[self.COMMITTED]:
                            x2 = drop[self.X] + dx * millis
                            y2 = drop[self.Y] + dy * millis
                            # TODO ignore drop's collider early
                            collisions = grid.collideRay(
                                            drop[self.X], drop[self.Y], x2, y2)
                            for collision in collisions:
                                penetration, tangent, nearest, collider \
                                    = collision
                                if collider is not drop[self.COLLIDER]:
                                    # Have slid along to the intersection with
                                    # another collider.  Switch over to the
                                    # new collider and stop so the next frame
                                    # will have the correct velocity.
                                    drop[self.COLLIDER] = collider
                                    drop[self.COMMITTED] = True
                                    drop[self.X], drop[self.Y] = nearest
                                    drop[self.DX] = 0
                                    drop[self.DY] = 0
                                    break
                        else:
                            drop[self.COMMITTED] = False
                else:
                    # No longer colliding, make it free-fall
                    drop[self.COLLIDER] = None

            if not drop[self.COLLIDER]:
                # Free-falling
                # Check for intersection in this time-step by approximating
                # trajectory to a ray
                dx = drop[self.DX] + self.acceleration[0] * millis
                dy = drop[self.DY] + self.acceleration[1] * millis
                dx -= dx * self.drag[0] * millis
                dy -= dy * self.drag[1] * millis
                x2 = drop[self.X] + dx * millis
                y2 = drop[self.Y] + dy * millis
                collisions = grid.collideRay(drop[self.X], drop[self.Y],
                                                 x2, y2)
                collision = grid.closestCollision(collisions)
                if collision and dx**2 + dy**2 > 0:
                    # Found ray collision.. bounce or slide or vaporize
                    penetration, tangent, nearest, collider = collision
                    response = collider.respondDrop(collider, nearest)
                    if response == collide.Behaviour.DROP_REMOVE:
                        # Filter at end of loop will deactivate it
                        drop[self.Y] = -20  
                    elif response == collide.Behaviour.DROP_BOUNCE:
                        # Make sure normal is opposite dir to velocity
                        nx, ny = -tangent[1], tangent[0]
                        mag = math.sqrt(nx**2 + ny**2)
                        nx, ny = nx/mag, ny/mag
                        dot = nx*dx + ny*dy
                        if dot > 0:
                            nx, ny = -nx, -ny
                            dot *= -1
                        rx = dx - 2 * nx * dot
                        ry = dy - 2 * ny * dot
                        drop[self.DX] = rx * 0.9
                        drop[self.DY] = ry * 0.9
                        # A bit dodgy.. warp droplet to collision point
                        drop[self.X], drop[self.Y] = nearest
                    else:
                        assert False
                        
                drop[self.DX] += self.acceleration[0] * millis
                drop[self.DY] += self.acceleration[1] * millis
                drop[self.DX] -= drop[self.DX] * self.drag[0] * millis
                drop[self.DY] -= drop[self.DY] * self.drag[1] * millis
            drop[self.X] += drop[self.DX] * millis
            drop[self.Y] += drop[self.DY] * millis
        # TODO is this best way to remove/deactivate dead drops?
        self.droplets = [drop for drop in self.droplets if drop[self.Y] > 0]


class Particles:
    # Each particle is array indexed with:
    X=0
    Y=1
    DX=2
    DY=3
    ACTIVE=4
    TTL=5
    SCALE=6
    CONDENSED=7
    
    def __init__(self, filename, 
                 count, rate, lifetime, origin, velocity, velocitySigma,
                 scaleVelocity, buoyancy, buoyancyAcceleration):
        """ rate: millis between particle creation """
        self.origin = origin
        self.velocity = velocity
        self.velocitySigma = velocitySigma
        self.buoyancyAcceleration = buoyancyAcceleration
        self.buoyancy = buoyancy
        self.scaleVelocity = scaleVelocity
        self.rate = rate
        self.lifetime = lifetime
        self.particles = [[0, 0, 0, 0, False, 0, 1.0, False] for i in range(count)]
        texture = res.getTexture(filename)
        self.tex, self.width, self.height, self.u, self.v \
            = texture.tex, texture.width, texture.height, texture.u, texture.v
        self.particleWaitTime = 0
        self.radius=max(self.width/2, self.height/2)
        self.producers = []
        self.producerIndex = 0
        self.originQueue = []

        self.list = glGenLists(1)
        hx = self.width/2
        hy = self.height/2
        glNewList(self.list, GL_COMPILE)
        glBegin(GL_QUADS)
        glTexCoord(0, 0)
        glVertex(-hx, -hy)
        glTexCoord(0, self.v)
        glVertex(-hx, hy)
        glTexCoord(self.u, self.v)
        glVertex(hx, hy)
        glTexCoord(self.u, 0)
        glVertex(hx, -hy)
        glEnd() 
        glEndList()

    def addParticle(self, point):
        self.originQueue.append(point)

    def clear(self):
        self.producers = []
        self.originQueue = []
        for particle in self.particles:
            particle[self.ACTIVE] = False

    def draw(self):
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        glBindTexture(GL_TEXTURE_2D, self.tex)
        for x, y, dx, dy, active, ttl, scale, condensed in self.particles:
            if not active:
                continue
            glPushMatrix()
            glColor(1, 1, 1, max(scale,1.0) * float(ttl)/self.lifetime)
            glTranslate(x, y, 0)
            glScale(scale, scale, 1)
            glCallList(self.list)
            glPopMatrix()
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_REPLACE)

    def update(self, millis, grid):
        self.particleWaitTime += millis
        particlesToAdd = self.particleWaitTime / self.rate * \
                         min(1, len(self.producers)) + len(self.originQueue)
        self.particleWaitTime -= self.rate * particlesToAdd
        for particle in self.particles:
            if not particle[self.ACTIVE] and particlesToAdd > 0:
                if self.originQueue:
                    origin = self.originQueue.pop()
                else:
                    self.producerIndex += 1
                    if self.producerIndex >= len(self.producers):
                        self.producerIndex = 0
                    origin = self.producers[self.producerIndex].particleOrigin
                particle[self.X] = origin[0]
                particle[self.Y] = origin[1]
                # TODO: performance of gauss vs uniform?
                particle[self.DX] = \
                    random.gauss(self.velocity[0], self.velocitySigma[0])
                particle[self.DY] = \
                    random.gauss(self.velocity[1], self.velocitySigma[1])
                particle[self.ACTIVE] = True
                particle[self.TTL] = self.lifetime
                particle[self.SCALE] = 0.0
                particle[self.CONDENSED] = False
                particlesToAdd -= 1
            elif not particle[self.ACTIVE]:
                continue

            # This test is a roundabout way of discouraging particles that
            # are bouncing against a wall from being buoyant.
            if particle[self.SCALE] > 0.5:
                u = millis*self.buoyancyAcceleration
                particle[self.DX] = particle[self.DX]*(1-u) + u*self.buoyancy[0]
                particle[self.DY] = particle[self.DY]*(1-u) + u*self.buoyancy[1]
            particle[self.X] += particle[self.DX] * millis
            particle[self.Y] += particle[self.DY] * millis
            particle[self.TTL] -= millis
            particle[self.SCALE] += self.scaleVelocity * millis
            # TODO: filter out closest collision earlier
            collisions = grid.collideSphere(particle[self.X], 
                                         particle[self.Y],
                                         particle[self.SCALE]*self.radius)
            collision = grid.closestCollision(collisions)
            if collision:
                penetration, tangent, nearestPoint, collider = collision
                # Find tangent direction closest to velocity
                dot = tangent[0]*particle[self.DX] \
                    + tangent[1]*particle[self.DY]
                if dot < 0:
                    tangent = -tangent[0], -tangent[1]
                # Normalize against current velocity
                mag = math.sqrt(tangent[0]**2 + tangent[1]**2)
                tangent = tangent[0]/mag, tangent[1]/mag
                mag = math.sqrt(particle[self.DX]**2 + particle[self.DY]**2)
                tangent = tangent[0]*mag, tangent[1]*mag
                particle[self.DX] = particle[self.DX]*0.2 + tangent[0]*0.8
                particle[self.DY] = particle[self.DY]*0.2 + tangent[1]*0.8
                sz = particle[self.SCALE]*self.radius + penetration
                particle[self.SCALE] = sz/self.radius
                # Some chance that a particle hitting a condensable surface
                # will condense.
                if not particle[self.CONDENSED]:
                    response =  collider.respondSteam(collider, nearestPoint,
                                                      particle[self.TTL])
                    # When a steam particle condenses into a droplet it
                    # doesn't get removed from the world (it looks ugly),
                    # instead it is marked as having condensed, and can't
                    # condense again until it is reincarnated.
                    if response == collide.Behaviour.STEAM_CONDENSE:
                        particle[self.CONDENSED] = True
            if particle[self.TTL] < 0:
                particle[self.ACTIVE] = False

class Widget(collide.PolygonCollider):
    def __init__(self, pos, width, height):
        x, y = pos
        self.x, self.y = x, y
        hx, hy = width/2, height/2
        collide.PolygonCollider.__init__(self, [
            (x-hx, y-hy), (x+hx, y-hy), (x+hx, y+hy), (x-hx, y+hy)])

        self.selectable = False
        self.hoverable = False

    def draw(self):
        pass

    def keepHover(self, x, y):
        return False
    
    def drawSelection(self):
        pass

    def beginDrag(self, x, y, alternateButton):
        pass

    def continueDrag(self, x, y):
        pass

    def completeDrag(self, x, y):
        pass

class Button(Widget):
    def __init__(self, pos, image, func):
        self.sprite = Sprite(image, pos)
        Widget.__init__(self, pos, self.sprite.width, self.sprite.height) 
        self.func = func

    def draw(self):
        self.sprite.draw()

    def beginDrag(self, x, y, alternateButton):
        self.func()

class TextButton(Widget):
    def __init__(self, pos, fnt, text, func, align=font.LEFT):
        width, height = fnt.textWidth(text), fnt.lineSize
        if align == font.LEFT:
            Widget.__init__(self, (pos[0]+width/2, pos[1]), width, height)
        elif align == font.CENTER:
            Widget.__init__(self, (pos[0], pos[1]), width, height)
        elif align == font.RIGHT:
            Widget.__init__(self, (pos[0]-width/2, pos[1]), width, height)
        self.func = func
        self.font = fnt
        self.text = text
        self.pos = pos
        self.align = align
        self.hoverable = True

    def draw(self):
        if game.hoverObject == self:
            self.font.draw(self.text, self.pos, align=self.align,
                           color=(0, 0.4, 0))
        else:
            self.font.draw(self.text, self.pos, align=self.align)

    def keepHover(self, x, y):
        return False

    def beginDrag(self, x, y, alternateButton):
        self.func()

class Tool(Button):
    def __init__(self, objectClass, factoryMethod, 
                 button, disabled, active, pos, allowed=True):
        Button.__init__(self, pos, button, None)

        self.disabledSprite = Sprite(disabled, pos)
        self.activeSprite = Sprite(active, pos)
        self.objectClass = objectClass
        self.factoryMethod = factoryMethod
        self.active = False
        self.disabled = not allowed
        self.stock = 1

        self.shadow = None

    def managesObject(self, object):
        return object.__class__ == self.objectClass

    def decrementStock(self):
        self.stock = max(self.stock-1, -1)
        game.level.stocks = game.getStocks()

    def incrementStock(self):
        self.stock += 1
        game.level.stocks = game.getStocks()

    def draw(self):
        if self.active or game.highlightTool is self:
            self.activeSprite.draw()

        if self.disabled or self.stock == 0:
            self.disabledSprite.draw()
        else:
            self.sprite.draw()

        if self.stock > 0:
            game.smallFont.draw('%d' % self.stock, 
                                (self.x-38, self.y + 5),
                                align=font.CENTER,
                                valign=font.BOTTOM)
                            

    def drawShadow(self):
        """ Shadow is what appears when tool is selected and mouse hovering
        in work area """
        if self.shadow:
            self.disabledSprite.draw(self.shadow[0], self.shadow[1])

    def drawSelection(self):
        pass

    def place(self, x, y):
        self.factoryMethod(x, y)
        if self.stock > 0:
            self.stock -= 1
        game.selectTool(None)

    def replace(self):
        if self.stock >= 0:
            self.stock += 1
        
    def beginDrag(self, x, y, alternateButton):
        if self.disabled or self.stock == 0:
            return
        if game.selectedTool == self:
            game.selectTool(None)
        else:
            game.selectTool(self)

    def continueDrag(self, x, y):
        pass

    def completeDrag(self, x, y):
        pass

class LevelButton(Button):
    def __init__(self, pos, level):
        self.texture = level.getThumbnailTexture()
        Button.__init__(self, pos, self.texture, lambda: game.play(level))
        self.level = level

    def draw(self):
        if self.sprite.pos[1] > game.windowSize[1]:
            return
        Button.draw(self)
        game.smallFont.draw('Level %d' % (self.level.sequence + 1),
                            pos=(self.sprite.pos[0], self.sprite.pos[1] - \
                                              self.texture.height/2 - 20),
                            align=font.CENTER) 
class Level:
    def __init__(self, filename=None):
        self.objects = []
        self.producers = []
        self.plants = []
        self.stocks = {} 
        self.filename = filename
        self.thumbnail = None
        if filename:
            self.load(filename)
        else:
            if len(game.levels) > 0:
                self.sequence = game.levels[-1].sequence + 1
            else:
                self.sequence = 0
            num = 1
            while os.path.exists('levels/level%02d.lvl' % num):
                num += 1
            self.filename = 'levels/level%02d.lvl' % num

    def saveBehaviour(self, behaviour):
        for key, val in game.behaviours.items():
            if val == behaviour:
                return key
        return None

    def save(self):
        p = {
            'objects': [],
            'stocks': self.stocks,
            'sequence': self.sequence
        }
        for object in self.objects:
            rep = {}
            if isinstance(object, LineStrip):
                rep['type'] = 'LineStrip'
                rep['points'] = object.points
                rep['texture'] = object.texture
                rep['behaviour'] = self.saveBehaviour(object.behaviour)
            elif isinstance(object, PlaceableObject):
                rep['type'] = 'PlaceableObject'
                rep['subtype'] = str(object.__class__)
                rep['pos'] = object.x, object.y
                rep['rotation'] = object.rotation
            p['objects'].append(rep)
        pickle.dump(p, open(self.filename, 'w'))

    def load(self, filename):
        self.filename = filename
        p = pickle.load(open(self.filename, 'r'))
        for rep in p['objects']:
            if rep['type'] == 'LineStrip':
                object = LineStrip(rep['points'], 
                                   rep['texture'],
                                   game.behaviours[rep['behaviour']])
                self.objects.append(object)
            elif rep['type'] == 'PlaceableObject':
                x, y = rep['pos']
                if rep['subtype'] == '__main__.MetalObject':
                    object = MetalObject(x, y, game.behaviours['metal'])
                elif rep['subtype'] == '__main__.WoodObject':
                    object = WoodObject(x, y, game.behaviours['wood'])
                elif rep['subtype'] == '__main__.HotplateObject':
                    object = HotplateObject(x, y, game.behaviours['vaporise'])
                elif rep['subtype'] == '__main__.KettleObject':
                    object = KettleObject(x, y)
                    self.producers.append(object)
                elif rep['subtype'] == '__main__.PlantObject':
                    object = PlantObject(x, y, game.dropGrid)
                    self.plants.append(object)
                object.setRotation(rep['rotation'])
                self.objects.append(object)
        self.stocks = p['stocks']
        self.sequence = p['sequence']

    def getCode(self):
        # Here's an abuse of hashing you never thought you'd see!
        hash = md5.new()
        hash.update(self.filename)
        bytes = hash.digest()
        chars = 'ABCDEFGHJKLMNPQR'
        code = ''
        for byte in bytes:
            code += chars[(ord(byte)>>4) & 0xf]
            code += chars[ord(byte) & 0xf]
        return code

    def getThumbnailTexture(self):
        if not self.thumbnail:
            w, h = 256, 256
            windowW, windowH = game.windowSize
            windowW = 680 # don't need tool shelf
            oldLevel = game.level
            game.level = self
            game.loadFrameEnabled = True
            game.frameEnabled = False
            glScale(float(w)/windowW, float(h)/windowH, 1)
            game.display(False)
            glLoadIdentity()
            game.level = oldLevel
            game.loadFrameEnabled = False
            game.frameEnabled = True

            tex = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, tex)
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glCopyTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 0, 0, w, h, 0)
            h /= float(windowW)/windowH
            self.thumbnail = res.Texture(tex, w, h, 1.0, 1.0)
        return self.thumbnail

class Game:
    def __init__(self):
        self.quit = False
        self.windowSize = (800, 600)
        self.windowAspect = float(self.windowSize[0]) / self.windowSize[1]
        self.workspaceMaxX = 655

    def clear(self):
        self.tools = []
        self.ui = []
        self.plants = []
        self.selectedTool = None
        self.highlightTool = None
        self.selectedObject = None
        self.hoverObject = None
        self.droplets.clear()
        self.particles.clear()
        self.dropGrid.clear()
        self.steamGrid.clear()
        self.interactiveGrid.clear()
        self.placedObjects = []
        self.level = None
        self.menuing = False
        self.choosingLevel = False
        self.editing = False
        self.playing = False
        self.satisfied = False
        self.frameEnabled = True
        self.loadFrameEnabled = False

    def editNew(self):
        level = Level()
        self.levels.append(level)
        self.edit(level)

    def editFirst(self):
        self.edit(self.levels[0])

    def playFirst(self):
        self.play(self.levels[0])

    def editNext(self):
        idx = self.levels.index(self.level)
        self.edit(self.levels[idx + 1])

    def playNext(self):
        idx = self.levels.index(self.level)
        if idx < len(self.levels) - 1:
            self.play(self.levels[idx + 1])
        else:
            self.menu()

    def editPrevious(self):
        idx = self.levels.index(self.level)
        self.edit(self.levels[idx - 1])

    def menu(self):
        self.clear()
        self.frameEnabled = False
        self.level = Level()
        self.menuing = True

        self.addWidget(TextButton((778, 140), self.smallFont,
                       'New Game', self.playFirst, align=font.RIGHT))
        self.addWidget(TextButton((775, 100), self.smallFont,
                       'Skip to Level', self.chooseLevel, align=font.RIGHT))
        self.addWidget(TextButton((770, 60), self.smallFont,
                       'Sandpit', self.playFree, align=font.RIGHT))
        self.addWidget(TextButton((765, 20), self.smallFont, 
                       'Level Editor', self.editFirst, align=font.RIGHT))

    def createTools(self):
        self.tools = [
            Tool(MetalObject, self.placeMetalObject, 
                 'tool_metal.png', 'toold_metal.png', 'tool_active.png',
                 (720,542)),
            Tool(WoodObject, self.placeWoodObject,
                 'tool_wood.png', 'toold_wood.png', 'tool_active.png',
                 (720,456)),
            Tool(HotplateObject, self.placeHotplateObject,
                 'tool_hotplate.png', 'toold_hotplate.png', 'tool_active.png',
                 (720,370)),
            Tool(KettleObject, self.placeKettleObject,
                 'tool_kettle.png', 'toold_kettle.png', 'tool_active.png',
                 (720,284)),
            Tool(PlantObject, self.placePlantObject,
                 'tool_plant.png', 'toold_plant.png', 'tool_active.png',
                 (720,198)),
            Tool(LineStrip, self.placeLineStrip,
                 'tool_lines.png', 'toold_lines.png', 'tool_active.png',
                 (720,112)),
        ]

    def chooseLevel(self):
        self.addLevelButtons(0)

    def addLevelButtons(self, startAt):
        self.clear()
        self.level = Level()
        winW, winH = self.windowSize
        thumbW, thumbH = 256, 256
        cols = 3
        rows = 2
        xspace = (winW%thumbW) / (cols + 1)
        yspace = (winH%thumbH) / (rows + 1)
        x = xspace + thumbW/2
        y = winH - (yspace + thumbH/2)
        self.levelButtons = []
        for level in self.accessibleLevels[startAt:startAt+cols*rows]:
            self.levelButtons.append(LevelButton((x, y), level))
            x += thumbW + xspace
            if x + thumbW/2 > winW:
                x = xspace + thumbW/2
                y -= thumbH + yspace
        for button in self.levelButtons:
            self.addWidget(button)
        if len(self.accessibleLevels) - startAt - rows*cols > 0:
            self.createButton((770, 20), 'spin_down.png', self.scrollLevelDown)
        if startAt > 0:
            self.createButton((770, 580), 'spin_up.png', self.scrollLevelUp)
        self.frameEnabled = False
        self.choosingLevel = True

        self.levelStartAt = startAt

    def scrollLevelUp(self):
        self.addLevelButtons(self.levelStartAt - 3)

    def scrollLevelDown(self):
        self.addLevelButtons(self.levelStartAt + 3)

    def playFree(self):
        self.clear()
        self.level = Level()
        self.createTools()

        for tool in self.tools:
            tool.stock = -1
            tool.addToGrid(self.interactiveGrid)

    def play(self, level):
        self.clear()
        self.level = level
        self.playing = True
        self.createTools()

        for tool in self.tools:
            if str(tool.objectClass) in self.level.stocks:
                tool.stock = self.level.stocks[str(tool.objectClass)]
            else:
                tool.stock = 0
        self.tools = [tool for tool in self.tools if tool.stock != 0]
        for tool in self.tools:
            tool.addToGrid(self.interactiveGrid)
        
        for object in self.level.objects:
            object.clear()
            object.updateGrids()

        self.particles.producers += self.level.producers
        self.plants += self.level.plants

    def edit(self, level):
        self.clear()
        self.level = level
        self.editing = True
        self.createTools()
        
        for tool in self.tools:
            tool.addToGrid(self.interactiveGrid)
            if str(tool.objectClass) in self.level.stocks:
                tool.stock = self.level.stocks[str(tool.objectClass)]
            else:
                tool.stock = -1
            self.createButton((tool.x + 50, tool.y + 10), 'spin_up.png',
                              tool.incrementStock)
            self.createButton((tool.x + 50, tool.y - 10), 'spin_down.png',
                              tool.decrementStock)

        self.createButton((775, 20), 'save.png', self.saveAll)
        self.createButton((745, 20), 'new.png', self.editNew)
        idx = self.levels.index(self.level) 
        if idx < len(self.levels) -1:
            self.createButton((715, 20), 'right.png', self.editNext)
            self.createButton((780, 70), 'spin_up.png', self.moveLevelForward)
        if idx > 0:
            self.createButton((685, 20), 'left.png', self.editPrevious)
            self.createButton((780, 50), 'spin_down.png', self.moveLevelBack)
            
        for object in self.level.objects:
            object.clear()
            object.addToGrid(self.interactiveGrid)
            object.updateGrids()
        self.particles.producers += self.level.producers
        self.plants += self.level.plants

    def init(self):
        pygame.display.init()
        pygame.display.set_caption('Nelly\'s Rooftop Garden')
        pygame.display.gl_set_attribute(pygame.GL_ALPHA_SIZE, 8)
        surface = pygame.display.set_mode(self.windowSize, 
                                          pygame.DOUBLEBUF |\
                                          pygame.OPENGL)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.windowSize[0], 0, self.windowSize[1], -10, 10)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.smallFont = font.Font('babelfish.ttf', 36)
        
        self.frame = Sprite('frame.png')
        self.loadFrame = Sprite('loadframe.png')
        self.frame.pos = (400, 300)
        self.loadFrame.pos = (400, 300)
        self.loadFrameBack = Sprite('loadframeback.png')
        self.loadFrameBack.pos = (400, 300)
        self.dialog = Sprite('dialog.png')
        self.dialog.pos = (330, 155)
        self.menuBackground = Sprite('menu.png')
        self.menuBackground.pos = (400, 300)
        self.levelBackground = Sprite('loadback.png')
        self.levelBackground.pos = (400, 300)

        self.dropGrid = collide.UniformGridCollider(800, 600, 30, 30)
        self.steamGrid = collide.UniformGridCollider(800, 600, 30, 30)
        self.interactiveGrid = collide.UniformGridCollider(800, 600, 10, 10)

        self.behaviours = {
            'metal': MetalBehaviour(self.dropGrid, self.steamGrid),
            'wood':  WoodBehaviour(self.dropGrid, self.steamGrid),
            'vaporise': VaporiseBehaviour(self.dropGrid, self.steamGrid)
        }

        self.particles = Particles('steam.png', 
                                   count=500, 
                                   rate=20, 
                                   lifetime=STEAM_TTL,
                                   origin=(400, 50), 
                                   velocity=(0, 0.05),
                                   velocitySigma=(0.01, 0.01),
                                   buoyancy=(0,0.05),
                                   buoyancyAcceleration=0.0005,
                                   scaleVelocity=0.0004)

        self.droplets = Droplets('drip.png',
                                 count=500,
                                 tangentAcceleration=0.00006,
                                 acceleration=(0,-0.0006),
                                 drag=(0.0005, 0))
        self.plants = []
        self.clear()

        self.levels = []
        for root, dirs, files in os.walk('.'):
            self.levels += [Level(os.path.join(root, file)) \
                            for file in files \
                            if file[-4:] == '.lvl']
        self.resequenceLevels()

        self.accessibleLevels = []
        self.loadProgress()

    def openProgressFile(self, mode):
        try:
            return open(os.path.expanduser('~/.nelly.savegame'), mode)
        except Exception:
            return None

    def saveProgress(self):
        file = self.openProgressFile('w')
        if file:
            for level in self.accessibleLevels:
                file.write('%s\n' % level.getCode())

    def loadProgress(self):
        self.accessibleLevels = []
        file = self.openProgressFile('r')
        nextseq = 0
        if file:
            codes = [line.strip() for line in file.readlines()]
            for level in self.levels:
                if level.getCode() in codes:
                    self.accessibleLevels.append(level)
        if not self.accessibleLevels:
            self.accessibleLevels.append(self.levels[0])

    def allowNextLevel(self, level):
        nextseq = level.sequence + 1
        if nextseq < len(self.levels) and \
            self.levels[nextseq] not in self.accessibleLevels:
            self.accessibleLevels.append(self.levels[nextseq])
            self.saveProgress()

    def resequenceLevels(self):
        # Fix broken sequence numbers
        self.levels.sort(lambda x,y: cmp(x.sequence, y.sequence))
        i = 0
        for level in self.levels:
            level.sequence = i
            i += 1

    def getStocks(self):
        stocks = {}
        for tool in self.tools:
            stocks[str(tool.objectClass)] = tool.stock
        return stocks

    def moveLevelBack(self):
        self.level.sequence -= 1.1
        self.resequenceLevels()
        self.edit(self.level)
        pass

    def moveLevelForward(self):
        self.level.sequence += 1.1
        self.resequenceLevels()
        self.edit(self.level)
        pass

    def saveAll(self):
        for level in self.levels:
            level.save()

    def createButton(self, pos, image, func):
        button = Button(pos, image, func)
        self.addWidget(button)

    def addWidget(self, widget):
        widget.addToGrid(self.interactiveGrid)
        self.ui.append(widget)

    def placeMetalObject(self, x, y):
        self.placeObject(MetalObject(x, y, self.behaviours['metal']))


    def placeWoodObject(self, x, y):
        self.placeObject(WoodObject(x, y, self.behaviours['wood']))

    def placeHotplateObject(self, x, y):
        self.placeObject(HotplateObject(x, y, self.behaviours['vaporise']))

    def placeKettleObject(self, x, y):
        obj = KettleObject(x, y)
        self.placeObject(obj)
        if self.editing:
            self.level.producers.append(obj)
        self.particles.producers.append(obj)

    def placePlantObject(self, x, y):
        obj = PlantObject(x, y, self.dropGrid)
        self.placeObject(obj)
        self.plants.append(obj)

    def placeLineStrip(self, x, y):
        obj = LineStrip([(x, y)], 'brick.jpg', self.behaviours['metal'])
        self.placeObject(obj)

    def placeObject(self, object):
        self.selectedObject = object
        self.selectedObject.addToGrid(self.interactiveGrid)
        if self.editing:
            self.level.objects.append(self.selectedObject)
        else:
            self.placedObjects.append(self.selectedObject)

    def removeObject(self, object):
        object.remove()
        self.selectedObject = None
        if isinstance(object, KettleObject):
            self.particles.producers.remove(object)
        if self.editing:
            self.level.objects.remove(object)
        else:
            self.placedObjects.remove(object)
        self.getTool(object).replace()
        self.interactiveGrid.updateCollider(object, object.getBoundingBox())
        self.interactiveGrid.removeCollider(object, object.getBoundingBox())
        
    def selectTool(self, tool):
        if self.selectedTool:
            self.selectedTool.active = False
            self.selectedTool.shadow = None
        self.selectedTool = tool
        if self.selectedTool:
            self.selectedTool.active = True

    def getTool(self, object):
        for tool in self.tools:
            if tool.managesObject(object):
                return tool
        return None

    def update(self, millis):
        # TODO move grid into particles, droplets?
        self.particles.update(millis, self.steamGrid)
        self.droplets.update(millis, self.dropGrid)
        satisfied = True
        for plant in self.plants:
            plant.update(millis)
            if not plant.isSatisfied():
                satisfied = False
        if self.playing and satisfied:
            self.satisfied = True
            self.interactiveGrid.clear()
            self.createButton((435, 85), 'dialog_ok.png', self.playNext)
            self.allowNextLevel(self.level)
            self.saveProgress()

    def display(self, finalPass=True):
        if not finalPass:
            glClearColor(0, 0, 0, 0)
        else:
            glClearColor(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        if self.menuing:
            self.menuBackground.draw()
        elif self.choosingLevel:
            self.levelBackground.draw()
        elif self.loadFrameEnabled:
            self.loadFrameBack.draw()
        self.particles.draw()
        self.droplets.draw()
        for object in self.level.objects:
            object.draw()
        for object in self.placedObjects:
            object.draw()

        if self.selectedTool:
            self.selectedTool.drawShadow()

        if self.selectedObject:
            self.selectedObject.drawSelection()
        elif self.hoverObject:
            self.hoverObject.drawSelection()

        if self.frameEnabled:
            self.frame.draw()
        elif self.loadFrameEnabled:
            self.loadFrame.draw()
        for tool in self.tools:
            tool.draw()
            
        if self.editing:
            self.smallFont.draw('Level %d' % (self.level.sequence + 1),
                                pos=(760, 50),
                                align=font.RIGHT)
        elif self.playing:
            self.smallFont.draw('Level %d' % (self.level.sequence + 1),
                                pos=(780, 20),
                                align=font.RIGHT)

        if self.satisfied:
            self.dialog.draw()
            self.smallFont.draw('Level %d complete!' % (self.level.sequence+1),
                                pos=(345, 155),
                                align=font.CENTER)
            idx = self.levels.index(self.level)
            if idx < len(self.levels) - 1:
                nextLevel = self.levels[idx+1]

        if self.choosingLevel:
            pass

        for widget in self.ui:
            widget.draw()
                            
        if finalPass:
            pygame.display.flip()

    def keyboard(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not self.menuing:
                    self.menu()
                else:
                    self.quit = True
            elif event.key == pygame.K_F5:
                if self.editing:
                    self.frameEnabled = not self.frameEnabled
            elif event.key == pygame.K_F4:
                if self.editing:
                    print self.level.filename
            elif False:
                if event.key == pygame.K_BACKSPACE:
                    self.codeBuffer = self.codeBuffer[:-1]
                elif event.key == pygame.K_RETURN:
                    self.playCode(self.codeBuffer)
                elif event.unicode.upper() in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    self.codeBuffer +=  event.unicode.upper()

    def mouse(self, event):
        x, y = event.pos
        y = 600-y
        dragButton = (hasattr(event, 'buttons') \
                      and (event.buttons[0] | \
                           event.buttons[1] | \
                           event.buttons[2])) \
                     or hasattr(event, 'button')
        collider = self.interactiveGrid.getColliderAt(x, y)
        if self.selectedObject and self.selectedObject.keepHover(x, y):
            collider = self.selectedObject

        self.highlightTool = None
        if self.selectedTool:
            self.selectedTool.shadow = x, y

        if event.type == pygame.MOUSEBUTTONDOWN:
            alternateButton = event.button != 1

            if alternateButton and self.selectedTool:
                self.selectTool(None)
                self.selectedObject = None
            elif self.selectedTool and \
                (not collider or not isinstance(collider, Widget)):
                self.selectedTool.place(x, y)
            elif self.hoverObject and self.hoverObject.keepHover(x,y):
                self.selectedObject = self.hoverObject
            elif collider is not self.selectedObject:
                self.selectedObject = collider
            self.hoverObject = None

            if dragButton and self.selectedObject:
                self.selectedObject.beginDrag(x, y, alternateButton)

        elif event.type == pygame.MOUSEMOTION:
            if dragButton and self.selectedObject:
                if x > self.workspaceMaxX and\
                   not isinstance(self.selectedObject, Widget):
                    # Highlight if dragging back to toolbox
                    self.highlightTool = self.getTool(self.selectedObject)
                self.selectedObject.continueDrag(x, y)
            elif not self.selectedTool:
                if collider and collider.hoverable:
                    self.hoverObject = collider
                elif not (self.hoverObject and self.hoverObject.keepHover(x,y)):
                    self.hoverObject = None
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.selectedTool and x < self.workspaceMaxX:
                self.selectedTool.place(x, y)
                self.hoverObject = None
            elif self.selectedObject:
                if x > self.workspaceMaxX and\
                   not isinstance(self.selectedObject, Widget):
                    self.removeObject(self.selectedObject)
                else:
                    self.selectedObject.completeDrag(x, y)

    def loop(self):
        clock = pygame.time.Clock()
        millis = 0
        while not self.quit:
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type in (pygame.KEYUP, pygame.KEYDOWN):
                    self.keyboard(event)
                elif event.type in (pygame.MOUSEMOTION, 
                                    pygame.MOUSEBUTTONUP,
                                    pygame.MOUSEBUTTONDOWN):
                    self.mouse(event)
                elif event.type == pygame.QUIT:
                    self.quit = True
            tick = clock.tick()
            millis += tick
            if millis > 1000:
                sys.stdout.write('FPS %05d\r' % clock.get_fps())
                sys.stdout.flush()
                millis = 0
            self.update(tick)
            self.display()

if __name__ == '__main__':
    global game
    game = Game()
    game.init()
    game.menu()
    game.loop()
