import numpy as N
import math

def vector(x,y=None):
    if y==None: return N.array(x, dtype=float)
    else: return N.array((x,y), dtype=float)

def integer(v):
    return (int(v[0]), int(v[1]))

def ceil_ip(v):
    v[0] = N.ceil(v[0])
    v[1] = N.ceil(v[1])
    
def length(v):
    return N.sqrt(N.dot(v,v))

def copy(v):
    return v.copy()

def normalize_ip(v):
    """Change vlen(v) to 1.  If v is 0,0, changes to 1,0"""
    leng = length(v)
    if leng == 0: v[0] = 1.0
    else: v /= leng

def normalize(v):
    w = v.copy()
    normalize_ip(w)
    return w
    
def cross(a,b):
    return N.cross_product(a,b)

def perp(v):
    """Return vector perpendicular to v"""
    return vector(v[1], -v[0])

def angle(v):
    return math.atan2(v[1], v[0])

def rotate(v, angle):
    sangle = math.sin(angle*math.pi/180.0)
    cangle = math.cos(angle*math.pi/180.0)
    v0 = cangle*v[0] - sangle*v[1]
    v1 = sangle*v[0] + cangle*v[1]
    return vector(v0, v1)

def truncate(v, maxleng):
    if maxleng <= 0: return
    leng = length(v)
    if leng > maxleng:
        v *= maxleng/leng
        
if __name__ == '__main__':
    v = vector((-14,17))
    truncate(v,10)
    print (v, length(v))
    print (integer(v))
