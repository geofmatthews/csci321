import pygame, math, datetime, collections, random, os
from pygame.locals import *
import settings, data, tip

# Okay, here's the deal. There are six simultaneous coordinate systems
#   going on at once.

# World coordinates: Zoom-level invariant coordinate system, where the
#   gameplay happens. Distances between game object should be computed
#   in this coordinate system.
# Hex coordinates: A skewed linear transform of world coordinates that
#   maps the tile centers to (integer) lattice points. Since edges are
#   midpoints between these, edges are obviously at half-integer
#   coordinates.
# Gameplay coordinates: Transformation of world coordinates to pixel
#   coordinates. The pixels in question are in some arbitrary surface
#   that doesn't necessarily correspond to the screen. The gameplay
#   surface can be resized when the gameplay area is extended, or when
#   the zoom level is changed. When these happen, the mapping to world
#   coordinates changes. Panning does not affect this mapping.
# View coordinates: The viewport is a rectangle that actually appears
#   on the screen. Generally it's a piece of the gameplay surface. The
#   mapping between gameplay coordinates and view coordinates can change
#   when the gameplay area is panned.
# Screen coordinates: The viewport doesn't have to be in the upper-left
#   corner of the window, in which case this coordinate system is used
#   for mouse coordinates and there's a transformation to view
#   coordinates that's just an offset.
# Mask coordinates: The mask is the surface that has the visibility-
#   blocking mask. It doesn't need very high resolution.

def Surface(x, y = None, color = None, alpha = True):
    if y is None:
        if isinstance(x, collections.Sequence):
            x, y = x
        else:
            y = x
    if alpha:
        surf = pygame.Surface((x,y), SRCALPHA).convert_alpha()
    else:
        surf = pygame.Surface((x,y), SRCALPHA).convert()
    if color is not None:
        surf.fill(color)
    return surf

icons = {}
class Icon(object):
    def __init__(self, name, color = (255, 255, 255)):  # TODO: replace with a real icon
        import graphics
        self.name = name
        size = settings.iconsize
        try:
            self.img = pygame.image.load(data.filepath(name + ".png")).convert_alpha()
            self.img = pygame.transform.smoothscale(self.img, (size, size))
        except:
            self.img = Surface(size, size, color)
        self.rect = self.img.get_rect()
        self.rect.center = settings.iconpos[self.name]
        self.ghost = graphics.ghostify(self.img)
        self.select = graphics.brighten(self.img)
        self.active = True
        self.selected = False
        
    def draw(self):
        img = (self.select if self.selected else self.img) if self.active else self.ghost
        _screen.blit(img, self.rect)
    
    def hit(self, pos):
        return self.rect.collidepoint(pos)

def iconhit(pos):
    for name, icon in icons.items():
        if icon.hit(pos):
            return name
    return None

musicicontext = None
def init():
    global screen, _screen, vrect, prect, zoom, psurf, rsurf, rrect
    global stars
    flags = FULLSCREEN | HWSURFACE if settings.fullscreen else 0
    _screen = pygame.display.set_mode(settings.size, flags)
    screen = Surface(settings.size, alpha = False)
    psurf = Surface(settings.psize, alpha = False)
    rsurf = Surface(settings.rsize, alpha = False)
    # TODO: decouple view and screen coordinates
    vrect = pygame.Rect(settings.vx0, settings.vy0, settings.vx, settings.vy)
    prect = pygame.Rect(settings.px0, settings.py0, settings.px, settings.py)
    rrect = pygame.Rect(settings.rx0, settings.ry0, settings.rx, settings.ry)

    for name in "zoomin zoomout pause music trash cut heal".split():
        icons[name] = Icon(name)
    stars = [(random.randint(64, 255), random.randint(-10000, 10000), random.randint(-10000, 10000)) for _ in range(settings.vx * settings.vy / 2000)]
    stars.sort()
    
    try:
        _screen.fill((0,0,0))
        splash = pygame.image.load("obb.png").convert()
        splash = pygame.transform.smoothscale(splash, (settings.sy, settings.sy))
        _screen.blit(splash, splash.get_rect(center = _screen.get_rect().center))
        pygame.display.flip()
    except:
        pass
    



wx0, wy0, wx1, wy1 = -6, -6, 6, 6  # Maximum extent of gameplay window
zoom = settings.zoom0
gx0, gy0 = 0, 0  # Gameplay location of world coordinate (0,0)

def setgrect((x0, y0, x1, y1)):
    global wx0, wy0, wx1, wy1, gx0, gy0, zoom
    wx0, wy0, wx1, wy1 = x0, y0, x1, y1

def zoomin():
    global zoom
    zs = [z for z in settings.zooms if z > zoom]
    if zs:
        zoom = min(zs)
