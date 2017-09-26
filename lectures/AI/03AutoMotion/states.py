"""
States for my players
Geoffrey Matthews
2007
"""
import pygame
from pygame.locals import *
import math
import random
import vectors as V
from constants import *

class _State(object):
    ## All states should respond to these:
    def enter(self, obj, **args): pass
    def execute(self, obj): pass
    def exit(self, obj): pass

class _Wait(_State):
    def execute(self, obj):
        obj.steering = 0.0 - obj.velocity

_wait = _Wait()
def Wait(): return _wait

class _User(_State):
    def enter(self, obj, **args):
        obj.velocity = obj.maxspeed*obj.heading*0.5

    def execute(self, obj):
        maxforward = obj.maxspeed*obj.heading*0.5
        pressed = pygame.key.get_pressed()
        if pressed[K_LEFT]:
            desired_velocity = V.rotate(maxforward, -5)         
        elif pressed[K_RIGHT]:
            desired_velocity = V.rotate(maxforward, 5)
        else:
            desired_velocity = obj.velocity
        obj.steering = 0.0
        obj.velocity = desired_velocity
        obj.heading = V.normalize(obj.velocity)

_user = _User()
def User(): return _user

class _Wander(_State):
    def enter(self, obj, **args):
        obj.velocity = obj.maxspeed*obj.heading
        
    def execute(self, obj):
        pos = obj.rect.center
        wp = obj.wanderpoint
        hd = obj.heading
        angle = math.atan2(wp[1], wp[0])
        angle += random.uniform(-0.5,0.5)
        wp[0] = math.cos(angle)
        wp[1] = math.sin(angle)
        seekvec = WANDER_OFFSET*hd + WANDER_RADIUS*wp
        desired_velocity = obj.maxspeed * V.normalize(seekvec)
        obj.steering = desired_velocity - obj.velocity
        V.truncate(obj.steering, obj.maxforce)

_wander = _Wander()
def Wander(): return _wander

class _Seek(_State):
    def enter(self, obj, **args):
        obj.target = args['target']

    def execute(self, obj):
        pos = V.vector(obj.rect.center)
        endpos = obj.target.rect.center
        desired_velocity = obj.maxspeed*V.normalize(endpos - pos)
        obj.steering = desired_velocity - obj.velocity
        V.truncate(obj.steering, obj.maxforce)

_seek = _Seek()
def Seek(): return _seek

class _Flee(_State):
    def enter(self, obj, **args):
        obj.target = args['target']

    def execute(self, obj):
        pos = V.vector(obj.rect.center)
        endpos = obj.target.rect.center
        desired_velocity = obj.maxspeed*V.normalize(pos - endpos)
        obj.steering = desired_velocity - obj.velocity
        V.truncate(obj.steering, obj.maxforce)

_flee = _Flee()
def Flee(): return _flee

class _Pursuit(_State):
    def enter(self, obj, **args):
        obj.target = args['target']

    def execute(self, obj):
        pos = V.vector(obj.rect.center)
        targpos = obj.target.rect.center
        traveltime = V.length(pos-targpos)/obj.maxspeed
        targvel = obj.target.velocity
        futurepos = targpos + targvel*traveltime
        desired_velocity = obj.maxspeed*V.normalize(futurepos - pos)
        obj.steering = desired_velocity - obj.velocity
        V.truncate(obj.steering, obj.maxforce)

_pursuit = _Pursuit()
def Pursuit(): return _pursuit

class _Evasion(_State):
    def enter(self, obj, **args):
        obj.target = args['target']

    def execute(self, obj):
        pos = V.vector(obj.rect.center)
        targpos = obj.target.rect.center
        traveltime = V.length(pos-targpos)/obj.maxspeed
        targvel = obj.target.velocity
        futurepos = targpos + targvel*traveltime
        desired_velocity = obj.maxspeed*V.normalize(pos - futurepos)
        obj.steering = desired_velocity - obj.velocity
        V.truncate(obj.steering, obj.maxforce)

_evasion = _Evasion()
def Evasion(): return _evasion
