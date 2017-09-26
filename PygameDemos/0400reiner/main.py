import pygame
from pygame.locals import *
import os
from random import randint, uniform
from reinerobject import Dino, Ogre, Tree2
import depthupdates
from imagemanager import ImageManager
from globalvariables import *

# Sprite groups
AllSprites = depthupdates.DepthUpdates()

Mobs = depthupdates.DepthUpdates()
Stats = depthupdates.DepthUpdates()

Dinos = depthupdates.DepthUpdates()
Ogres = depthupdates.DepthUpdates()
Trees = depthupdates.DepthUpdates()

# Main
def main():
    # Initialize display
    pygame.init()
    #screen_size = (800,600)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Depth updates.')

    # Create background
    grassfile = os.path.join('data','Tgrundvari','variationen','012.bmp')
    ImageManager().loadStatic(grassfile,'Grass',colorkey=False)
    grassimage = ImageManager().getStatic('Grass')
    background = pygame.Surface(screen.get_size())
    for x in range(0,background.get_width(),grassimage.get_width()):
        for y in range(0,background.get_height(),grassimage.get_height()):
            background.blit(grassimage, (x,y))

    # Create game objects
    w,h = screen.get_size()
    for i in range(5):
        x,y = randint(0,w-1), randint(0,h-1)
        d = Dino((x,y), screen)
        d.speed = randint(0,5)
        d.heading = randint(0,7)
        Dinos.add(d)
    for i in range(5):
        x,y = randint(0,w-1), randint(0,h-1)
        o = Ogre((x,y), screen)
        o.speed = randint(0,5)
        o.heading = randint(0,7)
        Ogres.add(o)
    for i in range(20):
        x,y = randint(0,w-1),randint(0,h-1)
        t = Tree2((x,y), screen, i%21)
        Trees.add(t)
    myogre = Ogres.sprites()[0]
    Mobs.add(Dinos, Ogres)
    Stats.add(Trees)
    AllSprites.add(Mobs, Stats)

    # Create clock
    clock = pygame.time.Clock()

    # Game loop
    while 1:
        # Slow game down to 30 fps:
        clock.tick(30)

        # Event queue handling:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                elif event.key == K_RIGHT:
                    myogre.heading -= 1
                    myogre.heading %= 8
                elif event.key == K_LEFT:
                    myogre.heading += 1
                    myogre.heading %= 8

        # Event polling:
        pressed = pygame.key.get_pressed()
        if pressed[K_UP]:
            myogre.speed = 4.0
        else:
            myogre.speed = 0.0

        # Update:
        AllSprites.update()
        for spr1 in Stats:
            for spr2 in [myogre]:
                if spr1 != spr2:
                    if pygame.Rect.colliderect(spr1.collisionRect,
                                                  spr2.collisionRect):
                        #spr1.backup()
                        spr2.backup()
        # Draw everything:
        screen.blit(background, (0,0))
        red = pygame.Color("red")
        pygame.draw.rect(screen, red, myogre.rect, 1)
        pygame.draw.rect(screen, red, myogre.collisionRect, 1)

        for spr in Stats:
            pygame.draw.rect(screen, red, spr.collisionRect, 1)
        AllSprites.draw(screen)

        pygame.display.flip()

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
        
                                  
    
    
