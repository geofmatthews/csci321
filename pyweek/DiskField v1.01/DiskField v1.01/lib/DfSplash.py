import sys

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from DfConstants import *
from DfMain import world
from data import *
from DfWorld import World
from DfSoundManager import SoundManager

global bPOTScale

def drawBorder():
	glColor4f(*BORDER_COLOR)
	glBegin(GL_QUADS)
	glVertex2f(0, 0)
	glVertex2f(0, BORDER_WIDTH)
	glVertex2f(SCREEN_RES[0], BORDER_WIDTH)
	glVertex2f(SCREEN_RES[0], 0)
	
	glVertex2f(0, SCREEN_RES[1])
	glVertex2f(0, SCREEN_RES[1] - BORDER_WIDTH)
	glVertex2f(SCREEN_RES[0], SCREEN_RES[1] - BORDER_WIDTH)
	glVertex2f(SCREEN_RES[0], SCREEN_RES[1])

	glVertex2f(0, -BOTTOM_PANEL_SIZE)
	glVertex2f(BORDER_WIDTH, -BOTTOM_PANEL_SIZE)
	glVertex2f(BORDER_WIDTH, SCREEN_RES[1])
	glVertex2f(0, SCREEN_RES[1])	

	glVertex2f(SCREEN_RES[0] - BORDER_WIDTH, SCREEN_RES[1])
	glVertex2f(SCREEN_RES[0], SCREEN_RES[1])
	glVertex2f(SCREEN_RES[0], -BOTTOM_PANEL_SIZE)
	glVertex2f(SCREEN_RES[0] - BORDER_WIDTH, -BOTTOM_PANEL_SIZE)
	
	glVertex2f(0, - BOTTOM_PANEL_SIZE)
	glVertex2f(0, BORDER_WIDTH- BOTTOM_PANEL_SIZE)
	glVertex2f(SCREEN_RES[0], BORDER_WIDTH - BOTTOM_PANEL_SIZE)
	glVertex2f(SCREEN_RES[0], - BOTTOM_PANEL_SIZE)	
	
	glEnd()
	
	
def scaleToPOT(texture):
	# Will be slightly crisper if machine supports NPOT textures
	if bPOTScale:
		x = 1
		y = 1
		
		while x < texture.get_width():
			x *= 2
		while y < texture.get_height():
			y *= 2	
		
		texture = pygame.transform.rotozoom(texture, 0, min(float(x) / texture.get_width(), float(y) / texture.get_height()))
			
		return pygame.transform.scale(texture, (x, y))
	else:
		return texture


