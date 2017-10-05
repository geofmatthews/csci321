import pygame, math, random,os
from resources import ResourceManager
from pygame.locals import *

from utilities import loadImage
from tiles import TileManager

class Thing(pygame.sprite.Sprite):
    def __init__(self, name,
                 width, height,
                 row, col,
                 nframes=1,
                 horizontal=True,
                 addframe=True,
                 scale = 3,
                 sheetfile='things.png',
                 folder = os.path.join('data','images')):
        pygame.sprite.Sprite.__init__(self)
        sheet = loadImage(sheetfile, folder)
        self.images = []
        for frame in range(nframes):
            img = pygame.Surface((width,height))
            x = col*width
            y = row*height
            if horizontal:
                x += frame*width
            else:
                y += frame*height
            img.blit(sheet, (0,0), ((x,y),(width,height)))
            img.set_colorkey(img.get_at((0,0)))
            self.images.append(pygame.transform.scale(img, (width*scale,height*scale)))
        self.image = self.images[0]
        if addframe and nframes == 3:
            self.images.append(self.images[1])
        self.rect = self.image.get_rect()
        self.frame = 0.0
        self.aspeed = 0.125
        self.name = name
        self.opening = False
        self.animated = False

    def activate(self):
        if not self.animated:
            self.opening = True
    
    def update(self):
        if self.animated:
            self.frame += self.aspeed
            if self.frame >= len(self.images):
                self.frame = 0.0
        elif self.opening:
            self.frame += self.aspeed
            if self.frame >= len(self.images):
                self.opening = False
                self.frame = len(self.images)-1
        self.image = self.images[int(self.frame)]

class _ThingManager():
    def __init__(self,
                 thingmap = 'thingmap.data',
                 thingfolder = os.path.join('data','text'),
                 imagefolder = os.path.join('data','images')
                 ):
        self.thingmap = thingmap
        self.thingfolder = thingfolder
        self.imagefolder = imagefolder
        self.initialized = False

    def initialize(self, scale=3):
        if self.initialized:
            return self
        self.initialized = True
        thingfile = open(os.path.join(self.thingfolder, self.thingmap),'r')
        thinglines = thingfile.read().splitlines()
        self.dict = {}
        self.things = pygame.sprite.RenderPlain()
        for x in thinglines:
            mapping = [s.strip() for s in x.split(',')]
            name,f,w,h,row,col,nframes,horiz,exf,roomrow,roomcol,anim = mapping
            width = int(w)
            height = int(h)
            row = int(row)
            col = int(col)
            nframes = int(nframes)
            horizontal = horiz == 'horizontal'
            extraframe = exf == 'extraframe'
            roomrow = int(roomrow)
            roomcol = int(roomcol)
            animate = anim == 'animate'

            if not self.dict.has_key(name):
                self.dict[name] = pygame.sprite.RenderPlain()
            newthing = Thing(name, width, height,
                             row, col,
                             nframes,
                             horizontal,
                             extraframe,
                             scale,
                             sheetfile=f,
                             folder=self.imagefolder)
            newthing.rect.topleft = (roomcol * width * scale,
                                     roomrow * height * scale)
            # special cases:
            if name == 'jaildoor':
                for img in newthing.images:
                    w,h = img.get_size()
                    img.set_colorkey(newthing.images[3].get_at((w-1,h-1)))
            if name == 'yellowtorch' or name == 'fireplace':
                newthing.animated = True
                    
            self.things.add(newthing)
            self.dict[name].add(newthing)
        return self

_thingmanager = _ThingManager()
def ThingManager():
    return _thingmanager

#### Some tests:
if __name__ == "__main__":
    scale = 3
    size = scale*16
    try:
        pygame.init()
        screen = pygame.display.set_mode((400*scale,240*scale))
        # now we can initialize the resource manager:
        tm = TileManager().initialize(scale=scale)
        thm = ThingManager().initialize(scale=scale)

        clock = pygame.time.Clock()               
        done = False
        while not(done): 
            clock.tick(30)
            screen.fill((0,0,0))
            
            tm.tiles.draw(screen)
            
            thm.things.update()
            thm.things.draw(screen)
            
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == QUIT:
                    done = True
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        done = True
                    elif event.key == K_SPACE:
                        for thing in thm.things:
                            thing.activate()
    finally:
        pygame.quit()
        
