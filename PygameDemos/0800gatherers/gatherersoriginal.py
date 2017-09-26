
import pygame,random,sys
from pygame.locals import *
from GM import utilities
from GM.statemachine import StateMachine, State
from GM.vector import *
import GM.makeimage

PERCEPTION_DISTANCE = 64
GOAL_RADIUS = 64
GATHERER_SPEED = 5
ENEMY_SPEED = 4
ENEMY_HEALTH = 100

def closest(actor, things):
    closest,closestdist = None,sys.maxint
    for thing in things:
        dist = distance(thing.pos, actor.pos)
        if dist < closestdist:
            closest,closestdist = thing, dist
    return closest,closestdist

class World():
    def __init__(self, screen):
        self.screen = screen
        self.center = screen.get_width()/2.0, screen.get_height()/2.0
        self.gatherers = pygame.sprite.Group()
        self.goodies = pygame.sprite.Group()
        self.collected = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.deadenemies = pygame.sprite.Group()
        self.allsprites = pygame.sprite.Group()

    def update(self):
        self.allsprites.update()

    def draw(self):
        self.allsprites.draw(self.screen)

    def addGatherer(self, pos):
        Gatherer(pos,self,self.gatherers,self.allsprites)

    def addGoody(self, pos):
        Goody(pos,self,self.goodies,self.allsprites)

    def collectGoody(self, goody):
        self.goodies.remove(goody)
        self.collected.add(goody)

    def uncollectGoody(self, goody):
        self.collected.remove(goody)
        self.goodies.add(goody)

    def addEnemy(self, pos):
        Enemy(pos,self,self.enemies,self.allsprites)

    def killEnemy(self, enemy):
        self.enemies.remove(enemy)
        self.deadenemies.add(enemy)
        enemy.speed = 0

    def randomPosition(self):
        x = random.randint(0,self.screen.get_width()-1)
        y = random.randint(0,self.screen.get_height()-1)
        return vector(x,y)

    def outside(self, actor):
        rect = actor.rect
        left = rect.right < 0
        right = rect.left > self.screen.get_width()
        up = rect.bottom < 0
        down = rect.top > self.screen.get_height()
        return left or right or up or down

############# Goodies  ###################

