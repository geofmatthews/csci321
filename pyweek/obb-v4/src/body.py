import pygame, random, math
from pygame.locals import *
import vista, mask, graphics, mechanics, noise

class Body(object):
    def __init__(self, (x, y) = (0, 0)):
        self.tick = 0   # Generic timekeeping

        self.parts = []
        self.suckers = []
        self.shields = []
        self.attackers = []
        self.organs = {}  # Reverse lookup

        self.takentiles = {}
        self.takenedges = {}
        self.takenbuds = {}
        self.calccontrol()

        self.mask = None
        self.mutagen = 0
        self.maxmutagen = mechanics.mutagen0
        self.plaster = 0
        self.maxplaster = mechanics.plaster0
        self.ncubes = 0

        self.core = Core(self, (x, y))
        self.addpart(self.core)

    def __getstate__(self):
        d = dict(self.__dict__)
        d["mask"] = None
        return d

    def addrandompart(self, n = 1, maxtries = 100):
        added = 0
        for tries in range(maxtries):
            parent = random.choice(self.parts)
            bud = parent.randombud()
            if not bud: continue
            pos, edge = bud
            r = random.random()
            if r < 0.8:
                appspec = mechanics.randomspec()
                part = Appendage(self, parent, pos, edge, appspec)
                if part.color != parent.budcolors[bud]: continue
            else:
                ostr, otype = random.choice(otypes.items())
                if mechanics.colors[ostr] != parent.budcolors[bud]: continue
                part = otype(self, parent, pos, edge)
            if not self.canaddpart(part): continue
            self.addpart(part)
            added += 1
            if added == n: return n
        return added

    def calccontrol(self):
        self.control = 0
        self.maxcontrol = 0
        for part in self.parts:
            self.control += part.controlneed
            self.maxcontrol += part.control

    def checkmutagen(self):
        x = self.mutagen
        self.mutagen = 0
        return x

    def checkplaster(self):
        x = self.plaster
        self.plaster = 0
        return x

    def nearestorgan(self, pos):
        """Nearest organ to the given world position"""
        hexpos = vista.HexGrid.nearesttile(pos)
        return self.organs[hexpos] if hexpos in self.organs else None

    def canplaceapp(self, edge, appspec):
        """If you can place the specified app on the specified edge,
        return the corresponding part. Otherwise return None"""
        for bud in (edge, vista.HexGrid.opposite(*edge)):
            if bud not in self.takenbuds: continue
            parent = self.takenbuds[bud]
            if parent.buds[bud] is not None: continue
            part = Appendage(self, parent, bud[0], bud[1], appspec)
            if part.color != parent.budcolors[bud]: continue
            return part
        return None

    def canplaceorgan(self, edge, ostr):
        """If you can place the specified organ type on the specified edge,
        return the corresponding part. Otherwise return None"""
        otype = otypes[ostr]
        for bud in (edge, vista.HexGrid.opposite(*edge)):
            if bud not in self.takenbuds: continue
            parent = self.takenbuds[bud]
            if parent.buds[bud] is not None: continue
            if mechanics.colors[ostr] != parent.budcolors[bud]: continue
            part = otype(self, parent, bud[0], bud[1])
            return part
        return None

    def canaddpart(self, part):
        tiles, edges = part.claimedsets()
        if part.controlneed and part.controlneed + self.control > self.maxcontrol: return False
        if any(tile in self.takentiles for tile in tiles): return False
        if any(edge in self.takenedges for edge in edges): return False
        return True

    def addpart(self, part):
        assert self.canaddpart(part)
        self.parts.append(part)
        if part.parent is not None:
            part.parent.buds[((part.x, part.y), part.edge)] = part
        part.status = ""
        tiles, edges = part.claimedsets()
        for tile in tiles: self.takentiles[tile] = part
        for edge in edges: self.takenedges[edge] = part
        for bud in part.buds: self.takenbuds[bud] = part
        if part.lightradius > 0 and self.mask is not None:
            self.mask.addp(*part.lightcircle())
            vista.setgrect(self.mask.bounds())
        self.calccontrol()
        if part.suction:
            self.suckers.append(part)
        if part.attacker:
            self.attackers.append(part)
        if part.shield > 0:
            self.shields.append(part)
        vista.icons["cut"].active = len(self.parts) > 1
        if isinstance(part, Organ):
            self.organs[(part.x, part.y)] = part
        self.maxmutagen += part.mutagen
        self.maxplaster += part.plaster
        self.ncubes += part.ncubes
        if not isinstance(part, Core):
            noise.play("addpart")

    def remakemask(self):
        """Build the mask from scratch"""
        circles = [part.lightcircle() for part in self.parts if part.lightradius > 0]
        self.mask = mask.Mask(circles)

    def removepart(self, part):
        """This is like the manual override. Shouldn't be called directly.
        Instead call part.die()"""
        assert not isinstance(part, Core)
        self.parts.remove(part)
        edge = (part.x, part.y), part.edge
        assert part.parent.buds[edge] is part
        part.parent.buds[edge] = None
        tiles, edges = part.claimedsets()
        for tile in tiles: del self.takentiles[tile]
        for edge in edges: del self.takenedges[edge]
        for bud in part.buds: del self.takenbuds[bud]
        assert part not in self.takentiles.values()
        assert part not in self.takenedges.values()
        if part.lightradius > 0:
            self.mask = None
        self.calccontrol()
        if part in self.suckers:
            self.suckers.remove(part)
        if part in self.attackers:
            self.attackers.remove(part)
        if part in self.shields:
            self.shields.remove(part)
        noise.play("removepart")
        vista.icons["cut"].active = len(self.parts) > 1
        if isinstance(part, Organ):
            del self.organs[(part.x, part.y)]
        self.maxmutagen -= part.mutagen
        self.maxplaster -= part.plaster
        self.ncubes -= part.ncubes

    def removebranch(self, part):
        """Remove a part and all its children"""
        for child in part.buds.values():
            if child is not None:
                self.removebranch(child)
        self.removepart(part)

    def think(self, dt, meter):
        shallheal = int(self.tick + dt) != int(self.tick)
        self.tick += dt
        for part in self.parts:
            part.think(dt)
        if self.mask is None:
            self.remakemask()
            vista.setgrect(self.mask.bounds())
        if shallheal:
            self.trytoheal(meter)

    def trytoheal(self, meter):
        toheal = [part for part in self.organs.values() if part.targetable and part.autoheal and part.hp < part.hp0]
        if not toheal: return
        random.shuffle(toheal)
        for part in toheal:
            available = int(meter.amount)
            if not available:
                return
            dhp = min(available, part.hp0 - part.hp)
            part.heal(dhp)
            meter.amount -= dhp

    def sethealstatus(self):
        for part in self.organs.values():
            part.status = "good" if part.autoheal else "bad"

    def claimtwinklers(self, ts):
        random.shuffle(self.suckers)
        for t in ts:
            if t.claimed or t.sucker is not None: continue
            for s in self.suckers:
                sx, sy = s.worldpos
                dx, dy = sx - t.x, sy - t.y
                if dx ** 2 + dy ** 2 < 2.5 ** 2:
                    t.sucker = s
                    break
        return None

    def attackenemies(self, es):
        random.shuffle(self.attackers)
        for e in es:
            if not e.alive(): continue
            for a in self.attackers:
                if a.canattack(e):
                    a.attack(e)
        return None

    
    def draw(self):
        for part in sorted(self.parts, key = lambda p: p.draworder):
            part.draw()
        for shield in self.shields:
            (x, y), r = shield.screenpos(), shield.shield
            pygame.draw.circle(vista.screen, (128, 128, 255), (x, y), r * vista.zoom, 1)

    def tracehexes(self, color = (128, 128, 128)):
        tiles = set([(part.x, part.y) for part in self.parts])
        for tile in tiles:
            vista.HexGrid.tracehex(tile, color)


