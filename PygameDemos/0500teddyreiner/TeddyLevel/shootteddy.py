#/usr/bin/env python
"""
Click on the bear and make him explode.
Designed to be similar to a Gamemaker game.

Geoffrey Matthews
2006
"""

#Import Modules
import os, pygame
from pygame.locals import *
from random import randint, random
from math import sin, cos, pi

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

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
        fullname = os.path.join('TeddyLevel', 'data', name)
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
            fullname = os.path.join('TeddyLevel', 'data', name)
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
    def __init__(self,x,y,Images,Sounds):
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
    def __init__(self, Images, screensize, Sprites, Sounds):
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
        self.Sprites = Sprites
        self.Sounds = Sounds
        self.Images = Images

    def update(self):
        "move the bear based on speed and direction"
        self.rect = self.rect.move(self.hspeed, self.vspeed)
        self.frame = (self.aspeed+self.frame)
        while self.frame >= self.nframes:
            self.frame -= self.nframes
        self.image = self.images[int(self.frame)]
        
    def kill(self):
        self.Sprites.add(Explosion(self.rect.centerx, self.rect.centery, self.Images, self.Sounds))
        pygame.sprite.Sprite.kill(self)
        
class Wall(pygame.sprite.Sprite):
    """static walls to bounce off"""
    def __init__(self,x,y, Images):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = Images.get('Square')
        self.rect = self.rect.move(x,y)

    def update(self):
        pass;

class Cursor(pygame.sprite.Sprite):
    """moves crosshairs following mouse"""
    def __init__(self, Images):
        pygame.sprite.Sprite.__init__(self) 
        self.image, self.rect = Images.get('cursor')
        
    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.centerx,self.rect.centery = pos

class TeddyRoom:
    
    def __init__(self, screen):
    #Initialize Everything
    # Global Resource Managers
        self.Images = ImageManager()
        self.Sounds = SoundManager()

        #Global Sprite Groups
        self.Sprites = pygame.sprite.RenderPlain()
        self.Bear_sprites = pygame.sprite.RenderPlain()
        self.Wall_sprites = pygame.sprite.RenderPlain()
        self.screen = screen
        self.screensize = screen.get_size()
        pygame.mouse.set_visible(False)

    #Create The Backgound
        self.background = pygame.Surface(screen.get_size())
        self.background = self.background.convert()
        self.Images.load_image('sky.gif')
        self.background_image, self.background_rect = self.Images.get('sky')
        for x in range(0,self.background.get_width(),self.background_image.get_width()):
            for y in range(0,self.background.get_height(),self.background_image.get_height()):
                self.background.blit(self.background_image,(x,y))
        
    #Prepare Game Resources
        self.Images.load_strip('explosion.bmp', 71, 100, -1)
        self.Images.load_strip('bear.bmp', 32, 32, -1)
        self.Images.load_image('Square.png')
        
        self.Sounds.load_sound('explosion.wav')
        
    #Create Game Objects
        self.cursor = Cursor(self.Images)
        self.Sprites.add(self.cursor)
        for bears in range(0,10):
            self.Bear_sprites.add(Bear(self.Images,self.screensize,self.Sprites,self.Sounds))
        self.Sprites.add(self.Bear_sprites)
        for wallpos in range(0,self.screensize[0],32):
            self.Wall_sprites.add(Wall(wallpos,0,self.Images))
            self.Wall_sprites.add(Wall(wallpos,self.screensize[1]-32,self.Images))
        for wallpos in range(0,self.screensize[1],32):
            self.Wall_sprites.add(Wall(0,wallpos,self.Images))
            self.Wall_sprites.add(Wall(self.screensize[0]-32,wallpos,self.Images))
        self.Sprites.add(self.Wall_sprites)
            
        self.background_offset = 0

    def run(self, events):
    #Main Loop body
    #Scroll background
        bgw,bgh = self.background.get_size()
        imw,imh = self.background_image.get_size()
        self.background_offset = (2 + self.background_offset) % imh
        for x in range(0,bgw,imw):
            for y in range(-imh,bgh,imh):
                self.background.blit(self.background_image,(x,y+self.background_offset))
        
    #Handle collisions:
        for bear in self.Bear_sprites:
            for otherbear in pygame.sprite.spritecollide(bear, self.Bear_sprites, 0):
                if bear != otherbear:
                    bounce(bear, otherbear)
            for wall in pygame.sprite.spritecollide(bear, self.Wall_sprites, 0):
                bounce(bear, wall)

    #Handle Input Events
        for event in events:
            if event.type == MOUSEBUTTONDOWN:
                for bear in pygame.sprite.spritecollide(self.cursor, self.Bear_sprites, 1):
                    pass
                   
    #Update sprites
        self.Sprites.update()

    #Draw Everything
        self.screen.blit(self.background, (0, 0))
        self.Sprites.draw(self.screen)
        pygame.display.flip()

#Game Over
