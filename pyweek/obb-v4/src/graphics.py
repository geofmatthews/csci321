"""Graphics module"""

import pygame, math, random
from pygame.locals import *
import vista, settings, mechanics, data
from fixes import pixels_alpha

colors = {}
colors["app0"] = 0, 0.8, 0.4, 1
colors["app1"] = 0.8, 0.4, 0, 1
colors["app2"] = 0.7, 0, 1, 1
colors["target"] = 1, 0, 0, 1
colors["core"] = 0.2, 1, 0.2, 1
colors["ghost"] = 1, 1, 1, 0.4
colors["badghost"] = 1, 0, 0, 0.4
colors["brain"] = 1, 0.85, 0.85, 1
colors["eye"] = 1, 1, 1, 1
colors["yellow"] = 1, 1, 0.4, 1
colors["shield"] = 0.7, 0.7, 1, 1
colors["cube"] = 0, 0.2, 1, 1
colors["bulb"] = 1, 0.5, 0.5, 1
colors["star"] = 1, 1, 0, 1
colors["mutagen"] = 0, 1, 1, 0
colors["plaster"] = 1, 1, 0, 1
colors["zotter"] = 1, 1, 0, 1
colors["bad"] = 1, 0, 0, 1
colors["good"] = 0, 1, 0, 1
colors["dust"] = 0.8, 0.4, 0, 1

def qBezier((x0,y0), (x1,y1), (x2,y2), n = 8, ccache = {}):
    """Quadratic bezier curve"""
    if n not in ccache:
        ts = [float(j) / n for j in range(n+1)]
        ccache[n] = [((1-t)**2, 2*t*(1-t), t**2) for t in ts]
    return [(a*x0+b*x1+c*x2, a*y0+b*y1+c*y2) for a,b,c in ccache[n]]

def cBezier((x0,y0), (x1,y1), (x2,y2), (x3,y3), n = 8, ccache = {}):
    """Cubic bezier curve"""
    if n not in ccache:
        ts = [float(j) / n for j in range(n+1)]
        ccache[n] = [((1-t)**3, 3*t*(1-t)**2, 3*t**2*(1-t), t**3) for t in ts]
    return [(a*x0+b*x1+c*x2+d*x3, a*y0+b*y1+c*y2+d*y3) for a,b,c,d in ccache[n]]

def drawgraycircles(surf, circs):
    for _, x, y, r, g in circs:
        pygame.draw.circle(surf, (g,g,g), (x, y), r, 0)

def drawcolorcircles(surf, circs):
    for _, x, y, r, color in circs:
        pygame.draw.circle(surf, color, (x, y), r, 0)

def drawchannelcircles(surf, allcircs):
    assert len(allcircs) <= 3
    circs = [(z,x,y,r,(g,0,0)) for z,x,y,r,g in allcircs[0]]
    if len(allcircs) > 1: circs += [(z,x,y,r,(0,g,0)) for z,x,y,r,g in allcircs[1]]
    if len(allcircs) > 2: circs += [(z,x,y,r,(0,0,g)) for z,x,y,r,g in allcircs[2]]
    for _, x, y, r, color in sorted(circs):
        pygame.draw.circle(surf, color, (x, y), r, 0)

def normcircles(circs, scale=1, (x0, y0) = (0, 0)):
    return [(z, int(scale*(x+x0)+.5), int(scale*(y+y0)+.5), max(int(scale*r+.5),1), min(max(int(255*g+.5),0),255))
                for z,x,y,r,g in sorted(circs)]

def normcolorcircles(circs, scale=1, (x0, y0) = (0, 0)):
    return [(z, int(scale*(x+x0)+.5), int(scale*(y+y0)+.5), max(int(scale*r+.5),1),
             (min(max(int(255*R+.5),0),255), min(max(int(255*G+.5),0),255), min(max(int(255*B+.5),0),255)))
                for z,x,y,r,(R,G,B) in sorted(circs)]

def filtersurface(surf, x, y, z, a=1):
    arr = pygame.surfarray.pixels3d(surf)
    if x != 1: arr[...,0] *= x
    if y != 1: arr[...,1] *= y
    if z != 1: arr[...,2] *= z
    if a != 1: pixels_alpha(surf)[:] *= a

def filtercolorsurface(surf, (x0,y0,z0,a0), (x1,y1,z1,a1)=(0,0,0,0), (x2,y2,z2,a2)=(0,0,0,0)):
    arr = pygame.surfarray.pixels3d(surf)
    r = arr[...,0] * x0 + arr[...,1] * x1 + arr[...,2] * x2
    g = arr[...,0] * y0 + arr[...,1] * y1 + arr[...,2] * y2
    b = arr[...,0] * z0 + arr[...,1] * z1 + arr[...,2] * z2
    arr[...,0] = r
    arr[...,1] = g
    arr[...,2] = b
    # TODO: what to do about transparency here??
    if a0 != 1: pixels_alpha(surf)[:] *= a0


def maketransparent(surf):
    filtersurface(surf, 1, 1, 1, 0.5)

class Circles(object):
    """A graphic that's made from repeated calls to pygame.draw.circles"""
    def __init__(self):
        self.cache = {}
        self.imgcache = {}

    def getargs(self, *args):
        """Return a sequence that's in the same order as the args to getkey
        and getcircles, with all the defaults filled in"""
        return args

    def getkey(self, *args):
        """args will exclude scale and offset"""
        return tuple((tuple(arg) if isinstance(arg, list) else arg) for arg in args)

    def getdrawargs(self, *args, **kw):
        return args, kw

    def getdrawkey(self, args, kw):
        return tuple(args), tuple(kw.items())

    def getcircles(self):
        """Be a generator, make things easier"""
        raise NotImplementedError

    def __call__(self, *args, **kw):
        """Return the list of circles (in world coordinates)
        args should exclude scale and offset"""
        args = self.getargs(*args, **kw)
        key = self.getkey(*args)
        if key in self.cache: return self.cache[key]
        rstate = random.getstate()
        random.seed(key)
        circs = list(self.getcircles(*args))
        random.setstate(rstate)
        self.cache[key] = circs
        return circs

    def draw(self, surf, scale, offset, *args, **kw):
        circs = self(*args, **kw)
        circs = normcircles(circs, scale, offset)
        drawgraycircles(surf, circs)

    def grayimg(self, scale, *args, **kw):
        scale = int(scale)
        drawargs, drawkw = self.getdrawargs(*args, **kw)
        key = scale, self.getdrawkey(drawargs, drawkw)
        if key in self.imgcache: return self.imgcache[key]
        img = vista.Surface(2*scale)
        offset = (1,1)
        self.draw(img, scale, offset, *drawargs, **drawkw)
        self.imgcache[key] = img
        return img

    def graytile(self, zoom = settings.tzoom0, *args, **kw):
        key = zoom, self.getdrawkey(*self.getdrawargs(*args, **kw))
        if key in self.imgcache: return self.imgcache[key]
        if zoom == settings.tzoom0:
            img0 = self.grayimg(zoom, *args, **kw)
            img = vista.Surface(2*zoom)
            img.blit(img0, img0.get_rect(center = (zoom,zoom)))
        else:
            img0 = self.graytile(settings.tzoom0, *args, **kw)
            img = pygame.transform.smoothscale(img0, (2*zoom, 2*zoom))
        self.imgcache[key] = img
        return img

