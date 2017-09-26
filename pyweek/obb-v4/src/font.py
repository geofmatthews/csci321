import pygame
from pygame.locals import *
import data, settings, vista
from itertools import chain

# The following functions are taken from the pygame wiki:
# http://pygame.org/wiki/TextWrapping 

def truncline(text, font, maxwidth):
        real=len(text)       
        stext=text           
        l=font.size(text)[0]
        cut=0
        a=0                  
        done=1
        old = None
        while l > maxwidth:
            a=a+1
            n=text.rsplit(None, a)[0]
            if stext == n:
                cut += 1
                stext= n[:-cut]
            else:
                stext = n
            l=font.size(stext)[0]
            real=len(stext)               
            done=0                        
        return real, done, stext             
        
def wrapline(text, font, maxwidth = settings.maxblockwidth): 
    done=0                      
    wrapped=[]                  
                               
    while not done:             
        nl, done, stext=truncline(text, font, maxwidth) 
        wrapped.append(stext.strip())                  
        text=text[nl:]                                 
    return wrapped
 
def wrap_multi_line(text, font, maxwidth = settings.maxblockwidth):
    """ returns text taking new lines into account.
    """
    lines = chain(*(wrapline(line, font, maxwidth) for line in text.splitlines()))
    return list(lines)


fonts = {}
def img(text = "", size = 32, color = (255, 255, 255), cache = {}):
    key = text, size, color
    if key in cache: return cache[key]
    if size not in fonts:
        fonts[size] = pygame.font.Font(data.filepath("suckgolf.ttf"), size)
    img = fonts[size].render(text.replace("0", "o"), True, color)
    if img.get_width() > settings.maxtextwidth:
        img = pygame.transform.smoothscale(img, (settings.maxtextwidth, img.get_height()))
    cache[key] = img
    return cache[key]


def blocktext(text = "", size = 32, color = (0, 0, 0), cache = {}):
    key = text, size, color
    if key in cache: return cache[key]
    if size not in fonts:
        fonts[size] = pygame.font.Font(data.filepath("suckgolf.ttf"), size)
    text = text.replace("0", "o")
    lines = wrap_multi_line(text, fonts[size])
    imgs = [fonts[size].render(line, True, color) for line in lines]
    if len(imgs) == 1:
        img = imgs[0]
    else:
        w = max(img.get_width() for img in imgs)
        h = max(img.get_height() for img in imgs)
        img = vista.Surface(w, h*len(imgs))
        for j, i in enumerate(imgs):
            r = i.get_rect(midtop = (w/2,j*h))
            img.blit(i, r)
    cache[key] = img
    return cache[key]



