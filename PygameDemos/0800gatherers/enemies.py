
import pygame,random,sys
from pygame.locals import *
from GM import utilities
from GM.statemachine import StateMachine, State
from GM.vector import *
import GM.makeimage
from functions import closest
from constants import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, world, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.images = GM.makeimage.rotating_arrow(ENEMY_SIZE, ENEMY_COLOR)
        self.frame = 0
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect()
        self.pos = vector(pos)
        self.rect.center = self.pos
        self.world = world

        self.heading = randomNormalVector()
        self.speed = ENEMY_SPEED
        self.stateMachine = StateMachine(self, Sneak())

        self.health = ENEMY_HEALTH
        
    def update(self):
        self.stateMachine.update()
        self.pos += self.speed*self.heading
        self.rect.center = self.pos
        angle = N.arctan2(self.heading[1],self.heading[0])*180.0/N.pi
        self.frame = int((angle % 360)/10.0)
        self.image = self.images[self.frame]

class DeadEnemy(pygame.sprite.Sprite):
    def __init__(self, pos, world, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.world = world
        self.image = GM.makeimage.cross(ENEMY_SIZE, (0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = pos


#### States for our Enemy
        
class EnemyState(State):
    pass

class _Sneak(EnemyState):
    def enter(self, actor):
        targets = actor.world.goodies.sprites()
        targets.extend(actor.world.collected.sprites())
        if targets:
            actor.goody = targets[random.randint(0,len(targets)-1)]
        else:
            actor.kill()
            return
            
    def update(self, actor):
        goody = actor.goody
        if actor.world.outside(actor) or not goody:
            actor.kill()
            return
        actor.heading = norm(goody.pos-actor.pos)
        # Check for change state:
        if actor.health <= 0:
            actor.stateMachine.ChangeState(Dead())
        if actor.rect.colliderect(goody) and goody.alive():
            actor.goody = goody
            actor.stateMachine.ChangeState(Steal())
            return
        if actor.health <= 0:
            actor.world.killEnemy(actor)
            return
        if actor.health < 0.5*ENEMY_HEALTH:
            actor.stateMachine.ChangeState(RunAway())
            return
_sneak = _Sneak()
def Sneak():
    return _sneak

class _Steal(EnemyState):

    def enter(self, actor):
        goody = actor.goody
        actor.world.uncollectGoody(goody)
        actor.heading = randomNormalVector()
        goody.pos = actor.pos
        
    def update(self, actor):
        goody = actor.goody
        if actor.world.outside(actor):
            actor.kill()
            goody.pos = actor.world.randomPosition()
            return
        if actor.health <= 0:
            actor.world.killEnemy(actor)
            return
        if actor.health < 0.5*ENEMY_HEALTH:
            actor.stateMachine.ChangeState(RunAway())
            goody.pos = vector(goody.pos)
            return
_steal = _Steal()
def Steal():
    return _steal
        
class _RunAway(EnemyState):
    def enter(self, actor):
        actor.speed *= 1.5
    def update(self, actor):
        if actor.world.outside(actor):
            actor.kill()
            return
        if actor.health <= 0:
            actor.world.killEnemy(actor)
            return
_runaway = _RunAway()
def RunAway():
    return _runaway

