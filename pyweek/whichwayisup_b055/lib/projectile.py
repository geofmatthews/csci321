'''One of the enemies, the spider, which climbs along walls and shoots at the player.'''

import pygame
import os

from pygame.locals import *

from locals import *

import data

from object import Gameobject
from sound import play_sound
from animation import Animation

class Projectile(Gameobject):

  def __init__(self, screen, x = None, y = None, dx = None, dy = None, damage = 5, set = "energy"):
    Gameobject.__init__(self, screen, False, False, x, y, -1)
    self.animations["default"] = Animation(set, "flying")
    self.animations["dying"] = Animation(set, "dying")
    self.image = self.animations[self.current_animation].update_and_get_image()
    self.rect = self.image.get_rect()
    self.dx = dx
    self.dy = dy
    self.saveddx =  None
    self.damage = damage
    self.itemclass = "projectile"
    return

  def update(self, level = None):
    Gameobject.update(self, level)
    if self.y < 0 and self.current_animation != "dying":  #This kills projectiles that wander off the screen from the top
      self.current_animation = "dying"
    if self.dx == 0 and self.dy == 0 and self.saveddx != None:
      self.dx = self.saveddx
      self.dy = self.saveddy
    return

  def flip(self):
    self.saveddx = -self.dy
    self.saveddy = self.dx
    Gameobject.flip(self)
    return