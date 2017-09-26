'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "gamelib"
package.
'''
import pygame, os, data
import game, music

def main():
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    jukebox = music.JukeBox()
    level = 'menu.txt'
    was_menu = True
    fullname = os.path.join('data', 'save', 'save.txt')
    first_time = False
    try:
        f = open(fullname, 'r')
    except:
        first_time = True
        f = open(fullname, 'w')
        f.close()
    while level:
        if level == 'menu.txt':
            was_menu = True
        else:
            was_menu = False
            first_time = data.first_time(level)
        level = game.start(jukebox, level, first_time)
        first_time = False
        if level == None and not was_menu:
            level = 'menu.txt'
    pygame.quit()
