import pygame, math
from pygame.locals import *
import vista, mechanics
from fixes import pixels_alpha

class Mask(object):
    """A fog-of-war style mask (black with a variable alpha)"""
    circs = {}
    def __init__(self, ps = (), color = (64, 64, 64), a = None):
        self.color = tuple(color)
        self.ps = list(ps)
        self.setrange(a)
        self.redraw()

    def setrange(self, a=None):
        if self.ps:
            self.x0 = min(x - r for (x, y), r in self.ps) - 0.1
            self.y0 = min(y - r for (x, y), r in self.ps) - 0.1
            self.x1 = max(x + r for (x, y), r in self.ps) + 0.1
            self.y1 = max(y + r for (x, y), r in self.ps) + 0.1
        else:
            self.x0, self.x1, self.y0, self.y1 = -1, 1, -1, 1
        area = (self.x1 - self.x0) * (self.y1 - self.y0)
        # TODO: set a according to area
        self.a = a if a is not None else 12
        self.sx, self.sy = self.worldtomask((self.x1, self.y0))

    def bounds(self):
        return self.x0, self.y0, self.x1, self.y1

    def worldtomask(self, (x, y)):
        return int((x - self.x0) * self.a + 0.5), int((self.y1 - y) * self.a + 0.5)

    def visibility(self, (x, y)):
        """Return the visibility (0 to 1) of the given world coordinate"""
        px, py = self.worldtomask((x, y))
        if not 0 <= px < self.sx or not 0 <= py < self.sy: return 0
        alpha = self.blue.get_at((px, py))[2]
        return alpha / 255.

    def isvisible(self, (x, y)):
        """Return whether the given world coordinate is visible"""
        return self.visibility((x, y)) > mechanics.vthreshold

    def redraw(self):
        """Draw entire surface from scratch"""
        self.surf = vista.Surface(self.sx, self.sy)
        self.surf.fill(self.color)
        self.blue = vista.Surface(self.sx, self.sy)
        self.blue.fill((0,0,0))
        for p, r in self.ps:
            self.addcirc(p, r)
        self.alphacopy()
        self.lastrequest = None  # Invalidate the last request

    def addp(self, p, r):
        self.ps.append((p, r))
        self.setrange()
        # TODO: don't need to redraw necessarily.
        self.redraw()
#        self.addcirc(p, r)
#        self.alphacopy()
#        self.lastrequest = None  # Invalidate the last request

    def addcirc(self, (x, y), r):
        """Add a circle onto the blue surface"""
        pr = int(self.a * r + 0.5)
        px, py = self.worldtomask((x, y))
        assert pr > 0
        self.blue.blit(self.getcirc(pr), (px-pr, py-pr))

    def alphacopy(self):
        """Copy from pixel data in the blue surface to the alpha
        channel of the main surface"""
        pixels_alpha(self.surf)[:,:] = 255 - pygame.surfarray.array2d(self.blue)

    def getmask(self, (x0, y0, x1, y1), (sx, sy)):
        """Return a piece of the mask that covers the rectangle of given
        world-coordinate edges and has the given pixel dimensions."""
        px0, py1 = self.worldtomask((x0, y0))
        px1, py0 = self.worldtomask((x1, y1))
        key = px0, py0, px1, py1, sx, sy
        if key == self.lastrequest:
            return self.lastresponse
        if 0 <= px0 and px1 <= self.sx and 0 <= py0 < py1 <= self.sy:
            img = self.surf.subsurface((px0, py0, px1-px0, py1-py0))
        else:
            img = vista.Surface(px1-px0, py1-py0)
            srect = self.surf.get_rect(topleft = (-px0, -py0))
            img.blit(self.surf, srect)
            if srect.left > 0:
                img.fill(self.color, img.get_rect(right = srect.left))
            if srect.right < img.get_width():
                img.fill(self.color, img.get_rect(left = srect.right))
            if srect.top > 0:
                img.fill(self.color, img.get_rect(bottom = srect.top))
            if srect.bottom < img.get_height():
                img.fill(self.color, img.get_rect(top = srect.bottom))
        img = pygame.transform.smoothscale(img, (sx, sy))
        self.lastrequest, self.lastresponse = key, img
        return img
        
    @staticmethod
    def getcirc(r):
        if r not in Mask.circs:
            # TODO: pygame.surfarray
            img = vista.Surface(2*r)
            for x in range(2*r):
                for y in range(2*r):
                    d2 = float((x - r) ** 2 + (y - r) ** 2) / r ** 2
                    d = math.sqrt(d2)
                    a = max(min(int(255 * 1 / (1 + math.exp(-20 + 24 * d))), 255), 0)
                    img.set_at((x,y), (0, 0, 255, a))
            Mask.circs[r] = img
        return Mask.circs[r]


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((480, 480))

    screen.fill((0, 0, 255))


    mask = Mask([((0,0),10)])
    surf = pygame.transform.smoothscale(mask.surf, (480, 480))

#    maskimg = pygame.Surface((480, 480), SRCALPHA)
#    maskimg.fill((0,0,0,0))
#    pygame.draw.circle(maskimg, (0, 255, 0, 128), (240, 240), 200, 0)
#    pygame.draw.circle(maskimg, (0, 255, 0), (240, 240), 100, 0)

    clock = pygame.time.Clock()
    while True:
        clock.tick()
        pygame.display.set_caption("%.1ffps" % clock.get_fps())
        if any(event.type in (QUIT, KEYDOWN) for event in pygame.event.get()):
            break
        screen.fill((0, 0, 255))
        t0 = pygame.time.get_ticks()
        screen.blit(surf, (0,0))
        t1 = pygame.time.get_ticks()
        print t1 - t0

        pygame.display.flip()



