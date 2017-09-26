import pygame
import data

class Text:
    def __init__(self, size=32):
        self.font = data.load_font('airstrip.ttf', size)
        
    def render(self, text, color=(255,255,255)):
        return self.font.render(text, 1, color)