class ColorCircles(Circles):
    """Allow for up to 3 colors"""
    def draw(self, surf, scale, offset, *args, **kw):
        circs = self(*args, **kw)
        circs = normcolorcircles(circs, scale, offset)
        drawcolorcircles(surf, circs)

class SegmentCircles(Circles):
    def getargs(self, (dx, dy), width, r0 = None, s0 = 0):
        if r0 is None: r0 = 0.03
        return (dx, dy), width, r0, s0

    def getcircles(self, (dx, dy), width, r0, s0):
        d = math.sqrt(dx ** 2 + dy ** 2)
        ncirc = int(4 * width * d / r0 ** 2)
        for j in range(ncirc):
            r = random.uniform(r0, 2*r0)
            z = random.uniform(-width/2, width/2)
            q = random.uniform(-width/2, width/2)
            if math.sqrt(z**2 + q**2) + r > width/2: continue
            p = random.uniform(0, d)
            g = 1 - abs(q / width)
            x = (p * dx + q * dy) / d
            y = (p * dy - q * dx) / d
            yield z, x, y, r, g
        if random.random() < 0.5:  # Gross blobby nodules??
            z = random.uniform(-width/2, width/2)
            q = random.uniform(0.3*width, 0.5*width) * random.choice([-1,1])
            p = random.uniform(0, d)
            x = (p * dx + q * dy) / d
            y = (p * dy - q * dx) / d
            yield z, x, y, 2*r0, 1
            

segmentcircles = SegmentCircles()

class StalkCircles(Circles):
    def getargs(self, ps, width = 0.3):
        return tuple(ps), width
    
    def getcircles(self, ps, width):
        for j in range(len(ps)-1):
            (x0, y0), (x1, y1) = ps[j], ps[j+1]
            for z, x, y, r, g in segmentcircles((x1-x0, y1-y0), width, None, j):
                yield z, x+x0, y+y0, r, g

stalkcircles = StalkCircles()

class AppCircles(Circles):
    def getargs(self, dedges, growth = 1, edge0 = 3, width = 0.3):
        segs = int(growth * 8)
        return tuple(dedges), edge0, width, segs
    
    def getcircles(self, dedges, edge0, width, segs):
        for dedge in dedges:
            p0 = eps[edge0]
            p1 = eips[edge0]
            p2 = eips[(edge0+dedge)%6]
            p3 = eps[(edge0+dedge)%6]
            ps = cBezier(p0, p1, p2, p3, 8)
            for circ in stalkcircles.getcircles(ps[:segs+1], width):
                yield circ

    def img(self, dedges, color, growth = 1, edge0 = 3, zoom = settings.tzoom0):
        gimg = self.graytile(zoom, tuple(dedges), growth, edge0).copy()
        if color in colors:
            color = colors[color]
        filtersurface(gimg, *color)
        return gimg

app = AppCircles()

class CoilCircles(ColorCircles):
    def getargs(self, growth = 1, edge0 = 3, width0 = 0.3):
        segs = int(growth * 40) / 4 * 4
        return edge0, width0, segs
    
    def getcircles(self, edge0, width0, segs):
        qs = [(0,-.866), (.5,0), (0,.5), (-.5,0), (0,0), (0,.15)]
        rs = [(-.2,.4), (.1,.5), (-.5,0), (.2,-.3), (.3,.3), (0,.3)]
        ps = []
        for j in range(5):
            (x0,y0), (x1,y1) = qs[j], qs[j+1]
            (dx0,dy0), (dx1,dy1) = rs[j], rs[j+1]
            ps.extend(cBezier((x0,y0), (x0+dx0,y0+dy0), (x1-dx1,y1-dy1), (x1,y1), 8)[:-1])
        angle = math.radians(edge0 * 60)
        S, C = math.sin(angle), math.cos(angle)
        for j in range(segs):
            width = width0 * (1 - j / 60.)
            for z, x, y, r, g in stalkcircles.getcircles(ps[j:j+2], width):
                yield z, -x*C - y*S, -x*S + y*C, r, (g, 0, 0)
        if segs == 40:
            dx, dy = ps[-1]
            dx, dy = -dx*C - dy*S, -dx*S + dy*C
            for z, x, y, r, g in spherecircles.getcircles(0.2, 0.03, (-1,-1,2)):
                yield z, x+dx, y + dy, r, (0, g, 0)

    def img(self, color = None, growth = 1, edge0 = 3, zoom = settings.tzoom0):
        gimg = self.graytile(zoom, growth, edge0).copy()
        if color in colors:
            color = colors[color]
        if not color:
            filtercolorsurface(gimg, colors[mechanics.colors["zotter"]], colors["zotter"])
        else:
            filtercolorsurface(gimg, color, color)
        return gimg

coil = CoilCircles()

