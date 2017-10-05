import os, pygame
from pygame.locals import *
from utilities import loadImage


class InvisibleBlock(pygame.sprite.Sprite):
    def __init__(self, rect):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect

    def draw(surface):
        pass

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, position, wall):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.rect.topleft = position
        self.wall = wall

class EmptyTile(pygame.sprite.Sprite):
    """Used to fill empty space, so that each cell of the board
       can hold some data.  For example, "Are you a wall?"""
    def __init__(self, wall = False):
        pygame.sprite.Sprite.__init__(self)
        self.wall = wall
    

class _TileManager():
    def __init__(self,tilefile='basictiles.png',
                 room='roomtiling.data',
                 tilemap='tilemap.data',
                 datafolder=os.path.join('data','text'),
                 imagefolder=os.path.join('data','images')
                 ):
        self.tilefile = tilefile
        self.room = room
        self.tilemap = tilemap
        self.datafolder = datafolder
        self.imagefolder = imagefolder
        self.invisibleBlocks = []
        self.initialized = False
        
    def initialize(self, scale = 3):
        if self.initialized:
            return self
        self.initialized = True
        # load all the tiles
        self.tilefile = loadImage( self.tilefile, self.imagefolder, colorkey=None)
        mapfile = open(os.path.join(self.datafolder, self.tilemap), 'r')
        maplines = mapfile.read().splitlines()
        self.dict = {}
        for x in maplines:
            mapping = [s.strip() for s in x.split(',')]
            key = mapping[6]
            self.dict[key] = {}
            w,h = int(mapping[2]), int(mapping[3])
            row, col = int(mapping[4]), int(mapping[5])
            self.dict[key]['name'] = mapping[0]
            self.dict[key]['file'] = mapping[1]
            self.dict[key]['width'] = w
            self.dict[key]['height'] = h
            self.dict[key]['row'] =  row
            self.dict[key]['col'] = col
            self.dict[key]['roomkey'] = mapping[6]
            self.dict[key]['wall'] = mapping[7] == 'wall'
                
            # find image for this tile
            #w, h = self.dict[key]['width'], self.dict[key]['height']
            #row, col = self.dict[key]['row'], self.dict[key]['col']
            image = pygame.Surface((w,h))
            image.blit(self.tilefile, (0,0),
                       ((col*w, row*h), (w,h)))
            image = pygame.transform.scale(image, (scale*w, scale*h))
            letter = self.dict[key]['roomkey']
            if letter in '12346':
                w,h = image.get_size()
                image.set_colorkey(image.get_at((w/2,h/2)))
            elif letter in '578':
                image.set_colorkey(image.get_at((0,0)))
            self.dict[key]['image'] = image

        # tile the room
        roomfile = open(os.path.join(self.datafolder, self.room),'r')
        roomrows = roomfile.read().splitlines()
        self.tiles = pygame.sprite.RenderPlain()
        self.tileArray = [[None for x in range(len(roomrows[0]))]
                          for y in range(len(roomrows))]
        for roomrow, keys in enumerate(roomrows):
            for roomcol, letter in enumerate(keys):
                if letter == '.':
                    newTile = EmptyTile()
                else:
                    data = self.dict[letter]
                    newTile = Tile(data['image'],
                                   (roomcol*scale*w, roomrow*scale*h),
                                   data['wall'])
                    if data['wall']:
                        newBlock = InvisibleBlock(
                            pygame.Rect(roomcol*scale*w, roomrow*scale*h,
                                        scale*w, scale*h))
                        self.invisibleBlocks.append(newBlock)
                    self.tiles.add(newTile)
                self.tileArray[roomrow][roomcol] = newTile
        return self

_tilemanager = _TileManager()
def TileManager():
    return _tilemanager

#### Some tests:
if __name__ == "__main__":
    scale = 3
    try:
        pygame.init()
        screen = pygame.display.set_mode((scale*400, scale*240))
        # now we can initialize the tile manager:
        tm = TileManager().initialize()
        done = False
        while not(done):
            screen.fill((128,0,0))
            tm.tiles.draw(screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == QUIT:
                    done = True
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    done = True
    finally:
        pygame.quit()
        


