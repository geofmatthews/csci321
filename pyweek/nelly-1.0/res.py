#!/usr/bin/python
# $Id: res.py,v 1.5 2006/04/22 08:46:36 alex Exp $

import pygame
from pygame.locals import *
import os.path

from OpenGL.GL import *

def pow2(x):
    y = 1
    while y < x:
        y <<= 1
    return y

class Texture:
    def __init__(self, tex, width, height, u, v):
        self.tex = tex
        self.width = width
        self.height = height
        self.u = u
        self.v = v

class Resources:
    def __init__(self):
        self.textures = {}      # filename -> (id, width, height, u, v)
        # u, v are the max texture coords for the image

    def getTexture(self, filename):
        if filename in self.textures:
            return self.textures[filename]
        else:
            img = pygame.image.load(filename)
            width = img.get_width()
            height = img.get_height()
            texwidth = pow2(width)
            texheight = pow2(height)
            if texwidth != width or texheight != height:
                data = chr(0) * texwidth* texheight*4
                surf = pygame.image.fromstring(data, 
                                               (texwidth, texheight), 'RGBA')
                surf.blit(img, (0,texheight-height))
                img = surf
            u, v = width / float(texwidth), height/float(texheight)
            tex = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, tex)
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, 4, texwidth, texheight,
                         0, GL_RGBA, GL_UNSIGNED_BYTE, 
                         pygame.image.tostring(img, 'RGBA', True))
            texture = Texture(tex, width, height, u, v)
            self.textures[filename] = texture
            return texture

res = Resources()

def getTexture(filename):
    return res.getTexture(os.path.join('textures', filename))