class BodyPart(object):
    lightradius = 0  # How much does this part extend your visibility
    draworder = 0
    growtime = 0
    dietime = 0.1
    control = 0
    controlneed = 0
    shield = 0
    suction = False
    targetable = False
    autoheal = True
    pulsefreq = 0
    hp0 = 0
    attacker = False
    glowtime = 0
    hearttime = 0
    mutagen = 0
    plaster = 0
    ncubes = 0
    def __init__(self, body, parent, (x,y), edge = 0):
        self.body = body
        self.parent = parent
        self.x, self.y = x, y
        self.worldpos = vista.grid.hextoworld((self.x, self.y))
        self.edge = edge  # Edge number of base
        self.edgeworldpos = vista.grid.edgeworld((self.x, self.y), self.edge)
        self.buds = {}  # New body parts that are formed off this one
                        # (set to None if no body part there yet)
        self.lastkey = None
        self.budcolors = {}
        self.status = ""
        self.growtimer = self.growtime
        self.dietimer = None
        self.hp = self.hp0
        self.dusts = []

    def __getstate__(self):
        d = dict(self.__dict__)
        d["lastkey"] = None
        d["img"] = None
        return d

    def think(self, dt):
        if self.growtimer > 0:
            if not self.parent or not self.parent.growtimer:
                self.growtimer = max(self.growtimer - dt, 0)
        elif self.dietimer is not None:
            candie = all(part is None for part in self.buds.values())
            if candie:
                self.dietimer -= dt
                if self.dietimer < 0:
                    self.body.removepart(self)
                    noise.play("addpart")
        else:
            if self.hp0 and self.hp < self.hp0:
                self.pulsefreq = 1. - float(self.hp) / self.hp0
        if self.hp < self.hp0:
            self.adddust(40 * dt * (1. - float(self.hp) / self.hp0))
        self.glowtime = max(self.glowtime - dt, 0)
        self.hearttime = max(self.hearttime - dt, 0)
        self.dusts = [(dx, dy, t-dt) for dx, dy, t in self.dusts if t > dt]

    def adddust(self, n = 1):
        for j in range(int(n) + (random.random() < n % 1)):
            dx = random.uniform(-3, 3)
            dy = random.uniform(-3, 3)
            self.dusts.append([dx, dy, 0.5])

    def hit(self, dhp = 1):
        self.hp -= dhp
        if self.hp < 0:
            self.adddust(200)
            self.die()
            noise.play("die")
        else:
            self.adddust(40)
            noise.play("ouch")

    def heal(self, dhp = None):
        if dhp is None: dhp = self.hp0 - self.hp
        if not dhp: return 0
        self.hp = self.hp0
        noise.play("heal")
        self.hearttime = 1
        self.pulsefreq = 0
        return dhp

    def die(self):
        for part in self.buds.values():
            if part is not None:
                part.die()
        self.dietimer = self.dietime

    def attached(self):
        return self in self.body.parts

    def setbranchstatus(self, status = ""):
        self.status = status
        for child in self.buds.values():
            if child is not None:
                child.setbranchstatus(status)

    def lightcircle(self):
        return vista.grid.hextoworld((self.x,self.y)), self.lightradius

    def tiles(self):
        return ()

    def edges(self):
        return self.buds.keys()

    def claimedsets(self):
        ts = set(self.tiles())
        es = set(vista.grid.normedge(p, e) for p,e in self.edges())
        return ts, es

    def screenpos(self):
        return vista.worldtoview(self.worldpos)

    def edgescreenpos(self):
        return vista.worldtoview(self.edgeworldpos)

    @staticmethod
    def budscreenpos(p, e):
        """Screen position of a given edge"""
        return vista.worldtoview(vista.grid.edgeworld(p, e))

    def randombud(self):
        """Return a bud that hasn't been used yet"""
        buds = [key for key,value in self.buds.items() if value == None]
        if not buds: return None
        return random.choice(buds)

    def getkey(self):
        zoom = int(vista.zoom + 0.5)
        if self.dietimer is not None:
            growth = self.dietimer / self.dietime
        elif "ghost" in self.status:
            growth = 1
        elif self.growtimer:
            growth = 1 - self.growtimer / self.growtime
        else:
            growth = 1
        return zoom, self.status, growth

    def drawglow(self, (px, py), t):
        for img in graphics.gettwinklerimgs(t * 3, r0 = 4):
            vista.screen.blit(img, img.get_rect(center = (px, py)))

    def drawheart(self, (px, py), t):
        alpha = t
        py -= int(vista.zoom * (1 - t) * 1.5)
        img = graphics.heartimg(alpha)
        vista.screen.blit(img, img.get_rect(center = (px, py)))

    def draw(self):
        wx, wy = vista.grid.hextoworld((self.x, self.y))
        key = self.getkey()
        if key != self.lastkey:
            self.lastkey = key
            self.img = self.draw0(*key)
        img = self.img
