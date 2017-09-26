import pygame
import os

from pygame.locals import *

from locals import *

import data
from util import dir_from_str

from tile import Tile
from spikes import Spikes
from item import Item
from player import Player
from spider import Spider
from scripted_event import Scripted_event

class Level:

  def __init__(self, screen, level_name = "0"):
    self.screen = screen
    self.bgimage = pygame.image.load(data.picpath("background", "static"))
    self.image = None
    self.rect = self.bgimage.get_rect()
    self.rect.centerx = SCREEN_WIDTH / 2
    self.rect.centery = SCREEN_HEIGHT / 2
    self.flipping = False
    self.flipcounter = 0

    self.tiles = []
    self.objects = []

    self.scripted_events = []

    conffile = open(data.levelpath(level_name))
    tiley = 0
    values = []
    set = "brown"  #Parsing this from the conf file should be added

    trigger = False
    current_event = None

    for line in conffile.readlines():

      if tiley < FULL_TILES_VER:
        tilex = 0
        while tilex < FULL_TILES_VER:
          if (line[tilex] == "W"):
            self.tiles.append(Tile(self.screen, tilex, tiley))
          if (line[tilex] == "B"):
            self.tiles.append(Tile(self.screen, tilex, tiley, set, "bars"))
          if (line[tilex] == "S"):
            self.tiles.append(Spikes(self.screen, tilex, tiley))
          tilex += 1
        tiley += 1

      else:
      
        if line.strip() != "":
          values = line.split()

          if trigger:
            if values[0] == "end" and values[1] == "trigger":
              trigger = False
            else:
              current_event.add_element(line)
            continue
          if values[0] == "trigger":
            trigger = True
            current_event = Scripted_event(values[1], int(values[2]))
            self.scripted_events.append(current_event)
            continue

          x = (float(values[1]) - (FULL_TILES_HOR - TILES_HOR)) * TILE_DIM
          y = (float(values[2]) - (FULL_TILES_VER - TILES_VER))* TILE_DIM
          if values[0] == "player":
            self.player = Player(self.screen, x, y)
            continue
          if values[0] == "spider":
            self.objects.append(Spider(self.screen, x, y, dir_from_str(values[3])))
            continue
          if values[0] == "key":
            self.objects.append(Item(self.screen, x, y, set, values[0]))
            continue
          if values[0] == "lever":
            trigger_type = TRIGGER_NONE
            if values[4] == "TRIGGER_FLIP":
              trigger_type = TRIGGER_FLIP
            self.objects.append( Item(self.screen, x, y, set, values[0], int(values[3]), trigger_type) )
            continue

    self.reset_active_tiles()
    return

  def update(self):
    return_trigger = TRIGGER_NONE
    if self.flipping:
      self.flipcounter += 1
      if self.flipcounter > FLIP_FRAMES:
        self.flipcounter = 0
        self.flipping = False
        self.reset_active_tiles()
        return_trigger = TRIGGER_FLIPPED
        self.image = None
      for t in self.tiles:
        t.update()
      return return_trigger
    return return_trigger

  def reset_active_tiles(self):
    self.active_tiles = []
    for t in self.tiles:
      if (t.x > 0 and t.y > 0):
        self.active_tiles.append(t)
    return

  def get_objects(self):
    return self.objects

  def get_player(self):
    return self.player
    
  def get_scripted_events(self):
    return self.scripted_events

  def render(self):
    if self.flipping or self.image == None:
      self.image = pygame.Surface((self.rect.width, self.rect.height))
      self.image.blit(self.bgimage, self.rect)
      for t in self.tiles:
        t.render(self.image)
    self.screen.blit(self.image, self.rect)
    return

  def flip(self):
    if self.flipping:
      return
    else:
      self.flipping = True
      for t in self.tiles:
        t.flip()
      return

  #Triggers an object in the position specified
  def trigger(self, x, y):
    for o in self.objects:
      if o.rect.collidepoint(x, y):
        if o.itemclass == "lever":
          trigg = o.activate()
          if trigg != TRIGGER_NONE:
            return trigg
    return TRIGGER_NONE

  #Gives an object from the level to the caller
  def pick_up(self, x, y):
    for o in self.objects:
      if o.rect.collidepoint(x, y):
        if o.pickable:
          self.objects.remove(o)
          return o
    return None

  #Checks the point for solid ground
  def ground_check(self, x, y):
    for t in self.active_tiles:
      if t.rect.collidepoint(x, y):
        return True
    return False

  #indexing: right left bottom top
  def collide(self, rect, dy, dx, topcollision = True):
    collision = [None, None, None, None, 0]
    for t in self.active_tiles:
      if t.rect.collidepoint(rect.right + 1, rect.centery - dy) and dx > 0:
        collision[RIGHT] = t.rect.left
      if (t.rect.collidepoint(rect.right + 1, rect.bottom - dy - 1) or t.rect.collidepoint(rect.right + 1, rect.top - dy + 1)) and dx > 0:
        collision[RIGHT] = t.rect.left
      if t.rect.collidepoint(rect.left - 1, rect.centery - dy) and dx < 0:
        collision[LEFT] = t.rect.right
      if (t.rect.collidepoint(rect.left - 1, rect.bottom - dy - 1) or t.rect.collidepoint(rect.left - 1, rect.top - dy + 1)) and dx < 0:
        collision[LEFT] = t.rect.right
      if (t.rect.collidepoint(rect.centerx - dx, rect.bottom + 1) or t.rect.collidepoint(rect.right - dx - 1, rect.bottom + 1) or t.rect.collidepoint(rect.left - dx + 1, rect.bottom + 1)) and dy > 0:
        collision[DOWN] = t.rect.top
        if (t.itemclass == "spikes"):
          collision[DAMAGE] = 5
      if t.rect.collidepoint(rect.centerx - dx, rect.top - 1) and dy < 0:
        collision[UP] = t.rect.bottom
      if (t.rect.collidepoint(rect.right - dx - 1, rect.top - 1) or t.rect.collidepoint(rect.left - dx + 1, rect.top - 1)) and dy < 0:
        collision[UP] = t.rect.bottom

    return collision
