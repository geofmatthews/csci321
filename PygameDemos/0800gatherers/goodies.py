
import pygame,random,sys
from pygame.locals import *
from GM import utilities
from GM.statemachine import StateMachine, State
from GM.vector import *
import GM.makeimage
from functions import closest
from constants import *


class Goody(pygame.sprite.Sprite):
    def __init__(self, pos, world, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.image = GM.makeimage.star(GOODY_SIZE, GOODY_COLOR)
        self.rect = self.image.get_rect()
        self.pos = vector(pos)
        self.rect.center = self.pos
        self.world = world

    def update(self):
        self.rect.center = self.pos