#        if self.pulsefreq:
#            img = self.pulseredimg(self.img, self.pulsefreq)
        px, py = vista.worldtoview((wx, wy))
        if self.glowtime:
            self.drawglow((px, py), self.glowtime)
        vista.screen.blit(img, self.img.get_rect(center = (px, py)))
        if self.hearttime:
            self.drawheart((px, py), self.hearttime)
        for dx, dy, t in self.dusts:
            x, y = wx + dx * (0.65 - t), wy + dy * (0.65 - t)
            px, py = vista.worldtoview((x, y))
            img = graphics.dustcloudimg(angle = t * 100, R = 1, alpha = 1.6 * t)
            vista.screen.blit(img, img.get_rect(center = (px, py)))

    def pulse(self, freq = 0):
        """A value that's usable as a pulsation amount. The frequency
        should be between 0 and 1"""
        return 0.5 + 0.5 * math.cos(self.body.tick * (1 + 20 * freq ** 2))

    def pulseredimg(self, img, freq = 0):
        img = img.copy()
        f = self.pulse(freq)
        graphics.filtercolorsurface(img, (1-f,0,0,1), (f/2,1-f,0,1), (f/2,0,1-f,1))
        return img

    @staticmethod
    def colorbycode(colorcode):
        return [(0,192,64), (64,64,192), (160,80,0)][colorcode]

