
from GM.vector import *

def closest(actor, things):
    closest,closestdist = None,9999999
    for thing in things:
        dist = distance(thing.pos, actor.pos)
        if dist < closestdist:
            closest,closestdist = thing, dist
    return closest,closestdist
