import pygame, random, math
import vista, mechanics, noise, data, settings, twinkler, graphics


def getimg(name, cache = {}):
    if name in cache: return cache[name]
    cache[name] = pygame.image.load(data.filepath(name + ".png")).convert_alpha()
    return cache[name]

def getshotimg(zoom, angle = 0, cache = {}):
    angle = int(angle % 90) / 5 * 5
    zoom  = int(zoom)
    key = zoom, angle
    if key in cache: return cache[key]
    cache[key] = pygame.transform.rotozoom(getimg("shot"), angle, float(zoom) / 400.)
    return cache[key]

spoils = []  # Twinklers that get created when you kill an enemy

spawnedshots = []


class Shot(object):
    """A projectile. No not that kind. Wait, actually, yes, that kind."""
    v0 = 3
    dhp = 2
    hp0 = 1
    ntwinklers = 1
    shieldprob = 0.5
    def __init__(self, (x, y), target, tpos = None):
        self.x, self.y = x, y
        self.target = target
        self.tx, self.ty = tpos or self.target.worldpos
        self.dx, self.dy = x - self.tx, y - self.ty
        d = math.sqrt(self.dx ** 2 + self.dy ** 2)
        self.t = d / self.v0
        self.dx /= self.t
        self.dy /= self.t
        self.passedshields = []
        self.active = True
        self.hp = self.hp0
        self.angle = 0
        self.omega = random.uniform(30, 120) * (1 if random.random() < 0.5 else -1)
        self.traj = math.degrees(math.atan2(self.dx, -self.dy))

    def think(self, dt):
        self.t -= dt
        self.angle += self.omega * dt
        self.x = self.tx + self.t * self.dx
        self.y = self.ty + self.t * self.dy
        for shield in self.target.body.shields:
            if shield in self.passedshields:
                continue
            sx, sy = shield.worldpos
            if (sx - self.x) ** 2 + (sy - self.y) ** 2 < shield.shield ** 2:
                if random.random() < self.shieldprob:
                    self.passedshields.append(shield)
                    shield.wobble()
                else:
                    self.active = False
                    noise.play("dink")
        if self.t <= 0 and self.active:
            self.active = False
            self.complete()


    def complete(self):
        self.target.hit(self.dhp)

    def hit(self, dhp = 1):
        self.hp -= dhp
        if self.hp <= 0:
            self.active = False
            for _ in range(self.ntwinklers):
                spoils.append(twinkler.Twinkler((self.x, self.y)))

    def alive(self):
        return self.active and self.t > 0

    def draw(self):
        pos = vista.worldtoview((self.x, self.y))
        img = getshotimg(vista.zoom, self.angle)
        vista.screen.blit(img, img.get_rect(center = pos))

class Ship(Shot):
    """A shot that spawns more shots. Yikes!"""
    shieldprob = 1
    shotrange = 6
    shottime = 5.
    hp0 = 12
    v0 = 1.5
    ntwinklers = 3

    def shoot(self, target):
        """Fire a bullet"""
        spawnedshots.append(Shot((self.x, self.y), target))

    def randomtarget(self):
        if not self.target: return None
        if not self.target.body: return None
        targs = [part for part in self.target.body.organs.values() if part.targetable]
        if not targs: return None
        dist2, nearest = self.shotrange ** 2, None
        for targ in targs:
            wx, wy = targ.worldpos
            d2 = (self.x - wx) ** 2 + (self.y - wy) ** 2
            if d2 < dist2:
                dist2, nearest = d2, targ
        return nearest

    def think(self, dt):
        if int((self.t - dt) / self.shottime) != int(self.t / self.shottime):
            target = self.randomtarget()
            if target:
                self.shoot(target)
        Shot.think(self, dt)

    def complete(self):
        pass

    def draw(self):
        pos = vista.worldtoview((self.x, self.y))
        img = graphics.shipimg(self.traj)
        vista.screen.blit(img, img.get_rect(center = pos))





def newshots(body):
    shots = []
    mx0, my0, mx1, my1 = body.mask.bounds()
    def scaleposout((x, y)):
        """Find a point roughly in that direction that's outside the mask"""
        x *= random.uniform(0.5, 1.5)
        y *= random.uniform(0.5, 1.5)
        while mx0 < x < mx1 and my0 < y < my1:
            x *= 1.3
            y *= 1.3
            x += random.uniform(-1, 1)
            y += random.uniform(-1, 1)
        return x, y

    dw = body.control / 10.
    

    for part in body.parts:
        if not part.targetable: continue
        wx, wy = part.worldpos
        w = math.sqrt(wx ** 2 + wy ** 2)
        p = 1 - math.exp(-((w+dw) / 35) ** 2)
        if settings.barrage:
            p = 0.5
        if random.random() < p:  # Deploy a single shot
            shots.append(Shot(scaleposout((wx, wy)), part))
        if w+dw > 10:
            p = 1 - math.exp(-((w+dw-10) / 35) ** 2)
            if random.random() < p:  # Deploy a single ship
                w2 = (wy,-wx) if random.random() < 0.5 else (-wy,wx)
                shots.append(Ship(scaleposout((wx, wy)), part, scaleposout(w2)))
            if w+dw > 20:
                p = 1 - math.exp(-((w+dw-20) / 35) ** 2)
                if random.random() < p:  # Deploy five ships
                    w2 = (wy,-wx) if random.random() < 0.5 else (-wy,wx)
                    x0, y0 = scaleposout((wx, wy))
                    x1, y1 = scaleposout(w2)
                    dx, dy = x1 - x0, y1 - y0
                    d = math.sqrt(dx ** 2 + dy ** 2)
                    dx /= d
                    dy /= d
                    for ex, ey in ((0,0), (dx,dy), (-dx,-dy), (dy,-dx), (-dy,dx)):
                        shots.append(Ship((x0+ex,y0+ey), part, (x1+ex,y1+ey)))
    return shots



