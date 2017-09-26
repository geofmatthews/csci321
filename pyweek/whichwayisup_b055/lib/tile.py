import pygame
import os

from pygame.locals import *

from locals import *

import data

from object import Gameobject
from animation import Animation

class Tile(Gameobject):
  def __init__(self, screen, tilex, tiley, set = "brown", tileclass = "wall"):
    Gameobject.__init__(self, screen, True)
    self.animations["default"] = Animation(set, tileclass)
    self.image = self.animations[self.current_animation].update_and_get_image()
    self.rect = self.image.get_rect()
    self.tilex = tilex
    self.tiley = tiley
    self.x = (tilex - (FULL_TILES_HOR - TILES_HOR) + 0.5) * TILE_DIM
    self.y = (tiley - (FULL_TILES_VER - TILES_VER) + 0.5) * TILE_DIM
    return

  def update(self, level = None):
    Gameobject.update(self, level)
    if not self.flipping:
      self.x = round((self.x/TILE_DIM), 1)*TILE_DIM
      self.y = round((self.y/TILE_DIM), 1)*TILE_DIM
    return