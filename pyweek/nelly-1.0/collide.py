#!/usr/bin/python
# $Id: collide.py,v 1.6 2006/04/01 20:37:52 alex Exp $

import math

def collideSphereLine(sx, sy, sradius, x1, y1, x2, y2):
    """ Intersect circle and line segment:
        http://astronomy.swin.edu.au/~pbourke/geometry/sphereline/

        return: None if no collision, or
                (distance, tangent, intersection) where
                    distance: penetration of sphere into line segment (-ve)
                    tangent:  (dx,dy) of tangent to line segment
                    intersect: (x,y) of intersection point
    """
    denom = (x2-x1)**2 + (y2-y1)**2
    if denom == 0:
        return None
    u = ((sx-x1)*(x2-x1) + (sy-y1)*(y2-y1)) / denom
    if u < 0 or u > 1:
        # Nearest colinear point is outside line-segment, but
        # could still be intersecting.. test against endpoints
        d1 = (sx-x1)**2 + (sy-y1)**2
        d2 = (sx-x2)**2 + (sy-y2)**2
        if d1 < d2:
            d, ix, iy = d1, x1, y1
        else:
            d, ix, iy = d2, x2, y2
    else:   
        # Distance to nearest colinear point within line-segment
        ix = x1 + u*(x2-x1)
        iy = y1 + u*(y2-y1)
        d = (sx-ix)**2 + (sy-iy)**2
    if d < sradius**2:
        return (math.sqrt(d) - sradius, (x2-x1, y2-y1), (ix, iy))
    return None

def collideLineLine(x1, y1, x2, y2, x3, y3, x4, y4):
    """ Intersect two line segments:
        http://astronomy.swin.edu.au/~pbourke/geometry/lineline2d/

        return: None if no collision, or
                (distance2, tangent, intersection) where
                    distance2 = square of distance from P1 to intersection
                    tangent = (dx,dy) of tangent of P3,P4
                    intersect = (x,y) intersection point
    """
    denom = (y4 - y3)*(x2 - x1) - (x4 - x3)*(y2 - y1)
    if denom == 0:
        return None    # parallel
    ua = ((x4 - x3)*(y1 - y3) - (y4 - y3)*(x1 - x3)) / denom
    ub = ((x2 - x1)*(y1 - y3) - (y2 - y1)*(x1 - x3)) / denom
    if ua >= 0 and ua <= 1 and ub >= 0 and ub <= 1:
        # Got an intersection
        ix = x1 + ua*(x2 - x1)
        iy = y1 + ua*(y2 - y1)
        distance2 = (ix - x1)**2 + (iy - y1)**2
        return distance2, (x4-x3, y4-y3), (ix, iy)
    return None