def splashScreen():
	global world
	global bPOTScale
	
	diskRadius = DISK_RADIUS * 1.5 
	
	bPOTScale = glGetString(GL_EXTENSIONS).find("GL_ARB_texture_non_power_of_two") == -1
	
	if bPOTScale:
		print "Non power of two textures not available"
	
	clock = pygame.time.Clock()
	clock.tick()	
	
	titleFont = pygame.font.Font(filepath(FONT_NAME), 128)
	titleSurf = titleFont.render("Disk Field", True, (0, 0, 0)).convert_alpha()
	
	normFont = pygame.font.Font(filepath(FONT_NAME), 64)
	startSurf = normFont.render("Start game", True, (0, 0, 0)).convert_alpha()	
	selectSurf = normFont.render("Select level", True, (0, 0, 0)).convert_alpha()		
	optionsSurf = normFont.render("Options", True, (0, 0, 0)).convert_alpha()		
	quitSurf = normFont.render("Quit game", True, (0, 0, 0)).convert_alpha()		
	
	titleTexture = glGenTextures(1)
	startTexture = glGenTextures(1)
	selectLevelTexture = glGenTextures(1)
	optionsTexture = glGenTextures(1)
	quitTexture = glGenTextures(1)

	glEnable(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D, titleTexture)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
	
	scaleTex = scaleToPOT(titleSurf)
	
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, scaleTex.get_width(), scaleTex.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(scaleTex, "RGBX", 1))
	
	glBindTexture(GL_TEXTURE_2D, startTexture)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)	
	
	scaleTex = scaleToPOT(startSurf)
	
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, scaleTex.get_width(), scaleTex.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(scaleTex, "RGBX", 1))
	
	glBindTexture(GL_TEXTURE_2D, selectLevelTexture)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)	
	
	scaleTex = scaleToPOT(selectSurf)
	
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, scaleTex.get_width(), scaleTex.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(scaleTex, "RGBX", 1))

	glBindTexture(GL_TEXTURE_2D, optionsTexture)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)	
	
	scaleTex = scaleToPOT(optionsSurf)
	
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, scaleTex.get_width(), scaleTex.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(scaleTex, "RGBX", 1))
	
	
	glBindTexture(GL_TEXTURE_2D, quitTexture)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)	
	
	scaleTex = scaleToPOT(quitSurf)
	
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, scaleTex.get_width(), scaleTex.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(scaleTex, "RGBX", 1))
	
	titleXBorder = (SCREEN_RES[0] - titleSurf.get_width()) / 2
	titleYBorder = 32
	
	xBorder = 160
	ySpacing = 4
	
	iSelected = 0
	iTick = 0
	
	while 1:
		glClear(GL_COLOR_BUFFER_BIT)
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			if event.type == KEYDOWN:
				if event.dict["key"] == K_UP:
					SoundManager().playInterfaceBeep()
					iSelected -= 1
					iSelected %= 4
				elif event.dict["key"] == K_DOWN:
					SoundManager().playInterfaceBeep()
					iSelected += 1
					iSelected %= 4
				elif event.dict["key"] == K_RETURN:
					if iSelected == 0:
						return 0
					elif iSelected == 1:
						levelPicked = pickLevel()
						if levelPicked != -1:
							glDeleteTextures(titleTexture)
							glDeleteTextures(startTexture)
							glDeleteTextures(selectLevelTexture)
							glDeleteTextures(optionsTexture)
							glDeleteTextures(quitTexture)
							return levelPicked
					elif iSelected == 2:
						optionsMenu()
					elif iSelected == 3:
						return -1
			
		glPushMatrix()
			
		glEnable(GL_TEXTURE_2D)
		glBindTexture(GL_TEXTURE_2D, titleTexture)
		glBegin(GL_QUADS)
		glTexCoord2f(0, 0)
		glVertex2f(titleXBorder, SCREEN_RES[1] - titleSurf.get_height() - titleYBorder)
		glTexCoord2f(0, 1)
		glVertex2f(titleXBorder, SCREEN_RES[1] - titleYBorder)
		glTexCoord2f(1, 1)
		glVertex2f(titleXBorder + titleSurf.get_width(), SCREEN_RES[1] - titleYBorder)
		glTexCoord2f(1, 0)
		glVertex2f(titleXBorder + titleSurf.get_width(), SCREEN_RES[1] - titleSurf.get_height() - titleYBorder)		
		glEnd()
		
		glTranslatef(0.0, - titleSurf.get_height() - titleYBorder - 2 * ySpacing, 0.0)
		
		glBindTexture(GL_TEXTURE_2D, startTexture)
		glBegin(GL_QUADS)
		glTexCoord2f(0, 0)
		glVertex2f(xBorder, SCREEN_RES[1] - startSurf.get_height())
		glTexCoord2f(0, 1)
		glVertex2f(xBorder, SCREEN_RES[1])
		glTexCoord2f(1, 1)
		glVertex2f(xBorder + startSurf.get_width(), SCREEN_RES[1])
		glTexCoord2f(1, 0)
		glVertex2f(xBorder + startSurf.get_width(), SCREEN_RES[1] - startSurf.get_height())		
		glEnd()
		
		glTranslatef(0.0, - startSurf.get_height() - ySpacing, 0.0)

		glBindTexture(GL_TEXTURE_2D, selectLevelTexture)
		glBegin(GL_QUADS)
		glTexCoord2f(0, 0)
		glVertex2f(xBorder, SCREEN_RES[1] - selectSurf.get_height())
		glTexCoord2f(0, 1)
		glVertex2f(xBorder, SCREEN_RES[1])
		glTexCoord2f(1, 1)
		glVertex2f(xBorder + selectSurf.get_width(), SCREEN_RES[1])
		glTexCoord2f(1, 0)
		glVertex2f(xBorder + selectSurf.get_width(), SCREEN_RES[1] - selectSurf.get_height())		
		glEnd()
		
		glTranslatef(0.0, - selectSurf.get_height() - ySpacing, 0.0)
		
		glBindTexture(GL_TEXTURE_2D, optionsTexture)
		glBegin(GL_QUADS)
		glTexCoord2f(0, 0)
		glVertex2f(xBorder, SCREEN_RES[1] - optionsSurf.get_height())
		glTexCoord2f(0, 1)
		glVertex2f(xBorder, SCREEN_RES[1])
		glTexCoord2f(1, 1)
		glVertex2f(xBorder + optionsSurf.get_width(), SCREEN_RES[1])
		glTexCoord2f(1, 0)
		glVertex2f(xBorder + optionsSurf.get_width(), SCREEN_RES[1] - optionsSurf.get_height())		
		glEnd()
		
		glTranslatef(0.0, - optionsSurf.get_height() - ySpacing, 0.0)		

		glBindTexture(GL_TEXTURE_2D, quitTexture)
		glBegin(GL_QUADS)
		glTexCoord2f(0, 0)
		glVertex2f(xBorder, SCREEN_RES[1] - quitSurf.get_height())
		glTexCoord2f(0, 1)
		glVertex2f(xBorder, SCREEN_RES[1])
		glTexCoord2f(1, 1)
		glVertex2f(xBorder + quitSurf.get_width(), SCREEN_RES[1])
		glTexCoord2f(1, 0)
		glVertex2f(xBorder + quitSurf.get_width(), SCREEN_RES[1] - quitSurf.get_height())		
		glEnd()
		
		
		glDisable(GL_TEXTURE_2D)		
		glPopMatrix()
		
		drawBorder()
			
		glPushMatrix()
	
		if iSelected == 0:
			glTranslatef(2 * xBorder / 3, SCREEN_RES[1] - titleSurf.get_height() - titleYBorder - 2 * ySpacing - startSurf.get_height() / 2, 0.0)
		elif iSelected == 1:
			glTranslatef(2 * xBorder / 3, SCREEN_RES[1] - titleSurf.get_height() - titleYBorder - 3 * ySpacing - startSurf.get_height() - selectSurf.get_height() / 2, 0.0)
		elif iSelected == 2:
			glTranslatef(2 * xBorder / 3, SCREEN_RES[1] - titleSurf.get_height() - titleYBorder - 4 * ySpacing - startSurf.get_height() - selectSurf.get_height() - optionsSurf.get_height() / 2, 0.0)
		elif iSelected == 3:
			glTranslatef(2 * xBorder / 3, SCREEN_RES[1] - titleSurf.get_height() - titleYBorder - 4 * ySpacing - startSurf.get_height() - selectSurf.get_height() - optionsSurf.get_height() - quitSurf.get_height() / 2, 0.0)
					
		
		glRotatef(-iTick * 8, 0.0, 0.0, 1.0)
		
		for j in range(4):
			if j % 2:
				glColor4f(*DISK_COLOR_1)
			else:
				glColor4f(*DISK_COLOR_2)		
			
			glBegin(GL_TRIANGLE_STRIP)	
			for i in range(46):
				angle = (i + (j * 45)) * pi / 90 
						
				glVertex2f(0.0, 0.0)
				glVertex2f(diskRadius * cos(angle), diskRadius * sin(angle))
				
			glEnd()
		
		glPopMatrix()
		
		pygame.display.flip()
		
		clock.tick(TICK_RATE)
		
		iTick += 1
		
