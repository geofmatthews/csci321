import pygame
from pygame.locals import *
from TeddyLevel.shootteddy import TeddyRoom
from ReinerLevel.reinerroom import ReinerRoom
from HelpLevel.helproom import HelpRoom

screensize = (800,600)
def main():
    pygame.init()
    screen = pygame.display.set_mode(screensize)
    pygame.display.set_caption('Rooms')
    # Loading screen
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Loading...", 1, (50, 100, 150))
        textrec = text.get_rect()
        textrec.center = screen.get_rect().center
        screen.blit(text, textrec)
    pygame.display.flip()

    clock = pygame.time.Clock()
    clock.tick(1)

    # Create resources.  May want to do this later,
    # as each level is accomplished.  Slows loading here.
    teddyroom = TeddyRoom(screen)
    reinerroom = ReinerRoom(screen)
    helproom = HelpRoom(screen)
    
    currentroom = helproom
    
    while 1:
        clock.tick(30)
        events = pygame.event.get();
        for event in events:
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN :
                if event.key == K_ESCAPE:
                    return
                elif event.key == K_F1:
                    currentroom = helproom
                elif event.key == K_F2:
                    currentroom = reinerroom
                elif event.key == K_F3:
                    currentroom = teddyroom
        currentroom.run(events)

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
        
