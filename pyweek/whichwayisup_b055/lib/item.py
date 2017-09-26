import pygame
import os

from pygame.locals import *

from locals import *

import data

from object import Gameobject
from animation import Animation

class Item(Gameobject):

  def __init__(self, screen, x = None, y = None, set = "brown", itemclass = "key", max_activations = 1, trigger = TRIGGER_FLIP):
    Gameobject.__init__(self, screen, True, False, x, y)
    self.animations["default"] = Animation(set, itemclass)

    try:
      self.animations["broken"] = Animation(set, itemclass + "_broken")
    except:
      self.animations["broken"] = self.animations["default"]
      
    self.image = self.animations[self.current_animation].update_and_get_image()
    self.rect = self.image.get_rect()
    self.itemclass = itemclass
    self.activated_times = 0
    self.max_activations = max_activations
    self.trigger = TRIGGER_NONE
    if self.itemclass == "key":
      self.pickable = True
    if self.itemclass == "lever":
      self.trigger = trigger
    return

  def activate(self):
    if self.itemclass == "lever":
      self.activated_times += 1
      if (self.activated_times <= self.max_activations) or (self.max_activations == -1):
        if (self.activated_times == self.max_activations):
          self.current_animation = "broken"
        return self.trigger
    return TRIGGER_NONE