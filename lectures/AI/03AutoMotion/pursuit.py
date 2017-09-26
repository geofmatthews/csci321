#/usr/bin/env python
"""
wait.py

Geoffrey Matthews
2006
"""

#Import Modules
import pygame, os
from pygame.locals import *
import random
from math import sin, cos, pi
#my own modules:
import vectors as V
import states as S
from datamanagers import Images, Sounds
from player import Player, PlayerGroup, Dino, Ogre
from constants import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

screen_size = (1024, 768)
screen_size = (800,600)

ticks = 10
ndinos = 6
nogres = 4

dinos = PlayerGroup()
ogres = PlayerGroup()
everybody = PlayerGroup()

def random_pos():
    return V.vector(random.randint(50,screen_size[0]-50),
                    random.randint(50,screen_size[1]-50))

def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode(screen_size, FULLSCREEN)
    pygame.display.set_caption('Wait!')
    pygame.mouse.set_visible(True)
    
#Create The Backgound
    Images.load_image('grass.jpg')
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background_image = Images.get('grass')
    for x in range(0,background.get_width(),background_image.get_width()):
        for y in range(0,background.get_height(),background_image.get_height()):
            background.blit(background_image,(x,y))

#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()
    
#Prepare Game Objects
    clock = pygame.time.Clock()
    
    Images.load_character('dino', os.path.join("T_dino_red", "dino red bitmaps"))
    Images.load_character('ogre', os.path.join("T_ogre", "ogre 96x bitmaps"))

    w,h = screen.get_size()
    
    for d in range(ndinos):  dinos.add(Dino(random_pos()))
    for o in range(nogres):  ogres.add(Ogre(random_pos()))
    
    everybody.add(dinos)
    everybody.add(ogres)

    for e in everybody: e.changeState(S.Wander())

#Main Loop
    while 1:
        clock.tick(ticks)

    #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                for e in everybody:
                    e.showheading = not e.showheading
            elif event.type == MOUSEBUTTONDOWN and event.button == 2:
                for e in everybody:
                    e.showbox = not e.showbox
            elif event.type == MOUSEBUTTONDOWN and event.button == 3:
                d = dinos.sprites()[0]
                if d.state == S.Wander():
                    randomogre = random.choice(ogres.sprites())
                    for d in dinos:
                        d.changeState(S.Pursuit(), target=randomogre)
                else:
                    for d in dinos:
                        d.changeState(S.Wander())
                        
    #Update sprites
        everybody.update()

    #Draw Everything
        screen.blit(background, (0, 0))
        everybody.draw(screen)
        pygame.display.flip()

#Game Over

#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
        

