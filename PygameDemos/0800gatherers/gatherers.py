
import pygame,random,sys
from pygame.locals import *
from GM import utilities
from GM.statemachine import StateMachine, State
from GM.vector import *
import GM.makeimage
from functions import closest
from constants import *

class Gatherer(pygame.sprite.Sprite):
    def __init__(self, pos, world, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.images = GM.makeimage.rotating_arrow(GATHERER_SIZE,GATHERER_COLOR)
        self.frame = 0
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect()
        self.pos = vector(pos)
        self.rect.center = self.pos
        self.world = world

        self.heading = randomNormalVector()
        self.speed = GATHERER_SPEED
        self.stateMachine = StateMachine(self, Search())

        self.goody = None
        
    def update(self):
        self.stateMachine.update()
        width, height = self.world.screen.get_size()
        angle = N.arctan2(self.heading[1],self.heading[0])*180.0/N.pi
        self.frame = int((angle % 360)/10.0)
        self.image = self.images[self.frame]
        self.pos += self.heading*self.speed
        if self.pos[0] < 0:
            self.pos[0] = 0
            self.heading[0] = -self.heading[0]
        if self.pos[0] > width:
            self.pos[0] = width
            self.heading[0] = -self.heading[0]
        if self.pos[1] < 0:
            self.pos[1] = 0
            self.heading[1] = - self.heading[1]
        if self.pos[1] > height:
            self.pos[1] = height
            self.heading[1] = - self.heading[1]

        self.rect.center = self.pos

######## States for the Gatherer:

class GathererState(State):
    pass

class _Search(GathererState):

    def update(self, actor):   
        if random.uniform(0.0,1.0) < 0.1:
            actor.heading = randomNormalVector()
        ## Check for state changes
        # First, look for enemies
        close, dist = closest(actor, actor.world.enemies)
        if dist < PERCEPTION_DISTANCE:
            actor.enemy = close
            actor.stateMachine.ChangeState(Attack())
            return
        # Second, look for goodies
        close, dist = closest(actor, actor.world.goodies)
        if dist < PERCEPTION_DISTANCE:
            actor.goody = close
            actor.stateMachine.ChangeState(GetGoody())

_search = _Search()
def Search():
    return _search

class _Attack(GathererState):

    def update(self, actor):
        enemy = actor.enemy
        actor.heading = norm(enemy.pos - actor.pos)
        if actor.rect.colliderect(enemy.rect):
            if random.uniform(0.0,1.0) < 0.5:
                enemy.health -= 1
        if enemy.health < 0 or actor.world.outside(enemy):
            actor.stateMachine.ChangeState(Search())
_attack = _Attack()
def Attack():
    return _attack

class _GetGoody(GathererState):
        
    def update(self, actor):
        goody = actor.goody
        actor.heading = norm(goody.pos-actor.pos)
        # Check for state changes
        if actor.rect.colliderect(goody.rect) and goody.alive():
            actor.stateMachine.ChangeState(DeliverGoody())
_getgoody = _GetGoody()
def GetGoody():
    return _getgoody

class _DeliverGoody(GathererState):

    def enter(self, actor):
        goody = actor.goody
        goody.pos = actor.pos
        actor.heading = norm(actor.world.center - actor.pos)
        actor.world.collectGoody(goody)
        
    def update(self, actor):
        goody = actor.goody
        # Check for state changes
        if distance(actor.pos, actor.world.center) < GOAL_RADIUS:
            if random.uniform(0.0,1.0) < 0.25:
                actor.stateMachine.ChangeState(Search())

    def exit(self, actor):
        goody = actor.goody
        goody.pos = vector(actor.pos)
        actor.goody = None

_delivergoody = _DeliverGoody()
def DeliverGoody():
    return _delivergoody
