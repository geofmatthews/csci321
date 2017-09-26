import pygame
import os

from pygame.locals import *

from locals import *

import data

class Frame:

  def __init__(self, object, anim_name, frameno, frame_length):
    self.image = pygame.image.load(data.picpath(object, anim_name, frameno)).convert_alpha()
    self.rect = self.image.get_rect()
    self.frame_length = frame_length
    return

  def get_image(self):
    return self.image

  def get_rect(self):
    return self.rect

  def get_time(self):
    return self.frame_length