class Core(BodyPart):
    """The central core of the body, that has the funny mouth"""
    lightradius = mechanics.corelightradius
    growtime = 1.8
    control = mechanics.corecontrol
    def __init__(self, body, (x,y) = (0,0)):
        BodyPart.__init__(self, body, None, (x,y), 0)
        for edge in range(6):  # One bud in each of six directions
            oppedge = vista.grid.opposite((x, y), edge)
            self.buds[oppedge] = None
            self.budcolors[oppedge] = "app%s" % (edge % 3)
        self.nmouth = 0

    def tiles(self):
        return ((self.x, self.y),)

    def draw0(self, zoom, status, growth):
        color = "core"
        return graphics.core(color, growth, zoom)

    def draw(self, *args):
        BodyPart.draw(self, *args)
        wx, wy = vista.grid.hextoworld((self.x, self.y))
        px, py = vista.worldtoview((wx, wy))
        mouth = graphics.mouthimg(self.nmouth)
        rect = mouth.get_rect(center = (px, py))
        vista.screen.blit(mouth, rect)
        

class Appendage(BodyPart):
    """A stalk that leads to one or more subsequent buds"""
    draworder = 1
    growtime = 0.3
    def __init__(self, body, parent, (x,y), edge, appspec):
        BodyPart.__init__(self, body, parent, (x,y), edge)
        self.appspec = appspec
        self.color = appspec.color
        for bud in self.appspec.outbuds((x, y), edge):
            self.buds[bud] = None
            self.budcolors[bud] = self.color

    def draw0(self, zoom, status, growth):
        return graphics.app.img(dedges = self.appspec.dedges, color = status or self.color, edge0 = self.edge, zoom = zoom, growth = growth)
            
