import os, pygame,random
import Numeric as N

def heading2angle(heading):
    return {'e':0, 'ne':N.pi*0.25,
            'n':N.pi*0.5, 'nw':N.pi*0.75,
            'w':N.pi, 'sw':N.pi*1.25,
            's':N.pi*1.5, 'se':N.pi*1.75}[heading]

def angle2heading(angle):
    if angle > 0:
        angle %= N.pi
    else:
        angle %= -N.pi
    hindex = round(4.0*angle/N.pi)
    return {0:'e',1:'ne',2:'n',3:'nw',4:'w',
            -1:'se',-2:'s',-3:'sw',-4:'w'}[hindex]

class Actor(pygame.sprite.Sprite):
    """
    Settable:  position (vector)
               velocity (vector, heading taken from velocity)
               angle (PROPERTY, angle of velocity vector)
               speed (PROPERTY, length of velocity vector)
               state (PROPERTY, animation filename from Reiner's files)
    """
    def __init__(self, pos, animations):
        pygame.sprite.Sprite.__init__(self)
        self.position = N.array(pos)
        self.velocity = N.array((0.0,0.0))
        
        self.animations = animations
        self._heading = 's'
        self._index = 0
        self.state = self.animations.keys()[0]
        self.image_speed = 1
        self.image = self.animations[self._state][self._heading][self._index]
        self.rect = self.image.get_rect()

    def getSpeed(self):
        v = self.velocity
        return N.sqrt(N.dot(v, v))
    def setSpeed(self, speed):
        if self.speed > 0:
            self.velocity *= speed/self.speed
        else:
            self.velocity[0] = speed
            self.angle = heading2angle(self._heading)
    speed = property(getSpeed, setSpeed)

    def getAngle(self):
        if self.speed > 0:
            return N.arctan2(-self.velocity[1], self.velocity[0])
        else:
            return heading2angle(self._heading)
    def setAngle(self, angle):
        s = self.speed
        self.velocity = s * N.array((N.cos(angle), -N.sin(angle)))
        self._heading = angle2heading(angle)            
    angle = property(getAngle, setAngle)

    def setState(self, state):
        self._state = state
        self.nframes = len(self.animations[self._state][self._heading])
        self._index %= self.nframes
        self.image = self.animations[self._state][self._heading][self._index]
        self.rect = self.image.get_rect()
    def getState(self):
        return self._state
    state = property(getState, setState)

    def update(self):
        self.position += self.velocity

        if self.speed > 0:
            ## get heading from angle of velocity
            angle = N.arctan2(-self.velocity[1], self.velocity[0])
            hindex = round(4.0*angle/N.pi)
            self._heading = {0:'e',1:'ne',2:'n',3:'nw',4:'w',
                             -1:'se',-2:'s',-3:'sw',-4:'w'}[hindex]

        anim = self.animations[self._state][self._heading]
        self._index += self.image_speed
        self._index %= self.nframes
        self.image = anim[self._index]
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def randomState(self):
        states = self.animations.keys()
        s = 'name'
        while s == 'name':
            s = random.choice(states)
        self.state = s
        if self.velocity[0] == self.velocity[1] == 0.0:
            self.angle = random.uniform(0.0, N.pi*2)
            self.speed = 1
        else:
            self.speed = 0

        
        
    
