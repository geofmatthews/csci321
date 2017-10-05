"""
A pygame program to draw an animated line.
Geoffrey Matthews, 2007
"""

import pygame
from pygame.locals import *
from lineclass import Line

def main():
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption("Animated Line")
    lines = [Line(screen) for x in range(20)]
    clock = pygame.time.Clock()
    while 1:
        clock.tick(30)
        screen.fill((50, 50, 100))
        for line in lines:
            line.update()
            line.draw()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                return
            
if __name__ == '__main__': main()