class PodCircles(ColorCircles):
    def getargs(self, growth = 1, edge0 = 3, R = 0.5, r0 = 0.03):
        growth = int(growth * 8) / 8.
        return edge0, growth, R, r0
    
    def getcircles(self, edge0, growth, R, r0):
        angle = math.radians(edge0 * 60)
        S, C = math.sin(angle), math.cos(angle)
        N = int(30 * R / r0)
        for j in range(int(N*growth)):
            beta = math.radians(180 * j / N)
            bS, bC = math.sin(beta), math.cos(beta)
            theta = 3 * beta + 1
            tS, tC = math.sin(theta), math.cos(theta)
            y = R * bC + random.uniform(-2*r0, 2*r0)
            x = R * tS * bS + random.uniform(-2*r0, 2*r0)
            z = R * tC * bS + random.uniform(-2*r0, 2*r0)
            g = random.uniform(0, 0.2) + 0.3 * z / R + 0.6
            r = random.uniform(r0, 2*r0)
            yield z, -x*C-y*S, y*C-x*S, r, (g, 0, 0)
            g = random.uniform(0, 0.2) - 0.3 * z / R + 0.6
            yield -z, x*C-y*S, y*C+x*S, r, (g, 0, 0)

        if growth > 0.2:
            for z, x, y, r, g in spherecircles.getcircles(R*growth, 0.03, (-1,-1,2)):
                yield z, x, y, r, (0, g, 0)

        dx, dy = eps[edge0]
        for z, x, y, r, g in spherecircles.getcircles(R*.7, 0.03, (-1,-1,2)):
            yield z, x+dx*.45, y+dy*.45, r, (g, 0, 0)
        segs = min(int(growth * 8 + 0.5), 3)
        if segs:
            for z, x, y, r, g in app.getcircles((3,), edge0, 0.3, segs):
                yield z, x, y, r, (g, 0, 0)

    def img(self, color0, color1, growth = 1, edge0 = 3, Rfac = 1., zoom = settings.tzoom0):
        gimg = self.graytile(zoom, growth, edge0, 0.4 * Rfac).copy()
        filtercolorsurface(gimg, color0, color1)
        return gimg

    def imgmutagen(self, color = None, growth = 1, edge0 = 3, Rfac = 1., zoom = settings.tzoom0):
        if color:
            if color in colors: color = colors[color]
            return self.img(color, color, growth, edge0, Rfac, zoom)
        color0 = colors[mechanics.colors["mutagenpod"]]
        color1 = colors["mutagen"]
        return self.img(color0, color1, growth, edge0, Rfac, zoom)

    def imgplaster(self, color = None, growth = 1, edge0 = 3, Rfac = 1., zoom = settings.tzoom0):
        if color:
            if color in colors: color = colors[color]
            return self.img(color, color, growth, edge0, Rfac, zoom)
        color0 = colors[mechanics.colors["plasterpod"]]
        color1 = colors["plaster"]
        return self.img(color0, color1, growth, edge0, Rfac, zoom)

    def giantimgmutagen(self, color = None, growth = 1, edge0 = 3, Rfac = 1.6, zoom = settings.tzoom0):
        return self.imgmutagen(color, growth, edge0, Rfac, zoom)

    def giantimgplaster(self, color = None, growth = 1, edge0 = 3, Rfac = 1.6, zoom = settings.tzoom0):
        return self.imgplaster(color, growth, edge0, Rfac, zoom)

pod = PodCircles()

class GeneratorCircles(ColorCircles):
    def getargs(self, growth = 1, edge0 = 3, R = 0.25, r0 = 0.03):
        growth = int(growth * 8) / 8.
        return edge0, growth, R, r0
    
    def getcircles(self, edge0, growth, R, r0):
        angle = math.radians(edge0 * 60)
        S, C = math.sin(angle), math.cos(angle)

        if growth > 0.5:
            s2 = math.sqrt(2)
            for z, x, y, r, g in spherecircles.getcircles(R*(.5+.5*growth), r0, (-1,1,2)):
                y *= 4
                y, z = (y + z) / s2, (y - z) / s2
                for s, c in ((0, 1), (.86,-.5), (-.86,-.5)):
                    ax, ay = (x*c+y*s), (y*c-x*s)
                    yield z, -ax*C-ay*S, ay*C-ax*S, r, (0, g*.5+.5, 0)
        if growth > 0.2:
            for z, x, y, r, g in spherecircles.getcircles(1.7*R*growth, r0, (-1,-1,2)):
                yield z, x, y, r, (g, 0, 0)

        segs = min(int(growth * 8 + 0.5), 3)
        if segs:
            for z, x, y, r, g in app.getcircles((3,), edge0, 0.3, segs):
                yield z, x, y, r, (g, 0, 0)

    def img(self, color0, color1, growth = 1, edge0 = 3, Rfac = 1, zoom = settings.tzoom0):
        gimg = self.graytile(zoom, growth, edge0, 0.2 * Rfac).copy()
        filtercolorsurface(gimg, color0, color1)
        return gimg

    def imgmutagen(self, color = None, growth = 1, edge0 = 3, Rfac = 1, zoom = settings.tzoom0):
        if color:
            if color in colors: color = colors[color]
            return self.img(color, color, growth, edge0, Rfac, zoom)
        color0 = colors[mechanics.colors["mutagenitor"]]
        color1 = colors["mutagen"]
        return self.img(color0, color1, growth, edge0, Rfac, zoom)

    def imgplaster(self, color = None, growth = 1, edge0 = 3, Rfac = 1, zoom = settings.tzoom0):
        if color:
            if color in colors: color = colors[color]
            return self.img(color, color, growth, edge0, Rfac, zoom)
        color0 = colors[mechanics.colors["plasteritor"]]
        color1 = colors["plaster"]
        return self.img(color0, color1, growth, edge0, Rfac, zoom)

    def giantimgmutagen(self, color = None, growth = 1, edge0 = 3, Rfac = 1.6, zoom = settings.tzoom0):
        return self.imgmutagen(color, growth, edge0, Rfac, zoom)

    def giantimgplaster(self, color = None, growth = 1, edge0 = 3, Rfac = 1.6, zoom = settings.tzoom0):
        return self.imgplaster(color, growth, edge0, Rfac, zoom)


generator = GeneratorCircles()





class StarCircles(ColorCircles):
    def getargs(self, growth = 1, edge0 = 3, R = 0.3, r0 = 0.03):
        growth = int(growth * 8) / 8.
        return edge0, growth, R, r0
    
    def getcircles(self, edge0, growth, R, r0):
        angle = math.radians(edge0 * 60)
        S, C = math.sin(angle), math.cos(angle)
        length = growth - 0.2
        if length > 0.1:
            betas = [0.3, 0.3, 1.3, 3.3, 3.3]
            thetas = [0.8, 2.2, -0.8, 0.8, 2.2]
