
import pygame
import numpy as N
from GM.vector import vector

def load_image(file_name):
    try:
        surface = pygame.image.load(file_name)
    except pygame.error as message:
        print ('Cannot load image: %s' % file_name)
        raise SystemExit( message)
    image = image.convert()
    colorkey = image.get_at((0,0))
    image.set_colorkey(colorkey, RLEACCEL)
    return image

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print ('Cannot load sound:' + fullname)
        raise SystemExit( message)
    return sound
        
    
    
    
         
