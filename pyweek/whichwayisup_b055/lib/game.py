import pygame
from pygame.locals import *
import os
import random

from locals import *

from player import Player
from spider import Spider
from particle import Particle
from level import Level
from sound import play_sound
from util import *
from variables import Variables

import data

def run(screen, level_number = 0, score = None, joystick = None):
  done = False
  objects = []
  particles = []

  if score == None:
    score = Score(0)

  level = Level(screen, str(level_number))

  objects = level.get_objects()
  player = level.get_player()
  objects.append(player)

  player.life = score.life

  clock = pygame.time.Clock()

  end_trigger = END_NONE
  scripted_event_on = False

  #There's no music at the moment:
  #pygame.mixer.music.load( data.filepath(os.path.join("music", "music.ogg")) )
  #pygame.mixer.music.play(-1)

  scripted_events = level.get_scripted_events()
  current_scripted_event = None

  scripted_event_trigger = TRIGGER_LEVEL_BEGIN

  '''  for ev in scripted_events:
    if ev.trigger_type == "level_begin":
      scripted_event_on = True
      current_scripted_event = ev
      current_scripted_event_element = None

  text = None
  phase = 0
  cleared = False        # Clearing dialog boxes'''

  flip_wait = -1

  pygame.mixer.init()

  keys_released = {}

  keys_released["K_z"] = True
  keys_released["K_DOWN"] = True
  keys_released["K_UP"] = True
  keys_released["J_B0"] = True
  keys_released["J_B1"] = True

  while (end_trigger == END_NONE):

    # Pygame event and keyboard input processing
    for event in pygame.event.get():
      if event.type == QUIT:
        end_trigger = END_HARD_QUIT
      if (event.type == KEYDOWN and event.key == K_ESCAPE):
        end_trigger = END_QUIT

    keys = pygame.key.get_pressed()
    inputs = [False, False, False, False, False, False, 0.0]

    trigger = TRIGGER_NONE

    if keys[K_LEFT]:
      inputs[LEFT] = True

    if keys[K_RIGHT]:
      inputs[RIGHT] = True

    if keys[K_DOWN]:
      if keys_released["K_DOWN"]:
        inputs[DOWN] = True
      keys_released["K_DOWN"] = False
    else:
      keys_released["K_DOWN"] = True

    if keys[K_z]:
      inputs[UP] = True
      if keys_released["K_z"]:
        inputs[JUMP] = True
      keys_released["K_z"] = False
    else:
      keys_released["K_z"] = True

    if keys[K_UP]:
      inputs[UP] = True
      if keys_released["K_UP"]:
        inputs[JUMP] = True
      keys_released["K_UP"] = False
    else:
      keys_released["K_UP"] = True

    if keys[K_F10]:
      inputs[SPECIAL] = True

    if joystick != None:   # Parse joystick input
      
      axis0 = joystick.get_axis(0)

      if axis0 < -0.1:
        inputs[LEFT] = True
        inputs[ANALOG] = -axis0

      if axis0 > 0.1:
        inputs[RIGHT] = True
        inputs[ANALOG] = axis0

      if joystick.get_button(0):
        inputs[UP] = True
        if keys_released["J_B0"]:
          inputs[JUMP] = True
        keys_released["J_B0"] = False
      else:
        keys_released["J_B0"] = True

      if joystick.get_button(1):
        if keys_released["J_B1"]:
          inputs[DOWN] = True
        keys_released["J_B1"] = False
      else:
        keys_released["J_B1"] = True


    if scripted_event_on:
      if inputs[JUMP] or inputs[DOWN]:
        cleared = True

    moved = False

    analog_multiplier = 1

    if not scripted_event_on and not level.flipping:
      if inputs[LEFT]:
        player.move((-PLAYER_MAX_ACC, 0))
        moved = True

      if inputs[RIGHT]:
        player.move((PLAYER_MAX_ACC, 0))
        moved = True

      if inputs[JUMP]:
        if (player.on_ground):
          count = 0
          while (count < 5):
            count += 1
            particles.append(Particle(screen, 10, player.rect.centerx - player.dx / 4 + random.uniform(-3, 3), player.rect.bottom, -player.dx * 0.1, -0.5, 0.3, COLOR_DUST, 4))
          player.jump()

      if inputs[UP] and not player.on_ground:
        player.jump()

      if inputs[DOWN]:
        pick_up_item = level.pick_up(player.x, player.y)
        if pick_up_item != None:
          play_sound("coins")
          player.inventory.append(pick_up_item)
          scripted_event_trigger = pick_up_item.itemclass

        trigger = level.trigger(player.x, player.y)

      if inputs[SPECIAL]:
        trigger = TRIGGER_FLIP

    if not moved or (player.current_animation == "dying" and player.on_ground):
      player.dec((PLAYER_MAX_ACC, 0))

    if trigger == TRIGGER_FLIP:
      if flip_wait == -1:
        flip_wait = 0
        play_sound("woosh")

    if flip_wait != -1:
      flip_wait += 1
      if flip_wait > FLIP_DELAY:
        flip_wait = -1
        level.flip()
        for o in objects:
          o.flip()
        for p in particles:
          p.flip()

    #Rendering and updating objects:

    if scripted_event_trigger == TRIGGER_NONE:
      scripted_event_trigger = level.update()
    else:
      level.update()
    level.render()

    if not scripted_event_on:
      for o in objects:
        if o.dead and o.itemclass != "player":
          objects.remove(o)
          continue
        new_particles = o.update(level)
        if o.itemclass == "projectile":
          if player.rect.collidepoint(o.x, o.y) and o.current_animation == "default":
            new_particles = player.take_damage(o.damage)
            o.die()
        if new_particles != None:
          for p in new_particles:
            particles.append(p)

    for o in objects:
      o.render()

    for p in particles:
      p.update()
      p.render()
      if p.dead:
        particles.remove(p)

    #Dust effect:

    if (player.current_animation == "walking"):
      particles.append(Particle(screen, 10, player.rect.centerx - player.dx / 2 + random.uniform(-2, 2), player.rect.bottom, -player.dx * 0.1, 0.1, 0.3))

    #Rendering GUI on top of everything else:

    render_gui(screen, player.life, score.score, (5, 5))

    # Scripted event triggering:

    if scripted_event_trigger != TRIGGER_NONE:
      if player.on_ground:
        for ev in scripted_events:
          if ev.trigger_type == scripted_event_trigger:
            scripted_event_on = True
            current_scripted_event = ev
            current_scripted_event_element = None
            text = None
            phase = 0
            cleared = False        # Clearing dialog boxes
            player.dy = 0
            player.dx = 0
            player.update()
            scripted_event_trigger = TRIGGER_NONE

    # Scripted event processing:

    if scripted_event_on:
      if (current_scripted_event_element == None) or (current_scripted_event_element.finished):

        current_scripted_event_element = current_scripted_event.next_element()

        if current_scripted_event_element.event_type == "end":
          scripted_event_on = False
          current_scripted_event_element = None

      else:

        if not Variables.vdict["dialogue"]:  #Dialogue skipping
          while (current_scripted_event_element.event_type == "dialogue" or current_scripted_event_element.event_type == "player"):
            current_scripted_event_element.finished = True
            current_scripted_event_element = current_scripted_event.next_element()
            if current_scripted_event_element.event_type == "end":
              current_scripted_event_element.finished = True

        if current_scripted_event_element.event_type == "wait":
          current_scripted_event_element.finished = True

        if current_scripted_event_element.event_type == "dialogue":
          if text == None:
            text = current_scripted_event_element.text
            phase = 0
          phase = render_text_dialogue(screen, text, phase)
          if (phase == -1) and cleared:
            current_scripted_event_element.finished = True
            phase = 0
            cleared = False
            text = None
          if cleared:
            phase = -1
            cleared = False

        if current_scripted_event_element.event_type == "player":
          if current_scripted_event_element.text == "orientation":
            player.orientation = current_scripted_event_element.orientation
          current_scripted_event_element.finished = True

        if current_scripted_event_element.event_type == "change_level":
          end_trigger = END_NEXT_LEVEL
          score.score += (level_number + 1) * 11 * player.life
          current_scripted_event_element.finished = True

    if player.dead:
      end_trigger = END_LOSE

    #Display, clock

    pygame.display.flip()

    clock.tick(FPS)

  score.life = player.life #To make the player's health stay the same to the next level

  return end_trigger