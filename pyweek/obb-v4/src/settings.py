import sys

# Attention players: I can't guarantee that the game will run properly
# if you mess with these settings. I haven't tested every possible
# combination. These settings are here for my benefit.

# Having said that, feel free to mess with these settings. :)
# At the very least, if you change any of the settings, you should
#   restart the game with --restart


# Controls
panonpoint = False # Viewport follows mouse cursor
panonarrows = True  # Use arrow keys (or WASD) to move viewport
zoomonscroll = True  # Zoom using scroll wheel
trashonrightclick = True  # Trash a tile by right-clicking on it
panonrightclick = False   # Jump to a position by right-clicking on viewport
panondrag = True  # Move the viewport by left-click and dragging

# Overall game window
sx, sy = 854, 480

fac = 1
if "--small" in sys.argv:
    fac = 0.75
    sx, sy = 640, 360
elif "--big" in sys.argv:
    fac = 1.25
    sx, sy = 1068, 600
elif "--huge" in sys.argv:
    fac = 1.5
    sx, sy = 1280, 720
def f(*args):
    return int(fac * args[0]) if len(args) == 1 else [int(fac*arg) for arg in args]


size = sx, sy
# Main game viewport
vsize = vx, vy = f(480), sy
vx0, vy0 = f(187), 0
# Tile panel (left)
psize = px, py = vx0, sy
px0, py0 = 0, 0
# Status panel (right)
rsize = rx, ry = sx - px - vx, sy
rx0, ry0 = px + vx, 0

class layout:
    meterbottom = f(330)
    mutagenmeterx = f(124)
    metermaxy = f(300)
    healmeterx = f(160)
    brainiconpos = f(-20, 486)
    controlpos = f(42, 450)
    countsize = f(60)  # Font size of counters
    organcountsize = f(40)
    cubeiconpos = f(42, 36)
    ptilesize = f(48) # Size of selectable tiles in the panel
    ptiley = f(70)  # Offset position of top tile
    buildiconsize = f(36)
    buildiconxs = f(752, 752-36, 752-2*36)

iconsize = f(70)
iconpos = {}
iconpos["zoomin"] = f(227, 440)
iconpos["zoomout"] = f(627, 440)
iconpos["pause"] = f(227, 40)
iconpos["music"] = f(627, 40)
iconpos["trash"] = f(51, 429)
iconpos["cut"] = f(136, 429)
iconpos["heal"] = f(803, 370)

maxtextwidth = f(140)
maxblockwidth = f(420)

tzoom0 = 144  # Default tile size
zooms = 16, 24, 32, 40, 48, 60, 72
zoom0 = max(z for z in zooms if z <= f(48))
largebuildicon = tzoom0


showstars = True
twisty = True  # Twisty paths

audiobuffer = False  # Works better for me with buffer off
soundvolume = 0.5

showtips = True


silent = "--silent" in sys.argv or "--nosound" in sys.argv
restart = "--restart" in sys.argv
fullscreen = "--fullscreen" in sys.argv
barrage = "--barrage" in sys.argv  # Loads of enemies. Not fun.
if "--slow" in sys.argv:
    showstars = False
    tzoom0 = 72
fast = "--doubletime" in sys.argv    

# Cheat
unlockall = "--unlockall" in sys.argv   # Will probably only work if you restart
debugkeys = False

showfps = "--showfps" in sys.argv
saveonquit = True
autosave = True
savetimer = 15  # seconds between autosaves

minfps, maxfps = 10, 60




