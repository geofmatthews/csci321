#/usr/bin/env python
"""
Click on the bear and make him explode.
Designed to be similar to a Gamemaker game.

Geoffrey Matthews
2006
"""

#Import Modules
import numpy
import os, pygame
from pygame.locals import *
from random import randint, random
from math import sin, cos, pi
from time import sleep

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

screensize = (640,480)

class ImageManager:
    def __init__(self):
        self.dict = {}
        # Build cursor image:
        width = 16
        surf = pygame.Surface((width,width))
        r = surf.get_rect()
        surf.fill((255,255,255))
        surf.set_colorkey((255,255,255))
        pygame.draw.line(surf,(0,0,0),(0,width/2),(width,width/2),1)
        pygame.draw.line(surf,(0,0,0),(width/2,0),(width/2,width),1)
        self.dict["cursor"] = surf, surf.get_rect()
        
    def get(self, name):
        return self.dict[name]
    
    def load_image(self, name, colorkey=None):
        """Loads a single image file and returns it"""
        dictname = name[0:name.find('.')]
        fullname = os.path.join('data', name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error as message:
            print (('Cannot load image:', fullname))
            raise SystemExit( message)
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        self.dict[dictname] = image, image.get_rect()

    def load_strip(self, name, width, height, colorkey=None):
        """Loads images from a strip file and stores it in dict under name.
        Images can be packed in rows and columns."""
        dictname = name[0:name.find('.')]
        self.load_image(name, colorkey)
        image, rect = self.dict[dictname]
        images = []
        for y in range(0, image.get_height(), height):
            for x in range(0, image.get_width(), width):
                newimage = pygame.Surface((width,height))
                newimage.blit(image,(0,0),pygame.Rect(x, y, width, height))
                newimage.convert()
                if colorkey is not None:
                    if colorkey is -1:
                        colorkey = newimage.get_at((0,0))
                    newimage.set_colorkey(colorkey, RLEACCEL)
                images.append(newimage)
        self.dict[dictname] = images, images[0].get_rect()

class SoundManager:
    def __init__(self):
        self.dict = {}
            
    def get(self,name):
        return self.dict[name]
    
    def load_sound(self, name):
        """Loads a sound from a file."""
        class NoneSound:
            def play(self): pass
        if not pygame.mixer or not pygame.mixer.get_init():
            sound = NoneSound()
        else:
            fullname = os.path.join('data', name)
            try:
                sound = pygame.mixer.Sound(fullname)
            except pygame.error as message:
                print (('Cannot load sound:', fullname))
                raise SystemExit( message)
        dictname = name[0:name.find('.')]
        self.dict[dictname] = sound

def bounce(sp1, sp2):
    """bounce sp1 off sp2
    Just reverses hspeed or vspeed, depending on relative positions."""
    hdist = sp1.rect.left - sp2.rect.left
    vdist = sp1.rect.top - sp2.rect.top
    if abs(hdist) > abs(vdist):
        if hdist < 0:
            sp1.hspeed = -abs(sp1.hspeed)
        else:
            sp1.hspeed = abs(sp1.hspeed)
    else:
        if vdist < 0:
            sp1.vspeed = -abs(sp1.vspeed)
        else:
            sp1.vspeed = abs(sp1.vspeed)
    
class Explosion(pygame.sprite.Sprite):
    """Explosion sprite.  Kills self after animation is done."""
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        Sounds.get('explosion').play()
        self.images, self.rect = Images.get('explosion')
        self.rect.centerx = x
        self.rect.centery = y
        self.nframes = len(self.images)
        self.frame = 0
        self.image = self.images[self.frame]
        self.aspeed = 0.5
        
    def update(self):
        self.frame = (self.frame+self.aspeed)
        if self.frame >= self.nframes:
            self.kill()
        else:
            self.image = self.images[int(self.frame)]
        
#classes for our game objects
class Bear(pygame.sprite.Sprite):
    """moves a teddy bear around the screen"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.images, self.rect = Images.get('bear')
        self.frame = 0
        self.aspeed = 0.5 + random()
        self.nframes = len(self.images)
        self.image = self.images[self.frame]
        direction = randint(0,359)
        angle = pi*direction/180.0
        speed = randint(5,10)
        self.hspeed = speed * cos(angle)
        self.vspeed = speed * sin(angle)
        self.rect = self.rect.move(randint(32,screensize[0]-32*2), randint(32,screensize[1]-32*2))

    def update(self):
        "move the bear based on speed and direction"
        self.rect = self.rect.move(self.hspeed, self.vspeed)
        self.frame = (self.aspeed+self.frame)
        while self.frame >= self.nframes:
            self.frame -= self.nframes
        self.image = self.images[int(self.frame)]
        
    def kill(self):
        Sprites.add(Explosion(self.rect.centerx, self.rect.centery))
        pygame.sprite.Sprite.kill(self)
        
class Wall(pygame.sprite.Sprite):
    """static walls to bounce off"""
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = Images.get('Square')
        self.rect = self.rect.move(x,y)

    def update(self):
        pass;

class Cursor(pygame.sprite.Sprite):
    """moves crosshairs following mouse"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.image, self.rect = Images.get('cursor')
        
    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.centerx,self.rect.centery = pos

# Global Resource Managers
Images = ImageManager()
Sounds = SoundManager()

#Global Sprite Groups
Sprites = pygame.sprite.RenderPlain()
Bear_sprites = pygame.sprite.RenderPlain()
Wall_sprites = pygame.sprite.RenderPlain()
    
def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
    
    global images, sounds, sprites
#Initialize Everything
    pygame.init()
    screen = pygame.display.set_mode(screensize)
    pygame.display.set_caption('Click the Bears!')
    pygame.mouse.set_visible(False)

#Create The Backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    Images.load_image('sky.gif')
    background_image, background_rect = Images.get('sky')
    for x in range(0,background.get_width(),background_image.get_width()):
        for y in range(0,background.get_height(),background_image.get_height()):
            background.blit(background_image,(x,y))
    
#Put Text On The Background, Centered
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("Click the Bears!", 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        textpos.centery = background.get_rect().centery
        background.blit(text, textpos)

#Display The Background
    screen.blit(background, (0, 0))
    pygame.display.flip()
    sleep(1)
    
#Prepare Game Resources
    clock = pygame.time.Clock()
    Images.load_strip('explosion.bmp', 71, 100, -1)
    Images.load_strip('bear.bmp', 32, 32, -1)
    Images.load_image('Square.png')
    
    Sounds.load_sound('explosion.wav')
    
#Create Game Objects
    cursor = Cursor()
    Sprites.add(cursor)
    for bears in range(0,10):
        Bear_sprites.add(Bear())
    Sprites.add(Bear_sprites)
    for wallpos in range(0,screensize[0],32):
        Wall_sprites.add(Wall(wallpos,0))
        Wall_sprites.add(Wall(wallpos,screensize[1]-32))
    for wallpos in range(0,screensize[1],32):
        Wall_sprites.add(Wall(0,wallpos))
        Wall_sprites.add(Wall(screensize[0]-32,wallpos))
    Sprites.add(Wall_sprites)
        
    background_offset = 0
    bgw,bgh = background.get_size()
    imw,imh = background_image.get_size()
    
#Main Loop
    while 1:
        clock.tick(30)
        
    #Scroll background
        background_offset = (2 + background_offset) % imh
        for x in range(0,bgw,imw):
            for y in range(-imh,bgh,imh):
                background.blit(background_image,(x,y+background_offset))
        
    #Handle collisions:
        for bear in Bear_sprites:
            for otherbear in pygame.sprite.spritecollide(bear, Bear_sprites, 0):
                if bear != otherbear:
                    bounce(bear, otherbear)
            for wall in pygame.sprite.spritecollide(bear, Wall_sprites, 0):
                bounce(bear, wall)

    #Handle Input Events
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == MOUSEBUTTONDOWN:
                for bear in pygame.sprite.spritecollide(cursor, Bear_sprites, 1):
                    pass
                   
    #Update sprites
        Sprites.update()

    #Draw Everything
        screen.blit(background, (0, 0))
        Sprites.draw(screen)
        pygame.display.flip()

#Game Over

#this calls the 'main' function when this script is executed
if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
