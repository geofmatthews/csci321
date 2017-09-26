'''Game main module.

Contains the entry point used by the run_game.py script.
The actual gameplay code is in game.py.
'''

import pygame
import os
import sys

from pygame.locals import *

from locals import *

import data
import game

from util import Score, parse_config, write_config
from variables import Variables
from menu import Menu

from sound import play_sound

def main():

    #Parsing level from parameters:

    level = 0

    user_supplied_level = False

    parse_config()

    if len(sys.argv) > 1:
        for arg in sys.argv:
          if level == -1:
            try:
              level = int(arg)
              user_supplied_level = True
            except:
              print "Error: incorrect level number"
              level = 0
          elif arg == "-l":
            level = -1

    #Initializing pygame and screen

    pygame.init()
    print "Which way is up starting up."
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption("Which way is up?")

    if (pygame.joystick.get_count() > 0):
      joystick = pygame.joystick.Joystick(0)
      joystick.init()
    else:
      joystick = None

    score = Score(0)

    done = False

    if (Variables.vdict["unlocked"] == 0) or user_supplied_level: # Go straight to the game
      end_trigger = END_NEXT_LEVEL
      menu_choice = -2
    else:                                      # Go to the menu first
      end_trigger = END_MENU
      menu_choice = 0

    #Menu and level changing loop, actual game code is in game.py:

    while not done:
      if end_trigger == END_NEXT_LEVEL:
        if level < TOTAL_LEVELS or user_supplied_level:
          end_trigger = game.run(screen, level, score, joystick)
          level += 1
          if end_trigger == END_QUIT:
            end_trigger = END_MENU
        else:
          end_trigger = END_WIN
      if end_trigger == END_LOSE:
        display_bg("lose", screen)
        end_trigger = END_MENU
      elif end_trigger == END_WIN:
        display_bg("victory", screen)
        end_trigger = END_MENU
      elif end_trigger == END_QUIT or end_trigger == END_HARD_QUIT:
        done = True
      elif end_trigger == END_MENU:
        prev_score = score.score
        score = Score(0)
        if prev_score != 0:
          menu = Menu(screen, prev_score)
        else:
          menu = Menu(screen)
        menu_choice = menu.run(menu_choice)
        if menu_choice == MENU_QUIT:
          end_trigger = END_QUIT
        elif menu_choice == MENU_SOUND:
          Variables.vdict["sound"] = not Variables.vdict["sound"]
          end_trigger = END_MENU
        elif menu_choice == MENU_DIALOGUE:
          Variables.vdict["dialogue"] = not Variables.vdict["dialogue"]
          end_trigger = END_MENU
        else:
          level = menu_choice
          end_trigger = END_NEXT_LEVEL
      else:
        if user_supplied_level:
          user_supplied_level = False
          end_trigger = END_WIN
        else:
          if Variables.vdict["unlocked"] < level:
            Variables.vdict["unlocked"] = level
            print "Unlocked level " + str(Variables.vdict["unlocked"])

    write_config()

    return

def display_bg(key, screen):
  bg_image = pygame.image.load(data.picpath("bg", key))
  rect = bg_image.get_rect()
  screen.blit(bg_image, rect)
  return

if __name__ == "__main__":
  main()
