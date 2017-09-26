
from visual import *
nodecolor = (255,0,0)
numnodes = 6
linkcolor = (0,0,255)
linkradius = 0.2

scene.background = (255,255,255)

def makeNode(name,x,y,z=0):
    s = sphere(pos = (x,y,z), color = nodecolor)
    label(text=name, pos=(x,y,z), opacity=0.25)
    return s

def randomNode(name,low,hi):
    x = low + random.random()*(hi-low)
    y = low + random.random()*(hi-low)
    z = low + random.random()*(hi-low)
    return makeNode(name,x,y,z)

def makeLink(i,j):
    n1 = nodes[i]
    n2 = nodes[j]
    p1 = n1.pos
    p2 = n2.pos
    return cylinder(pos=p1, axis=p2-p1, radius=linkradius, color=linkcolor)

nodes = [randomNode(repr(i),-20,20) for i in range(numnodes)]

links = [makeLink(i,j) for (i,j) in ((0,1),(0,2),(1,4),(2,3),(3,4),(3,5),(4,5))]