# Need to fix overflow. 2 Lines/loop box. Preview on right?
def pickLevel():
	numOptions = 5

	clock = pygame.time.Clock()
	clock.tick()	

	diskRadius = DISK_RADIUS * 1.5

	dataFile = "unlockedLevels.txt"
	f = open(filepath(dataFile), "r")
	numLevels = int(f.readline().rstrip("\n"))
	if not RELEASE:
		numLevels = NUM_LEVELS + 1
	
	titleFont = pygame.font.Font(filepath(FONT_NAME), 100)
	titleSurf = titleFont.render("Select Level", True, (0, 0, 0)).convert_alpha()
	
	titleTexture = glGenTextures(1)
	
	glEnable(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D, titleTexture)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
	
	scaleTex = scaleToPOT(titleSurf)
	
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, scaleTex.get_width(), scaleTex.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(scaleTex, "RGBX", 1))
	
	
	textures = [int(t) for t in glGenTextures(numLevels + 1)]
	#textures = glGenTextures(numLevels + 1)
	normFont = pygame.font.Font(filepath(FONT_NAME), 54)
	
	surfList = []
	
	for i in range(numLevels):
		surf = normFont.render("Level " + str(i + 1), True, (0, 0, 0)).convert_alpha()
		surfList.append(surf)
	
		glBindTexture(GL_TEXTURE_2D, textures[i])
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)	
		
		scaleTex = scaleToPOT(surf)
		
		glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, scaleTex.get_width(), scaleTex.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(scaleTex, "RGBX", 1))
	
	surf = normFont.render("Back", True, (0, 0, 0)).convert_alpha()
	surfList.append(surf)
	
	glBindTexture(GL_TEXTURE_2D, textures[numLevels])
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)	
	
	scaleTex = scaleToPOT(surf)
	
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, scaleTex.get_width(), scaleTex.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(scaleTex, "RGBX", 1))
	glDisable(GL_TEXTURE_2D)
	
	titleXBorder = (SCREEN_RES[0] - titleSurf.get_width()) / 2
	titleYBorder = 28	
	
	ySpacing = 0
	yTitleSpace = 16
	xBorder = 140
	
	
	height = 0
	for surf in surfList:
		height += surf.get_height() + ySpacing
		
	iTick = 0
	iSelected = 0
	
	prevWorld = World(0)
	
	while 1:
		glClear(GL_COLOR_BUFFER_BIT)
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			if event.type == KEYDOWN:
				if event.dict["key"] == K_UP:
					SoundManager().playInterfaceBeep()			
					iSelected -= 1
					iSelected %= numLevels + 1
					if iSelected != numLevels:
						prevWorld = World(iSelected)
				elif event.dict["key"] == K_DOWN:
					SoundManager().playInterfaceBeep()		
					iSelected += 1
					iSelected %= numLevels + 1
					if iSelected != numLevels:
						prevWorld = World(iSelected)
				elif event.dict["key"] == K_RETURN:
					if iSelected == numLevels:
						glDeleteTextures(textures)
						return -1
					return iSelected
				elif event.dict["key"] == K_ESCAPE:
					glDeleteTextures(textures)
					return -1
				
		if iSelected != numLevels:
			widthRatio = float(pygame.display.get_surface().get_width()) / SCREEN_RES[0]
			heightRatio = float(pygame.display.get_surface().get_height()) / SCREEN_RES[1]
			
			glPushAttrib(GL_VIEWPORT_BIT)
			glViewport(int(widthRatio * SCREEN_RES[0] / 2), int(heightRatio * (SCREEN_RES[1] / 2 - 180)), int(widthRatio * 360), int(heightRatio * 270))
			prevWorld.update(bPreview = True)
			prevWorld.draw(bPreview = True)		
			glPopAttrib()
		
		drawBorder()
		
		glEnable(GL_TEXTURE_2D)
		glBindTexture(GL_TEXTURE_2D, titleTexture)
		glBegin(GL_QUADS)
		glTexCoord2f(0, 0)
		glVertex2f(titleXBorder, SCREEN_RES[1] - titleSurf.get_height() - titleYBorder)
		glTexCoord2f(0, 1)
		glVertex2f(titleXBorder, SCREEN_RES[1] - titleYBorder)
		glTexCoord2f(1, 1)
		glVertex2f(titleXBorder + titleSurf.get_width(), SCREEN_RES[1] - titleYBorder)
		glTexCoord2f(1, 0)
		glVertex2f(titleXBorder + titleSurf.get_width(), SCREEN_RES[1] - titleSurf.get_height() - titleYBorder)		
		glEnd()		
			
		glPushMatrix()
		
		glTranslatef(xBorder, - titleSurf.get_height() - titleYBorder - yTitleSpace, 0.0)
		
		if numLevels + 1 > numOptions:
			offset = min(numLevels + 1 - numOptions, max(iSelected - numOptions / 2, 0))
		else:
			offset = 0
		
		for i in range(offset, min(min(numLevels + 1, numOptions) + offset, max(numLevels + 1, numOptions))):
		
			glBindTexture(GL_TEXTURE_2D, textures[i])
			
			glBegin(GL_QUADS)
			glTexCoord2f(0, 0)
			glVertex2f(0, SCREEN_RES[1] - surfList[i].get_height())
			glTexCoord2f(0, 1)
			glVertex2f(0, SCREEN_RES[1])
			glTexCoord2f(1, 1)
			glVertex2f(surfList[i].get_width(), SCREEN_RES[1])
			glTexCoord2f(1, 0)
			glVertex2f(surfList[i].get_width(), SCREEN_RES[1] - surfList[i].get_height())	
			glEnd()
			
			if i == iSelected:
				glDisable(GL_TEXTURE_2D)
				glPushMatrix()

				glTranslatef(- xBorder / 3, SCREEN_RES[1] - surfList[i].get_height() / 2, 0.0)
				glRotatef(-iTick * 8, 0.0, 0.0, 1.0)
				
				for j in range(4):
					if j % 2:
						glColor4f(*DISK_COLOR_1)
					else:
						glColor4f(*DISK_COLOR_2)		
					
					glBegin(GL_TRIANGLE_STRIP)	
					for k in range(46):
						angle = (k + (j * 45)) * pi / 90 
								
						glVertex2f(0.0, 0.0)
						glVertex2f(diskRadius * cos(angle), diskRadius * sin(angle))
						
					glEnd()
					
				glEnable(GL_TEXTURE_2D)
		
				glPopMatrix()					
			
			glTranslatef(0.0, - surfList[i].get_height(), 0.0)
		
			
		glDisable(GL_TEXTURE_2D)
		
		glPopMatrix()
		
		pygame.display.flip()
		
		clock.tick(TICK_RATE)
		
		iTick += 1
		
