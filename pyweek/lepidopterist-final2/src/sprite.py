# This module is probably going to balloon out of control, but here goes.

import pygame, random, math
from pygame.locals import *
import data, vista, settings

frames = {}
class Frame(object):
    def __init__(self, filename, (dx, dy), hflip = False):
        self.filename = filename
        self.image = pygame.image.load(data.filepath(self.filename)).convert_alpha()
        if hflip:
            self.image = pygame.transform.flip(self.image, True, False)
        self.dx, self.dy = dx, dy
        self.nabbed = False
    def draw(self, (x, y)):
        vista.blit(self.image, (x - self.dx, y + self.dy))
        if settings.showdots:
            vista.dot((x, y))
#        pygame.draw.circle(surf, (255, 128, 0, 255), (int(px), int(py)), 4)
    def place(self, (x,y)):  # Doesn't use the vista's transformation.
        vista.screen.blit(self.image, (x - self.dx, y - self.dy))
    def reverse(self):
        return Frame(self.filename, (self.image.get_width() - self.dx, self.dy), True)

def load():
    frames["stand"] = Frame("you-stand.png", (94, 150))
    frames["run0"] = Frame("you-run-0.png", (84, 145))
    frames["run1"] = Frame("you-run-1.png", (84, 150))
    frames["run2"] = Frame("you-run-2.png", (84, 145))
    frames["nab0"] = Frame("nab-0.png", (94, 150))
    frames["nab1"] = Frame("nab-1.png", (94, 150))
    frames["nab2"] = Frame("nab-2.png", (94, 150))
    frames["nab3"] = Frame("nab-3.png", (94, 150))
    frames["skynab0"] = Frame("skynab-0.png", (94, 150))
    frames["skynab1"] = Frame("skynab-1.png", (94, 150))
    frames["skynab2"] = Frame("skynab-2.png", (94, 150))
    frames["skynab3"] = Frame("skynab-3.png", (94, 150))
    frames["bound"] = Frame("bound.png", (94, 150))
    frames["dart"] = Frame("dart.png", (94, 150))
    frames["roll0"] = Frame("roll-0.png", (94, 150))
    frames["roll1"] = Frame("roll-1.png", (94, 150))
    frames["roll2"] = Frame("roll-2.png", (94, 150))
    frames["roll3"] = Frame("roll-3.png", (94, 150))
    frames["roll4"] = Frame("roll-4.png", (94, 150))
    frames["roll5"] = Frame("roll-5.png", (94, 150))
    frames["roll6"] = Frame("roll-6.png", (94, 150))
    frames["roll7"] = Frame("roll-7.png", (94, 150))
    frames["blue0"] = Frame("blue-butterfly-0.png", (36, 36))
    frames["blue1"] = Frame("blue-butterfly-1.png", (36, 36))
    frames["red0"] = Frame("red-butterfly-0.png", (36, 36))
    frames["red1"] = Frame("red-butterfly-1.png", (36, 36))
    frames["yellow0"] = Frame("yellow-butterfly-0.png", (36, 36))
    frames["yellow1"] = Frame("yellow-butterfly-1.png", (36, 36))
    for c in ("white", "purple", "grey", "green"):
        for n in (0,1):
            frames["%s%s" % (c,n)] = Frame("%s-%s.png" % (c,n), (36, 36))
    frames["fairy-blue"] = Frame("fairy-blue.png", (36, 36))
    frames["fairy-red"] = Frame("fairy-red.png", (36, 36))
    frames["fairy-green"] = Frame("fairy-green.png", (36, 36))
    for k in frames.keys():
        frames[k + "-b"] = frames[k].reverse()

    frames["twirl0"] = Frame("twirl-0.png", (84, 150))
    frames["twirl1"] = Frame("twirl-1.png", (84, 150))
    frames["twirl2"] = Frame("twirl-2.png", (84, 150))
    frames["twirl3"] = Frame("twirl-3.png", (84, 150))
    frames["leveldisk"] = Frame("level-disk.png", (50, 46))

    frames["key-space"] = Frame("key-space.png", (20, 20))
    frames["key-up"] = Frame("key-up.png", (20, 20))
    frames["key-left"] = Frame("key-left.png", (20, 20))
    frames["key-right"] = Frame("key-right.png", (20, 20))
    
    frames["head-m"] = Frame("head-mortimer.png", (-100,-100))
    frames["head-e"] = Frame("head-elmer.png", (-500,-100))
    frames["head-s"] = Frame("head-sensei.png", (-500,-100))
    frames["head-v"] = Frame("head-victoria.png", (-500,-100))

    frames["glow0"] = Frame("glow-0.png", (200, 80))
    frames["glow1"] = Frame("glow-1.png", (200, 80))
    frames["glow2"] = Frame("glow-2.png", (200, 80))
    frames["glow3"] = Frame("glow-3.png", (200, 80))