#            betas = betas + [beta + math.pi for beta in betas]
#            thetas = thetas + thetas
            for point, (beta, theta) in enumerate(zip(betas, thetas)):
                bS, bC = math.sin(beta), math.cos(beta)
                tS, tC = math.sin(theta), math.cos(theta)
                for z, x, y, r, g in segmentcircles.getcircles((0, length), 0.3, r0, point):
                    x *= 1 - y / length
                    z *= 1 - y / length
                    y, z = y * bS + z * bC, y * bC - z * bS
                    x, z = x * tS - z * tC, x * tC + z * tS
                    z = -z
                    g = 0.7 + 0.2 * z / length + random.uniform(-.1, .1)
                    yield z, -x*C-y*S, y*C-x*S, r, (g, 0, 0)

        if growth > 0.2:
            for z, x, y, r, g in spherecircles.getcircles(R*growth, r0, (-1,-1,2)):
                yield z, x, y, r, (0, g, 0)

        segs = min(int(growth * 8 + 0.5), 4)
        if segs:
            for z, x, y, r, g in app.getcircles((3,), edge0, 0.3, segs):
                yield z, x, y, r, (g, 0, 0)

    def img(self, color = None, growth = 1, edge0 = 3, zoom = settings.tzoom0):
        gimg = self.graytile(zoom, growth, edge0).copy()
        if color in colors:
            color = colors[color]
        if not color:
            filtercolorsurface(gimg, colors[mechanics.colors["star"]], colors["star"])
        else:
            filtercolorsurface(gimg, color, color)
        return gimg

star = StarCircles()



class CubeCircles(ColorCircles):
    def getargs(self, growth = 1, edge0 = 3, R = 0.45, r0 = 0.03):
        growth = int(growth * 8) / 8.
        return edge0, growth, R, r0
    
    def getcircles(self, edge0, growth, R, r0):
        angle = math.radians(edge0 * 60)
        S, C = math.sin(angle), math.cos(angle)

        s = R * growth
        s2 = math.sqrt(2)
        for j in range(int((s/r0)**3)):
            r = random.uniform(r0,2*r0)
            x = random.uniform(-s+r, s-r)
            y = random.uniform(-s+r, s-r)
            z = random.uniform(-s+r, s-r)
            m = max(abs(x), abs(y), abs(z))
            if m == abs(x):
                g = random.uniform(0.4, 0.5)
            elif m == abs(y):
                g = random.uniform(0.9, 1)
            else:
                g = random.uniform(0.6, 0.7)
            x, z = (x - z) / s2, (x + z) / s2
            y, z = (y - z) / s2, (y + z) / s2
            yield z, x, -y, r, (0, g, 0)
#            yield z, -x*C-y*S, y*C-x*S, r, (0, g, 0)

        if growth > 0.2:
            dx, dy = eps[edge0]
            for z, x, y, r, g in spherecircles.getcircles(R*.7, 0.03, (-1,-1,2)):
                yield z, x+dx*.45, y+dy*.45, r, (g, 0, 0)
        segs = min(int(growth * 8 + 0.5), 3)
        if segs:
            for z, x, y, r, g in app.getcircles((3,), edge0, 0.3, segs):
                yield z, x, y, r, (g, 0, 0)

    def img(self, color = None, growth = 1, edge0 = 3, zoom = settings.tzoom0):
        gimg = self.graytile(zoom, growth, edge0).copy()
        if color in colors:
            color = colors[color]
        if not color:
            filtercolorsurface(gimg, colors[mechanics.colors["cube"]], colors["cube"])
        else:
            filtercolorsurface(gimg, color, color)
        return gimg

cube = CubeCircles()

class BulbCircles(ColorCircles):
    def getargs(self, growth = 1, edge0 = 3, R = 0.6, r0 = 0.03):
        growth = int(growth * 8) / 8.
        return edge0, growth, R, r0
    
    def getcircles(self, edge0, growth, R, r0):
        angle = math.radians(edge0 * 60)
        S, C = math.sin(angle), math.cos(angle)
        R *= growth
        for z, x, y, r, g in spherecircles.getcircles(R, r0, (1,1,2)):
            f = 0.6 - 0.55 * y / R
            x *= f
            z *= f
            y += 0.1
            yield z, -x*C-y*S, y*C-x*S, r, (0,g,0)
        if growth > 0.2:
            dx, dy = eps[edge0]
            for z, x, y, r, g in spherecircles.getcircles(0.3, 0.03, (-1,-1,2)):
                yield z, x+dx*.45, y+dy*.45, r, (g, 0, 0)
        segs = min(int(growth * 8 + 0.5), 3)
        if segs:
            for z, x, y, r, g in app.getcircles((3,), edge0, 0.3, segs):
                yield z, x, y, r, (g, 0, 0)

    def img(self, color = None, growth = 1, edge0 = 3, zoom = settings.tzoom0):
        gimg = self.graytile(zoom, growth, edge0).copy()
        if color in colors:
            color = colors[color]
        if not color:
            filtercolorsurface(gimg, colors[mechanics.colors["bulb"]], colors["bulb"])
        else:
            filtercolorsurface(gimg, color, color)
        return gimg

bulb = BulbCircles()





def heximg(scale, cache = {}):
    if scale in cache: return cache[scale]
    s3 = math.sqrt(3)
    img = vista.Surface(2*scale)
    spos = lambda x,y: (int(scale*(1+x)+.5), int(scale*(1-y)+.5))
    vpos = [(1,0),(.5,-.5),(-.5,-.5),(-1,0),(-.5,.5),(.5,.5)]
    vps = [spos(x,s3*y) for x,y in vpos]  # Vertex positions
    vips = [spos(.92*x,.92*s3*y) for x,y in vpos]  # inner vertex positions
    pygame.draw.polygon(img, (128, 128, 128), vps, 0)
    pygame.draw.polygon(img, (64, 64, 64), vips, 0)
    cache[scale] = img
    return img
    

class PanelTile(Circles):
    """A hexagonal tile that appears on the left"""
    def getargs(self, dedges):
        return tuple(dedges),

    def getdrawkey(self, (dedges,), kw):
        return tuple(dedges),
    
    def getcircles(self, dedges):
        for circ in app.getcircles(dedges, 3, 0.3, 8):
            yield circ

    def draw(self, surf, scale, offset, dedges):
        himg = heximg(scale)
        surf.blit(himg, himg.get_rect(center = surf.get_rect().center))
        Circles.draw(self, surf, scale, offset, dedges)

    def img(self, dedges, color, zoom = settings.tzoom0):
        gimg = self.graytile(zoom, dedges).copy()
        if color in colors:
            color = colors[color]
        filtersurface(gimg, *color)
        return gimg

