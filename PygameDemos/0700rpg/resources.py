import os, pygame
from pygame.locals import *

imagePixels = 16
scaledPixels = 64

def _loadSound(name, folder=os.path.join("data", "sounds")):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        sound = NoneSound()
    else:
        fullname=os.path.join(folder, name)
        try:
            sound = pygame.mixer.Sound(fullname)
        except pygame.error as message:
            print "Cannot load sound:", fullname
            raise SystemExit(message)
        return sound

def _loadImage(name, folder=os.path.join("data","images"),colorkey=-1):
    fullname = os.path.join(folder, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print "Cannot load image:", fullname
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey)
    return image

def _loadSpritesheet(name,
                    start = (0,0),
                    imagesize=(imagePixels,imagePixels),
                    count=8,
                    folder=os.path.join("data","images")):
    spritesheet = _loadImage(name, folder, colorkey=None)
    
    images = []
    for row in range(count):
        image = pygame.Surface(imagesize).convert()
        x = start[0] + row*imagesize[0]
        y = start[1]
        image.blit(spritesheet, (0,0), ((x,y),imagesize))
        image.set_colorkey(image.get_at((0,0)))
        images.append(pygame.transform.scale(image, (scaledPixels,scaledPixels)))
    return images

def _loadTileset(name,
                 imagesize=(imagePixels,imagePixels),
                 rows = 8, cols = 8,
                 folder=os.path.join("data","images")):
    tileset = _loadImage(name, folder, colorkey = None)
    images = {}
    for i in range(rows):
        images[i] = {}
    for row in range(rows):
        for col in range(cols):
            im = pygame.Surface(imagesize)
            im.fill((255,0,0))
            im.blit(tileset,
                       (0,0),
                       ((col*imagesize[0], row*imagesize[1]),
                        imagesize))
            #im.set_colorkey(im.get_at((0,0)))
            images[row][col] = pygame.transform.scale(im, (scaledPixels,scaledPixels))
    return images

class _ResourceManager:
    def __init__(self,
                 imgpath=os.path.join("data","images"),
                 sndpath=os.path.join("data","sounds")):
        self.imgpath = imgpath
        self.sndpath = sndpath
        self.initialized = False
        
    # can't initialize until after pygame display is initialized:
    def initialize(self):
        if self.initialized:
            return self
        self.initialized = True
        self.tileset = _loadImage('basictiles.png')
        self.basicTiles = _loadTileset('basictiles.png',
                                       (imagePixels,imagePixels),
                                       15,8)
        self.char = {}
        south, west, east, north = 0,1,2,3
        for char in range(4):
            self.char[char] = {}
            for direction in (south, west, east, north):
                self.char[char][direction] = _loadSpritesheet('characters.png',
                                                   (imagePixels*char*3, imagePixels*direction),
                                                   (imagePixels,imagePixels),
                                                   3)
        for char in range(4):
            self.char[char+4] = {}
            for direction in (south, west, east, north):
                self.char[char+4][direction] = _loadSpritesheet('characters.png',
                                                              (imagePixels*char*3,imagePixels*4+imagePixels*direction),
                                                              (imagePixels,imagePixels),
                                                              3)
        return self

# singleton interface, can't initialize until later:
_resourcemanager = _ResourceManager()
def ResourceManager():
    return _resourcemanager

#### Some tests:
if __name__ == "__main__":
    try:
        pygame.init()
        screen = pygame.display.set_mode((1280, 960))
        # now we can initialize the resource manager:
        rm = ResourceManager().initialize()
        done = False
        while not(done):
            screen.fill((0,0,255))

            #screen.blit(rm.tileset, (scaledPixels*10, 0))
            
            for row in range(15):
                for col in range(8):
                    screen.blit(rm.basicTiles[row][col],
                                (col*scaledPixels, row*scaledPixels))

            for char in range(8):
                for direction in range(4):
                    for pose in range(3):
                        screen.blit(rm.char[char][direction][pose],
                                    (300 + char*3*scaledPixels + pose*scaledPixels, direction*scaledPixels))
                
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == QUIT:
                    done = True
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    done = True
    finally:
        pygame.quit()
        


