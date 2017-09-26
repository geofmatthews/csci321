"""Tile graphics"""

import pygame, math, random
from pygame.locals import *
import vista, settings

def qBezier((x0,y0), (x1,y1), (x2,y2), n = 8):
    """Quadratic bezier curve"""
    ts = [float(j) / n for j in range(n+1)]
    cs = [((1-t)**2, 2*t*(1-t), t**2) for t in ts]
    return [(a*x0+b*x1+c*x2, a*y0+b*y1+c*y2) for a,b,c in cs]    

def mutatecolor((r, g, b), f = 1, d = 10):
    def mutate(x):
        return min(max(x + random.randint(-d, d), 0), 255)
    return mutate(r*f), mutate(g*f), mutate(b*f)


def drawblobs(surf, color, (x0, y0), (x1, y1), width = None, r0 = None, s0 = 0):
    """A set of random circles within a rectangle going between the two
    specified endpoints. Simulates blobbiness."""
    rstate = random.getstate()
    seed = x0, y0, x1, y1, width, r0, s0
    random.seed(seed)
    dx, dy = x1 - x0, y1 - y0
    d = math.sqrt(dx ** 2 + dy ** 2)
    if width is None: width = d
    if r0 is None: r0 = width / 8
    circs = []
    ncirc = int(4 * width * d / r0 ** 2)
    for j in range(ncirc):
        r = int(random.uniform(r0, 2*r0))
        z = random.uniform(-width/2, width/2)
        q = random.uniform(-width/2, width/2)
        if math.sqrt(z**2 + q**2) + r > width/2: continue
        p = random.uniform(0, d)
        shade = mutatecolor(color, 1 - abs(q / width), 0)
        circs.append((z, p, q, r, shade))
    if random.random() < 0.1:
        while True:  # Add the suction cup
            r = int(2*r0)
            z = random.uniform(-width/2, width/2)
            q = random.uniform(width/3, width/2)
            if math.sqrt(z**2 + q**2) > width/2: continue
            if s0 % 2: q = -q
            p = 0.5 * d
            circs.append((z, p, q, r, (255, 255, 0)))
            break
        
    circs.sort()

    for _, p, q, r, shade in circs:
        x = int(x0 + (p * dx + q * dy) / d + 0.5)
        y = int(y0 + (p * dy - q * dx) / d + 0.5)
        pygame.draw.circle(surf, shade, (x, y), r, 0)
    random.setstate(rstate)

def drawblobsphere(surf, color, (x0, y0), R, r0 = None):
    """A set of random circles within a sphere"""
    rstate = random.getstate()
    seed = x0, y0, R, r0
    random.seed(seed)
    circs = []
    if r0 is None: r0 = R / 10.
    ncirc = int(50 * R ** 2 / r0 ** 2)
    for j in range(ncirc):
        r = int(random.uniform(r0, 2*r0))
        x = random.uniform(-R, R)
        y = random.uniform(-R, R)
        z = random.uniform(-R, R)
        if math.sqrt(x ** 2 + y ** 2 + z ** 2) + r > R: continue
        cr, cg, cb = color
        shade = mutatecolor(color, 1 - 0.35 * (R-(z-x-y)/1.7)/R)
        circs.append((z, x, y, r, shade))
    circs.sort()
    
    for _, x, y, r, shade in circs:
        px = int(x0 + x + 0.5)
        py = int(y0 + y + 0.5)
        pygame.draw.circle(surf, shade, (px, py), r, 0)
    random.setstate(rstate)


def drawapp(dedges, color, zoom = settings.tzoom0, edge0 = 3, cache = {}):
    """Draw appendage"""
    key = tuple(dedges), color, zoom, edge0
    if key in cache:
        return cache[key]
    if zoom == settings.tzoom0:
        img = pygame.Surface((2*zoom, 2*zoom), SRCALPHA)
        if len(dedges) == 1:
            def hextooffset((x, y)):
                """Convert hex coordinates to offset within this image"""
                wx, wy = vista.grid.hextoworld((x, y))
                px = int(zoom + zoom * wx + 0.5)
                py = int(zoom - zoom * wy + 0.5)
                return px, py
            p0 = hextooffset(vista.grid.edgehex((0,0), edge0))
            p1 = (zoom, zoom)
            p2s = [hextooffset(vista.grid.edgehex((0,0), edge0 + dedge)) for dedge in dedges]
            pss = [qBezier(p0, p1, p2) for p2 in p2s]
            img.lock()
            for j in range(len(pss[0])-1):
                for ps in pss:
                    drawblobs(img, color, ps[j], ps[j+1], 0.3*zoom, s0=j)
            img.unlock()
        else:
            for dedge in dedges:
                img.blit(drawapp((dedge,), color), (0,0))
    else:
        img0 = drawapp(dedges, color, settings.tzoom0, edge0)
        img = pygame.transform.scale(img0, (2*zoom, 2*zoom))
    cache[key] = img
    return img

