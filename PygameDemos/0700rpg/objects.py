import pygame, math, random
from resources import ResourceManager
from pygame.locals import *

from tiles import TileManager
        
#### Some tests:
if __name__ == "__main__":
    try:
        pygame.init()
        screen = pygame.display.set_mode((800,480))
        # now we can initialize the resource manager:
        tm = TileManager().initialize()
        done = False
        while not(done):
            screen.fill((0,0,0))
            tm.tiles.draw(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == QUIT:
                    done = True
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    done = True
    finally:
        pygame.quit()
        
