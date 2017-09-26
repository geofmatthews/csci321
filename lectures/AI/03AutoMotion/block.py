
import pygame
from datamanagers import Images
   
class Block(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = Images.get('square')
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
 
