import pygame
from pygame.locals import *
import os
from random import randint, uniform
from reinerobject import Dino, Ogre, Tree2

import depthupdates
from imagemanager import ImageManager

class ReinerRoom:
    def __init__(self, screen):
        self.screen = screen
        # Sprite groups
        self.AllSprites = depthupdates.DepthUpdates()
        self.Dinos = depthupdates.DepthUpdates()
        self.Ogres = depthupdates.DepthUpdates()
        self.Trees = depthupdates.DepthUpdates()

        # Create background
        grassfile = os.path.join('ReinerLevel','data','Tgrundvari','variationen','012.bmp')
        ImageManager().loadStatic(grassfile,'Grass',colorkey=False)
        grassimage = ImageManager().getStatic('Grass')
        self.background = pygame.Surface(screen.get_size())
        for x in range(0,self.background.get_width(),grassimage.get_width()):
            for y in range(0,self.background.get_height(),grassimage.get_height()):
                self.background.blit(grassimage, (x,y))

        # Create game objects
        w,h = self.screen.get_size()
        for i in range(5):
            x,y = randint(0,w-1), randint(0,h-1)
            d = Dino((x,y), screen)
            d.speed = randint(0,5)
            d.heading = randint(0,7)
            self.Dinos.add(d)
        for i in range(5):
            x,y = randint(0,w-1), randint(0,h-1)
            o = Ogre((x,y), screen)
            o.speed = randint(0,5)
            o.heading = randint(0,7)
            self.Ogres.add(o)
        for i in range(42):
            x,y = randint(0,w-1),randint(0,h-1)
            t = Tree2((x,y), screen, i%21)
            self.Trees.add(t)
        self.myogre = self.Ogres.sprites()[0]    
        self.AllSprites.add(self.Dinos, self.Ogres, self.Trees)

    def run(self, events):

        # Event queue handling:
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    self.myogre.heading -= 1
                    self.myogre.heading %= 8
                elif event.key == K_LEFT:
                    self.myogre.heading += 1
                    self.myogre.heading %= 8

        # Event polling:
        pressed = pygame.key.get_pressed()
        if pressed[K_UP]:
            self.myogre.speed = 4.0
        else:
            self.myogre.speed = 0.0

        # Update:
        self.AllSprites.update()

        # Draw everything:
        self.screen.blit(self.background, (0,0))
        pygame.draw.rect(self.screen, pygame.Color("red"), self.myogre.rect, 1)
        self.AllSprites.draw(self.screen)

        pygame.display.flip()
        
                                  
    
    