class UniformGridCollider:
    def __init__(self, width, height, cols, rows):
        self.width, self.height = width, height
        self.cols, self.rows = cols, rows
        self.ux, self.uy = self.width / self.cols, self.height / self.rows
        self.clear()

    def clear(self):
        self.grid = [[] for i in range(self.cols*self.rows)]
        self.colliders = []

    def boxToGrid(self, x1, y1, x2, y2):
        x1, y1, x2, y2 = (min(max(int(x1/self.ux), 0), self.cols-1),
                         min(max(int(y1/self.uy), 0), self.rows-1),
                         min(max(int(x2/self.ux), 0), self.cols-1),
                         min(max(int(y2/self.uy), 0), self.rows-1))
        if x1 > x2:
            x2, x1 = x1, x2
        if y1 > y2:
            y2, y1 = y1, y2
        return x1, y1, x2, y2

    def addCollider(self, collider, bbox):
        self.colliders.append(collider)
        x1, y1, x2, y2 = bbox
        x1, y1, x2, y2 = self.boxToGrid(x1, y1, x2, y2)
        cols = self.cols
        for gx in range(x1, x2+1):
            for gy in range(y1, y2+1):
                self.grid[gy*cols+gx].append(collider)

    def removeCollider(self, collider, bbox):
        self.colliders.remove(collider)
        x1, y1, x2, y2 = bbox
        x1, y1, x2, y2 = self.boxToGrid(x1, y1, x2, y2)
        cols = self.cols
        for gx in range(x1, x2+1):
            for gy in range(y1, y2+1):
                self.grid[gy*cols+gx].remove(collider)

    def collideSphere(self, x, y, radius):
        x1, y1, x2, y2 = self.boxToGrid(x-radius, y-radius, x+radius, y+radius)
        collisions = []
        # When steam particles get large they intersect many boxes, so
        # avoid rechecking same collider
        # TODO use sets instead of list
        colliders = {} 
        cols = self.cols
        for gx in range(x1, x2 + 1):
            for gy in range(y1, y2+1):
                for collider in self.grid[gy*cols+gx]:
                    if collider not in colliders:
                        collision = collider.collideSphere(x, y, radius)
                        colliders[collider] = 1
                        if collision:
                            collisions.append(collision)
        return collisions

    def collideRay(self, x1, y1, x2, y2):
        gx1, gy1, gx2, gy2 = self.boxToGrid(x1, y1, x2, y2)
        collisions = []
        cols = self.cols
        for gx in range(gx1, gx2 + 1):
            for gy in range(gy1, gy2+1):
                for collider in self.grid[gy*cols+gx]:
                    collision = collider.collideRay(x1, y1, x2, y2)
                    if collision:
                        collisions.append(collision)
        return collisions

    def getColliderAt(self, x, y):
        a, b, gx, gy = self.boxToGrid(x, y, x, y)
        cols = self.cols
        for collider in self.grid[gy*cols+gx]:
            if collider.containsPoint(x, y):
                return collider
        return None

    def closestCollision(self, collisions):
        if not collisions:
            return None
        else:
            best = None
            for collision in collisions:
                if not best or collision[0] < best[0]:
                    best = collision
            return best

    def draw(self):
        for collider in self.colliders:
            collider.draw()

    def updateCollider(self, collider, bbox):
        # Remove from grid #TODO can improve this
        cols = self.cols
        for gx in range(self.cols):
            for gy in range(self.rows):
                self.grid[gy*cols+gx] = \
                    [c for c in self.grid[gy*cols+gx] if c is not collider]

        # Add to grid
        self.addCollider(collider, bbox)

class Behaviour:
    DROP_REMOVE = 1
    DROP_BOUNCE = 2
    STEAM_CONDENSE = 3
    STEAM_BOUNCE = 4

    def __init__(self):
        self.grids = []
    
    def respondDrop(self, collider, point):
        assert False

    def respondSteam(self, collider, point, ttl):
        assert False

# Abstract base class; not really needed but good for doc ('cause I still think
# like a Java/C++ programmer)
class Collider(Behaviour):
    def __init__(self, behaviour=None):
        if not behaviour:
            behaviour = Behaviour()
        self.behaviour = behaviour
        self.grids = []

    def addToGrid(self, grid):
        self.grids.append(grid)
        grid.updateCollider(self, self.getBoundingBox())

    def updateGrids(self):
        bbox = self.getBoundingBox()
        for grid in self.behaviour.grids + self.grids:
            grid.updateCollider(self, bbox)

    def removeGrids(self):
        bbox = self.getBoundingBox()
        for grid in self.behaviour.grids + self.grids:
            grid.removeCollider(self, bbox)

    def clear(self):
        self.updateGrids()
        self.removeGrids()
        self.grids = []

    def getBoundingBox(self):
        assert False

    def collideSphere(self, x, y, radius):
        assert False

    def collideRay(self, x1, y1, x2, y2):
        assert False

    def respondDrop(self, collider, point):
        return self.behaviour.respondDrop(collider, point)

    def respondSteam(self, collider, point, ttl):
        return self.behaviour.respondSteam(collider, point, ttl)

