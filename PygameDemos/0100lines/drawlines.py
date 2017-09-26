import pygame
from pygame.locals import *
from random import randint

def randpoint (screen):
    h,w = screen.get_size()
    return randint(0, w-1), randint(0, h-1)

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("My first drawing.")
    screen.fill((200, 200, 255))
    for i in range(1,20):
        start = randpoint(screen)
        stop = randpoint(screen)
        pygame.draw.line(screen, (255,0,0), start, stop, 1)
    pygame.display.flip()
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            
if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
        
