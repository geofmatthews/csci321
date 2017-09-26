# numeric integration illustration
# Runge Kutta integration for a spring under Hook's law

import pygame, time
from pygame.locals import *
from pygame.color import *
from numpy import *

pygame.init()
screen = pygame.display.set_mode((640,480))
background = pygame.Surface(screen.get_size())
background.fill((128,128,255))
  
m = 10.0
k = 4.0
t = 0

estate = array((20, 0, t), dtype=float)
rstate = estate.copy()
mstate = estate.copy()

def xt(state): return (int(state[2]*5), int(state[0]+480/2))

def d(state):
    x, v, t = state
    # force is proportional to displacement
    f = -k*x
    # f = ma
    a = f/m
    # deriv of position is velocity:
    dx = v
    # deriv of velocity is acceleration:
    dv = a
    # dt/dt:
    dt = 1
    return array((dx,dv,dt),dtype=float)

def euler(state, dt):
    k = d(state)
    newstate = state + k*dt
    return newstate
    
def midpoint(state, dt):
    k1 = d(state)
    k2 = d(state + k1 * dt/2)
    newstate = state + k2 * dt
    return newstate

def rungekutta(state, dt):
    k1 = d(state)
    k2 = d(state + k1 * dt/2)
    k3 = d(state + k2 * dt/2)
    k4 = d(state + k3 * dt)
    newstate = state + (k1 + 2*k2 + 2*k3 + k4) * dt/6
    return newstate
  
dt = 0.1

screen.blit(background, (0,0))

clock = pygame.time.Clock()

running = 1
while running:
    clock.tick(88888)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = 0
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            running = 0
    if t < screen.get_width():
        pygame.draw.circle(background, (255,0,0), xt(estate), 1)
        pygame.draw.circle(background, (0,255,0), xt(mstate), 1)
        pygame.draw.circle(background, (0,0,255), xt(rstate), 1)
        screen.blit(background, (0,0))
        t += dt
        estate = euler(estate, dt)
        mstate = midpoint(mstate, dt)
        rstate = rungekutta(rstate, dt)
        pygame.display.flip()
            
pygame.quit()

