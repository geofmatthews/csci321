import pygame
import os

from pygame.locals import *

from locals import *

import data

from tile import Tile
from animation import Animation

class Spikes(Tile):
  def __init__(self, screen, tilex, tiley, set = "brown"):
    Tile.__init__(self, screen, tilex, tiley, set, "spikes")
    self.itemclass = "spikes"
    self.y = round((self.y/TILE_DIM), 1)*TILE_DIM + SPIKES_VER_OFFSET
    return

  def update(self, level = None):
    Tile.update(self, level)
    if not self.flipping:
      self.x = round((self.x/TILE_DIM), 1)*TILE_DIM + SPIKES_VER_OFFSET
      self.y = round((self.y/TILE_DIM), 1)*TILE_DIM + SPIKES_VER_OFFSET
    return