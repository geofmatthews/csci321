import pygame, os, cPickle
from pygame.locals import *
import data, vista, context, settings, play, graphics, noise


pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=(4096 if settings.audiobuffer else 0))
pygame.init()

def main():
    vista.init()
    pygame.display.set_caption("Obb is loading.... Please wait")
    savefile = data.filepath("savegame.pkl")
    noise.nexttrack()
    if settings.restart:
        context.push(play.Play())
    else:
        try:
            context.push(cPickle.load(open(savefile, "rb")))
        except:
            context.push(play.Play())
    clock = pygame.time.Clock()
    savetime = settings.savetimer
    while context.top():
        dt = min(clock.tick(settings.maxfps) * 0.001, 1./settings.minfps)
        if settings.fast:
            dt *= 2
        con = context.top()
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        mousepos = pygame.mouse.get_pos()
        buttons = pygame.mouse.get_pressed()

        if settings.autosave:
            savetime -= dt
            if savetime < 0:
                cPickle.dump(con, open(savefile, "wb"))
                savetime = settings.savetimer

        for event in events:
            if event.type == QUIT:
                if settings.saveonquit:
                    cPickle.dump(con, open(savefile, "wb"))
                return
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                if settings.saveonquit:
                    cPickle.dump(con, open(savefile, "wb"))
                return
            if event.type == KEYDOWN and event.key == K_F12:
                vista.screencap()
            if event.type == KEYDOWN and event.key == K_F9:  # Manual save
                cPickle.dump(con, open(savefile, "wb"))

        con.think(dt, events, keys, mousepos, buttons)
        con.draw()
        if settings.showfps:
            pygame.display.set_caption("Obb - %.1ffps" % clock.get_fps())
            if settings.fullscreen:
                print clock.get_fps()
        else:
            pygame.display.set_caption("Obb")
        
        

    
