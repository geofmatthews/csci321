
import pygame,random,sys
from pygame.locals import *

from constants import *
from gatherers import Gatherer
from enemies import Enemy, DeadEnemy
from world import World
from goodies import Goody

def main():
    pygame.init()
    world = World(pygame.display.set_mode(SCREEN_SIZE))
    pygame.display.set_caption('Gatherers')

    background = pygame.Surface(world.screen.get_size())
    background = background.convert()
    background.fill(BACKGROUND_COLOR)

    world.screen.blit(background, (0,0))
    pygame.display.flip()

    clock = pygame.time.Clock()

    gatherers = pygame.sprite.Group()

    for i in range(20):
        x = random.randint(0,world.screen.get_width())
        y = random.randint(0,world.screen.get_height())
        world.addGoody((x,y))

    while 1:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == MOUSEBUTTONDOWN:
                m = pygame.mouse.get_pressed()
                if m[0]:
                    world.addGatherer(pygame.mouse.get_pos())
                if m[2]:
                    world.addEnemy(pygame.mouse.get_pos())

        world.update()
        world.screen.blit(background, (0,0))
        world.draw()
        pygame.display.flip()

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
        

