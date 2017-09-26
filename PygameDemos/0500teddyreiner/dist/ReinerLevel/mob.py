import pygame

class Mob(pygame.sprite.Sprite):
    def __init__(self, pos, screen):
        pygame.sprite.Sprite.__init__(self)
        self.pos = vector(pos)
        self.screen = screen
        self.heading = vector(0,1)
        self.speed = 0.0
        self.aspeed = 1

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):

        # move:
        self.pos += self.speed * self.heading

        # wrap screen:
        screen_size = self.screen.get_size()
        if self.rect.centerx < 0: self.rect.centerx = screen_size[0]
        elif self.rect.centerx > screen_size[0]: self.rect.centerx = 0
        elif self.rect.centery < 0: self.rect.centery = screen_size[1]
        elif self.rect.centery > screen_size[1]: self.rect.centery = 0

        
        
        
