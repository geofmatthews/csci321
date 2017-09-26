# numeric integration illustration
# Simple Riemann integration for a particle under gravity

import pygame, time
from pygame.locals import *
from pygame.color import *
from numpy import *

pygame.init()
screen = pygame.display.set_mode((640,480))
background = pygame.Surface(screen.get_size())
background.fill((128,128,255))

"""
Suppose we have some differential equations, like Newton's classical
equations of motion under gravity:

dp/dt = v
dv/dt = a
a = (0,g)

Velocity is the derivative of position, and acceleration
is the derivative of velocity, and the acceleration is zero
in the x direction, and constant in the y direction.

This can be simplified to:

p' = v
v' = a
a = (0,g)

Now, given initial values for our variables, say

p = (0, 100)
v = (5, -10)

We can advance this by a time step.

p[1] = p[0] + dt * p'[0]
v[1] = v[0] + dt * v'[0]

or, updating the variables in place:

p += dt * v
v += dt * (0, g)

Here it is in python and pygame:
"""

p = array((10, 470), dtype=float)
v = array((12, -15), dtype=float)
f = array((0, 4), dtype=float)  # constant gravity
m = 10.0

t = 0
dt = 0.1

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
    pygame.draw.circle(background, (0,0,0), (x,y), 1)
    pygame.draw.circle(background, (255,0,0), p[0:2], 1)
    screen.blit(background, (0,0))
    t += dt
    p += dt * v
    v += dt * f/m
    pygame.display.flip()
            
pygame.quit()

