# Module for taking care of key combos
# The rule is: two keys are

import pygame
from pygame.locals import *

watched = (K_UP, K_LEFT, K_RIGHT, K_SPACE)
waspressed = dict((k, False) for k in watched)
combokeys = set()
combostart = None

combodict = {}
def addcombo(keys, name):
    combodict[tuple(sorted(keys))] = name

addcombo((K_SPACE,), "nab")
addcombo((K_UP,), "leap")
addcombo((K_LEFT,), "turn-r")
addcombo((K_RIGHT,), "turn-l")
addcombo((K_UP, K_SPACE), "twirl")
addcombo((K_RIGHT, K_SPACE), "roll-r")
addcombo((K_LEFT, K_SPACE), "roll-l")
addcombo((K_RIGHT, K_UP), "dart-r")
addcombo((K_LEFT, K_UP), "dart-l")  # bound and dart are opposites

def check(pressed):
    global waspressed, combokeys, combostart
    ispressed = dict((k, pressed[k]) for k in watched)
    newkeys = [k for k in watched if ispressed[k] and not waspressed[k]]
    r = ()
    if combokeys:
        if not all(pressed[k] for k in combokeys):  # End the combo now
            r = combokeys
            if newkeys:
                combokeys = set(newkeys)
                combostart = pygame.time.get_ticks()
            else:
                combokeys = set()
                combostart = None
        elif newkeys:
            combokeys |= set(newkeys)
        if combokeys and pygame.time.get_ticks() - combostart > 100:  # Combo timed out
            r = combokeys
            combokeys = set()
            combostart = None
    elif newkeys:
        combokeys = set(newkeys)
        combostart = pygame.time.get_ticks()
    waspressed = ispressed
    r = tuple(sorted(r))
    return combodict[r] if r in combodict else ""

if __name__ == "__main__":
    pygame.init()

    pygame.display.set_mode((800, 300))
    clock = pygame.time.Clock()
    while True:
        dt = clock.tick(60) * 0.001
        pygame.event.get()
        k = pygame.key.get_pressed()
        r = check(k)
        if r: print r
        if k[K_ESCAPE]:
            exit()

