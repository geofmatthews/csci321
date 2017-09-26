
import pygame,random,sys
from pygame.locals import *
from GM import utilities
from GM.statemachine import StateMachine, State
from GM.vector import *
import GM.makeimage
from functions import closest
from constants import *

from gatherers import Gatherer
from enemies import Enemy, DeadEnemy
from goodies import Goody

class World():
    def __init__(self, screen):
        self.screen = screen
        self.center = screen.get_width()/2.0, screen.get_height()/2.0
        self.gatherers = pygame.sprite.Group()
        self.goodies = pygame.sprite.Group()
        self.collected = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.deadenemies = pygame.sprite.Group()
        self.allsprites = pygame.sprite.Group()

    def update(self):
        self.allsprites.update()

    def draw(self):
        self.allsprites.draw(self.screen)

    def addGatherer(self, pos):
        Gatherer(pos,self,self.gatherers,self.allsprites)

    def addGoody(self, pos):
        Goody(pos,self,self.goodies,self.allsprites)

    def collectGoody(self, goody):
        self.goodies.remove(goody)
        self.collected.add(goody)

    def uncollectGoody(self, goody):
        self.collected.remove(goody)
        self.goodies.add(goody)

    def addEnemy(self, pos):
        Enemy(pos,self,self.enemies,self.allsprites)

    def killEnemy(self, enemy):
        pos = enemy.pos
        enemy.kill()
        enemy.rect.center = -100,-100
        DeadEnemy(pos, self, self.deadenemies, self.allsprites)
        
    def randomPosition(self):
        x = random.randint(0,self.screen.get_width()-1)
        y = random.randint(0,self.screen.get_height()-1)
        return vector(x,y)


    def outside(self, actor):
        rect = actor.rect
        left = rect.right < 0
        right = rect.left > self.screen.get_width()
        up = rect.bottom < 0
        down = rect.top > self.screen.get_height()
        return left or right or up or down

        