paneltile = PanelTile()

def drawpaneltile(dedges, color, tilt = 0):
    img = paneltile.img(dedges, color, zoom = settings.layout.ptilesize)
    return pygame.transform.rotate(img, -tilt) if tilt else img


class SphereCircles(Circles):
    def getargs(self, R, r0 = 0.05, lvector = (-1,-1,2)):
        return R, r0, tuple(lvector)

    def getcircles(self, R, r0, (lx, ly, lz)):
        sl = math.sqrt(lx ** 2 + ly ** 2 + lz ** 2)
        fx, fy, fz = [l / sl / (R-r0) for l in (lx, ly, lz)]
        ncirc = int(40 * R ** 2 / r0 ** 2)
        for j in range(ncirc):
            r = random.uniform(r0, 2*r0)
            x = random.uniform(-R, R)
            y = random.uniform(-R, R)
            z = random.uniform(-R, R)
            if math.sqrt(x ** 2 + y ** 2 + z ** 2) + r > R: continue
            g = 0.55 + 0.45 * (fx*x+fy*y+fz*z)
            yield z, x, y, r, g

    def img(self, R, color = None, zoom = settings.tzoom0):
        gimg = self.graytile(zoom, R).copy()
        if color in colors:
            color = colors[color]
        filtersurface(gimg, *color)
        return gimg


spherecircles = SphereCircles()

class OrganCircles(Circles):
    def getargs(self, growth = 1, edge0 = 3, r0 = 0.05, width = 0.3, lvector = (-1,-1,2)):
        segs = min(int(growth * 6), 3)
        R = int(growth * 8) / 8. - 0.5
        return R, edge0, segs, r0, width, tuple(lvector)

    def getcircles(self, R, edge0, segs, r0, width, lvector):
        for circ in spherecircles.getcircles(R, r0, lvector):
            yield circ
        dx, dy = eps[edge0]
        for z, x, y, r, g in spherecircles.getcircles(R*.5, r0, lvector):
            yield z, x+dx*.45, y+dy*.45, r, g
        for circ in app.getcircles((3,), edge0, width, segs):
            yield circ

    def img(self, growth = 1, color = None, edge0 = 3, zoom = settings.tzoom0):
        gimg = self.graytile(zoom, growth, edge0).copy()
        if color in colors:
            color = colors[color]
        filtersurface(gimg, *color)
        return gimg

organ = OrganCircles()

def eyeball(R, edge0 = 3, blink = 1, color = (0, 255, 0), cache = {}):
    R = int(R + 0.5)
    blink = int(blink * 20) / 20.
    edge0 = 0 if blink == 1 else edge0 % 3
    key = R, edge0, blink, color
    if key in cache: return cache[key]
    img = vista.Surface(2*R)
    if blink == 1:
        pygame.draw.circle(img, color, (R, R), int(R * 0.35))
    else:
        rect = pygame.Rect(0, 0, int(R * 0.7), int(R * 0.7 * blink))
        rect.center = R, R
        pygame.draw.ellipse(img, color, rect)
    if blink >= 0.4:
        pygame.draw.circle(img, (0, 0, 0), (R, R), int(R * 0.15))
    if edge0:
        img = pygame.transform.rotozoom(img, -60 * edge0, 1)
    cache[key] = img
    return cache[key]

class EyeCircles(ColorCircles):
    def getargs(self, growth = 1, edge0 = 3, blink = 1, r0 = 0.05, width = 0.3, lvector = (-1,-1,2)):
        segs = min(int(growth * 6), 3)
        R = int(growth * 8) / 8. - 0.5
        return R, edge0, segs, r0, width, tuple(lvector)

    def getcircles(self, R, edge0, segs, r0, width, lvector):
        for z, x, y, r, g in organ.getcircles(R, edge0, segs, r0, width, lvector):
            yield z, x, y, r, (g, 0, 0)

    def draw(self, surf, scale, offset, growth, edge0, blink):
        ColorCircles.draw(self, surf, scale, offset, growth, edge0, blink)
        if growth == 1:
            eimg = eyeball(scale, edge0, blink)
            surf.blit(eimg, eimg.get_rect(center=surf.get_rect().center))

    def img(self, growth = 1, color = None, edge0 = 2, blink = 1, zoom = settings.tzoom0):
        gimg = self.graytile(zoom, growth, edge0, blink).copy()
        if color in colors:
            color = colors[color]
        if not color:
            filtercolorsurface(gimg, colors[mechanics.colors["eye"]], colors["eye"])
        else:
            filtercolorsurface(gimg, color, color)
        return gimg

eye = EyeCircles()

class TripleEyeCircles(ColorCircles):
    def getargs(self, growth = 1, edge0 = 3, blink = 1, r0 = 0.05, width = 0.3, lvector = (-1,-1,2)):
        segs = min(int(growth * 6), 3)
        growth = int(growth * 8) / 8.
        R = (growth - 0.5) * 0.7
        return R, edge0, segs, r0, width, tuple(lvector)

    def getcircles(self, R, edge0, segs, r0, width, lvector):
        dx, dy = eps[edge0]
        for z, x, y, r, g in spherecircles.getcircles(R*.7, r0, lvector):
            yield z, x+dx*.45, y+dy*.45, r, (g, 0, 0)
        for z, x, y, r, g in app.getcircles((3,), edge0, width, segs):
            yield z, x, y, r, (g, 0, 0)
        angle = edge0 * 60
        ds = [(0.25*math.sin(math.radians(angle+da)), 0.25*math.cos(math.radians(angle+da))) for da in (0, 120, 240)]
        for z, x, y, r, g in spherecircles.getcircles(R, r0, lvector):
            for dx, dy in ds:
                yield z, x+dx, y+dy, r, (g, 0, 0)

    def draw(self, surf, scale, offset, growth, edge0, blink):
        ColorCircles.draw(self, surf, scale, offset, growth, edge0, blink)
        if growth == 1:
            angle = -edge0 * 60
            ds = [(0.3*math.sin(math.radians(angle+da)), 0.3*math.cos(math.radians(angle+da))) for da in (0, 120, 240)]
            for j, (dx, dy) in enumerate(ds):
                eimg = eyeball(0.65*scale, edge0-2*j, 0.9*blink)
                x, y = surf.get_rect().center
                surf.blit(eimg, eimg.get_rect(center=(int(x+dx*scale),int(y+dy*scale))))

    def img(self, growth = 1, color = None, edge0 = 3, blink = 1, zoom = settings.tzoom0):
        gimg = self.graytile(zoom, growth, edge0, blink).copy()
        if color in colors:
            color = colors[color]
        if not color:
            filtercolorsurface(gimg, colors[mechanics.colors["eye"]], colors["eye"])
        else:
            filtercolorsurface(gimg, color, color)
        return gimg

