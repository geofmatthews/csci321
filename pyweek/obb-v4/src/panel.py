import pygame
import settings, vista, graphics, mechanics, font


class Panel(object):
    """Place where available tiles appear and you can pick them"""
    def __init__(self, body):
        self.body = body
        self.tiles = [self.newspec(c) for c in (0,1,2,3,4,5)]
        self.ages = [-2, -2.4, -2.8, -3.2, -3.6, -4.0]
        self.centers = None
        self.selected = None

    def getlayout(self):
        ys = [(j*0.95+1)*settings.layout.ptilesize for j in (0,1,2,3,4,5)]
        xs = [(.85 if j % 2 else -.85) * settings.layout.ptilesize for j in (0,1,2,3,4,5)]
        self.centers = [(int(settings.px/2 + x), int(y + settings.layout.ptiley)) for x,y in zip(xs, ys)]
        self.loadrate = mechanics.baseloadrate
        self.cubeimg = graphics.cube.img(zoom = settings.layout.organcountsize, edge0 = 0)
        self.cuberect = self.cubeimg.get_rect(center = settings.layout.cubeiconpos)
        self.ncuberect = self.cuberect

    def __getstate__(self):
        d = dict(self.__dict__)
        d["centers"] = None
        if "cubeimg" in d: del d["cubeimg"]
        return d

    def newspec(self, jtile):
        return mechanics.randomspec("app%s" % int(jtile/2))

    def think(self, dt):
        if not self.centers:
            self.getlayout()
        self.loadrate = mechanics.baseloadrate + mechanics.cubeloadrate * self.body.ncubes
        for j in range(len(self.ages)):
            self.ages[j] = min(self.ages[j] + (1 if self.ages[j] > -1 else self.loadrate) * dt, 0)
        vista.icons["trash"].active = self.selected is not None
        
    def draw(self):
        for j, (age, appspec, (cx, cy)) in enumerate(zip(self.ages, self.tiles, self.centers)):
            color = "app%s" % int(j/2)
            if age < -1:
                img = graphics.loadbar(1 - ((-age-1) / 5), color)
                rect = img.get_rect(center = (cx, cy))
            else:
                img = graphics.drawpaneltile(appspec.dedges, color, tilt = age*450)
                if self.selected == j:
                    img = graphics.brighten(img)
#                    pygame.draw.circle(vista.psurf, (255, 255, 255), self.centers[self.selected], settings.layout.ptilesize, 2)
                rect = img.get_rect(center = (cx + age*300, cy))
            vista.psurf.blit(img, rect)

        # Draw cube tally
        color, size = (0,0,0), settings.layout.countsize
        img = font.img("%s" % (self.body.ncubes), size=size, color=color)
        vista.psurf.blit(self.cubeimg, self.cuberect)
        self.ncuberect = img.get_rect(midleft = self.cuberect.midright)
        vista.psurf.blit(img, self.ncuberect)

    def choosetip(self, (mx, my)):
        mousepos = mx - settings.px0, my - settings.py0
        if self.cuberect.collidepoint(mousepos) or self.ncuberect.collidepoint(mousepos):
            return "the more me have of that organ, the faster the new stalks come"
        


    def iconp(self, (mx, my)):
        """Any icons under this position?"""
        if not self.centers:
            self.getlayout()
        mx -= settings.px0
        my -= settings.py0
        for j, (age, (cx, cy)) in enumerate(zip(self.ages, self.centers)):
            if age == 0 and (cx - mx) ** 2 + (cy - my) ** 2 < settings.layout.ptilesize ** 2:
                return j
        return None

    def selecttile(self, jtile = None):
        self.selected = jtile if jtile != self.selected else None

    def claimtile(self, jtile = None):
        if jtile is None: jtile = self.selected
        self.tiles[jtile] = self.newspec(jtile)
        self.ages[jtile] = -6
        self.selected = None


