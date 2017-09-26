

import pygame, time
from pygame.locals import *
from pygame.color import *
import numpy as N

#### Globals
pygame.init()
screen = pygame.display.set_mode((int(640*3/2),int(480*3/2)))
backcolor = (0,0,0)#(128,128,255)
background = pygame.Surface(screen.get_size())
background.fill(backcolor)

myfont = pygame.font.Font(None, 24)

class Ball():
    def __init__(self, screen):
        w,h = screen.get_size()
        x = N.random.random()*w*0.8 + 0.1*w
        y = N.random.random()*h*0.8 + 0.1*h
        self.position = N.array((x,y))
        self.velocity = N.random.random(2)*10.0 - 5.0
        self.acceleration = N.zeros(3)
        self.radius = N.random.random(1)*30.0 + 10.0
        self.mass = self.radius*self.radius
        self.color = N.random.randint(0, 255, 3)

def textout(txt, pos, txtcolor = (128,128,255)):
    rtext = myfont.render(txt, 1, txtcolor, backcolor)
    textrec = rtext.get_rect()
    textrec.topright = (screen.get_width(), pos)
    screen.blit(rtext, textrec)

def fpsout(fps):
    textout("fps: %f" % fps, 0)
    
class BallSystem():
    def __init__(self, screen, numBalls=20):
        self.screen = screen
        self.balls = [Ball(screen) for i in range(numBalls)]
        
    def Step(self):
        self.MoveBalls()
        self.CollideBalls()
        self.Draw()

    def Forces(self):
        for b in self.balls:
            b.acceleration = 0.0
            # drag:
            b.acceleration -= 0.00001 * b.velocity * b.mass
            # gravity:
            b.acceleration[1] += 0.2
            
    def MoveBalls(self):
        size = screen.get_size()
        self.Forces()
        for b in self.balls:
            #Euler integration:
            b.velocity += b.acceleration
            b.position += b.velocity               
            # wall collisions: back up and reverse velocity:
            for i in (0,1):
                if b.position[i] < b.radius:
                    b.position[i] = b.radius
                    b.velocity[i] *= -1
                if b.position[i] > size[i] - b.radius:
                    b.position[i] = size[i] - b.radius
                    b.velocity[i] *= -1
            
    def CollideBalls(self):
        numBalls = len(self.balls)
        for bn1 in range(numBalls-1):
            for bn2 in range(bn1+1,numBalls):
                if bn1 != bn2:
                    b1,b2 = self.balls[bn1],self.balls[bn2]
                    v = b2.position - b1.position
                    dist = N.sqrt(N.dot(v,v))
                    v /= dist
                    r = b1.radius + b2.radius
                    if dist < r:
                        # Move apart:
                        b1.position -= v*0.5*(r-dist)
                        b2.position += v*0.5*(r-dist)
                        self.Collide(b1,b2)
                        
    def Collide(self, b1, b2):
        collVector = b2.position - b1.position
        collVector /= N.sqrt(N.dot(collVector, collVector))
        v1 = collVector * N.dot(b1.velocity,collVector)
        v2 = collVector * N.dot(b2.velocity,collVector)
        v1other = b1.velocity - v1
        v2other = b2.velocity - v2      
        m1 = b1.mass
        m2 = b2.mass
        m12 = m1+m2
        newv1 = (v1*(m1-m2) + 2*m2*v2)/m12
        newv2 = (v2*(m2-m1) + 2*m1*v1)/m12
        b1.velocity = newv1 + v1other
        b2.velocity = newv2 + v2other

    def Draw(self):
        for b in self.balls:
            x,y = b.position
            pygame.draw.circle(self.screen, b.color, (int(x),int(y)), b.radius)


def main():
    global screen
    balls = BallSystem( screen)

    clock = pygame.time.Clock()
    running = 1
    screen.blit(background, (0,0))

    frames = 0
    elapsedtime = 0.0
    fps = 0.0
    
    while running:
        frametime = clock.tick(30)
        frames += 1
        elapsedtime += frametime
        if frames >= 100:
            fps = 1000.0*float(frames)/(elapsedtime)
            frames = 0
            elapsedtime = 0.0
            
        for event in pygame.event.get():
            if event.type == QUIT:
                running = 0
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = 0
                elif event.key == K_F12:
                    balls = BallSystem(screen)
                elif event.key == K_SPACE:
                    for b in balls.balls:
                        b.velocity[1] -= 10

        for i in range(2):
            balls.Step()
                    
        screen.blit(background, (0,0))
        balls.Draw()
        fpsout(fps)
        pygame.display.flip()

if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit()

    
               
