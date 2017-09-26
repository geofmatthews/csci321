import pygame
import os

from pygame.locals import *

from locals import *

import data

from object import Gameobject
from sound import play_sound
from animation import Animation

class Player(Gameobject):

  def __init__(self, screen, x = None, y = None):
    Gameobject.__init__(self, screen, False, True, x, y, PLAYER_LIFE)
    #Changing some of the values from gameobject:
    self.animations["default"] = Animation("guy", "standing")
    self.animations["walking"] = Animation("guy", "walking")
    self.animations["arrow"] = Animation("guy", "arrow")
    self.animations["dying"] = Animation("guy", "dying")
    self.animations["shouting"] = Animation("guy", "shouting")
    self.animations["jumping"] = Animation("guy", "standing")
    self.image = self.animations[self.current_animation].update_and_get_image()
    self.rect = self.image.get_rect()
    self.itemclass = "player"

    #Variables spesific to this class:
    self.inventory = []
    self.on_ground = False
    self.umbrella_on = False
    return

  def move(self, direction):
    if self.current_animation == "dying":
      return
    if not self.on_ground:
      direction = (direction[0] * PLAYER_ACC_AIR_MULTIPLIER, direction[1])

    if direction[0] > 0 and self.dx < PLAYER_MAX_SPEED:
      self.acc(direction)
      if self.dx > PLAYER_MAX_SPEED:
        self.dx = PLAYER_MAX_SPEED
    if direction[0] < 0 and self.dx > -PLAYER_MAX_SPEED:
      self.acc(direction)
      if self.dx < -PLAYER_MAX_SPEED:
        self.dx = -PLAYER_MAX_SPEED
    return

  def update(self, level = None):
    blood = Gameobject.update(self, level)
    if self.animations[self.current_animation].finished and self.current_animation != "dying":
      self.animations[self.current_animation].reset()
      self.current_animation = "default"
    if self.on_ground:
      if self.current_animation == "jumping":
        self.current_animation = "default"
      if self.dx != 0 and self.current_animation == "default":
        self.current_animation = "walking"
      if (self.dx == 0) and self.current_animation == "walking" :
        self.current_animation = "default"
    elif self.current_animation != "dying":
      self.current_animation = "jumping"
    return blood

  def dec(self, direction):
    if not self.on_ground:
      direction = (direction[0] * PLAYER_ACC_AIR_MULTIPLIER, direction[1])
    Gameobject.dec(self, direction)
    return

  def render(self):
    self.rect.centerx = int(self.x)
    self.rect.centery = int(self.y)
    if self.rect.bottom > 0:
      Gameobject.render(self)
    else:
      self.arrowimage = self.animations["arrow"].update_and_get_image()
      self.arrowrect = self.arrowimage.get_rect()
      self.arrowrect.centerx = int(self.x)
      self.arrowrect.top = 5
      self.screen.blit(self.arrowimage, self.arrowrect)
    if self.umbrella_on:
      self.umbrella_on = False # This should be set again before next render by the jump function
    return

  def jump(self):
    if (self.on_ground):
      self.dy = -PLAYER_JUMP_ACC
      self.on_ground = False
      play_sound("boing", 0.5)
    else:
      self.dy -= PLAYER_AIR_JUMP
      self.umbrella_on = True
    return

  def flip(self):
    self.x = self.x - 2
    Gameobject.flip(self)
    self.on_ground = False
    if self.current_animation == "arrow":
      self.current_animation = "default"
    return