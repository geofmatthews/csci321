import pygame
from pygame.locals import *
import os

import data

from variables import Variables

sounds = {}

def play_sound(sound_id, volume = 1.0):
  if not Variables.vdict["sound"]:
    return
  snd = None
  if (not sounds.has_key(sound_id)):
    try:
      sound_path = data.filepath(os.path.join("sounds", sound_id + ".ogg"))
      snd = sounds[sound_id] = pygame.mixer.Sound(sound_path)
    except:
      print "Error: Sound file not found."
      return
  else:
    snd = sounds[sound_id]
  try:
    snd.set_volume(volume)
    snd.play()
  except:
    print "Error: Could not play sound"
  return
