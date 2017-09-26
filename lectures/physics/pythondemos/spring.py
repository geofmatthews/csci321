# numeric integration illustration
# Runge Kutta integration for a spring under Hook's law

import pygame, time
from pygame.locals import *
from pygame.color import *
from numpy import *

def xt(state):
    maxval = 9999
    if abs(state[0]) < maxval:
        return (int(state[2]*5), int(state[0]+480/2))
    else:
        return (int(state[2]*5), maxval)

def d(state):
    global k,m
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

evenodd = 0
def symplectic(state, dt):
    global evenodd
    tempstate = state + d(state)*dt
    newstate1 = state + d(state)*dt
    newstate2 = state + d(tempstate)*dt
    newstate = newstate1
    newstate[evenodd] = newstate2[evenodd]
    evenodd = 1 - evenodd
    return newstate

prevstate = None
def verlet(state, dt):
    global prevstate
    if prevstate!=None:
        x,  v,  t  = state
        px, pv, pt = prevstate
        ddx, ddv, ddt = d(state)
        np = x + x - px + ddv*dt*dt
        newstate = array((np, 0, t+dt), dtype=float)
        prevstate = state.copy()
        # velocity not used:
        return newstate
    else:
        prevstate = state.copy()
        return euler(state, dt)

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
    newstate = state + (k1 + 2*k2 + 2*k3 + k4) * dt/6.0
    return newstate

def main():
    global k,m
       
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    background = pygame.Surface(screen.get_size())
    background.fill((128,128,255))
    screen.blit(background, (0,0))
    
    m = 10.0
    k = 4.0
    t = 0
    dt = 2

    startstate = array((20,0,t), dtype=float)
    eulerstate = startstate.copy()
    rungestate = startstate.copy()
    midpointstate = startstate.copy()
    verletstate = startstate.copy()
    sympstate = startstate.copy()

    running = 1
    while t*5 < screen.get_width():
        #pygame.draw.circle(background, (255,0,0), xt(eulerstate), 1)
        #pygame.draw.circle(background, (0,255,0), xt(midpointstate), 1)
        pygame.draw.circle(background, (0,0,255), xt(rungestate), 1)
        pygame.draw.circle(background, (0,255,255), xt(verletstate), 1)
        pygame.draw.circle(background, (255,255,0), xt(sympstate), 1)
        screen.blit(background, (0,0))
        t += dt
        midpointstate = midpoint(midpointstate, dt)
        rungestate = rungekutta(rungestate, dt)
        sympstate = symplectic(sympstate, dt)
        verletstate = verlet(verletstate, dt)
        steps = 1
        for i in range(steps):
            eulerstate += d(eulerstate)*(dt/steps)
        pygame.display.flip()
            
    clock = pygame.time.Clock()

    waiting = 1
    while waiting:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == QUIT:
                waiting = 0
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                waiting = 0

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()

