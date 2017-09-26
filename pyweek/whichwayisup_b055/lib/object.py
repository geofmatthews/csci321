import pygame
import os
import random
'''A game object class for almost everything - there's an awful lot of badly organized code here, and
 a layer of inheritance should probably be added between this and the dynamic objects... perhaps after PyWeek.'''

from math import *

from pygame.locals import *

from locals import *

import data

from animation import Animation
from particle import Particle

from sound import play_sound

class Gameobject:

  #The last parameter might be one of the stupidest hacks ever, and has to do with objects staying off the screen after flipping out.
  #I really have to rework this some time.
  def __init__(self, screen, static = False, gravity = False, x = None, y = None, life = -1, not_really_static = False):
    self.screen = screen
    self.animations = {}
    self.animations["default"] = Animation("object", "idle")
    self.current_animation = "default"
    self.image = self.animations[self.current_animation].update_and_get_image()
    self.rect = self.image.get_rect()
    self.x = x
    self.y = y
    if (self.x == None):
      self.x = SCREEN_WIDTH / 2
    if (self.y == None):
      self.y = SCREEN_HEIGHT / 2
    self.dx = 0.0
    self.dy = 0.0
    self.gravity = gravity
    self.static = static
    self.not_really_static = not_really_static

    self.flipping = False
    self.flipcounter = 0
    self.flip_init_angle = 0

    self.orientation = RIGHT
    self.itemclass = "not_item"
    self.pickable = False
    self.life = life
    self.dead = False
    self.destructable = True
    self.invincible = 0
    if (self.life == -1):
      self.destructable = False
    return
    
  def acc(self, direction):
    self.dx += direction[0]
    self.dy += direction[1]
    return

  def dec(self, direction):
    if abs(self.dx) < direction[0]:
      self.dx = 0
    else:
      if self.dx > 0:
        self.dx -= direction[0]
      else:
        self.dx += direction[0]

    if abs(self.dy) < direction[1]:
      self.dy = 0
    else:
      if self.dy > 0:
        self.dy -= direction[1]
      else:
        self.dy += direction[1]
    return

  def update(self, level = None):
    blood = []

    if self.flipping:

      if self.flipcounter == 0:
        rela_x = self.x - PLAY_AREA_CENTER_X
        rela_y = self.y - PLAY_AREA_CENTER_Y
        self.rad = sqrt(rela_x**2 + rela_y**2)
        self.flip_init_angle = atan2(rela_y, rela_x)

      self.flipcounter += 1
      self.flip_angle = self.flipcounter * (pi * 0.5 / (FLIP_FRAMES + 1))
      self.angle = self.flip_angle + self.flip_init_angle
      self.x = PLAY_AREA_CENTER_X + cos(self.angle) * self.rad
      self.y = PLAY_AREA_CENTER_Y + sin(self.angle) * self.rad

      if self.flipcounter > FLIP_FRAMES:
        self.flipcounter = 0
        self.flipping = False
        self.dx = 0
        self.dy = 0
        return
      return

    if self.static and not self.not_really_static:
      return

    if self.gravity:
      self.dy += GRAVITY

    self.x += self.dx
    self.y += self.dy

    anycollision = False

    self.on_ground = False

    if (level != None):
      self.rect.centerx = int(self.x)
      self.rect.centery = int(self.y)
      if self.itemclass == "player":
        self.rect.top += PLAYER_COLLISION_ADJUST
        self.rect.height -= PLAYER_COLLISION_ADJUST
        level_collision = level.collide(self.rect, self.dy, self.dx, True)
        self.rect.height += PLAYER_COLLISION_ADJUST
        self.rect.top -= PLAYER_COLLISION_ADJUST
      else:
        level_collision = level.collide(self.rect, self.dy, self.dx, True)
      if (level_collision[RIGHT] != None):
        self.x = level_collision[RIGHT] - float(self.rect.width) / 2.0 - 1.0
        self.dx = 0
        anycollision = True
      if (level_collision[LEFT] != None):
        self.x = level_collision[LEFT] + float(self.rect.width) / 2.0 + 1.0
        self.dx = 0
        anycollision = True
      if (level_collision[DOWN] != None):
        self.y = level_collision[DOWN] - float(self.rect.height) / 2.0 - 1.0
        self.dy = 0
        self.on_ground = True
        anycollision = True
      if (level_collision[UP] != None):
        if self.itemclass == "player":
          self.y = level_collision[UP] + float(self.rect.height) / 2.0 + 1.0 - PLAYER_COLLISION_ADJUST
        else:
          self.y = level_collision[UP] + float(self.rect.height) / 2.0 + 1.0
        self.dy = 0
        anycollision = True
      if (level_collision[DAMAGE] > 0):
        blood = self.take_damage(level_collision[DAMAGE], self.x, self.rect.bottom - 4)
        if self.current_animation != "dying":
          self.dy -= level_collision[DAMAGE]*PLAYER_JUMP_ACC / 4.5

    if self.static:
      return

    if self.x < 0 + self.rect.width / 2:
      self.x = 0 + self.rect.width  / 2
      self.dx = 0
      anycollision = True

    if self.x > PLAY_AREA_WIDTH - self.rect.width  / 2:
      self.x = PLAY_AREA_WIDTH - self.rect.width  / 2
      self.dx = 0
      anycollision = True

    # The commented block is the collision code for the upper edge of the screen.
    '''if self.y < 0 + self.rect.height / 2:
      self.y = 0 + self.rect.height  / 2
      self.dy = 0'''

    if self.y > PLAY_AREA_HEIGHT - self.rect.height / 2:
      self.y = PLAY_AREA_HEIGHT - self.rect.height  / 2
      self.dy = 0
      self.on_ground = True
      anycollision = True

    if (self.itemclass == "projectile") and anycollision:
      self.die()

    if self.animations[self.current_animation].finished and self.current_animation == "dying":
      self.dead = True
    return blood

  def take_damage(self, amount, x = None, y = None):
    blood = []
    if (x == None):
      x = self.x
      y = self.y
    if self.destructable:
      self.life -= amount
      count = 0
      if self.current_animation != "dying":
        if (self.itemclass == "player"):
          self.current_animation = "shouting"
          play_sound("augh")
        while (count < amount):
          blood.append(Particle(self.screen, 15, x + random.uniform(-3, 3), y + random.uniform(-3, 3), 0, 0, 0.3, COLOR_BLOOD, 4))
          count += 1
      if self.life < 1:
        self.life = 0
        self.die()
    return blood

  def die(self):
    if self.animations.has_key("dying"):
      self.current_animation = "dying"
    else:
      self.dead = True
    return

  def render(self, surface = None, topleft = None):
    self.image = self.animations[self.current_animation].update_and_get_image()
    if topleft == None:
      self.rect.centerx = int(self.x)
      self.rect.centery = int(self.y)
    else:
      self.rect.left = topleft[0]
      self.rect.top = topleft[1]

    self.orientation = self.get_orientation()

    drawsurface = self.screen
    if surface != None:
      drawsurface = surface
    if self.orientation == RIGHT:
      drawsurface.blit(self.image, self.rect)
    if self.orientation == LEFT:
      drawsurface.blit(pygame.transform.flip(self.image, True, False), self.rect)
    if self.orientation == UP:
      drawsurface.blit(pygame.transform.rotate(self.image, 90), self.rect)
    if self.orientation == DOWN:
      drawsurface.blit(pygame.transform.rotate(self.image, -90), self.rect)
    return

  def get_orientation(self):
    if (self.dx < 0):
      orientation = LEFT
    if (self.dx > 0):
      orientation = RIGHT
    try:
      return orientation
    except:
      return self.orientation

  def flip(self):
    if self.flipping:
      return
    else:
      self.flipping = True
      return