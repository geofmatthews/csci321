from shape import Circle
from constants import *
import pygame

class Star:
    def __init__(self, position, image_dict):
        self.circle = Circle(position[0], position[1], STAR.RADIUS)
        
        self.base_image = image_dict['star']
        self.image = self.base_image
        self.image_position = [position[0] - STAR.RADIUS, position[1] - STAR.RADIUS]
        self.angle = 0
        self.d_angle = STAR.D_ANGLE
        self.d_d_angle = STAR.D_D_ANGLE
        self.decay = False
        self.decay_time = STAR.DECAY_TIME
        
    def update(self, player, delta):
        if self.decay:
            return self.update_decay(player, delta)
        else:
            return self.update_normal(player, delta)
        
    def update_normal(self, player, delta):
        self.d_angle -= self.angle * self.d_d_angle * delta * 0.001
        self.angle += self.d_angle * delta * 0.001
        self.image = pygame.transform.rotozoom(self.base_image, self.angle, 1.0)
        self.image_position = [self.circle.center[0] - self.image.get_width()/2, self.circle.center[1] - self.image.get_height()/2]
        if self.circle.collide_circle(player.circle):
            self.decay = True
            self.d_d_angle = STAR.DECAY_D_D_ANGLE
            return True
        return False
        
    def update_decay(self, player, delta):
        self.decay_time -= delta
        if self.decay_time < 0:
            return True
        self.d_angle += self.angle * self.d_d_angle * delta * 0.001
        self.angle += self.d_angle * delta * 0.001
        size = 1.0*self.decay_time/STAR.DECAY_TIME
        self.image = pygame.transform.rotozoom(self.base_image, self.angle, size)
        self.image_position = [self.circle.center[0] - self.image.get_width()/2, self.circle.center[1] - self.image.get_height()/2]
        self.image.set_alpha(size*255)
        return False
 
class Part:
    def __init__(self, x,y, image):
        self.base_image = image
        radius = (image.get_width() + image.get_height()) /4
        self.circle = Circle(x, y, radius)
        self.decay = False
        self.decay_time = STAR.DECAY_TIME
        self.image = self.base_image.copy()
        self.image_position = [x-image.get_width()/2, y-image.get_height() /2]
        
    def update(self, player, delta):
        if self.decay:
            self.decay_time -= delta
            if self.decay_time < 0:
                return True
            size = 1.0*self.decay_time/STAR.DECAY_TIME
            self.image = pygame.transform.rotozoom(self.base_image, 0, size)
            self.image_position = [self.circle.center[0] - self.image.get_width()/2, self.circle.center[1] - self.image.get_height()/2]
            self.image.set_alpha(size*255)
            return False
        else:
            if self.circle.collide_circle(player.circle):
                self.decay = True
                return True
            return False