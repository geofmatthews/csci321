import numpy as N
import pygame
from GM.vector import *

def cross(size, color):
    """A grave marker type cross"""
    surface = pygame.Surface((size,size)).convert()
    if color[0] == color[1] == color[2] == 0:
        backgroundColor = (255,255,255)
    else:
        backgroundColor = (0,0,0)
    surface.fill(backgroundColor)
    surface.set_colorkey(backgroundColor)
    a = (size/2.0, 0)
    b = (size/2.0, size)
    pygame.draw.line(surface, color, a,b, 3)
    c = (0.25*size, size/3.0)
    d = (0.75*size, size/3.0)
    pygame.draw.line(surface, color, c,d, 3)
    return surface

def plus(size, color):
    surface = pygame.Surface((size,size)).convert()
    if color[0] == color[1] == color[2] == 0:
        backgroundColor = (255,255,255)
    else:
        backgroundColor = (0,0,0)
    surface.fill(backgroundColor)
    surface.set_colorkey(backgroundColor)
    a = (size/2.0, 0)
    b = (size/2.0, size)
    pygame.draw.line(surface, color, a,b, 2)
    c = (0, size/2.0)
    d = (size, size/2.0)
    pygame.draw.line(surface, color, c,d, 2)
    return surface

def cross_hairs(size, color):
    surface = pygame.Surface((size,size)).convert()
    if color[0] == color[1] == color[2] == 0:
        backgroundColor = (255,255,255)
    else:
        backgroundColor = (0,0,0)
    surface.fill(backgroundColor)
    surface.set_colorkey(backgroundColor)
    a = (size/2.0, 0)
    b = (size/2.0, size)
    pygame.draw.line(surface, color, a,b, 2)
    c = (0, size/2.0)
    d = (size, size/2.0)
    pygame.draw.line(surface, color, c,d, 2)
    pygame.draw.circle(surface, color, size/2.0, size/2.0, size/4.0, 2)
    return surface
    

def arrow(size, angle, color, fill=True):
    surface = pygame.Surface((size,size)).convert()
    if color[0] == color[1] == color[2] == 0:
        backgroundColor = (255,255,255)
    else:
        backgroundColor = (0,0,0)
    surface.fill(backgroundColor)
    surface.set_colorkey(backgroundColor)
    radius = size/2.0
    angleleft = N.pi*(angle+150)/180.0
    angleright = N.pi*(angle-150)/180.0
    angle = N.pi*angle/180.0
    center = vector(radius, radius)
    p1 = center + (radius*N.cos(angle), radius*N.sin(angle))
    p2 = center + (radius*N.cos(angleleft), radius*N.sin(angleleft))
    p3 = center + (radius*N.cos(angleright), radius*N.sin(angleright))
    if fill:
        width=0
    else:
        width=1
    pygame.draw.polygon(surface, color, [p1,p2,p3], width)
    return surface

def rotating_arrow(size, color, n=36, fill=True):
    return [arrow(size, i*360.0/n, color, fill) for i in range(n)]

def star(size,color):
    surface = pygame.Surface((size,size)).convert()
    if color[0] == color[1] == color[2] == 0:
        backgroundColor = (255,255,255)
    else:
        backgroundColor = (0,0,0)
    surface.fill(backgroundColor)
    surface.set_colorkey(backgroundColor)
    radius = size/2.0
    center = vector(radius,radius)
    angles1 = [i*2*N.pi/5.0 - N.pi/2.0 for i in range(5)]
    p1 = [(radius*N.cos(a), radius*N.sin(a)) for a in angles1]
    angles2 = [i*2*N.pi/5.0 - N.pi/2.0 + 2*N.pi/10.0 for i in range(5)]
    p2 = [(0.4*radius*N.cos(a),0.4*radius*N.sin(a)) for a in angles2]
    points = []
    for a,b in zip(p1,p2):
        points.extend((center+a,center+b))
    width=0
    pygame.draw.polygon(surface, color, points, width)
    return surface
    