tripleeye = TripleEyeCircles()

class LobeCircles(SphereCircles):
    def getargs(self, R, angle = 0, r0 = 0.05, lvector = (-1, -1, 2)):
        return R, angle, r0, tuple(lvector)

    def getcircles(self, R, angle, r0, lvector):
        C, S = math.cos(math.radians(angle)), math.sin(math.radians(angle))
        for z, x, y, r, g in SphereCircles.getcircles(self, R, r0, lvector):
            if abs(x) < 0.95*r: continue
            if math.sqrt((1.2*x) ** 2 + y ** 2 + z ** 2) + r > R: continue
            x, y = C * x - S * y, C * y + S * x
            yield z, x, y, r, g

lobecircles = LobeCircles()

class BrainCircles(ColorCircles):
    def getargs(self, growth = 1, edge0 = 3, Rfac = 1, lvector = (-1,-1,2)):
        segs = min(int(growth * 6), 3)
        growth = int(growth * 8) / 8.
        R = (growth - 0.5) * Rfac
        r0 = 0.05
        width = 0.3
        return R, edge0, segs, r0, width, tuple(lvector)

    def getcircles(self, R, edge0, segs, r0, width, lvector):
        angle = edge0 * 60 + 180
        for z, x, y, r, g in lobecircles.getcircles(R, angle, r0, lvector):
            yield z, x, y, r, (g, 0, 0)
        for z, x, y, r, g in app.getcircles((3,), edge0, width, segs):
            yield z, x, y, r, (0, g, 0)

    def img(self, growth = 1, color = None, edge0 = 3, Rfac = 1, zoom = settings.tzoom0):
        gimg = self.graytile(zoom, growth, edge0, Rfac).copy()
        if color in colors:
            color = colors[color]
        if not color:
            filtercolorsurface(gimg, colors["brain"], colors[mechanics.colors["brain"]])
        else:
            filtercolorsurface(gimg, color, color)
        return gimg

    def giantimg(self, growth = 1, color = None, edge0 = 3, zoom = settings.tzoom0):
        return self.img(growth, color, edge0, 1.6, zoom)

brain = BrainCircles()

class EyeBrainCircles(BrainCircles):
    def getargs(self, growth = 1, edge0 = 3, blink = 1, lvector = (-1,-1,2)):
        segs = min(int(growth * 6), 3)
        growth = int(growth * 8) / 8.
        R = growth - 0.5
        if growth != 1: blink = 1
        r0 = 0.05
        width = 0.3
        return R, edge0, blink, segs, r0, width, tuple(lvector)

    def getcircles(self, R, edge0, blink, segs, r0, width, lvector):
        return brain.getcircles(R, edge0, segs, r0, width, lvector)

    def draw(self, surf, scale, offset, growth, edge0, blink):
        brain.draw(surf, scale, offset, growth, edge0)
        x0, y0 = surf.get_rect().center
        if growth == 1:
            for dedge,r in ((0,0.3),(1,0.4),(2,0.1),(2,0.45),(3,0.35),(4,0.4),(5,.25)):
                angle = math.radians((edge0 + dedge) * 60 + 20)
                dx = int(scale * r * math.sin(angle) / 1.2)
                dy = -int(scale * r * math.cos(angle) / 1.2)
                eyeimg = eyeball(int(0.3*scale), (dedge+edge0)%6, blink=1-r/2, color=(0,0,255))
                surf.blit(eyeimg, eyeimg.get_rect(center = (x0+dx,y0+dy)))

    def img(self, growth = 1, color = None, edge0 = 3, blink = 1, zoom = settings.tzoom0):
        gimg = self.graytile(zoom, growth, edge0, blink).copy()
        if color in colors:
            color = colors[color]
        if not color:
            filtercolorsurface(gimg, colors["brain"], colors[mechanics.colors["brain"]], colors["eye"])
        else:
            filtercolorsurface(gimg, color, color, color)
        return gimg

eyebrain = EyeBrainCircles()

class ShieldCircles(ColorCircles):
    def getargs(self, growth = 1, edge0 = 3, lvector = (-1,-1,2)):
        segs = min(int(growth * 6), 3)
        growth = int(growth * 8) / 8.
        R0 = growth - 0.6
        R1 = growth - 0.8
        r0 = 0.05
        width = 0.3
        return R0, R1, edge0, segs, r0, width, tuple(lvector)

    def getcircles(self, R0, R1, edge0, segs, r0, width, lvector):
        dx, dy = eps[edge0]

        for z, x, y, r, g in spherecircles.getcircles(R0, r0, lvector):
            yield z, x, y, r, (0, g, 0)
        for z, x, y, r, g in spherecircles.getcircles(R0*.5, r0, lvector):
            yield z, x+dx*.45, y+dy*.45, r, (g, 0, 0)
            yield z, x-dx*.35, y-dy*.35, r, (g, 0, 0)
            yield z, x-dy*.35, y+dx*.35, r, (g, 0, 0)
            yield z, x+dy*.35, y-dx*.35, r, (g, 0, 0)
            yield z+.35, x, y, r, (g, 0, 0)
        for z, x, y, r, g in app.getcircles((3,), edge0, width, segs):
            yield z, x, y, r, (0, g, 0)

    def img(self, growth = 1, color = None, edge0 = 3, zoom = settings.tzoom0):
        gimg = self.graytile(zoom, growth, edge0).copy()
        if color in colors:
            color = colors[color]
        if not color:
            filtercolorsurface(gimg, colors["shield"], colors[mechanics.colors["shield"]])
        else:
            filtercolorsurface(gimg, color, color)
        return gimg

shield = ShieldCircles()




