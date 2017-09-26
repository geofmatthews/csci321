import pygame
import os

from pygame.locals import *

from locals import *

import data

from util import Score, render_text, bool_to_str
from variables import Variables
from level import Level

from sound import play_sound

class Menu:

  def __init__(self, screen, score = None):
    self.screen = screen
    self.score = score
    return

  def run(self, menu_choice = 0):
    done = False

    clock = pygame.time.Clock()

    menu_items = ["Quit", "Sound: " + bool_to_str(Variables.vdict["sound"]), "Dialogue: " + bool_to_str(Variables.vdict["dialogue"]) ]

    count = 0

    while (count <= Variables.vdict["unlocked"] and count < TOTAL_LEVELS):
      menu_items.append("Level " + str(count + 1))
      count += 1
      
    if self.score != None:
      menu_image = render_text("Your final score: " + str(self.score), COLOR_GUI)
      rect = menu_image.get_rect()
      rect.centerx = SCREEN_WIDTH / 2
      rect.top = GUI_MENU_TOP - 25
      self.screen.blit(menu_image, rect)

    while not done:

      # Pygame event and keyboard input processing
      for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
          menu_choice = MENU_QUIT
          done = True
        elif (event.type == KEYDOWN and event.key == K_DOWN) or (event.type == JOYAXISMOTION and event.axis == 1 and event.value > 0.7):
          if menu_choice + 4 < len(menu_items):
            menu_choice += 1
            play_sound("click")
        elif (event.type == KEYDOWN and event.key == K_UP) or (event.type == JOYAXISMOTION and event.axis == 1 and event.value < -0.7):
          if menu_choice + 3 > 0:
            menu_choice -= 1
            play_sound("click")
        elif (event.type == KEYDOWN and (event.key == K_z or event.key == K_SPACE or event.key == K_RETURN)) or (event.type == JOYBUTTONDOWN and (event.button == 0 or event.button == 1)):
          done = True

      #Menu rendering
      
      menu_offset =  -(len(menu_items) - 6) * 10

      menu_bg = pygame.image.load(data.picpath("menu", "bg")).convert_alpha()
      rect = menu_bg.get_rect()
      rect.centerx = SCREEN_WIDTH / 2
      rect.top = GUI_MENU_TOP
      self.screen.blit(menu_bg, rect)

      menu_head = render_text("Which way is up?")
      rect = menu_head.get_rect()
      rect.centerx = SCREEN_WIDTH / 2
      rect.top = GUI_MENU_TOP + 50 + menu_offset
      self.screen.blit(menu_head, rect)

      current_menu_index = -3

      for m in menu_items:
        if (menu_choice == current_menu_index):
          color = COLOR_GUI_HILIGHT
        else:
          color = COLOR_GUI
        menu_image = render_text(m, color)
        rect = menu_image.get_rect()
        rect.centerx = SCREEN_WIDTH / 2
        rect.top = GUI_MENU_TOP + 60 + (current_menu_index + 4) * 20 + menu_offset
        self.screen.blit(menu_image, rect)
        current_menu_index += 1

      #Display, clock

      pygame.display.flip()

      clock.tick(FPS)

    return menu_choice
