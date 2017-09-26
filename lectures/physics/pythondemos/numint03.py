# numeric integration illustration
# Midpoint method integration for a particle under gravity

import pygame, time
from pygame.locals import *
from pygame.color import *
from numpy import *

pygame.init()
screen = pygame.display.set_mode((640,480))
background = pygame.Surface(screen.get_size())
background.fill((128,128,255))

  
m = 10.0
g = 4.0
t=0

state = array((10, 470, 12, -15, 0, g/m, t), dtype=float)
mstate = state.copy()

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
    
def midpoint(state, dt):
    k1 = d(state)
    k2 = d(state + k1 * dt/2)
    newstate = state + k2 * dt
    return newstate
  
dt = 5

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
    pygame.draw.circle(background, (255,0,0), state[0:2], 1)
    pygame.draw.circle(background, (0,255,0), mstate[0:2], 1)
    screen.blit(background, (0,0))
    t += dt
    mstate = midpoint(mstate, dt)
    state += d(state)*dt
    pygame.display.flip()
            
pygame.quit()

