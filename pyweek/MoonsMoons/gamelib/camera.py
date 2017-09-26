import pygame, math
from constants import *
from shape import Circle
from function import *

class Camera:
    def __init__(self, player):
        position = player.circle.center
        self.center = [position[0], position[1]]
        self.offset = [0,0]
        self.circle = Circle(position[0], position[1], CAMERA.RADIUS)
        self.rect = pygame.Rect(position[0], position[1], SCREEN.WIDTH+CAMERA.RECT_OFFSET, SCREEN.HEIGHT+CAMERA.RECT_OFFSET)
        self.position = [position[0], position[1]]
        self.x = position[0]-SCREEN.WIDTH/2
        self.y = position[1]-SCREEN.HEIGHT/2
        self.player = player # used for collisions and angle
        self.shaking = False
        self.extra = [0,0]
        self.shaking_amount = 0
        
    def shake(self, amount = 15):
        self.shaking = pygame.time.get_ticks()
        self.shaking_amount = amount
        
    def shift(self, vector):
        return (int(vector[0] - self.x), int(vector[1] - self.y))
    
    def update(self):
        av = self.player.angle_vector
        self.offset = [0,0] #av[0]*CAMERA.OFFSET, av[1]*CAMERA.OFFSET
        self.circle.center[0] = self.center[0] + self.offset[0]
        self.circle.center[1] = self.center[1] + self.offset[1]
        self.position[0]-SCREEN.WIDTH/2
        if not self.circle.collide_point(self.player.circle.center):
            diff = subtract(self.player.circle.center, self.circle.center)
            l = pythagory(diff[0], diff[1])
            c = (l - self.circle.radius) / l
            self.center[0] += diff[0]*c
            self.center[1] += diff[1]*c
        diff = self.center[0] - self.position[0], self.center[1] - self.position[1]
        if 0: #diff[0] + diff[1] > 1:
            self.position[0] += diff[0] * CAMERA.DELAY_RATIO
            self.position[1] += diff[1] * CAMERA.DELAY_RATIO
        else:
            self.position[0] = self.center[0]
            self.position[1] = self.center[1]
        #self.position = pl_center
        if self.shaking:
            time = pygame.time.get_ticks() - self.shaking
            if time > CAMERA.SHAKE_DURATION:
                self.shaking = None
                self.extra = [0,0]
            else:
                ratio = time/float(CAMERA.SHAKE_DURATION)
                c = math.sin(ratio * 15)  * (1 - ratio) * self.shaking_amount
                self.extra = av[0] * c, av[1] * c
        self.x = self.position[0]-SCREEN.WIDTH/2 + self.extra[0]
        self.y = self.position[1]-SCREEN.HEIGHT/2 + self.extra[1]
        self.rect.topleft = self.x-CAMERA.RECT_OFFSET/2, self.y-CAMERA.RECT_OFFSET/2