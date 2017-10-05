import pygame, math, random,os
from resources import ResourceManager
from pygame.locals import *

from utilities import loadImage
from tiles import TileManager
from things import ThingManager

class Char(pygame.sprite.Sprite):
    def __init__(self, name,
                 width, height,
                 row, col,
                 nframes=3,
                 scale=2,
                 sheetfile='characters.png',
                 folder=os.path.join('data','images')):
        pygame.sprite.Sprite.__init__(self)
        sheet = loadImage(sheetfile, folder)
        self.name = name
        self.scale = scale
        self.images = {}
        for d,direction in enumerate(['south','west','east','north']):
            self.images[direction] = []
            for i in range(nframes):
                image = pygame.Surface((width, height))
                image.blit(sheet, (0,0), (((col+i)*width, (row+d)*height), (width,height)))
                image.set_colorkey(image.get_at((0,0)))
                image = pygame.transform.scale(image, ((scale*width), (scale*height)))
                self.images[direction].append(image)
            self.images[direction].append(self.images[direction][1])
        self.direction = 'south'
        self.speed = 0
        self.image = self.images['south'][0]
        self.rect = self.image.get_rect()
        self.frame = 0.0
        self.aspeed = 0.25
        self.name = name
        self.cellsize = (width*scale, height*scale)

    def collide(self):
        if self.speed > 0:
            things = TileManager().invisibleBlocks
            newrect = self.rect.inflate(5,5)
            if self.direction == 'south':
                point = newrect.midbottom
            elif self.direction == 'north':
                point = newrect.midtop
            elif self.direction == 'east':
                point = newrect.midright
            elif self.direction == 'west':
                point = newrect.midleft
            for thing in TileManager().invisibleBlocks:
                if thing.rect.collidepoint(point):
                    return True
            for thing in [a for a in ThingManager().things if a.solid]:
                if thing.rect.collidepoint(point):
                    return True
        return False          
        
    def update(self):
        if self.speed == 0:
            self.frame = 1
            self.image = self.images[self.direction][int(self.frame)]
        else:
            self.frame += self.aspeed
            if self.frame >= len(self.images[self.direction]):
                self.frame = 0.0
            self.image = self.images[self.direction][int(self.frame)]
            if self.direction == 'south':
                self.rect.top += self.speed
            elif self.direction == 'north':
                self.rect.top -= self.speed
            elif self.direction == 'west':
                self.rect.left -= self.speed
            elif self.direction == 'east':
                self.rect.left += self.speed
            cellx, celly = self.cellsize
            if self.rect.left % cellx == 0 and self.rect.top % celly == 0:
                self.speed = 0
            
    def face(self, direction):
        self.direction = direction

    def move(self, direction):
        if self.speed == 0:
            self.direction = direction
            self.speed = 1*self.scale
            if self.collide():
                self.speed = 0

class _CharManager():
    def __init__(self,
                 charfile = 'characters.data',
                 charfolder = os.path.join('data','text'),
                 sheet = 'characters.png',
                 imagefolder = os.path.join('data','images')
                 ):
        self.charfile = charfile
        self.charfolder = charfolder
        self.imagefolder = imagefolder
        self.initialized = False

    def initialize(self, scale=2):
        if self.initialized:
            return self
        self.initialized = True
        charfile = open(os.path.join(self.charfolder, self.charfile))
        charlines = charfile.read().splitlines()
        self.dict = {}
        self.chars = pygame.sprite.RenderPlain()
        for x in charlines:
            mapping = [s.strip() for s in x.split(',')]
            name,f,w,h,row,col,nframes,direction,roomrow,roomcol = mapping
            sheet = f
            width = int(w)
            height = int(h)
            row = int(row)
            col = int(col)
            nframes = int(nframes)
            roomrow = int(roomrow)
            roomcol = int(roomcol)

            if not self.dict.has_key(name):
                self.dict[name] = pygame.sprite.RenderPlain()
            newchar = Char(name, width, height,
                           row, col,
                           nframes,
                           scale,
                           sheet, self.imagefolder)
            newchar.rect.topleft = (roomcol * width * scale, roomrow * height * scale)
            newchar.face(direction)

            self.chars.add(newchar)
            self.dict[name].add(newchar)

        return self

_charmanager = _CharManager()
def CharManager():
    return _charmanager

#### Some tests:
if __name__ == "__main__":
    scale = 2
    size = scale*16
    try:
        pygame.init()
        world = pygame.Surface((400*scale, 240*scale))
        screensize = (320*scale, 240*scale)
        screen = pygame.display.set_mode(screensize)
        # now we can initialize the resource managers:
        tm = TileManager().initialize(scale=scale)
        thm = ThingManager().initialize(scale=scale)
        cm = CharManager().initialize(scale=scale)

        avatar = Char('gal',16,16,0,6,3,scale)
        avatar.rect.topleft = (15*size, 11*size)
        cm.chars.add(avatar)
        visiblerect = pygame.Rect(((0,0), screensize))
        visiblerect.center = avatar.rect.center

        clock = pygame.time.Clock()               
        done = False
        while not(done):
            clock.tick(30)
            world.fill((0,0,0))
            
            tm.tiles.draw(world)
            
            thm.things.update()
            thm.things.draw(world)

            cm.chars.update()
            cm.chars.draw(world)

            visiblerect.center = avatar.rect.center
            screen.blit(world, (0,0), visiblerect)
          
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == QUIT:
                    done = True
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        done = True
                    elif event.key == K_SPACE:
                        for thing in thm.things.sprites():
                            crect = avatar.rect.inflate(2,2)
                            if crect.colliderect(thing.rect):
                                thing.activate()

            pressed = pygame.key.get_pressed()
            if pressed[K_LEFT]:
                avatar.move('west')
            elif pressed[K_RIGHT]:
                avatar.move('east')
            elif pressed[K_UP]:
                avatar.move('north')
            elif pressed[K_DOWN]:
                avatar.move('south')
            
    finally:
        pygame.quit()
        
