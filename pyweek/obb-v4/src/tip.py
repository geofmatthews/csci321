import pygame
from pygame.locals import *
import font, graphics, settings

currenttip = ""
def settip(newtip = ""):
    global currenttip
    currenttip = newtip
    
def think(dt):
    global surf, rect
    import vista
    if not settings.showtips: return
    if not currenttip:
        surf = None
    else:
        surf = font.blocktext(currenttip)
        
    
def draw():
    """Should be called after the main blit, even after the overlays"""
    import vista
    currenttip = ""
    if not settings.showtips:
        return
    if surf:
        bubble = graphics.thoughtbubble(surf.get_height())
        bubblerect = bubble.get_rect(midtop = vista.vrect.midtop)
        rect = surf.get_rect(center = bubblerect.center)
        vista._screen.blit(bubble, bubblerect)
        vista._screen.blit(surf, rect)