class Butterfly(object):
    fnames = ("blue0", "blue1")
    ymin, ymax = 40, 260
    name = "butterfly"
    fullname = "Abstract Butterfly"
    value = 1
    vx0, vy0 = 100, 20
    flighttime = 0.5
    def __init__(self, p = None):
        if p == None:
            self.x = random.uniform(vista.vx0, vista.vx1)
            self.y = random.uniform(self.ymin, self.ymax)
        else:
            self.x, self.y = p
        self.bangle = None
        self.flaptick = random.random()
    def think(self, dt):
        if random.uniform(0, self.flighttime) < dt or self.bangle is None:
            self.bangle = random.uniform(0, 6.28)
            self.vx, self.vy = self.vx0 * math.cos(self.bangle), self.vy0 * math.sin(self.bangle)
        self.flaptick += dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.y = max(min(self.y, self.ymax), self.ymin)
        self.x, self.y = vista.constrain(self.x, self.y)
    def draw(self):
        bpicname = self.fnames[int(self.flaptick / 0.1) % len(self.fnames)]
        if self.vx > 0: bpicname = bpicname + "-b"
        frames[bpicname].draw((self.x, self.y))

class BlueButterfly(Butterfly):
    fnames = ("blue0", "blue1")
    ymin, ymax = 40, 260
    name = "bbutterfly"
    fullname = "Bourgeois Blue"
    value = 1
    vx0, vy0 = 100, 20

class YellowButterfly(Butterfly):
    name = "ybutterfly"
    fullname = "Homely Swallowtail"
    fnames = ("yellow0", "yellow1")
    ymin, ymax = 140, 320
    vx0, vy0 = 200, 40
    value = 2

class RedButterfly(Butterfly):
    name = "rbutterfly"
    fullname = "Deposed Monarch"
    fnames = ("red0", "red1")
    ymin, ymax = 260, 500
    vx0, vy0 = 300, 60
    value = 4

class WhiteButterfly(Butterfly):
    name = "wbutterfly"
    fullname = "Salty Peppered Moth"
    fnames = ("white0", "white1")
    ymin, ymax = 260, 500
    vx0, vy0 = 300, 60
    value = 4

class GreyButterfly(Butterfly):
    name = "greybutterfly"
    fullname = "Two Ply Moth"
    fnames = ("grey0", "grey1")
    ymin, ymax = 100, 600
    vx0, vy0 = 40, 400
    value = 8

class PurpleButterfly(Butterfly):
    name = "pbutterfly"
    fullname = "Splotched Fritillary"
    fnames = ("purple0", "purple1")
    ymin, ymax = 260, 500
    vx0, vy0 = 300, 60
    value = 4

class GreenButterfly(Butterfly):
    name = "gbutterfly"
    fullname = "Rib Tickling Skipper"
    fnames = ("green0", "green1")
    ymin, ymax = 60, 500
    vx0, vy0 = 400, 200
    value = 3

class BlueFairy(Butterfly):
    fnames = ("fairy-blue",)
    ymin, ymax = 300, 500
    name = "bfairy"
    fullname = "Annoying Kokiri Fairy"
    value = 8
    vx0, vy0 = 600, 200
    flighttime = 0.2

class RedFairy(Butterfly):
    fnames = ("fairy-red",)
    ymin, ymax = 400, 600
    name = "rfairy"
    fullname = "Scenester Pixie"
    value = 12
    vx0, vy0 = 600, 200
    flighttime = 0.2

class GreenFairy(Butterfly):
    fnames = ("fairy-green",)
    ymin, ymax = 500, 900
    name = "gfairy"
    fullname = "Laminated Yosei"
    value = 15
    vx0, vy0 = 600, 600
    flighttime = 0.2

