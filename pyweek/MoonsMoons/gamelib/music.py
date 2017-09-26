import pygame.mixer
from data import *

FADE = 500

class JukeBox:
    def __init__(self): 
        pygame.mixer.init()
        self.sounds = {}
        self.songs = {}
        for x in range(4): 
            self.songs[str(x+1)] = load_music('song'+str(x+1)+'.ogg')
        self.playing = False
        self.muted = False
        self.played = None

    def play_song(self, id = '1'):
        self.fadeout()
        if not self.muted:
            self.played = self.songs[id]
            self.played.play(-1, 0, FADE)
            self.playing = True
        
    def fadeout(self):
        if self.playing:
            self.played.fadeout(FADE)
        self.playing = False

    def fadein(self, id = None):
        if id is None:
            if not self.muted:
                self.played.play(-1, 0, FADE)
        else:
            self.played = self.songs[id]
            if not self.muted:
                self.played.play(-1)
        self.playing = True
        
    def toggle(self):
        if self.playing:
            self.muted = True
            self.fadeout()
        else:
            self.muted = False
            self.fadein()