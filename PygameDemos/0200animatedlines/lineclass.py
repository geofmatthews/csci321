"""
This module defines a simple class for drawing a line on the screen.
Geoffrey Matthews, 2007
"""

from random import randint
import numpy, pygame

def randpoint (screen):
    w,h = screen.get_size()
    return randint(0, w-1), randint(0, h-1)

class Line:
    def __init__(self, screen):
        self.screen = screen
        self.start = numpy.array(randpoint(screen))
        self.stop = numpy.array(randpoint(screen))
        self.start_speed = numpy.array((5,5))
        self.stop_speed = numpy.array((5,5))
        
    def draw(self):
        pygame.draw.line(self.screen, (255,0,0), self.start, self.stop, 1)
        
    def update(self):
        screen = self.screen
        self.start += self.start_speed
        self.stop += self.stop_speed
        if self.start[0] >= screen.get_width() or self.start[0] < 0:
            self.start_speed[0] *= -1
        if self.start[1] >= screen.get_height() or self.start[1] < 0:
            self.start_speed[1] *= -1
        if self.stop[0] >= screen.get_width() or self.stop[0] < 0:
            self.stop_speed[0] *= -1
        if self.stop[1] >= screen.get_height() or self.stop[1] < 0:
            self.stop_speed[1] *= -1
