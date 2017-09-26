#/usr/bin/env python
"""
Cloned from a GameMaker game, which I cloned from a pygame game, Astrocrash
Geoffrey Matthews
2017
"""

import os, pygame
from pygame.locals import *

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

from objects import ObjectManager
from resources import ResourceManager
    
def main():
        
    screensize = (640,480)
    pygame.init()
    screen = pygame.display.set_mode(screensize)
    pygame.mixer.music.load(os.path.join("data","music","theme.mid"))
    pygame.mixer.music.play(-1)
  
    # initialize resources before objects
    rm = ResourceManager().initialize()
    om = ObjectManager().initialize()
    ship = om.ships.sprites()[0]

    # start the game loop
    clock = pygame.time.Clock()
    done = False
    while not(done):
        clock.tick(30)

        # check user events
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            ship.left()
        if keys[K_RIGHT]:
            ship.right()
        if keys[K_UP]:
            ship.accelerate()
        if not keys[K_UP]:
            ship.coast()
        if keys[K_SPACE]:
            ship.fire()

        # update objects
        om.objects.update()

        # draw everything
        screen.blit(ResourceManager().nebula, (0,0))
        om.objects.draw(screen)
        pygame.display.flip()  
              
        # poll keyboard
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                done = True
            elif event.type == USEREVENT: # game over
                done = True


#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
