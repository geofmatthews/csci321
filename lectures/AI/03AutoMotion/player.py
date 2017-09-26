"""
player.py
Defines Player and PlayerGroup class
Geoffrey Matthews
2007
"""

import pygame
import random, math
import vectors as V
from datamanagers import Images
import states as S
from constants import *

class AutoObject(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.depth = 0
        self.prevpos = V.vector(pos)
        self.velocity = V.vector(0,0)
        self.visible = True
        self.showheading = False
        self.showbox = False
        
    def update(self): pass
    def draw(self, screen): pass
    def changeState(self, newstate, **args): pass

class Block(AutoObject):
    def __init__(self, pos):
        AutoObject.__init__(self, pos)
        self.image = Images.get('square')
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.imagesize = self.rect.size

    def draw(self, screen):
        if self.showbox:
            pygame.draw.rect(screen, (255,0,0), self.rect, 1) 
            pygame.draw.rect(screen, (255,125,125), (self.topleft,self.imagesize),  1)
            
    def _gettopleft(self):
        return self.rect.topleft
    
    topleft = property(fget=_gettopleft)
 
class Player(AutoObject):
    wpos, hpos = 0.5, 0.7  # rel pos for center of rect in image
    wfrac, hfrac = 0.3, 0.2 # rel size of rect to image
    
    def __init__(self, name, pos, maxspeed=PLAYER_MAXSPEED, screen=None):
        AutoObject.__init__(self, pos)

        # Image and rect vars
        self.name = name
        self.images = Images.get(self.name)['e']['looking']
        self.imagesize = self.images[0].get_size()
        w,h = self.imagesize
        self.rect = pygame.Rect(0, 0, Player.wfrac*w, Player.hfrac*h)
        self.rect.center = V.vector(pos)

        # Physics vars
        self.obstacles = []
        self.state = S.Wait()
        
        self.maxspeed = maxspeed
        self.maxforce = maxspeed*0.1

        self.velocity = V.vector(0,0)
        self.steering = V.vector(0,0)
        randang = random.uniform(0, 2*math.pi)
        x,y = math.cos(randang), math.sin(randang)
        self.heading = V.vector(x,y)
        self.dir = 's'

        # Animation vars
        self.depth = 0
        self.nframes = len(self.images)
        self.frame = random.randint(0,self.nframes-1)
        self.mass = 1.0

        # Vars that should be in the state (IMHO):
        wanderangle = random.uniform(0, 2*math.pi)
        self.wanderpoint = V.vector(math.cos(wanderangle), math.sin(wanderangle))
        V.normalize_ip(self.wanderpoint)

        self.seektarget = None
        self.seektarget2 = None

    def _gettopleft(self):
        """pos to blit the image"""
        w,h = self.imagesize
        x = int(self.rect.centerx - Player.wpos*w)
        y = int(self.rect.centery - Player.hpos*h)
        return (x,y)

    topleft = property(fget=_gettopleft)
        
    def changeState(self, newstate, **args):
        self.state.exit(self)
        self.state = newstate
        self.state.enter(self, **args)

    def update(self):

        self.prevpos = V.vector(self.rect.center).copy()

        self.state.execute(self)
        
        ## Add a tiny force toward the center of the field
        if False:#self.state != S.Wait():
            center = V.vector(pygame.display.get_surface().get_rect().center)
            towardcenter = center - self.rect.center
            V.normalize_ip(towardcenter)
            self.steering += 0.5*towardcenter      
        
        self.velocity += FORCE_PER_TICK*self.steering/(self.mass)
        V.truncate(self.velocity, self.maxspeed)

        speed = V.length(self.velocity)
        if speed > 0.001:
            self.heading = V.normalize(self.velocity)
        self.rect.center += self.velocity
        self.depth = -self.rect.centery
        
    #determine which image direction to use, based on heading and velocity:
        if speed >= 0.001:
            small = 0.382 # sin(22.5 degrees)
            big = 0.923  # cos(22.5 degrees)
            x,y = self.heading
            if y >= big: self.dir = 's'
            elif small <= y:
                if x > 0: self.dir = 'se'
                else: self.dir = 'sw'
            elif -small <= y:
                if x > 0: self.dir = 'e'
                else: self.dir = 'w'
            elif -big <= y:
                if x > 0: self.dir = 'ne'
                else: self.dir = 'nw'
            else: self.dir = 'n'
        else:
            self.velocity[0] = self.velocity[1] = 0.0
        
    #image action:  stopped or moving?
        if speed < 0.001: 
            self.aspeed = 0.5
            action = 'looking'
        else: 
            self.aspeed = 0.2*speed
            action = 'walking'
            
        self.images = Images.get(self.name)[self.dir][action]
        self.nframes = len(self.images)
        
    #advance animation frame
        self.frame = self.aspeed+self.frame
        while self.frame >= self.nframes: self.frame -= self.nframes
        self.image = self.images[int(self.frame)]

    def draw(self, screen):
        if self.showbox:
            pygame.draw.rect(screen, (255,0,0), self.rect, 1) 
            #pygame.draw.rect(screen, (255,125,125), (self.topleft,self.imagesize),  1)
        if self.showheading:
            pos = self.rect.center
            endpos = pos + 20*self.velocity
            pygame.draw.line(screen, (0,0,255), pos, endpos, 2)
            if self.state == S.Wander():
                col = (200,200,100)
                wcent = V.integer(pos + WANDER_OFFSET*self.heading)
                wpoint = V.integer(wcent + WANDER_RADIUS*self.wanderpoint)
                pygame.draw.circle(screen, col, wcent, WANDER_RADIUS,1)
                pygame.draw.circle(screen, col, wpoint, 5)

def playercollideany(sprite, group):
    """a spritecollide that ignores self"""
    spritecollide = sprite.rect.colliderect
    for s in group:
        if spritecollide(s.rect) and s != sprite:
            return s
    return None
    
class PlayerGroup(pygame.sprite.Group):
    def __init__(self, *sprites):
        pygame.sprite.Group.__init__(self)
        self.add(*sprites)

    def update(self, solids, *args):
        """call sprite.update, and back them up when rects collide"""
        sprites = self.sprites()
        for s in sprites:
            s.update(*args)
            collision = playercollideany(s, solids)
            if collision:
                s.rect.center = s.prevpos
                s.velocity[0] = s.velocity[1] = 0.0
                    
    def draw(self, surface):
        """draws all sprites to surface in depth order (deepest first)
           and at spr.topleft, not at spr.rect
           also calls the sprite draw function, if it exists"""
        sprites = self.sprites()
        sprites.sort(key = lambda x:x.depth, reverse=True)
        surface_blit = surface.blit
        spritedict = self.spritedict
        for spr in sprites:
            if spr.visible:
                spr.draw(surface)
                spritedict[spr] = surface_blit(spr.image, spr.topleft)
        self.lostsprites = []
           

class Dino(Player):
    def __init__(self,pos):
        Player.__init__(self,'dino',pos)
        
class Ogre(Player):
    def __init__(self,pos):
        Player.__init__(self,'ogre',pos)
        
class Ball(Player):
    def __init__(self,pos):
        Player.__init__(self,'ball',pos,2*PLAYER_MAXSPEED)

if __name__ == '__main__':
    import auto
    try:
        auto.main()
    finally:
        pygame.quit()
        
    
