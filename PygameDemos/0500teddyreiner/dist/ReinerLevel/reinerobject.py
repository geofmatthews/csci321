import pygame
import os
from gameobject import Stat, Mob
from imagemanager import ImageManager

_headings = ('e','ne','n','nw','w','sw','s','se')

class ReinerMob(Mob):
    def __init__(self, pos, screen, animations):
        self.animations = animations
        self.aspeed = 0.5
        self.frame = 0
        self.image = animations['s']['looking'][0]
        self.rect = self.image.get_rect()
        Mob.__init__(self, pos, screen)
        
    def update(self):
        d = _headings[self.heading]
        if self.speed > 0.05: a = 'walking'
        else: a = 'looking'
        frames = self.animations[d][a]
        self.frame += self.aspeed
        self.frame %= len(frames)
        self.image = frames[int(self.frame)]
        Mob.update(self)

class Dino(ReinerMob):
    def __init__(self, pos, screen):
        folder = os.path.join('ReinerLevel','data','T_dino_red','dino red bitmaps')
        ImageManager().loadAnimations(folder, 'Dino')
        animations = ImageManager().getAnimations('Dino')
        ReinerMob.__init__(self, pos, screen, animations)

class Ogre(ReinerMob):
    def __init__(self, pos, screen):
        folder = os.path.join('ReinerLevel','data','T_ogre','ogre 96x bitmaps')
        ImageManager().loadAnimations(folder, 'Ogre')
        animations = ImageManager().getAnimations('Ogre')
        ReinerMob.__init__(self, pos, screen, animations)
        
class Tree2(Stat):
    def __init__(self, pos, screen, index):
        filename = os.path.join('ReinerLevel','data','T_trees2','trees2 tileset.bmp')
        ImageManager().loadStatic(filename, 'Tree2')
        tileset = ImageManager().getStatic('Tree2')
        self.image = pygame.Surface((128,128))
        x,y = 128*(index % 4), 128*int(index / 4)
        self.image.blit(tileset, (0,0), pygame.Rect(x,y,128,128))
        self.image.set_colorkey(self.image.get_at((0,0)))
        self.rect = self.image.get_rect()
        Stat.__init__(self, pos, screen)
    
