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

state = array((20, 0, t), dtype=float)
vstate = state.copy()
prevstate = None

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

def d2(state):
    x, v, t = state
    # force is proportional to displacement
    f = -k*x
    # f = ma
    a = f/m
    d2x = a
    d2v = 0
    d2t = 0
    return array((d2x,d2v,d2t),dtype=float)

def euler(state, dt):
    return state + dt*d(state)
    
def verlet(state, prevstate, dt):
    if prevstate != None:
        return 2*state - prevstate + (dt**2)*d2(state), state
    else:
        return euler(state, dt), state

try:
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
            pygame.draw.circle(background, (255,0,0), xt(state), 1)
            pygame.draw.circle(background, (0,255,0), xt(vstate), 1)
            screen.blit(background, (0,0))
            t += dt
            vstate, prevstate = verlet(vstate, prevstate, dt)
            state += d(state)*dt
            pygame.display.flip()
finally:
    pygame.quit()

