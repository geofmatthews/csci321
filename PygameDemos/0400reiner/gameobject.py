import pygame
import numpy as N
import random

_xsteps = (1.0,  0.7,  0.0, -0.7, -1.0, -0.7, 0.0, 0.7)
_ysteps = (0.0, -0.5, -0.7, -0.5,  0.0,  0.5, 0.7, 0.5)
_steps = [N.array((x,y)) for x,y in zip(_xsteps, _ysteps)]

class GameObject(pygame.sprite.Sprite):
    def __init__(self, pos, screen):
        pygame.sprite.Sprite.__init__(self)
        self.pos = N.array(pos, dtype="float")
        self.rect.center = pos
        self.heading = 0
        self.speed = 0.0
        self.screen = screen
        width = self.rect.width*0.3
        height = self.rect.height*0.2
        self.collisionRect = pygame.Rect(0,0,width,height)
        self.collisionRect.centerx = self.rect.centerx
        self.collisionRect.centery = self.rect.bottom - 0.25*self.rect.height

    def update(self):
        pass

    def backup(self):
        pass

class Stat(GameObject):
    def __init__(self, pos, screen):
        GameObject.__init__(self, pos, screen)
        self.collisionRect.centery = self.rect.bottom - 0.1*self.rect.height


class Mob(GameObject):
    def __init__(self, pos, screen):
        GameObject.__init__(self, pos, screen)

    def update(self):
        # move:
        self.heading %= 8
        self.pos += self.speed * _steps[self.heading]
        
        # wrap screen:
        w,h = self.screen.get_size()
        if self.pos[0] < 0: self.pos[0] = w-1
        elif self.pos[0] >= w: self.pos[0] = 0
        elif self.pos[1] < 0: self.pos[1] = h-1
        elif self.pos[1] >= h: self.pos[1] = 0

        self.rect.center = self.pos
        self.collisionRect.centerx = self.rect.centerx
        self.collisionRect.centery = self.rect.bottom - 0.25*self.rect.height

    def backup(self):
        self.pos -= self.speed * _steps[self.heading]
        self.rect.center = self.pos
        self.collisionRect.centerx = self.rect.centerx
        self.collisionRect.centery = self.rect.bottom - 0.25*self.rect.height

