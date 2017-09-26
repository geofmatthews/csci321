# System for keeping track of available feats

import pygame, random
from pygame.locals import *
import vista, effect, settings, sprite

allfeats = ("nab", "leap", "turn", "twirl", "bound", "dart", "roll")

known = {}
known["nab"] = 2
known["leap"] = 1

if settings.cheat:
    known = dict((f, 6) for f in allfeats)

upgradecost = {}
upgradecost["nab"] = (5, 10, 30, 80, 200)
upgradecost["leap"] = (10, 20, 60, 140, 300)
upgradecost["turn"] = (20, 50, 120, 280, 400)
upgradecost["twirl"] = (80, 200, 450, 800, 2000)
upgradecost["bound"] = (80, 200, 450, 800, 2000)
upgradecost["dart"] = (80, 200, 450, 800, 2000)
upgradecost["roll"] = (200, 500, 2000, 5000, 20000)

keys = {}
keys["nab"] = ("sp",)
keys["leap"] = ("up",)
keys["turn"] = ("back",)
keys["twirl"] = ("up", "sp")
keys["bound"] = ("up", "back")
keys["dart"] = ("up", "forward")
keys["roll"] = ("forward", "sp")

learnat = (0, 2, 4, 6, 8, 10, 999)

def growtime(n, nmax):
    return 2. + 0.5 * (nmax - n)

def startlevel(fillbars = True):
    global bars, feattick, feateffects, currentfeattick
    if fillbars: bars = dict(known)
    feattick = dict((featname, 0) for featname in known)
    feateffects = {}
    for featname in allfeats:
        if featname in known:
            name = featname
            feateffects[featname] = effect.FeatIndicator(name, len(feateffects))
    for f in feateffects.values():
        f.position(vista.screen)
    currentfeattick = 0

def attempt(featname):
    global currentfeat, currentfeattick
    if featname not in known:
        return False
    if not bars[featname]:
        return False
    bars[featname] -= 1
    feattick[featname] = growtime(bars[featname], known[featname])
    currentfeat, currentfeattick = featname, 0.4
    return True
    
def think(dt):
    global currentfeattick
    for featname in known:
        if feattick[featname]:
            feattick[featname] = max(feattick[featname] - dt, 0)
            if not feattick[featname]:
                bars[featname] += 1
                if bars[featname] < known[featname]:
                    feattick[featname] = growtime(bars[featname], known[featname])
    if currentfeattick:
        currentfeattick = max(currentfeattick - dt, 0)

def draw(facingright = True, shopping = False):
    if shopping:
        img = pygame.surface.Surface((300, 250)).convert_alpha()
        img.fill((0,0,0,0))
        xoff, yoff = 160, 60
    else:
        img = vista.screen
        if settings.hidefeatnames:
            xoff, yoff = -105, 0
        else:
            xoff, yoff = 0, 0
    
    if currentfeattick and not settings.hidefeatnames:
        for n,f in enumerate(allfeats):
            if f == currentfeat:
                g = random.choice(("glow0", "glow1", "glow2", "glow3"))
                sprite.frames[g].place((110 - 11*len(f), 25 + 32 * n))
    for n,f in enumerate(allfeats):
        if f not in known: continue
        if shopping or not settings.hidefeatnames:
            feateffects[f].draw(img)
        kmap = dict((("sp", "key-space"), ("up", "key-up"),
                     ("forward", ("key-right" if facingright else "key-left")),
                     ("back", ("key-left" if facingright else "key-right"))))
        ks = keys[f]
        if len(ks) == 2:
            sprite.frames[kmap[ks[0]]].place((115 + xoff, 24 + 32 * n + yoff))
            sprite.frames[kmap[ks[1]]].place((142 + xoff, 24 + 32 * n + yoff))
        else:
            sprite.frames[kmap[ks[0]]].place((128 + xoff, 24 + 32 * n + yoff))
        for j in range(known[f]):
            if shopping or not settings.hidefeatnames:
                r = pygame.Rect((160 + 20 * j), (12 + 32 * n), 16, 20)
            else:
                r = pygame.Rect((52 + 8 * j), (12 + 32 * n), 8, 20)
            fill = (255, 0, 0) if j < bars[f] else (0, 0, 0)
            pygame.draw.rect(img, fill, r)
            pygame.draw.rect(img, (255, 255, 255), r, 2)
    if shopping:
        vista.screen.blit(img, (xoff, yoff))
    
    
def land():
    for f in known:
#        if f != "nab":
            bars[f] = known[f]
            feattick[f] = 0

def getupgradecost(featname):
    ucost = upgradecost[featname]
    if known[featname] > len(ucost):
        return 0
    else:
        return ucost[known[featname] - 1]

def checknewfeat(ncaught):
    if len(known) >= len(allfeats):
        return []
    newfeat = []
    while ncaught >= learnat[len(known) - 1]:
        known[allfeats[len(known)]] = 1
        newfeat = ["You learned a|new ability!"]
    if newfeat:
        startlevel()
    return newfeat


