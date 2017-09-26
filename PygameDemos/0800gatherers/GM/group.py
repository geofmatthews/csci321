
import pygame
from pygame.locals import *

class Group(pygame.sprite.Group):
    def draw(self, surface):
        pygame.sprite.Group.draw(self, surface)
        for s in self.sprites():
            s.draw(surface)
            
class Sprite(pygame.sprite.Sprite):
    def draw(self, surface):
        pass
