import numpy as N

def vector(x,y=None):
    if y==None: return N.array(x)
    else: return array((x,y))
