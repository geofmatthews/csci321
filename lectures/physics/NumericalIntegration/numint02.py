# numeric integration illustration
# Simple Riemann integration for a particle under gravity
# phase space version

import pygame, time
from pygame.locals import *
from pygame.color import *
from numpy import *

pygame.init()
screen = pygame.display.set_mode((640,480))
background = pygame.Surface(screen.get_size())
background.fill((128,128,255))

"""
In more generality, all variables can be put into a single vector:
(p, v, a)
and their derivatives expressed as a function:
(p, v, a)' = f(p, v, a)
"""
  
m = 10.0
g = 4.0
t = 0

state = array((10, 470, 12, -15, 0, g/m, t), dtype=float)

def d(state):
    x,y,vx,vy,ax,ay,t = state
    # deriv of position is velocity:
    dx = vx
    dy = vy
    # deriv of velocity is acceleration:
    dvx = ax
    dvy = ay
    # acceleration is constant:
    dax = 0
    day = 0
    # dt/dt:
    dt = 1
    return array((dx,dy,dvx,dvy,dax,day,dt),dtype=float)
  
t = 0
dt = 1

screen.blit(background, (0,0))

clock = pygame.time.Clock()

running = 1
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = 0
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = 0
    # analytic solution:
    x = 12*t + 10              + 2
    y = .2*t*t - 15*t + 470    - 2
    pygame.draw.circle(background, (0,0,0), array((x,y),dtype=int), 1)
    pygame.draw.circle(background, (255,0,0), array(state[0:2],dtype=int), 1)
    screen.blit(background, (0,0))
    t += dt
    state += d(state) * dt
    pygame.display.flip()
            
pygame.quit()