def optionsMenu():
	clock = pygame.time.Clock()
	clock.tick()	
	
	diskRadius = DISK_RADIUS * 1.5 

	iSelected = 0
	
	numOptions = 2

	titleFont = pygame.font.Font(filepath(FONT_NAME), 100)
	titleSurf = titleFont.render("Options", True, (0, 0, 0)).convert_alpha()
	
	titleTexture = glGenTextures(1)
	
	glEnable(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D, titleTexture)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
	
	scaleTex = scaleToPOT(titleSurf)
	
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, scaleTex.get_width(), scaleTex.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(scaleTex, "RGBX", 1))
	
	
	#screenRes = (pygame.display.get_surface().get_width(), pygame.display.get_surface().get_height())
	#availableRes = pygame.display.list_modes()
	
	#availableRes.sort(reverse = True)	
	
	normFont = pygame.font.Font(filepath(FONT_NAME), 54)
	soundOnSurf = normFont.render("Sound: On", True, (0, 0, 0)).convert_alpha()
	musicOnSurf = normFont.render("Music: On", True, (0, 0, 0)).convert_alpha()
	backSurf = normFont.render("Back", True, (0, 0, 0)).convert_alpha()
	soundOffSurf = normFont.render("Sound: Off", True, (0, 0, 0)).convert_alpha()
	musicOffSurf = normFont.render("Music: Off", True, (0, 0, 0)).convert_alpha()
	
	glEnable(GL_TEXTURE_2D)
	soundOnTexture = glGenTextures(1)
	soundOffTexture = glGenTextures(1)
	musicOnTexture = glGenTextures(1)
	musicOffTexture = glGenTextures(1)
	backTexture = glGenTextures(1)
	
	glBindTexture(GL_TEXTURE_2D, soundOnTexture)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)	
		
	scaleTex = scaleToPOT(soundOnSurf)	
		
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, scaleTex.get_width(), scaleTex.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(scaleTex, "RGBX", 1))

	glBindTexture(GL_TEXTURE_2D, musicOnTexture)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)	
		
	scaleTex = scaleToPOT(musicOnSurf)
		
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, scaleTex.get_width(), scaleTex.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(scaleTex, "RGBX", 1))

	glBindTexture(GL_TEXTURE_2D, soundOffTexture)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)	
		
	scaleTex = scaleToPOT(soundOffSurf)
		
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, scaleTex.get_width(), scaleTex.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(scaleTex, "RGBX", 1))

	glBindTexture(GL_TEXTURE_2D, musicOffTexture)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)	
		
	scaleTex = scaleToPOT(musicOffSurf)
		
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, scaleTex.get_width(), scaleTex.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(scaleTex, "RGBX", 1))
	
	
	glBindTexture(GL_TEXTURE_2D, backTexture)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)	
		
	scaleTex = scaleToPOT(backSurf)
		
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, scaleTex.get_width(), scaleTex.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(scaleTex, "RGBX", 1))
	glDisable(GL_TEXTURE_2D)

	titleXBorder = (SCREEN_RES[0] - titleSurf.get_width()) / 2
	titleYBorder = 28		
	
	ySpacing = 0
	yTitleSpace = 16
	xBorder = 160	
	
	iTick = 0
	
	soundManager = SoundManager()

	while 1:
		glClear(GL_COLOR_BUFFER_BIT)
	
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			if event.type == KEYDOWN:
				if event.dict["key"] == K_UP:
					soundManager.playInterfaceBeep()	
					iSelected -= 1
					iSelected %= numOptions + 1
				elif event.dict["key"] == K_DOWN:
					soundManager.playInterfaceBeep()		
					iSelected += 1
					iSelected %= numOptions + 1					
				if event.dict["key"] in (K_LEFT, K_RIGHT):
					if iSelected == 0:
						soundManager.toggleSound()
						soundManager.playInterfaceBeep()	
					elif iSelected == 1:
						soundManager.toggleMusic()
						if not soundManager.isMusicOn():
							soundManager.stopMusic()
						else:
							soundManager.playMusic()
						soundManager.playInterfaceBeep()
				elif event.dict["key"] == K_RETURN:
					if iSelected == 0:
						soundManager.toggleSound()
					elif iSelected == 1:
						soundManager.toggleMusic()
						if not soundManager.isMusicOn():
							soundManager.stopMusic()
						else:
							soundManager.playMusic()						
					elif iSelected == numOptions:
						glDeleteTextures(soundOnTexture)
						glDeleteTextures(soundOffTexture)
						glDeleteTextures(musicOnTexture)
						glDeleteTextures(musicOffTexture)
						glDeleteTextures(backTexture)
						soundManager.saveOptions()
						return
						
				elif event.dict["key"] == K_ESCAPE:
					glDeleteTextures(soundOnTexture)
					glDeleteTextures(soundOffTexture)
					glDeleteTextures(musicOnTexture)
					glDeleteTextures(musicOffTexture)
					glDeleteTextures(backTexture)
					soundManager.saveOptions()
					return
					
		
		glEnable(GL_TEXTURE_2D)
		glBindTexture(GL_TEXTURE_2D, titleTexture)
		glBegin(GL_QUADS)
		glTexCoord2f(0, 0)
		glVertex2f(titleXBorder, SCREEN_RES[1] - titleSurf.get_height() - titleYBorder)
		glTexCoord2f(0, 1)
		glVertex2f(titleXBorder, SCREEN_RES[1] - titleYBorder)
		glTexCoord2f(1, 1)
		glVertex2f(titleXBorder + titleSurf.get_width(), SCREEN_RES[1] - titleYBorder)
		glTexCoord2f(1, 0)
		glVertex2f(titleXBorder + titleSurf.get_width(), SCREEN_RES[1] - titleSurf.get_height() - titleYBorder)		
		glEnd()
		
		glPushMatrix()
		glTranslatef(xBorder, - titleSurf.get_height() - titleYBorder - yTitleSpace, 0.0)
		
		if soundManager.isSoundOn():
			soundTexture = soundOnTexture
			soundSurf = soundOnSurf
		else:
			soundTexture = soundOffTexture
			soundSurf = soundOffSurf
			
		glBindTexture(GL_TEXTURE_2D, soundTexture)
		glBegin(GL_QUADS)
		glTexCoord2f(0, 0)
		glVertex2f(0, SCREEN_RES[1] - soundSurf.get_height())
		glTexCoord2f(0, 1)
		glVertex2f(0, SCREEN_RES[1])
		glTexCoord2f(1, 1)
		glVertex2f(soundSurf.get_width(), SCREEN_RES[1])
		glTexCoord2f(1, 0)
		glVertex2f(soundSurf.get_width(), SCREEN_RES[1] - soundSurf.get_height())		
		glEnd()		
		
		glTranslatef(0, - ySpacing - soundOnSurf.get_height(), 0.0)
		
		if soundManager.isMusicOn():
			musicTexture = musicOnTexture
			musicSurf = musicOnSurf
		else:
			musicTexture = musicOffTexture
			musicSurf = musicOffSurf		
		
		glBindTexture(GL_TEXTURE_2D, musicTexture)
		glBegin(GL_QUADS)
		glTexCoord2f(0, 0)
		glVertex2f(0, SCREEN_RES[1] - musicSurf.get_height())
		glTexCoord2f(0, 1)
		glVertex2f(0, SCREEN_RES[1])
		glTexCoord2f(1, 1)
		glVertex2f(musicSurf.get_width(), SCREEN_RES[1])
		glTexCoord2f(1, 0)
		glVertex2f(musicSurf.get_width(), SCREEN_RES[1] - musicSurf.get_height())		
		glEnd()		

		glTranslatef(0, - ySpacing - musicOnSurf.get_height(), 0.0)
		
		glBindTexture(GL_TEXTURE_2D, backTexture)
		glBegin(GL_QUADS)
		glTexCoord2f(0, 0)
		glVertex2f(0, SCREEN_RES[1] - backSurf.get_height())
		glTexCoord2f(0, 1)
		glVertex2f(0, SCREEN_RES[1])
		glTexCoord2f(1, 1)
		glVertex2f(backSurf.get_width(), SCREEN_RES[1])
		glTexCoord2f(1, 0)
		glVertex2f(backSurf.get_width(), SCREEN_RES[1] - backSurf.get_height())		
		glEnd()				
		
		glDisable(GL_TEXTURE_2D)
		glPopMatrix()
		
		glPushMatrix()

		if iSelected == 0:
			glTranslatef(2 * xBorder / 3, SCREEN_RES[1] - titleSurf.get_height() - titleYBorder - yTitleSpace - soundOnSurf.get_height() / 2, 0.0)
		elif iSelected == 1:
			glTranslatef(2 * xBorder / 3, SCREEN_RES[1] - titleSurf.get_height() - titleYBorder - ySpacing - yTitleSpace - soundOnSurf.get_height() - musicOnSurf.get_height() / 2, 0.0)
		elif iSelected == 2:
			glTranslatef(2 * xBorder / 3, SCREEN_RES[1] - titleSurf.get_height() - titleYBorder - 2 * ySpacing - yTitleSpace - soundOnSurf.get_height() - musicOnSurf.get_height() - backSurf.get_height() / 2, 0.0)

		glRotatef(-iTick * 8, 0.0, 0.0, 1.0)
		
		for j in range(4):
			if j % 2:
				glColor4f(*DISK_COLOR_1)
			else:
				glColor4f(*DISK_COLOR_2)		
			
			glBegin(GL_TRIANGLE_STRIP)	
			for k in range(46):
				angle = (k + (j * 45)) * pi / 90 
						
				glVertex2f(0.0, 0.0)
				glVertex2f(diskRadius * cos(angle), diskRadius * sin(angle))
				
			glEnd()
		
		glPopMatrix()				
		
		drawBorder()
		
	
		pygame.display.flip()
		
		clock.tick(TICK_RATE)
		
		iTick += 1		
		
