import pygame
from data import filepath

import random

class SoundManager:
	__shared_state = {}
	def __init__(self):
		self.__dict__ = self.__shared_state
		
		try:
			self.bInit
		except:
			self.bInit = True
			if pygame.mixer.get_init():
				self.mixerAvailable = True		
				
				pygame.mixer.music.load(filepath("tradeyourkid.ogg"))
				pygame.mixer.music.set_volume(0.5)		
				
				try:
					f = open(filepath("sound.cfg"), "r")
					self.bSound = int(f.readline().rstrip("\n"))
					self.bMusic = int(f.readline().rstrip("\n"))
					f.close()
				except IOError:
					self.bSound = 1
					self.bMusic = 1
				
				self.beepSound = pygame.mixer.Sound(filepath("Electron-wwwbeat-1897.wav"))
				self.levelEndSound = pygame.mixer.Sound(filepath("Arcade_S-wwwbeat-1889.wav"))
				self.levelEndSound.set_volume(0.4)
				self.blackHoleSound = pygame.mixer.Sound(filepath("delay_me-dog-298.wav"))
				self.whiteHoleSound = pygame.mixer.Sound(filepath("pop-SodaBush-1015.wav"))
				self.endSound = pygame.mixer.Sound(filepath("Applause-J_Fairba-1717.wav"))
				
				self.thudSounds = [pygame.mixer.Sound(filepath("thud.ogg")),
								   pygame.mixer.Sound(filepath("thud2.ogg")),
							       pygame.mixer.Sound(filepath("thud3.ogg"))]				
				
			else:
				self.mixerAvailable = False
								
	def isMusicOn(self):
		if self.mixerAvailable:
			return self.bMusic
		return False
		
	def isSoundOn(self):
		if self.mixerAvailable:
			return self.bSound
		return False
		
	def toggleMusic(self):
		if self.mixerAvailable:
			self.bMusic = not self.bMusic
		
	def toggleSound(self):
		if self.mixerAvailable:
			self.bSound = not self.bSound
		
	def playInterfaceBeep(self):
		if self.isSoundOn():
			self.beepSound.play()
			
	def playLevelEnd(self):
		if self.isSoundOn():
			self.levelEndSound.play()	
			
	def playThudSound(self, volume):
		if self.isSoundOn():
			sound = random.choice(self.thudSounds)
			sound.set_volume(volume)
			sound.play()
			
	def playBlackHoleSound(self):
		if self.isSoundOn():
			self.blackHoleSound.play()
			
	def playWhiteHoleSound(self):	
		if self.isSoundOn():
			self.blackHoleSound.stop()
			self.whiteHoleSound.play()
			
	def playEndSound(self):
		if self.isSoundOn():
			self.endSound.play()
			
	def playMusic(self):
		if self.mixerAvailable:
			pygame.mixer.music.play(-1)
		
	def stopMusic(self):
		if self.mixerAvailable:
			pygame.mixer.music.stop()
			
	def saveOptions(self):
		if self.mixerAvailable:
			f = open(filepath("sound.cfg"), "w")
			f.write(str(int(self.bSound)) + "\n")
			f.write(str(int(self.bMusic)) + "\n")
			f.close()		