def zoomout():
    global zoom
    zs = [z for z in settings.zooms if z < zoom]
    if zs:
        zoom = max(zs)

# TODO: scroll icons

def think(dt, (mx, my), keys):
    global gx0, gy0, overlays
    xmin, xmax = vrect.width - wx1 * zoom, -wx0 * zoom
    ymin, ymax = vrect.height + wy0 * zoom, wy1 * zoom
    f = math.exp(-0.1 * dt)
#    if vrect.collidepoint(mx,my) and pygame.mouse.get_focused():
    if settings.panonpoint:
        if pygame.mouse.get_focused():
            mx, my = mx - vrect.left, my - vrect.top
            # Potentially set the window based on mouse position
            gx0 = xmax + (xmin - xmax) * mx / vrect.width
            gy0 = ymax + (ymin - ymax) * my / vrect.height
        else:
            gx0 += (min(max(vrect.width/2, xmin), xmax) - gx0) * f
            gy0 += (min(max(vrect.height/2, ymin), ymax) - gy0) * f

    if settings.panonarrows:
        dx = (keys[K_RIGHT] or keys[K_e] or keys[K_d]) - (keys[K_LEFT] or keys[K_a])
        dy = (keys[K_DOWN] or keys[K_o] or keys[K_s]) - (keys[K_UP] or keys[K_COMMA] or keys[K_w])
        gx0 -= 10 * dt * dx * zoom
        gy0 -= 10 * dt * dy * zoom


    gx0 = max(min(gx0, xmax), xmin) if xmin < xmax else (xmin + xmax) / 2
    gy0 = max(min(gy0, ymax), ymin) if ymin < ymax else (ymin + ymax) / 2

    overlays = []
    icons["zoomout"].active = zoom != min(settings.zooms)
    icons["zoomin"].active = zoom != max(settings.zooms)

def jumptoscreenpos((x, y)):
    global gx0, gy0
    """Try to get the specified screen pos in the center of the screen"""
    wx, wy = screentoworld((x, y))
    gx0 = settings.vx / 2 - zoom * wx
    gy0 = settings.vy / 2 + zoom * wy

def scoot((dx, dy)):
    global gx0, gy0
    gx0 += dx
    gy0 += dy


def worldtogameplay((x, y)):
    return int(gx0 + x * zoom + 0.5), int(gy0 - y * zoom + 0.5)

def gameplaytoworld((gx, gy)):
    return float(gx - gx0) / zoom, -float(gy - gy0) / zoom

def worldtoview((x, y)):
    return worldtogameplay((x, y))  # TODO... maybe?

def worldtoscreen((x, y)):
    vx, vy = worldtogameplay((x, y))
    return settings.vx0 + vx, settings.vy0 + vy

def screentoworld((x, y)):
    return gameplaytoworld((x - settings.vx0, y - settings.vy0))

def clear(color = (0, 0, 0)):
    screen.fill(color)
    psurf.fill((144, 144, 144))
    rsurf.fill((144, 144, 144))
    if settings.showstars:
        for c, x, y in stars:
            px = int(x+gx0*c/400)%settings.vx
            py = int(y+gy0*c/400)%settings.vy
            screen.set_at((px, py), (c, c, c))
        


def screencap():
    if not os.path.exists("screenshots"): os.mkdir("screenshots")
    dstr = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    pygame.image.save(_screen, "screenshots/screenshot-%s.png" % dstr)

def addmask(mask):
    global screen
    x0, y0 = gameplaytoworld((0, vrect.height))  # Bottom left world coordinates
    x1, y1 = gameplaytoworld((vrect.width, 0))   # Top right world coordinates
    gsx, gsy = worldtogameplay((wx1, wy0))
    screen.blit(mask.getmask((x0, y0, x1, y1), vrect.size), (0,0))

def addoverlay(surf, rect):
    """Something that needs to be drawn on very top, irrespective of
    panel boundaries"""
    overlays.append((surf, rect))

def flip():
#    screen.blit(gsurf)  # TODO
    _screen.blit(screen, vrect)
    _screen.blit(psurf, prect)
    _screen.blit(rsurf, rrect)
    for surf, rect in overlays:
        _screen.blit(surf, rect)
    for icon in icons.values(): icon.draw()
    if musicicontext:
        rect = musicicontext.get_rect(midright = icons["music"].rect.center)
        _screen.blit(musicicontext, rect)
    tip.draw()
    pygame.display.flip()