def endScreen():
	glClear(GL_COLOR_BUFFER_BIT)
	
	SoundManager().playEndSound()
	
	titleFont = pygame.font.Font(filepath(FONT_NAME), 120)
	titleSurf = titleFont.render("The End", True, (0, 0, 0)).convert_alpha()
	
	titleTexture = glGenTextures(1)
	
	glEnable(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D, titleTexture)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
	
	scaleTex = scaleToPOT(titleSurf)
	
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, scaleTex.get_width(), scaleTex.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(scaleTex, "RGBX", 1))
	
	glBindTexture(GL_TEXTURE_2D, titleTexture)
	glBegin(GL_QUADS)
	glTexCoord2f(0, 0)
	glVertex2f((SCREEN_RES[0] - titleSurf.get_width()) / 2, (SCREEN_RES[1] - titleSurf.get_height()) / 2)
	glTexCoord2f(0, 1)
	glVertex2f((SCREEN_RES[0] - titleSurf.get_width()) / 2, (SCREEN_RES[1] + titleSurf.get_height()) / 2)
	glTexCoord2f(1, 1)
	glVertex2f((SCREEN_RES[0] + titleSurf.get_width()) / 2, (SCREEN_RES[1] + titleSurf.get_height()) / 2)
	glTexCoord2f(1, 0)
	glVertex2f((SCREEN_RES[0] + titleSurf.get_width()) / 2, (SCREEN_RES[1] - titleSurf.get_height()) / 2)		
	glEnd()	
	
	glDisable(GL_TEXTURE_2D)
	
	drawBorder()
	
	pygame.display.flip()
	
	clock = pygame.time.Clock()
	clock.tick()

	time = 0
	
	while 1:
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			elif event.type == KEYDOWN:
				return
				
		time += clock.tick()
		if time > 5000:
			return
			