class Organ(BodyPart):
    """A functional body part that terminates a stalk"""
    draworder = 2
    growtime = 0.3
    controlneed = 1
    targetable = True
    hp0 = 8
    def draw0(self, zoom, status, growth):
        return graphics.organ.img(zoom = zoom, color = status or self.color, edge0 = self.edge)

    def tiles(self):
        return ((self.x, self.y),)

class Eye(Organ):
    """Extends your visible region"""
    lightradius = mechanics.eyelightradius

    def __init__(self, *args, **kw):
        Organ.__init__(self, *args, **kw)
        self.tblink = 0

    def think(self, dt):
        Organ.think(self, dt)
        if self.tblink == 0 and random.random() * 4 < dt:
            self.tblink = 0.3
        if self.tblink:
            self.tblink = max(self.tblink - dt, 0)
        if self.growtimer:
            self.tblink = 0.45

    def getkey(self):
        blink = abs(self.tblink - 0.15) / 0.15 if self.tblink else 1
        while blink > 1.0001: blink = abs(blink - 2)
        if "ghost" in self.status: blink = 1
        return Organ.getkey(self) + (blink,)

    def draw0(self, zoom, status, growth, blink = 1):
        return graphics.eye.img(zoom = zoom, growth = growth, color = status, edge0 = self.edge, blink = blink)

class TripleEye(Eye):
    lightradius = 1.5 * mechanics.eyelightradius

    def draw0(self, zoom, status, growth, blink = 1):
        return graphics.tripleeye.img(zoom = zoom, growth = growth, color = status, edge0 = self.edge, blink = blink)



class Brain(Organ):
    """Lets you control more organs"""
    control = mechanics.braincontrol
    controlneed = 0

    def draw0(self, zoom, status, growth):
        return graphics.brain.img(zoom = zoom, growth = growth, color = status, edge0 = self.edge)

class GiantBrain(Organ):
    """Lets you control even more organs"""
    control = 2 * mechanics.braincontrol
    controlneed = 0

    def draw0(self, zoom, status, growth):
        return graphics.brain.giantimg(zoom = zoom, growth = growth, color = status, edge0 = self.edge)

class EyeBrain(Brain):
    """Hey, you got eyeballs in my brain! Hey, you got brains in my eyeball!"""
    lightradius = mechanics.eyelightradius

    def draw0(self, zoom, status, growth):
        return graphics.eyebrain.img(zoom = zoom, growth = growth, color = status, edge0 = self.edge)


class MutagenPod(Organ):
    mutagen = mechanics.mutagenpodsize
    def draw0(self, zoom, status, growth):
        return graphics.pod.imgmutagen(zoom = zoom, growth = growth, color = status, edge0 = self.edge)

# By the way I couldn't think of what to call the stuff you heal yourself
#   with so I went with plaster. But in the game it's called ooze.
class PlasterPod(Organ):
    plaster = mechanics.plasterpodsize
    def draw0(self, zoom, status, growth):
        return graphics.pod.imgplaster(zoom = zoom, growth = growth, color = status, edge0 = self.edge)

class GiantMutagenPod(Organ):
    mutagen = 2 * mechanics.mutagenpodsize
    def draw0(self, zoom, status, growth):
        return graphics.pod.giantimgmutagen(zoom = zoom, growth = growth, color = status, edge0 = self.edge)

class GiantPlasterPod(Organ):
    plaster = 2 * mechanics.plasterpodsize
    def draw0(self, zoom, status, growth):
        return graphics.pod.giantimgplaster(zoom = zoom, growth = growth, color = status, edge0 = self.edge)

class Mutagenitor(Organ):
    """Collects twinklers and generates mutagen"""
    suction = True
    amount = mechanics.mutagenhit

    def draw0(self, zoom, status, growth):
        return graphics.generator.imgmutagen(zoom = zoom, growth = growth, color = status, edge0 = self.edge)

    def energize(self):
        if self.attached():
            self.body.mutagen += self.amount
        self.glowtime = 0.5

