import pygame
from shape import Circle

class Button:
    def __init__(self, x, y, event, image, mouseover_image = None):
        self.circle = Circle(x,y,30)
        self.event = event
        self.base_image = image.copy()
        self.was_pressed = False
        if mouseover_image:
            self.mouseover_image = mouseover_image.copy()
        else:
            self.mouseover_image = image.copy()
        self.image_position = [x - image.get_width()/2, y - image.get_height()/2]
            
    def update(self):
        x, y = pygame.mouse.get_pos()
        if self.circle.collide_point((x,y)):
            self.image = self.mouseover_image
            pressed =  pygame.mouse.get_pressed()
            if pressed[0] and not self.was_pressed:
                self.was_pressed = True
                return self.event
            elif not pressed[0]:
                self.was_pressed = False
        else:
            self.image = self.base_image
        