class Goody(pygame.sprite.Sprite):
    def __init__(self, pos, world, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.image = GM.makeimage.star(24, (255,0,0))
        self.rect = self.image.get_rect()
        self.pos = vector(pos)
        self.rect.center = self.pos
        self.world = world

    def update(self):
        self.rect.center = self.pos

############### Enemy class #################

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, world, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.images = GM.makeimage.rotating_arrow(32, (0,0,0))
        self.frame = 0
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect()
        self.pos = vector(pos)
        self.rect.center = self.pos
        self.world = world

        self.heading = randomNormalVector()
        self.speed = ENEMY_SPEED
        self.stateMachine = StateMachine(Sneak(self))

        self.health = ENEMY_HEALTH
        
    def update(self):
        self.stateMachine.update()
        self.pos += self.speed*self.heading
        self.rect.center = self.pos
        angle = N.arctan2(self.heading[1],self.heading[0])*180.0/N.pi
        self.frame = int((angle % 360)/10.0)
        self.image = self.images[self.frame]

#### States for our Enemy
        
class EnemyState(State):
    pass

class Sneak(EnemyState):
    def enter(self):
        actor = self.actor
        targets = actor.world.goodies.sprites()
        targets.extend(actor.world.collected.sprites())
        if targets:
            self.actor.goody = targets[random.randint(0,len(targets)-1)]
        else:
            actor.kill()
            return
            
    def update(self):
        actor, goody = self.actor, self.actor.goody
        if actor.world.outside(actor) or not goody:
            actor.kill()
            return
        actor.heading = norm(goody.pos-actor.pos)
        # Check for change state:
        if actor.health <= 0:
            actor.stateMachine.ChangeState(Dead(actor))
        if actor.rect.colliderect(goody) and goody.alive():
            actor.goody = goody
            actor.stateMachine.ChangeState(Steal(actor))
        if actor.health < 0.25*ENEMY_HEALTH:
            actor.stateMachine.ChangeState(RunAway(actor))

class Steal(EnemyState):

    def enter(self):
        actor, goody = self.actor, self.actor.goody
        actor.world.uncollectGoody(actor.goody)
        actor.heading = randomNormalVector()
        goody.pos = actor.pos
        
    def update(self):
        actor, goody = self.actor, self.actor.goody
        if actor.world.outside(actor):
            actor.kill()
            goody.pos = actor.world.randomPosition()
            return
        if actor.health <= 0:
            actor.world.killEnemy(actor)
            goody.pos = vector(goody.pos)
            return
        if actor.health < 0.5*ENEMY_HEALTH:
            actor.stateMachine.ChangeState(RunAway(actor))
            goody.pos = vector(goody.pos)
            return
        
class RunAway(EnemyState):
    def enter(self):
        self.actor.speed *= 1.5
    def update(self):
        actor = self.actor
        if actor.world.outside(actor):
            actor.kill()
            return
        if actor.health <= 0:
            actor.world.killEnemy(actor)
            return

        
############# Gatherer class ####################

class Gatherer(pygame.sprite.Sprite):
    def __init__(self, pos, world, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.images = GM.makeimage.rotating_arrow(16, (0,0,255))
        self.frame = 0
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect()
        self.pos = vector(pos)
        self.rect.center = self.pos
        self.world = world

        self.heading = randomNormalVector()
        self.speed = GATHERER_SPEED
        self.stateMachine = StateMachine(Search(self))

        self.goody = None
        
    def update(self):
        self.stateMachine.update()
        width, height = self.world.screen.get_size()
        angle = N.arctan2(self.heading[1],self.heading[0])*180.0/N.pi
        self.frame = int((angle % 360)/10.0)
        self.image = self.images[self.frame]
        self.pos += self.heading*self.speed
        if self.pos[0] < 0:
            self.pos[0] = 0
            self.heading[0] = -self.heading[0]
        if self.pos[0] > width:
            self.pos[0] = width
            self.heading[0] = -self.heading[0]
        if self.pos[1] < 0:
            self.pos[1] = 0
            self.heading[1] = - self.heading[1]
        if self.pos[1] > height:
            self.pos[1] = height
            self.heading[1] = - self.heading[1]

        self.rect.center = self.pos

######## States for the Gatherer:

class GathererState(State):
    pass

class Search(GathererState):

    def update(self):
        actor = self.actor       
        if random.uniform(0.0,1.0) < 0.1:
            actor.heading = randomNormalVector()
        ## Check for state changes
        # First, look for enemies
        close, dist = closest(actor, actor.world.enemies)
        if dist < PERCEPTION_DISTANCE:
            actor.enemy = close
            actor.stateMachine.ChangeState(Attack(actor))
            return
        # Second, look for goodies
        close, dist = closest(actor, actor.world.goodies)
        if dist < PERCEPTION_DISTANCE:
            actor.goody = close
            actor.stateMachine.ChangeState(GetGoody(actor))

class Attack(GathererState):

    def update(self):
        actor,enemy = self.actor,self.actor.enemy
        actor.heading = norm(enemy.pos - actor.pos)
        if actor.rect.colliderect(enemy.rect):
            if random.uniform(0.0,1.0) < 0.5:
                enemy.health -= 1
        if enemy.health < 0 or actor.world.outside(enemy):
            actor.stateMachine.ChangeState(Search(actor))

class GetGoody(GathererState):
        
    def update(self):
        actor,goody = self.actor, self.actor.goody
        actor.heading = norm(goody.pos-actor.pos)
        # Check for state changes
        if actor.rect.colliderect(goody.rect) and goody.alive():
            actor.stateMachine.ChangeState(DeliverGoody(actor))

class DeliverGoody(GathererState):

    def enter(self):
        actor, goody = self.actor, self.actor.goody
        goody.pos = actor.pos
        actor.heading = norm(actor.world.center - actor.pos)
        actor.world.collectGoody(goody)
        
    def update(self):
        actor,goody = self.actor, self.actor.goody
        # Check for state changes
        if distance(actor.pos, actor.world.center) < GOAL_RADIUS:
            if random.uniform(0.0,1.0) < 0.25:
                actor.stateMachine.ChangeState(Search(actor))

    def exit(self):
        actor, goody = self.actor, self.actor.goody
        goody.pos = vector(actor.pos)
        actor.goody = None

            
################  Main ###################    

def main():
    pygame.init()
    world = World(pygame.display.set_mode((640,480)))
    pygame.display.set_caption('Gatherers')

    background = pygame.Surface(world.screen.get_size())
    background = background.convert()
    background.fill((200,255,200))

    world.screen.blit(background, (0,0))
    pygame.display.flip()

    clock = pygame.time.Clock()

    gatherers = pygame.sprite.Group()

    for i in range(20):
        x = random.randint(0,world.screen.get_width())
        y = random.randint(0,world.screen.get_height())
        world.addGoody((x,y))

    while 1:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == MOUSEBUTTONDOWN:
                m = pygame.mouse.get_pressed()
                if m[0]:
                    world.addGatherer(pygame.mouse.get_pos())
                if m[2]:
                    world.addEnemy(pygame.mouse.get_pos())

        world.update()
        world.screen.blit(background, (0,0))
        world.draw()
        pygame.display.flip()

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
        