class HelixCircles(Circles):
    def getargs(self, (dx, dy), offs = (0, 0.4), R = 12, r = 4, coil = 60):
        return (dx, dy), tuple(offs), R, r, coil
    
    def getcircles(self, (dx, dy), offs, R, r, coil):
        d = math.sqrt(dx ** 2 + dy ** 2)
        nextrung = r
        for j in range(int(2. * d / r)):
            h = j / (2. / r)
            angles = [(h / coil + off) * 2 * math.pi for off in offs]
            Ss = [math.sin(angle) for angle in angles]
            Cs = [math.cos(angle) for angle in angles]
            xs = [R * S * dy / d + h * dx / d for S in Ss]
            ys = [-R * S * dx / d + h * dy / d for S in Ss]
            gs = [0.8 + 0.2 * C for C in Cs]
            zs = Cs
            for z,x,y,g in zip(zs, xs, ys, gs):
                yield z, x, y, r, g
            if len(offs) == 2 and h > nextrung:
                nextrung += 1.7 * r
                (x0, x1), (y0, y1), (g0, g1), (z0, z1) = xs, ys, gs, zs
                for k in range(20):
                    k *= 0.05
                    x = x0 + k * (x1 - x0)
                    y = y0 + k * (y1 - y0)
                    z = z0 + k * (z1 - z0)
                    g = g0 + k * (g1 - g0)
                    yield z, x, y, r*.6, g

helixcircles = HelixCircles()

def helixmeter(height, f=3):
    img = vista.Surface(40*f, f*height)
    helixcircles.draw(img, f, (20, height), (0, -height))
    if f != 1:
        img = pygame.transform.smoothscale(img, (40, height))
    return img

def stalkmeter(height, f=3):
    img = vista.Surface(40*f, f*height)
    h = height / 60.
    ps = []
    for y in range(int(h)+1):
        p0 = 0, -y
        p1 = 0.15 * math.sin(y**2), -y-0.3
        p2 = 0.15 * -math.sin((y+1)**2), -y-0.7
        p3 = 0, -y-1
        ps += cBezier(p0, p1, p2, p3)[:-1]
    stalkcircles.draw(img, 60*f, (1/3., h), ps, width=0.3)
    if f != 1:
        img = pygame.transform.smoothscale(img, (40, height))
    return img


def loadbar(f, color = "eye", w = 60, h = 8):
    if color in colors: color = colors[color]
    r,g,b,_ = color
    color = int(255*r), int(255*g), int(255*b)
    img = vista.Surface(w+2,h+2,color)
    if 0 < f < 1:
        img.fill((0,0,0), (1+int(f*w),1,w-int(f*w),h))
    return img
    


# TODO
stalkimages = []
def core(_color, growth = 0, zoom = settings.tzoom0):
    z = settings.tzoom0
    img = vista.Surface(3*z)
    if not stalkimages:
        for edge in range(6):
            stalkimg = vista.Surface(2*z)
            x0, y0 = stalkimg.get_rect().center
            stalkimg.fill((0,0,0,0))
            r, g, b, a = colors["app%s" % (edge % 3)]
            S, C = math.sin(math.radians(60 * edge)), -math.cos(math.radians(60 * edge))
            dx, dy = 0.3 * S, 0.3 * C
            segmentcircles.draw(stalkimg, z, (1, 1), (dx, dy), 0.3)
            filtersurface(stalkimg, r, g, b, a)
            stalkimages.append(stalkimg)
    for edge in range(6):
        stalkimg = stalkimages[edge]
        x0, y0 = stalkimg.get_rect().center
        S, C = math.sin(math.radians(60 * edge)), -math.cos(math.radians(60 * edge))
        dx, dy = 0.3 * S * z, 0.3 * C * z
        dr = min(max((1 - growth) * 4 - 0.2 * (5 - edge), 0), 0.5) if growth != 1 else 0
        x, y = (1.5+(.65-dr)*S) * z, (1.5+(.65-dr)*C) * z
        img.blit(stalkimg, stalkimg.get_rect(center = (x,y)))
    sphereimg = spherecircles.img(R = 0.75, color = "core", zoom = z)
#    return sphereimg
    img.blit(sphereimg, sphereimg.get_rect(center = img.get_rect().center))
    return pygame.transform.smoothscale(img, (3*zoom, 3*zoom))


# Coordinates of vertices and edges
epos = [(0,.5),(.75,.25),(.75,-.25),(0,-.5),(-.75,-.25),(-.75,.25)]
s3 = math.sqrt(3)
spos = lambda x,y: (x, -y)
eps = [spos(x,s3*y) for x,y in epos]
if settings.twisty:
    angles = [math.radians(60*a+10) for a in range(6)]
    eips = [spos(.5*math.sin(a),.5*math.cos(a)) for a in angles]
else:
    eips = [spos(0,0) for a in range(6)]


def meter(img, level, color1 = (0.5, 0, 1), color0 = (0.2, 0.2, 0.2)):
    img2 = img.copy()
    h = img2.get_height()
    p = h - level
    arr = pygame.surfarray.pixels3d(img2)
    x, y, z = color1[:3]
    if x != 1: arr[...,p:,0] *= x
    if y != 1: arr[...,p:,1] *= y
    if z != 1: arr[...,p:,2] *= z
    x, y, z = color0[:3]
    if x != 1: arr[...,:p,0] *= x
    if y != 1: arr[...,:p,1] *= y
    if z != 1: arr[...,:p,2] *= z
    return img2

def icon(name, size = settings.layout.buildiconsize, cache = {}):
    key = name, size
    if key in cache:
        return cache[key]
    s = settings.largebuildicon
    img = vista.Surface(s)
    r, g, b, a = colors[mechanics.colors[name]]
    color0 = int(r*255), int(g*255), int(b*255)
    color1 = int(r*32), int(g*32), int(b*32)
    img.fill(color0)
    img.fill(color1, (6, 6, s-12, s-12))
    import body
    otype = body.otypes[name]
    part = otype(None, None, (0, 0), 3)
    partimg = part.draw0(zoom = int(s*.6), status = "", growth = 1)
    img.blit(partimg, partimg.get_rect(center = img.get_rect().center))
    img = pygame.transform.smoothscale(img, (size, size))
    return img

def ghostify(img):
    img2 = img.copy()
    arr = pygame.surfarray.pixels3d(img2)
    g = (arr[...,0]/8 + arr[...,1]/8 + arr[...,2]/8) + 32
    arr[...,0] = arr[...,1] = arr[...,2] = g
    return img2

def brighten(img):
    img2 = img.copy()
    arr = pygame.surfarray.pixels3d(img2)
    arr[...] = arr[...] / 2 + 127
    return img2

