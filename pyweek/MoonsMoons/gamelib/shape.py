from collision import *

class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.vector = start[0] - end[0], start[1] - end[1]
        self.width = abs(start[0] - end[0])
        self.height = abs(start[1] - end[1])
        x = start[0]
        if end[0] < x:
            x = end[0]
        y = start[1]
        if end[1] < y:
            y = end[1]
        self.topleft = x,y
        x += self.width/2
        y += self.height/2
        self.center = x,y

    def move(self, speed):
        self.center[0] += speed[0]
        self.center[1] += speed[1]
        self.topleft[0] += speed[0]
        self.topleft[1] += speed[1]
    
    def set_center(self, x, y):
        self.center = [x,y]
        self.topleft = [x-self.width/2, y-self.height/2]
    
    def set_topleft(self, x, y):
        self.topleft = [x,y]
        self.center = [x+self.width/2, y+self.height/2]
        
    def collide_circle(self, circle, border = 0):
        return collide_circle_line(circle.center, circle.radius, self.start, self.end, border)
        
class Circle:
    def __init__(self, x, y, radius):
        self.center = [x,y]
        self.topleft = [x-radius, y-radius]
        self.radius = radius
        
    def collide_point(self, point):
        return collide_circle_point(self.center, self.radius, point)
        
    def collide_circle(self, circle):
        return collide_circle_circle(self.center, self.radius, circle.center, circle.radius)
        
    def collide_circle_extended(self, circle):
        return collide_circle_circle_extended(self.center, self.radius, circle.center, circle.radius)
    
    def collide_line(self, line, border = 0):
        return collide_circle_line(self.center, self.radius, line.start, line.end, border)

    def collide_line_extended(self, line, border = 0):
        return collide_circle_line_extended(self.center, self.radius, line.start, line.end, border)
        
    def move(self, speed):
        self.center[0] += speed[0]
        self.center[1] += speed[1]
        self.topleft[0] += speed[0]
        self.topleft[1] += speed[1]
    
    def set_center(self, x, y):
        self.center = [x,y]
        self.topleft = [x-self.radius, y-self.radius]
    
    def set_topleft(self, x, y):
        self.topleft = [x,y]
        self.center = [x+self.radius, y+self.radius]