def drawcore(color, zoom = settings.tzoom0, cache = {}):
    """Draw the body core"""
    key = zoom, color
    if key in cache: return cache[key]
    if zoom == settings.tzoom0:
        img = pygame.Surface((2*zoom, 2*zoom), SRCALPHA)
        drawblobsphere(img, color, (zoom, zoom), int(0.85*zoom))
    else:
        img0 = drawcore(color, settings.tzoom0)
        img = pygame.transform.scale(img0, (2*zoom, 2*zoom))
    cache[key] = img
    return img

def drawhex(color0, color1, zoom = settings.tzoom0, cache = {}):
    key = color0, color1, zoom
    if key in cache:
        return cache[key]
    img = pygame.Surface((2*zoom, 2*zoom), SRCALPHA)
    s3 = math.sqrt(3)
    ps = [(int(zoom*(1+x)+0.5), int(zoom*(1+y)+0.5)) for x,y in
          ((1,0),(.5,-s3/2),(-.5,-s3/2),(-1,0),(-.5,s3/2),(.5,s3/2))]
    pygame.draw.polygon(img, color0, ps, 0)
    ps = [(int(zoom*(1+.95*x)+0.5), int(zoom*(1+.95*y)+0.5)) for x,y in
          ((1,0),(.5,-s3/2),(-.5,-s3/2),(-1,0),(-.5,s3/2),(.5,s3/2))]
    pygame.draw.polygon(img, color1, ps, 0)
    cache[key] = img
    return img

def drawtile(dedges, color, zoom = settings.tzoom0, tilt = 0, cache = {}):
    """Draw one of the placeable tiles that appears in the side panel"""
    tilt = -int(tilt / 10 + 0.5) * 10 % 360
    key = tuple(dedges), color, zoom, tilt
    if key in cache:
        return cache[key]
    if tilt == 0:
        if zoom == settings.tzoom0:
            img = drawhex(mutatecolor(color, 0.4, 0), mutatecolor(color, 0.2, 0)).copy()
            img.blit(drawapp(dedges, color, zoom), (0,0))
        else:
            img0 = drawtile(dedges, color)
            img = pygame.transform.scale(img0, (2*zoom, 2*zoom))
    else:
        img0 = drawtile(dedges, color, zoom)
        img = pygame.transform.rotate(img0, tilt)
    cache[key] = img
    return img

drawqueue = []

def queueapp(dedges, colors, zoom = None):
    if zoom is None: zoom = vista.zoom
    for color in colors:
        for edge0 in range(6):
            spec = tuple(dedges), color, 60, edge0
            drawqueue.append(("app", spec))

def killtime(tmax = 20):
    tstart = pygame.time.get_ticks()
    tend = tstart + tmax
    n = 0
    while drawqueue and pygame.time.get_ticks() < tend:
        name, spec = drawqueue[0]
        del drawqueue[0]
        if name == "app":
            drawapp(*spec)
        n += 1
    print pygame.time.get_ticks() - tstart, n, len(drawqueue), name, spec

for a in range(5):
    for b in range(5):
        if a > b: continue
        dedges = (a+1,) if a == b else (a+1,b+1)
        queueapp(dedges, [(0,192,64), (64,64,192), (160,80,0)])


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((400, 400))

    screen.fill((0, 0, 0))
#    drawapp(screen, (1,2,3,4,), (0, 192, 96), (200, 200), 160)
#    drawblobsphere(screen, (0, 192, 96), (200, 200), 120)
    screen.blit(drawtile((1,2), (0, 192, 96)), (0, 0))
    screen.blit(drawtile((3,), (0, 192, 96)), (200, 0))
#    mini = pygame.transform.smoothscale(screen, (120, 120))
#    screen.fill((0, 0, 0))
#    screen.blit(mini, mini.get_rect(center = (200, 200)))

    while True:
        if any(event.type in (QUIT, KEYDOWN) for event in pygame.event.get()):
            break
        pygame.display.flip()
    