def thoughtbubble(h, w = settings.maxblockwidth, cache = {}):
    key = w, h
    if key in cache:
        return cache[key]
    circs = []
    for j in range(int(w*h*0.05)):
        x = random.uniform(0, w)
        y = random.uniform(0, h)
        z = random.uniform(0.5, 1)
        r = random.uniform(10, 20)
        g = z
        circs.append((z, x, y, r, g))
    circs = normcircles(circs, 1, (20, 20))
    img = vista.Surface(w+40, h+40)
    drawgraycircles(img, circs)
    cache[key] = img
    return img


def gettwinklerimg(zoom, angle, cache = {}):
    angle = int(angle % 90) / 5 * 5
    zoom  = int(zoom)
    key = zoom, angle
    if key in cache: return cache[key]
    if "base" not in cache:
        cache["base"] = pygame.image.load(data.filepath("twinkler.png")).convert_alpha()
    img = pygame.transform.rotozoom(cache["base"], angle, float(zoom) / 240.)
    
    cache[key] = img
    return cache[key]

def gettwinklerimgs(t, r0 = 1):
    return [gettwinklerimg(vista.zoom*r*r0, angle) for r, angle in
            [(1, t * 40), (0.8, t * 100), (0.8, t * -100)]]
    

def dustcloudimg(angle = 0, alpha = 1, R = 1, cache = {}):
    z = int(R * vista.zoom)
    angle = int(angle % 360) / 10 * 10
    alpha = min(max(int(alpha * 10) / 10., 0), 1)
    key = z, angle, alpha
    if key in cache:
        return cache[key]
    if "base" not in cache:
        img0 = spherecircles.img(R = 0.3, color = "dust", zoom = settings.tzoom0)
        cache["base"] = vista.Surface(0.8*settings.tzoom0)
        cache["base"].blit(img0, img0.get_rect(center = cache["base"].get_rect().center))
    img = pygame.transform.rotozoom(cache["base"], angle, float(z) / settings.tzoom0)
    if alpha != 1:
        pixels_alpha(img)[:] *= alpha
    cache[key] = img
    return cache[key]

def shipimg(angle = 0, cache = {}):
    z = int(vista.zoom)
    angle = int((angle + 2.5) % 360) / 5 * 5
    key = z, angle
    if key in cache:
        return cache[key]
    if "base" not in cache:
        cache["base"] = pygame.image.load(data.filepath("ship.png")).convert_alpha()
    img = pygame.transform.rotozoom(cache["base"], angle, float(z) / 150.)
    cache[key] = img
    return cache[key]

def heartimg(alpha = 1, cache = {}):
    z = int(vista.zoom)
    alpha = min(max(int(alpha * 10) / 10., 0), 1)
    key = z, alpha
    if key in cache:
        return cache[key]
    if "base" not in cache:
        cache["base"] = pygame.image.load(data.filepath("heart.png")).convert_alpha()
    img = pygame.transform.smoothscale(cache["base"], (z, z))
    if alpha != 1:
        pixels_alpha(img)[:] *= alpha
    cache[key] = img
    return cache[key]



def mouthimg(n = 0, cache = {}):
    z = int(0.7 * vista.zoom)
    key = z, n
    if key in cache:
        return cache[key]
    if (n, "base") not in cache:
        cache[(n, "base")] = pygame.image.load(data.filepath("mouth-%s.png" % n)).convert_alpha()
    img = pygame.transform.smoothscale(cache[(n, "base")], (3*z,3*z))
    cache[key] = img
    return cache[key]




if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((400, 400))

    screen.fill((0, 0, 0))
    img = vista.Surface(200)

    if False:
        t0 = pygame.time.get_ticks()
        loadallappimages([60])
        t1 = pygame.time.get_ticks()
        print t1 - t0

    
    if False:
        circs = [(random.uniform(-100, 100), random.uniform(-100, 100), random.uniform(5, 20), random.uniform(64, 192)) for _ in range(2000)]
        circs = [(int(x),int(y),int(r),c) for x,y,r,c in circs if x**2 + y**2 < 100**2]

        for _ in range(10):
            img.fill((0,0,0))
            t0 = pygame.time.get_ticks()
            drawgraycircles(img, circs, (100, 100))
            s = pygame.surfarray.pixels3d(img)
            s[...,0] *= 1
            s[...,1] *= 0.6
            s[...,2] *= 0
            del s
            t1 = pygame.time.get_ticks()
            print t1 - t0
    if False:
        for _ in range(10):
            img.fill((0,0,0))
            t0 = pygame.time.get_ticks()
            drawgraysegment(img, (100, 50), (100, 150))
            filtersurface(img, 1, 0.6, 0)
            t1 = pygame.time.get_ticks()
            print t1 - t0
    if False:
        for _ in range(10):
            t0 = pygame.time.get_ticks()
            img = app((1,2,3), (1, 0.8, 0), 1, 60)
            filtersurface(img, 1, 1, 0)
            t1 = pygame.time.get_ticks()
            print t1 - t0
    if False:
        img = sphere(0.5, color = "ghost", zoom = 60)
    if True:
#        drawgraylobes(img, (100, 100), 60, 10)
#        img = sphere(0.5, color = "ghost", zoom = 60)
#        img = brain()
#        img = brain(edge0=1)
#        img = grayapp((2,3))
#        img = brain.grayimg(160)
#        filtercolorsurface(img, (1, 0.8, 0.8, 1), (0, 0.5, 1, 1))
#        img = tripleeye.img(zoom = 80, edge0 = 2)
#        img = star.img(zoom = 80, edge0 = 2)
#        img = coil.img(zoom = 80)
#        img = eyebrain.img(zoom = 80)
#        helixcircles.draw(img, 1, (100, 200), (0, -160))
#        img = helixmeter(200)
#        img = meter(img, 120)
#        img = pod.giantimgmutagen(zoom = 80)
#        img = spherecircles.img(zoom = 200, R = 0.3, color = (0.8, 0.3, 0.3, 1))
        img = dustcloudimg()
        pass
    if False:
        img = vista.Surface(40, 400, (0, 0, 0))
        drawgrayhelix(img, (20,0), (20,400))
        img = meter(img, 100)
        
    t0 = pygame.time.get_ticks()
    screen.blit(img, (0,0))
    t1 = pygame.time.get_ticks()
    print t1 - t0
    

    while True:
        if any(event.type in (QUIT, KEYDOWN) for event in pygame.event.get()):
            break
        pygame.display.flip()


