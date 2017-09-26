#/usr/bin/env python
"""
auto.py
Demo some of Reynold's autonomous behaviors
Geoffrey Matthews
2007
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
from player import *
from constants import *

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

world_size = (1024, 768)
#screen_size = (1024, 768)
screen_size = (640, 480)
show_world = False

ndinos = 5
nogres = 1
ticks = 20

blocks = PlayerGroup()
dinos = PlayerGroup()
ogres = PlayerGroup()
mobs = PlayerGroup()
everything = PlayerGroup()

def random_pos():
    return V.vector(random.randint(100,world_size[0]-100),
                    random.randint(100,world_size[1]-100))

def add_mob(group):
    if group == dinos:
        noob = Dino(random_pos())
        while playercollideany(noob, mobs):
            noob = Dino(random_pos())
        group.add(noob)
        mobs.add(noob)
    elif group == ogres:
        noob = Ogre(random_pos())
        while playercollideany(noob, mobs):
            noob = Ogre(random_pos())
        group.add(noob)
        mobs.add(noob)
        
def pick_on(targets, group, gstate):
    #for t in targets:
    #    t.changeState(S.Wander())
    targets = targets.sprites()
    for g in group:
        g.changeState(gstate, target = random.choice(targets))

def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
    global ticks, show_world
#Initialize Everything
    pygame.init()
    font = pygame.font.Font(None, 36)
    textcolor = (100, 255, 255)
    text = font.render("Autonomous Motion Demo", 1, textcolor)
    screen = pygame.display.set_mode(screen_size)#, FULLSCREEN)
    pygame.display.set_caption('Autonomous Motion Demo')
    pygame.mouse.set_visible(False)
    world = pygame.Surface(world_size)
    world = world.convert()
    
#Create The Backgound
    Images.load_image('grass.jpg')
    background = pygame.Surface(world_size)
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

    Images.load_image('square.png')
    Images.load_character('dino', os.path.join("T_dino_red", "dino red bitmaps"))
    Images.load_character('ogre', os.path.join("T_ogre", "ogre 96x bitmaps"))

    w,h = world_size

    # Blocks
    if (True):
        b = Block((0,0))
        bw, bh = b.rect.size

        for x in range(0,w,bw):
            blocks.add(Block((x,0)))
            blocks.add(Block((x,h-bh)))
        for y in range(bh,h-bh,bh):
            blocks.add(Block((0,y)))
            blocks.add(Block((w-bw,y)))

    # Mobs
    
    for d in range(ndinos):  add_mob(dinos)
    for o in range(nogres):  add_mob(ogres)
    mobs.add(dinos)
    mobs.add(ogres)

    everything.add(mobs)
    everything.add(blocks)
    dtext = "Wait"
    for o in ogres:
        o.changeState(S.User())
    print """
c: slow clock
H: show heading
F12: show world
b: show box
0: wait
w: wander
s: seek
p: pursuit
f: flee
e: evasion
"""
    

#Main Loop
    while 1:
        clock.tick(ticks)

    #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                elif event.key == K_c:
                    if ticks < 30 : ticks = 30
                    else: ticks = 10
                elif event.key == K_F12:
                    show_world = not show_world
                    if show_world:
                        screen = pygame.display.set_mode(world_size)#, FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode(screen_size)#, FULLSCREEN)
                elif event.key == K_h:
                    for m in mobs:
                        m.showheading = not m.showheading
                elif event.key == K_b:
                    for m in everything:
                        m.showbox = not m.showbox
                elif event.key == K_0:
                    dtext = "Wait"
                    text = font.render(dtext, 1, textcolor)
                    for m in dinos:
                        m.changeState(S.Wait())
                elif event.key == K_w:
                    dtext = "Wander"
                    text = font.render(dtext, 1, textcolor)                    
                    for m in dinos:
                        m.changeState(S.Wander())
                elif event.key == K_s:
                    dtext = "Seek"
                    text = font.render(dtext, 1, textcolor)
                    pick_on(ogres, dinos, S.Seek())
                elif event.key == K_p:
                    dtext = "Pursuit"
                    text = font.render(dtext, 1, textcolor)
                    pick_on(ogres, dinos, S.Pursuit())
                elif event.key == K_f:
                    dtext = "Flee"
                    text = font.render(dtext, 1, textcolor)
                    pick_on(ogres, dinos, S.Flee())
                elif event.key == K_e:
                    dtext = "Evasion"
                    text= font.render(dtext, 1, textcolor)
                    pick_on(ogres, dinos, S.Evasion())
                                               
    #Update sprites
        mobs.update(everything)

    #Draw Everything
        world.blit(background, (0,0))
        everything.draw(world)
        screen.fill((0,0,0))
        if show_world:
            screen.blit(world, (0,0))
        else:
            screen.blit(world, (0,0), ogres.sprites()[0].rect.inflate(screen_size))
        screen.blit(text, (32,32))
        pygame.display.flip()

#Game Over

#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
        

