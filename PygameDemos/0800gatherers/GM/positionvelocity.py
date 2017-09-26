
import Numeric as N

class PositionVelocity(object):
    """
    """
    def __init__(self, pos=(0.0,0.0), vel = (0.0,0.0)):
        self.position = N.array(pos)
        self.velocity = N.array(vel)

    def tick(self, deltaT=0.1):
        self.position += deltaT*self.velocity

if __name__ == "__main__":
    p = PositionVelocity()
    p.position[0] += 3.0
    p.position[1] += 1.0
    p.velocity[0] = 1.0
    p.velocity[1] = 3.0
    for i in range(10):
        print p.position, p.velocity
        p.tick()
    

        
