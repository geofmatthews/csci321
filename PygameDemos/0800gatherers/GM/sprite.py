import os
import pygame
import utilities

class DepthGroup(pygame.sprite.OrderedUpdates):
    """Sprites are repeatedly sorted by sprite.rect.centery,
       smallest first, so that we can use
       them in an isometric game and "farther" sprites
       will be rendered before "nearer" ones."""

    def __init__(self, *sprites):
        pygame.sprite.OrderedUpdates.__init__(self, *sprites)

    def sprites(self):
        return sorted(self._spritelist, key=lambda s: s.rect.centery)

class Group(pygame.sprite.Group):
    def draw(self, surface):
        pygame.sprite.Group.draw(self, surface)
        for s in self.sprites():
            s.draw(surface)
            
class Sprite(pygame.sprite.Sprite):
    def draw(self, surface):
        pass
    
class ReinerSprite(pygame.sprite.Sprite):
    def __init__(self, spec, name, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.actions = {}
        self.loadAllActions(spec[name])

    def loadAllActions(self, spec):
        for action in spec.keys():
            actiondict = spec[action]
            self.loadAction(action,
                            actiondict['fileroot'],
                            actiondict['headings'],
                            actiondict['frames'],
                            actiondict['suffix'])

    def loadAction(self,action,fileroot,headings,frames,suffix):
        self.actions[action] = {}
        for h in headings:
            self.actions[action][h] = []
            for f in frames:
                filename = fileroot + action + h + f + '.' + suffix
                self.actions[action][h].append(utilities.load_image(filename))

                
            
        
            
