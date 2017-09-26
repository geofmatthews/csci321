import pygame
import data, text
from function import *
from constants import *

class Element:
    def __init__(self, pos, image, effects = ''):
        self.pos = pos
        self.base_image = image
        self.image = self.base_image.copy()
        self.image_position = subtract(self.pos, multiply((image.get_width(), image.get_height()), 0.5))
        self.effects = effects.split()
        self.angle = 0
        self.d_angle = STAR.D_ANGLE
        self.size = 1.0
        self.timer = 0.0
        
    def update(self, delta, new_image = None):
        if new_image != None:
            self.base_image = new_image
        else:
            if 'swing' in self.effects:
                self.d_angle -= self.angle * STAR.D_D_ANGLE * delta * 0.001
                self.angle += self.d_angle * delta * 0.001
            if 'pulse' in self.effects:
                self.timer += delta
                if self.timer > STAR.PULSE_TIME:
                    self.timer = 0.0
                    self.effects.remove('pulse')
                    self.size = 1.0
                else:
                    self.size = 0.7+(self.timer/STAR.PULSE_TIME)
                    if self.size > 1.3:
                        self.size = 1.3 - (self.size - 1.3)
            self.image = pygame.transform.rotozoom(self.base_image, self.angle, self.size)
            self.image_position = subtract(self.pos, multiply((self.image.get_width(), self.image.get_height()), 0.5))
        return

class Hud:
    def __init__(self, width, height, img_dict):
        self.width = width
        self.height = height
        self.base_image = pygame.Surface((width, height))
        self.base_image = self.base_image.convert_alpha()
        self.base_image.fill((1,1,1,0))
        self.image = self.base_image.copy()
        self.star_counter = 0
        self.tries_counter = 1
        self.img_dict = img_dict
        self.text = text.Text()
        self.stars = []
        self.stars.append(Element((50, 40), img_dict['star_empty']))
        self.stars.append(Element((100, 40), img_dict['star_empty']))
        self.stars.append(Element((150, 40), img_dict['star_empty']))
        self.tries = Element((80, 100), self.text.render('try 1'))
        for s in self.stars:
            self.image.blit(s.image, s.pos)
        self.image.blit(self.tries.image, self.tries.image_position)
            
    def update(self, delta, star_counter, tries):
        if self.star_counter != star_counter:
            self.star_counter = star_counter
            i = 0
            self.stars[star_counter-1].effects.append('pulse')
            while i < self.star_counter:
                self.stars[i].update(delta, self.img_dict['star'])
                self.stars[i].effects.append('swing')
                i +=1
        if self.tries_counter != tries:
            self.tries_counter = tries
            string = 'try ' + str(tries)
            self.tries.update(delta, self.text.render(string))
            self.tries.effects.append('pulse')
            
        self.image = self.base_image.copy()
        for s in self.stars:
            s.update(delta)
            self.image.blit(s.image, s.image_position)
        self.tries.update(delta)
        self.image.blit(self.tries.image, self.tries.image_position)
                
        