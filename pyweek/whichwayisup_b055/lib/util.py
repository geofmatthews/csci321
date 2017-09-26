import pygame
from pygame.locals import *
import os
import codecs

from locals import *

import data

from sound import play_sound

from variables import Variables

class Score:
  def __init__(self, score, life = PLAYER_LIFE):
    self.score = score
    self.life = life
    return

class Util:

  pygame.font.init()
  smallfont = pygame.font.Font(data.filepath(os.path.join("misc", "Vera.ttf")), FONT_SIZE)
  cached_text_images = {}
  cached_images = {}
  cached_images["dialogueskip"] = pygame.image.load(data.picpath("skip", "dialogue"))

# This function is a fixed version of a similar piece of code in Trip on the Funny Boat.
def get_config_path():
  pathname = ""
  try:
    pathname = os.path.join(os.environ["HOME"], ".wwisup")
  except:
    try:
      pathname = os.path.join(os.environ["APPDATA"], "Wwisup")
    except:
      print "Error: Couldn't get environment variable for home directory, using data directory instead"
      pathname = data.filepath("saves")
  if not os.path.exists(pathname):
    os.mkdir(pathname)
  return pathname

def parse_config():
  Variables.vdict["unlocked"] = 0
  Variables.vdict["sound"] = True
  Variables.vdict["dialogue"] = True
  file_path = os.path.join(get_config_path(), "config.txt")
  try:
    conffile = open(file_path)
    for line in conffile.readlines():
      if line.strip() != "":
        values = line.split("\t")
        if values[0] == "unlocked":
          Variables.vdict["unlocked"] = int(values[1])
        if values[0] == "sound":
          Variables.vdict["sound"] = str_to_bool(values[1])
        if values[0] == "dialogue":
          Variables.vdict["dialogue"] = str_to_bool(values[1])
  except:
    if write_config():
      print "Created configuration file to " + file_path
  return

def write_config():
  file_path = os.path.join(get_config_path(), "config.txt")
  try:
    conffile = codecs.open(file_path, "w", "utf_8")
    print >> conffile, "unlocked\t%s" % Variables.vdict["unlocked"]
    print >> conffile, "sound\t%s" % bool_to_str(Variables.vdict["sound"])
    print >> conffile, "dialogue\t%s" % bool_to_str(Variables.vdict["dialogue"])
  except:
    print "Error: Could not write configuration file to " + file_path
    return False
  return True

def str_to_bool(string):
  string = string.strip()
  return (string == "true" or string == "True" or string == "1" or string == "on")

def bool_to_str(bool):
  if bool:
    return "on"
  else:
    return "off"

def render_gui(screen, life, score, topleft):
  score_image = render_text("Score: " + str(score) )
  life_image = render_text("Life: " + str(life) )
  version_image = render_text("0.5.5")

  rect = score_image.get_rect()
  rect.left = topleft[0]
  rect.top = topleft[1]
  screen.blit(score_image, rect)

  rect = life_image.get_rect()
  rect.left = topleft[0]
  rect.top = topleft[1] + 20
  screen.blit(life_image, rect)

  rect = version_image.get_rect()
  rect.right = SCREEN_WIDTH - 2
  rect.bottom = SCREEN_HEIGHT - 2
  screen.blit(version_image, rect)
  return

#This function renders text on screen and handles caching of text images:
def render_text(string, color = COLOR_GUI):
  if Util.cached_text_images.has_key(string + str(color)):
    final_image = Util.cached_text_images[string + str(color)]
  else:
    text_image_bg = Util.smallfont.render(string, True, COLOR_GUI_BG)
    text_image_fg = Util.smallfont.render(string, True, color)
    rect = text_image_bg.get_rect()
    final_image = pygame.Surface((rect.width + 2, rect.height + 2)).convert_alpha()
    final_image.fill((0,0,0,0))
    final_image.blit(text_image_bg, rect)
    final_image.blit(text_image_bg, (2,2))
    final_image.blit(text_image_bg, (0,2))
    final_image.blit(text_image_bg, (2,0))
    final_image.blit(text_image_fg, (1,1))
    Util.cached_text_images[string + str(color)] = final_image
  return final_image

def render_text_dialogue(screen, string, phase):
  if phase == -1:
    phase = len(string)

  rendered_string = string[0:phase]
  string_image = render_text(rendered_string)
  rect = string_image.get_rect()
  rect.centerx = SCREEN_WIDTH / 2
  rect.centery = SCREEN_HEIGHT / 2
  screen.blit(string_image, rect)

  skip_image = Util.cached_images["dialogueskip"]
  skip_rect = skip_image.get_rect()
  skip_rect.centerx = SCREEN_WIDTH / 2
  skip_rect.top = rect.bottom + 5
  screen.blit(skip_image, skip_rect)

  if phase < len(string):
    phase += 1
    play_sound("click")
  else:
    return -1

  return phase

def cycle_clockwise(orientation):
  orientation += 1
  if orientation > 3:
    orientation = 0
  return orientation

def get_direction(orientation):
  if orientation == RIGHT:
    return (1, 0)
  if orientation == LEFT:
    return (-1, 0)
  if orientation == UP:
    return (0, -1)
  if orientation == DOWN:
    return (0, 1)
  return (0, 0)

def dir_from_str(string):
  if string == "LEFT":
    return LEFT
  if string == "UP":
    return UP
  if string == "DOWN":
    return DOWN
  return RIGHT