class SegmentCollider(Collider):
    """ Proxy class for LineStripCollider; allows single line segments of one
    large object to be tested for collision separately (hence more
    efficiently)"""
    def __init__(self, point1, point2, behaviour=None):
        Collider.__init__(self, behaviour)
        self.point1, self.point2 = point1, point2

    def getBoundingBox(self):
        return (min(self.point1[0], self.point2[0]),
                min(self.point1[1], self.point2[1]),
                max(self.point1[0], self.point2[0]),
                max(self.point1[1], self.point2[1]) )

    def collideSphere(self, x, y, radius):
        collision = collideSphereLine(x, y, radius,
                                              self.point1[0], self.point1[1],
                                              self.point2[0], self.point2[1])
        if collision:
            distance, tangent, intersection = collision
            return distance, tangent, intersection, self
        return None

    def collideRay(self, x1, y1, x2, y2):
        collision = collideLineLine(x1, y1, x2, y2,
                                            self.point1[0], self.point1[1],
                                            self.point2[0], self.point2[1])
        if collision:
            distance2, tangent, intersection = collision
            return distance2, tangent, intersection, self
        return None

class LineStripCollider(Collider):
    def __init__(self, points, behaviour=None):
        Collider.__init__(self, behaviour)
        self.points = [[p[0], p[1]] for p in points]
        self.createColliders()

    def createColliders(self):
        self.colliders = \
            [SegmentCollider(self.points[i], self.points[i+1], self.behaviour) \
             for i in range(len(self.points)-1)]

    def updateGrids(self):
        """ Override to use individual bounding boxes with proxies """
        for collider in self.colliders:
            for grid in self.grids + self.behaviour.grids:
                grid.updateCollider(collider, collider.getBoundingBox())

    def removeGrids(self):
        """ Override to use individual bounding boxes with proxies """
        for collider in self.colliders:
            for grid in self.grids + self.behaviour.grids:
                grid.removeCollider(collider, collider.getBoundingBox())

class PolygonCollider(Collider):
    """ More efficient than a LineStripCollider for small objects that
    typically fit in one grid cell. """
    def __init__(self, points, behaviour=None):
        Collider.__init__(self, behaviour)
        self.setPoints(points)

    def setPoints(self, points):
        self.points = points
        self.lines = [(points[i], points[i+1]) for i in range(len(points)-1)]
        self.lines.append((points[-1], points[0]))

    def getBoundingBox(self):
        x1, y1, x2, y2 = (self.points[0][0], self.points[0][1],
                          self.points[0][0], self.points[0][1])
        for point in self.points:
            x1 = min(x1, point[0])
            y1 = min(y1, point[1])
            x2 = max(x2, point[0])
            y2 = max(y2, point[1])
        return x1, y1, x2, y2

    def collideSphere(self, x, y, radius):
        minPenetration = 0
        for line in self.lines:
            collision = collideSphereLine(x, y, radius,
                                                    line[0][0], line[0][1],
                                                    line[1][0], line[1][1])
            if collision:
                penetration, tangent, intersect = collision
                if penetration < minPenetration:
                    candidate = penetration, tangent, intersect, self
                    minPenetration = penetration
        if minPenetration < 0:
            return candidate
        return None

    def collideRay(self, x1, y1, x2, y2):
        candidate = None
        for line in self.lines:
            x3, y3 = line[0]
            x4, y4 = line[1]
            collision = collideLineLine(x1, y1, x2, y2, 
                                                x3, y3, x4, y4)
            if collision:
                distance2, tangent, intersect = collision
                if not candidate or distance2 < candidate[0]:
                    candidate = distance2, tangent, intersect, self
        if candidate:
            return candidate
        return None

    def containsPoint(self, x, y):
        # Cast ray from point to bottom edge of screen parallel to y axis
        # Count intersections between ray and edges.  If odd, point is inside.
        count = 0
        for line in self.lines:
            x1,y1 = line[0]
            x2,y2 = line[1]
            if x2 == x1:
                continue # skip vertical lines
            if not ((x >= x1 and x <= x2) or (x >= x2 and x <= x1)):
                continue # point out of bounds
            m = (y2-y1)/(x2-x1)
            c = y1 - m*x1
            iy = m*x + c
            if iy > y and ((iy >= y2 and iy <= y1) or (iy >= y1 and iy <= y2)):
                count += 1
        return count % 2 != 0

    def __repr__(self):
        return self.lines.__repr__()