class Plasteritor(Organ):
    """Collects twinklers and generates mutagen"""
    suction = True
    amount = mechanics.plasterhit

    def draw0(self, zoom, status, growth):
        return graphics.generator.imgplaster(zoom = zoom, growth = growth, color = status, edge0 = self.edge)

    def energize(self):
        if self.attached():
            self.body.plaster += self.amount
        self.glowtime = 0.5

class GiantMutagenitor(Mutagenitor):
    amount = 3 * mechanics.mutagenhit
    def draw0(self, zoom, status, growth):
        return graphics.generator.giantimgmutagen(zoom = zoom, growth = growth, color = status, edge0 = self.edge)

class GiantPlasteritor(Plasteritor):
    amount = 3 * mechanics.plasterhit
    def draw0(self, zoom, status, growth):
        return graphics.generator.giantimgplaster(zoom = zoom, growth = growth, color = status, edge0 = self.edge)

class Cube(Organ):
    """Faster tile generation"""
    ncubes = 1

    def draw0(self, zoom, status, growth):
        return graphics.cube.img(zoom = zoom, growth = growth, color = status, edge0 = self.edge)


class Shield(Organ):
    """Shield"""
    shield = mechanics.shieldradius

    def draw0(self, zoom, status, growth):
        return graphics.shield.img(zoom = zoom, growth = growth, color = status, edge0 = self.edge)

    def wobble(self):
        """Something penetrated the shield"""

class Bulb(Organ):
    """Silent but deadly. Actually not so silent."""
    attacker = True
    attackrange = mechanics.bulbrange
    dhp = mechanics.bulbdhp
    def __init__(self, *args):
        Organ.__init__(self, *args)
        self.target = None
        self.shoottime = 0
        self.recovertime = 0

    def cansee(self, (x, y)):
        x0, y0 = self.worldpos
        dx, dy = x - x0, y - y0
        d = math.sqrt(dx ** 2 + dy ** 2)
        if d > self.attackrange: return False
        angle = math.radians(self.edge * 60)
        S, C = math.sin(angle), math.cos(angle)
        return -S * dx - C * dy > 0.8 * d

    def canattack(self, enemy):
        if self.target is not None: return False
        if self.recovertime: return False
        return self.cansee((enemy.x, enemy.y))

    def attack(self, enemy):
        self.target = enemy.x, enemy.y
        self.shoottime = 0.15
        self.recovertime = 0.25
        enemy.hit(self.dhp)
        noise.play("zot")

    def think(self, dt):
        Organ.think(self, dt)
        self.shoottime = max(self.shoottime - dt, 0)
        self.recovertime = max(self.recovertime - dt, 0)
        if not self.shoottime:
            self.target = None

    def draw0(self, zoom, status, growth):
        return graphics.bulb.img(zoom = zoom, growth = growth, color = status, edge0 = self.edge)
    
    def draw(self, *args):
        if self.target:
            p0 = vista.worldtoview(self.worldpos)
            p1 = vista.worldtoview(self.target)
            r = int(2 + vista.zoom * 4 * (0.15 - self.shoottime))
            pygame.draw.circle(vista.screen, (255, 0, 0), p1, r, 1)
            pygame.draw.aaline(vista.screen, (255, 0, 0), p0, p1, 1)
        Organ.draw(self, *args)