s3 = math.sqrt(3.)
class HexGrid(object):
    def __init__(self, p0 = None, a = 60):
        self.a = a  # circumradius of tile
        if p0 is None: p0 = settings.sx / 2, settings.sy / 2
        self.x0, self.y0 = p0
        
    def gcenter(self, (x, y)):
        """Screen coordinate of center of tile at (x,y)"""
        px = self.x0 + 1.5 * x * self.a
        py = self.y0 - s3 * (y + 0.5 * x) * self.a
        return int(px + .5), int(py + .5)

    def gvertex(self, (x, y), v):
        """Screen coordinate of vth vertex of tile at (x,y)"""
        dx, dy = [(0.5,-0.5), (1,0), (0.5,0.5),
                  (-0.5,0.5), (-1,0), (-0.5,-0.5)][v%6]
        px = self.x0 + (1.5 * x + dx) * self.a
        py = self.y0 - s3 * (y + 0.5 * x + dy) * self.a
        return int(px + .5), int(py + .5)

    def gedge(self, (x, y), e):
        """Screen coordinate of center of eth edge of tile at (x,y)"""
        dx, dy = [(0,0.5), (0.75,0.25), (0.75,-0.25),
                  (0,-0.5), (-0.75,-0.25), (-0.75,0.25)][e%6]
        px = self.x0 + (1.5 * x + dx) * self.a
        py = self.y0 - s3 * (y + 0.5 * x + dy) * self.a
        return int(px + .5), int(py + .5)

    @staticmethod
    def edgehex((x, y), e):
        """Hex coordinates of given edge"""
        dx, dy = [(0,0.5), (0.5,0), (0.5,-0.5),
                  (0,-0.5), (-0.5,0), (-0.5,0.5)][e%6]
        return x+dx, y+dy

    @staticmethod
    def edgeworld((x, y), e):
        """World coordinates of given edge"""
        return HexGrid.hextoworld(HexGrid.edgehex((x, y), e))

    @staticmethod
    def vertexworld((x, y), v):
        """World coordinates of given vertex"""
        dx, dy = [(1,0),(.5,-.5),(-.5,-.5),(-1,0),(-.5,.5),(.5,.5)][v%6]
        wx, wy = HexGrid.hextoworld((x,y))
        return wx+dx, wy+s3*dy

    @staticmethod
    def worldtohex((x, y)):
        """Convert hex coordinates to world coordinates"""
        return 2./3 * x, -x/3. + y/s3

    @staticmethod
    def hextoworld((x, y)):
        """Convert world coordinates to hex coordinates"""
        return 3./2 * x, s3*(x/2. + y)

    @staticmethod
    def opposite((x, y), e):
        """The tile and edge that's opposite the specified edge"""
        dx, dy = [(0,1), (1,0), (1,-1), (0,-1), (-1,0), (-1,1)][e%6]
        return (x+dx, y+dy), (e+3)%6

    @staticmethod
    def normedge(p, e):
        """The "normalized" edge, used for comparison"""
        return (p,e%6) if e%6 < 3 else HexGrid.opposite(p, e)

    @staticmethod
    def nearesttile(pos):
        """Tile that the given world coordinate is over"""
        hx, hy = [int(math.floor(p)) for p in HexGrid.worldtohex(pos)]
        d2 = lambda (x0, y0), (x1, y1): (x0 - x1) ** 2 + (y0 - y1) ** 2
        d2s = [(d2(pos, HexGrid.hextoworld((ax, ay))), (ax, ay))
                for ax in (hx,hx+1) for ay in (hy,hy+1)]
        return min(d2s)[1]

    @staticmethod
    def nearestedge(pos):
        """Nearest edge to given world coordinate (not normalized)"""
        tile = HexGrid.nearesttile(pos)
        d2 = lambda (x0, y0), (x1, y1): (x0 - x1) ** 2 + (y0 - y1) ** 2
        d2s = [(d2(pos, HexGrid.edgeworld(tile, edge)), (tile, edge))
                for edge in range(6)]
        return min(d2s)[1]

    def tnearest(self, (px, py)):
        """The tile that the given screen position is over"""
        x0 = math.floor(float(px - self.x0) / self.a / 1.5)
        y0 = math.floor(-float(py - self.y0) / self.a / s3 - 0.5 * x0)
        d2 = lambda (x0, y0), (x1, y1): (x0 - x1) ** 2 + (y0 - y1) ** 2
        d2s = [(d2((px, py), self.gcenter((x, y))), (x, y))
                for x in (x0,x0+1) for y in (y0,y0+1)]
        return min(d2s)[1]

    @staticmethod
    def drawhex((x, y), color=None):
        if color is None:
            # TODO: support alpha
            color = [(32,0,0,32),(0,32,0,32),(0,0,32,32)][(y-x)%3]
        vs = [worldtogameplay(HexGrid.vertexworld((x, y), v)) for v in range(6)]
        pygame.draw.polygon(screen, color, vs)

    @staticmethod
    def tracehex((x, y), color=(128, 128, 128)):
        vs = [worldtogameplay(HexGrid.vertexworld((x, y), v)) for v in range(6)]
        pygame.draw.aalines(screen, color, True, vs)

grid = HexGrid(a = 30)