def pauseScreen():
	glColor4f(1.0, 1.0, 1.0, 0.3)
	glBegin(GL_QUADS)
	glVertex2f(0, 0)
	glVertex2f(0, SCREEN_RES[1])
	glVertex2f(SCREEN_RES[0], SCREEN_RES[1])
	glVertex2f(SCREEN_RES[0], 0)
	glEnd()
	
	glColor4f(1.0, 1.0, 1.0, 1.0)

	titleFont = pygame.font.Font(filepath(FONT_NAME), 120)
	titleSurf = titleFont.render("Paused", True, (0, 0, 0)).convert_alpha()
	
	titleTexture = glGenTextures(1)
	
	glEnable(GL_TEXTURE_2D)
	glBindTexture(GL_TEXTURE_2D, titleTexture)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
	
	scaleTex = scaleToPOT(titleSurf)
	
	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, scaleTex.get_width(), scaleTex.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(scaleTex, "RGBX", 1))
	
	glBindTexture(GL_TEXTURE_2D, titleTexture)
	glBegin(GL_QUADS)
	glTexCoord2f(0, 0)
	glVertex2f((SCREEN_RES[0] - titleSurf.get_width()) / 2, (SCREEN_RES[1] - titleSurf.get_height()) / 2)
	glTexCoord2f(0, 1)
	glVertex2f((SCREEN_RES[0] - titleSurf.get_width()) / 2, (SCREEN_RES[1] + titleSurf.get_height()) / 2)
	glTexCoord2f(1, 1)
	glVertex2f((SCREEN_RES[0] + titleSurf.get_width()) / 2, (SCREEN_RES[1] + titleSurf.get_height()) / 2)
	glTexCoord2f(1, 0)
	glVertex2f((SCREEN_RES[0] + titleSurf.get_width()) / 2, (SCREEN_RES[1] - titleSurf.get_height()) / 2)		
	glEnd()	
	
	glDisable(GL_TEXTURE_2D)
		
	pygame.display.flip()
	
	while 1:
		for event in pygame.event.get():
			if event.type == QUIT:
				sys.exit(0)
			elif event.type == KEYDOWN:
				return
				
	