class Zotter(Organ):
    """It's a coil. Tesla coil that is...."""
    attacker = True
    attackrange = mechanics.zotterrange
    dhp = mechanics.zotterdhp
    def __init__(self, *args):
        Organ.__init__(self, *args)
        self.target = None
        self.shoottime = 0
        self.recovertime = 0

    def canattack(self, enemy):
        if not self.wavetime: return False
        return self.cansee((enemy.x, enemy.y))

    def attack(self, enemy):
        dhp = self.dhp
        enemy.hit(dhp)
        noise.play("zot")

    def cansee(self, (x, y)):
        x0, y0 = self.worldpos
        dx, dy = x - x0, y - y0
        d = math.sqrt(dx ** 2 + dy ** 2)
        return d < self.attackrange

    def canattack(self, enemy):
        if self.target is not None: return False
        if self.recovertime: return False
        return self.cansee((enemy.x, enemy.y))

    def attack(self, enemy):
        self.target = enemy.x, enemy.y
        self.shoottime = 0.25
        self.recovertime = 2
        enemy.hit(1)
        noise.play("zot")

    def think(self, dt):
        Organ.think(self, dt)
        self.shoottime = max(self.shoottime - dt, 0)
        self.recovertime = max(self.recovertime - dt, 0)
        if not self.shoottime:
            self.target = None

    def draw0(self, zoom, status, growth):
        return graphics.coil.img(zoom = zoom, growth = growth, color = status, edge0 = self.edge)
    
    def draw(self, *args):
        if self.target:
            p0 = vista.worldtoview(self.worldpos)
            p1 = vista.worldtoview(self.target)
            r = int(2 + vista.zoom * 3 * (0.25 - self.shoottime))
            pygame.draw.circle(vista.screen, (255, 0, 0), p1, r, 1)
            pygame.draw.aaline(vista.screen, (255, 0, 0), p0, p1, 1)
        Organ.draw(self, *args)



class Star(Organ):
    """Unleashes a wave of destruction! Unleashes it I say!"""
    attacker = True
    attackrange = 0
    suction = True
    dhp = mechanics.stardhp
    range0 = mechanics.starrange
    def __init__(self, *args):
        Organ.__init__(self, *args)
        self.wavetime = 0
        self.recovertime = 0

    def cansee(self, (x, y)):
        x0, y0 = self.worldpos
        dx, dy = x - x0, y - y0
        d = math.sqrt(dx ** 2 + dy ** 2)
        if d > self.attackrange: return False
        return True

    def canattack(self, enemy):
        if not self.wavetime: return False
        return self.cansee((enemy.x, enemy.y))

    def attack(self, enemy):
        dhp = self.dhp
        enemy.hit(dhp)
        noise.play("wavehit")

    def think(self, dt):
        Organ.think(self, dt)
        self.wavetime = max(self.wavetime - dt, 0)
        self.attackrange = self.range0 * (1 - self.wavetime / 0.5) if self.wavetime else 0
        self.recovertime = max(self.recovertime - dt, 0)

    def energize(self):
        if self.recovertime:
            return
        self.wavetime = 0.5
        noise.play("wavego")
        self.glowtime = 0.5
        self.recovertime = 5

    def draw0(self, zoom, status, growth):
        return graphics.star.img(zoom = zoom, growth = growth, color = status, edge0 = self.edge)
    
    def draw(self, *args):
        if self.attackrange:
            p0 = vista.worldtoview(self.worldpos)
            for dr, g in ((0, 255), (0.2, 192), (0.4, 128), (0.6, 64)):
                r = int(vista.zoom * (self.attackrange - dr))
                if r < 0.1: continue
                pygame.draw.circle(vista.screen, (g, 0, 0), p0, r, 1)
        Organ.draw(self, *args)




otypes = {"eye":Eye, "brain":Brain, "giantbrain":GiantBrain, "eyebrain":EyeBrain, "tripleeye":TripleEye,
        "cube":Cube, "zotter":Zotter,
        "bulb":Bulb, "star":Star,
        "mutagenpod":MutagenPod, "plasterpod":PlasterPod,
        "giantmutagenpod":GiantMutagenPod, "giantplasterpod":GiantPlasterPod,
        "mutagenitor":Mutagenitor, "plasteritor":Plasteritor,
        "giantmutagenitor":GiantMutagenitor, "giantplasteritor":GiantPlasteritor,
        "shield":Shield}




