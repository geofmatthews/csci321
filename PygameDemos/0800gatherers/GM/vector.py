import numpy as N
import random

def vector(x, y=None):
    """Make float vector out of two numbers or a pair"""
    if y is None:
        return N.array(x, dtype=N.float)
    else:
        return N.array((x,y), dtype = N.float)

def dot(v1,v2):
    return N.vdot(v1,v2)

def mag2(v):
    return N.sum(N.vdot(v,v))
    
def mag(v):
    """Return vector length of v"""
    return N.sqrt(N.sum(N.vdot(v,v)))

def distance(a,b):
    return mag(vector(a)-vector(b))

def norm(v):
    """Return vector of length 1, (1,0) otherwise"""
    leng = mag(v)
    if leng > 0:
        return v/leng
    else:
        return vector(1,0)

def normalize(v):
    """Make unit length, (1,0) otherwise"""
    leng = mag2(v)
    if leng > 0:
        v /= N.sqrt(leng)
    else:
        v[0] = 1.0

def truncate(v, maxlength):
    """Make v no longer than maxlength"""
    m = mag(v)
    if m > maxlength:
        normalize(v)
        v *= maxlength

def perpLeft(v):
    """Return vector turned left 90 degrees"""
    return vector(v[1], -v[0])

def perpRight(v):
    """Return vector turned right 90 degrees"""
    return vector(-v[1], v[0])

def randomNormalVector():
    v = vector(random.uniform(-1.0,1.0), random.uniform(-1.0,1.0))
    return norm(v)

def rotationMatrix(theta):
    """clockwise (in pygame coords) rotation of theta radians"""
    cosT = N.cos(theta)
    sinT = N.sin(theta)
    return N.array([[cosT, -sinT],[sinT,cosT]])
    
def rotate(v, theta):
    """Rotates v clockwise (in pygame coords) theta radians"""
    return N.dot(v,rotationMatrix(theta))

def headingToAngle(heading):
    return N.arctan2(heading[1],heading[0])

def localToWorld(point, localHeading, localPos):
    angle = -headingToAngle(localHeading)
    rotation = rotationMatrix(angle)
    newpoint = N.dot(point, rotation)
    return newpoint + localPos

def worldToLocal(point, localHeading, localPos):
    newpoint = point - localPos
    angle = headingToAngle(localHeading)
    rotation = rotationMatrix(angle)
    return N.dot(newpoint, rotation)

def angle(v1, v2):
    """Angle from v1 to v2, clockwise (in pygame coords)"""
    a1 = N.arctan2(v1[1],v1[0])
    a2 = N.arctan2(v2[1],v2[0])
    return a2-a1

def segmentIntersection(p1,p2,p3,p4):
    """
    Do the line segments p1-p2 and p3-p4 intersect?
    Returns a pair: (bool, point)
    bool is true if the intersection is within the segments,
    false if outside the segments, or the lines are parallel.
    http://local.wasp.uwa.edu.au/~pbourke/geometry/
    """
    p1 = vector(p1) # just in case we have ints
    x1,y1 = p1
    x2,y2 = p2
    x3,y3 = p3
    x4,y4 = p4
    denom = (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)
    if denom == 0:
        return (False, None)
    numera = (x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)
    numerb = (x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)
    ua = numera/denom
    ub = numerb/denom
    onsegment = (0 <= ua <= 1) and (0 <= ub <= 1)
    x = x1 + ua*(x2-x1)
    y = y1 + ua*(y2-y1)
    return (onsegment, N.array((x,y)))

def closestPointToLine(p1, p2, p3):
    """
    Closest point to p3 on line segment p1-p2
    Returns a pair:  (bool, point)
    bool is true if the point lies on the segment,
    false otherwise
    http://local.wasp.uwa.edu.au/~pbourke/geometry/
    """
    p1 = vector(p1) #promote to floats
    if all(p1 == p2):
        return (True,p1)
    x1,y1 = p1
    x2,y2 = p2
    x3,y3 = p3
    numer = (x3-x1)* (x2-x1) + (y3-y1)*(y2-y1)
    denom = mag2(p2-p1)
    u = numer/denom
    x = x1 + u*(x2-x1)
    y = y1 + u*(y2-y1)
    onsegment = 0 <= u <= 1
    return (onsegment, N.array((x,y)))

def closestPointToRay(p1, vec, p3):
    """
    Closest point to p3 on line segment p1-(p1+vec)
    Returns a pair:  (bool, point)
    bool is true if the point lies on the segment,
    false otherwise
    http://local.wasp.uwa.edu.au/~pbourke/geometry/
    """
    vec = vector(vec)
    return closestPointToLine(p1, p1+vec, p3)
         
# Some tests
if __name__ == '__main__':

    print (angle(vector(1,0), vector(1,1))*180.0/N.pi,"<==should be 45")
    print (angle(vector(1,1), vector(1,0))*180.0/N.pi,"<==should be -45")
    v = vector(1,1)
    print (v, mag(v))
    v = rotate(v, N.pi/4.0)
    print (v, mag(v))
    v = rotate(v, -N.pi/4.0)
    print (v, mag(v))
    normalize(v)
    print (v, mag(v))
    v = rotate(v, N.pi/4.0)
    print (v, mag(v))

    print (segmentIntersection((0,0),(1,1),(0,1),(1,0)),"<===should be .5,.5")
    print (segmentIntersection((0,0),(1,1),(0,0),(1,1)),"<===should be false")
    print (closestPointToLine((0,0),(1,1),(0,1)),"<====should be .5,.5")
    print (closestPointToLine((0,0),(1,1), (10,0)),"<====should be false, 5,5")

    heading = norm(vector(1,1))
    pos = vector(20,10)
    point = vector(1,1)
    rotpt = localToWorld(point, heading,pos)
    print (rotpt, "<== should be %s, %s"%(20,10+N.sqrt(2.0)))
    unrotpt = worldToLocal(rotpt,heading,pos)
    print (unrotpt, "<== should be %s %s"%tuple(point))
    
    
