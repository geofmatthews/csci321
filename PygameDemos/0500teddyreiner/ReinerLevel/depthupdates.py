import pygame

class DepthUpdates(pygame.sprite.RenderUpdates):
    """A sprite group that renders sprites in y-coordinate order.
       Useful for isometric and other pseudo-3d games where things
       can walk behind and in front of others."""

    def sprites(self):
        spr = pygame.sprite.RenderUpdates.sprites(self)
        spr.sort(key=lambda s:s.rect.bottom)
        return spr
