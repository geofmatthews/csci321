import sys

world = None
def noFunc(): pass

try:
	import pygame
	from pygame.locals import *
except ImportError, errmsg:
	print "Requires PyGame"
	print errmsg
	sys.exit(1)	
try:
	from OpenGL.GL import *
	from OpenGL.GLU import *
	
except ImportError, errmsg:
	print "Requires PyOpenGL"
	print errmsg
	sys.exit(1)
try:
	import numpy
except ImportError, errmsg:
	print "Requires numpy"
	print errmsg
	sys.exit(1)

from data import filepath

from DfConstants import *
from DfArrow import *
from DfWorld import *
from DfSplash import splashScreen, endScreen, pauseScreen
from DfSoundManager import SoundManager


world = None

def main():
	try:
		import psyco
		psyco.full()
	except:
		print "Pysco recommended for optimal performance (not available on all platforms)"

	global world
	pygame.mixer.pre_init(22050, -16, 2, 1024)
	pygame.init()
	setupScreen()
	initOGL()
	
	if RELEASE:
		try:
			error.ErrorChecker.registerChecker(noFunc)
		except:
			print "Error checking cannot be disabled."
			print "Please upgrade to the latest version of PyOpenGL"	
	
	if SoundManager().isMusicOn():
		SoundManager().playMusic()
	
	while 1:
		result = splashScreen()
		if result == -1:
			sys.exit(0)	
		else:
			world = World(result)

		
		clock = pygame.time.Clock()
		clock.tick()
		
		
		while 1:
			eventCheck = checkEvents()
			if eventCheck == -1:
				break
		
			checkKeyStates()
			
			update()
			if not world:
				endScreen()
				break
			draw()
			
			pygame.display.flip()
			
			if eventCheck == 1:
				pauseScreen()			

			clock.tick(TICK_RATE)
			#print 1000.0 / clock.tick(TICK_RATE)
			#print 1000.0 / clock.tick(1)
			#print 1000.0 / clock.tick()
		
def setupScreen():
	icon = pygame.image.load(filepath("icon_pygame.png"))
	icon.set_colorkey((255, 0, 255))
	pygame.display.set_icon(icon)
	pygame.display.set_mode((800, 600 + BOTTOM_PANEL_SIZE), OPENGL | DOUBLEBUF)
	"""try:
		icon = pygame.image.load(filepath("icon_pygame.png")).convert_alpha()
		pygame.display.set_icon(icon)
	except:
		print "icon alpha failure"""
def initOGL():
	glClearColor(*GROUND_COLOR)
	glClear(GL_COLOR_BUFFER_BIT)
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	glShadeModel(GL_SMOOTH)
	
	glEnable(GL_LINE_SMOOTH)
	glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
	
	glEnable(GL_POINT_SMOOTH)
	glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)	
	
	glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
	
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluOrtho2D(0, SCREEN_RES[0], 0, SCREEN_RES[1] + BOTTOM_PANEL_SIZE)
		
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	
	glTranslatef(0, BOTTOM_PANEL_SIZE, 0)
	
	#glViewport(0, 100, 800, 600)
		
def checkEvents():
	for event in pygame.event.get():
		if event.type == QUIT:
			sys.exit(0)
		if event.type == KEYDOWN:
			if event.dict["key"] == K_ESCAPE:
				return -1
			if event.dict["key"] in (K_PAUSE, K_p):
				return 1
			
		#print pygame.key.get_focused()
			
def checkKeyStates():
	pressed = pygame.key.get_pressed()
	if pressed[K_LEFT]:
		world.rotate(False)
	elif pressed[K_RIGHT]:
		world.rotate(True)
		
def update():
	global world
	world.update()
	if world.isFinished():
		world = world.genNextLevel()
		
		if world:
			f = open(filepath("unlockedLevels.txt"), "w")
			f.write(str(world.iLevel + 1))
			f.close()
			
def draw():
	glClear(GL_COLOR_BUFFER_BIT)
	world.draw()