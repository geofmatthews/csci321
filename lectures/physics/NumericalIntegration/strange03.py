# numeric integration illustration
# Runge Kutta integration lorenz attractor,
# butterfly effect!

import pygame, time
from pygame.locals import *
from pygame.color import *
from numpy import *

pygame.init()
screen = pygame.display.set_mode((1200,900))
background = pygame.Surface(screen.get_size())
background.fill((128,128,255))

"""
The Lorenz attractor has strange forces acting on it, giving
rise to chaotic behavior
"""

p1 = array((10, 10, 10), dtype=float)
p2 = array((10, 10, 10.01), dtype=float)
sigma, beta, rho = 10.0, 8/3.0, 28.0

def d(state):
    x,y,z = state
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return array((dx, dy, dz))

def rungekutta(state, dt):
    k1 = d(state)
    k2 = d(state + k1 * dt/2)
    k3 = d(state + k2 * dt/2)
    k4 = d(state + k3 * dt)
    newstate = state + (k1 + 2*k2 + 2*k3 + k4) * dt/6
    return newstate
  
t = 0
dt = 0.001

screen.blit(background, (0,0))

clock = pygame.time.Clock()

def getpt(state):
    return 16*state[1:3] + (500, 80)

running = 1
while running:
   # clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = 0
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = 0
    oldp1 = getpt(p1)
    oldp2 = getpt(p2)
    screen.blit(background, (0,0))
    t += dt
    p1 = rungekutta(p1, dt)
    p2 = rungekutta(p2, dt)
    pygame.draw.line(background, (255,0,0), oldp1, getpt(p1), 1)
    pygame.draw.line(background, (0,255,0), oldp2, getpt(p2), 1)
    pygame.display.flip()
            
pygame.quit()

