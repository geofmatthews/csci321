#/usr/bin/env python
# Geoffrey Matthews
# 2017
# simple demo of rpg style game
# demo how to load maps from text files
# resources from opengameart.org, Tiny16:Basic

# Note, motion must be in steps that divide the cell size
# so that each character moves to the exact next cell on some
# step.  If the remainder of cell size divided by char speed
# is nonzero, chars may not stop on cells.

import pygame, math, random,os
from resources import ResourceManager
from pygame.locals import *

from utilities import loadImage
from tiles import TileManager
from things import ThingManager
from characters import CharManager

scale = 3
size = scale*16
def main():
    pygame.init()
    world = pygame.Surface((500*scale, 500*scale))
    screensize = (320*scale, 240*scale)
    screen = pygame.display.set_mode(screensize)
    # now we can initialize the resource managers:
    tm = TileManager().initialize(scale=scale)
    thm = ThingManager().initialize(scale=scale)
    cm = CharManager().initialize(scale=scale)


    visiblerect = pygame.Rect(((0,0), screensize))
    avatarIndex = 0
    avatar = cm.chars.sprites()[avatarIndex]

    clock = pygame.time.Clock()               
    done = False
    while not(done):
        clock.tick(30)
        
        # handle user events
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    done = True
                elif event.key == K_SPACE:
                    for thing in thm.things.sprites():
                        crect = avatar.rect.inflate(2,2)
                        if crect.colliderect(thing.rect):
                            thing.activate()
                elif event.key == K_c:
                    avatarIndex += 1
                    avatarIndex %= len(cm.chars.sprites())
                    avatar = cm.chars.sprites()[avatarIndex]

        pressed = pygame.key.get_pressed()
        if pressed[K_LEFT]:
            avatar.move('west')
        elif pressed[K_RIGHT]:
            avatar.move('east')
        elif pressed[K_UP]:
            avatar.move('north')
        elif pressed[K_DOWN]:
            avatar.move('south')
            
        # update world
        thm.things.update()
        cm.chars.update()

        # draw everything
        world.fill((0,0,0))
        pygame.draw.rect(world,
                         pygame.Color(0,0,255,255),
                         world.get_rect(),
                         16)
        tm.tiles.draw(world)
        thm.things.draw(world)
        cm.chars.draw(world)

        visiblerect.center = avatar.rect.center
        worldrect = world.get_rect()
        visiblerect.top = max(visiblerect.top, worldrect.top)
        visiblerect.bottom = min(visiblerect.bottom, worldrect.bottom)
        visiblerect.left = max(visiblerect.left, worldrect.left)
        visiblerect.right = min(visiblerect.right, worldrect.right)
        screen.blit(world, (0,0), visiblerect)
      
        pygame.display.flip()

if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit()
        
