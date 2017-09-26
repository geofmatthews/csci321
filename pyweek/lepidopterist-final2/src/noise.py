import pygame
import data, settings

sounds = {}
songs = {}
songs["xylo"] = data.filepath("xylophone-symposium.ogg")
songs["gnos"] = data.filepath("gnossienne1.ogg")
songs["one"] = data.filepath("one-five-nine.ogg")
songs["girl"] = data.filepath("another-girl.ogg")

def init():
    if not settings.nosound:
        sounds["woosh"] = pygame.mixer.Sound(data.filepath("woosh.ogg"))
        sounds["woosh"].set_volume(0.5)
        sounds["rotor"] = pygame.mixer.Sound(data.filepath("rotor.ogg"))
        sounds["rotor"].set_volume(0.5)
        sounds["cha-ching"] = pygame.mixer.Sound(data.filepath("cha-ching.ogg"))
        sounds["cha-ching"].set_volume(0.5)
        sounds["win-1"] = pygame.mixer.Sound(data.filepath("win-1.ogg"))
        sounds["win-1"].set_volume(0.5)
        sounds["win-2"] = pygame.mixer.Sound(data.filepath("win-2.ogg"))
        sounds["win-2"].set_volume(0.5)
        sounds["win-3"] = pygame.mixer.Sound(data.filepath("win-3.ogg"))
        sounds["win-3"].set_volume(0.5)
        sounds["hop"] = pygame.mixer.Sound(data.filepath("hop.wav"))
        sounds["hop"].set_volume(0.5)
        sounds["pick"] = pygame.mixer.Sound(data.filepath("pick.wav"))
        sounds["pick"].set_volume(0.5)
        sounds["choose"] = pygame.mixer.Sound(data.filepath("choose.wav"))
        sounds["choose"].set_volume(0.5)
    if not settings.nomusic:
        pygame.mixer.music.set_volume(0.3)

def play(name):
    if name in sounds:
        if settings.nosound: return
        sounds[name].play()
    elif name in songs:
        if settings.nomusic: return
        pygame.mixer.music.load(songs[name])
        pygame.mixer.music.play()

def stop():
    if settings.nomusic: return
    pygame.mixer.music.stop()


