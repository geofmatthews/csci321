import pygame, math, random
import data
from function import *
from constants import *
from shape import Circle, Line
class Platform:
    def __init__(self, start, end, image_dict, colour):
        self.set_self(start, end, image_dict, colour)

    def set_self(self, start, end, image_dict, colour):
        self.line = Line(start, end)
        self.colour = colour
        line_length = int(round(pythagory(self.line.vector[0], self.line.vector[1])))
        w = line_length + 2*PLATFORM.BORDER + 2*PLATFORM.SIDE_GAP
        h = PLATFORM.IMAGE_HEIGHT
        base_image = pygame.Surface([w, h])
        base_image = base_image.convert_alpha()
        base_image.fill((1,1,1,0))
        base_image.blit(image_dict['platform' + colour + '-left'], (0,0))
        side_w = image_dict['platform' + colour + '-left'].get_width()
        for x in range(line_length/PLATFORM.MIDDLE_WIDTH):
            base_image.blit(image_dict['platform' + colour + '-middle'], (side_w+x*PLATFORM.MIDDLE_WIDTH,0))
        #if line_length%PLATFORM.MIDDLE_WIDTH != 0:
        base_image.blit(image_dict['platform' + colour + '-middle'], (side_w+(line_length/PLATFORM.MIDDLE_WIDTH)*PLATFORM.MIDDLE_WIDTH,0), pygame.Rect(0,0, line_length%PLATFORM.MIDDLE_WIDTH, PLATFORM.IMAGE_HEIGHT))
        base_image.blit(image_dict['platform' + colour + '-right'], (w-side_w,0))
        
        self.image = pygame.transform.rotozoom(base_image, -vector_to_angle(self.line.vector)-90, 1.0)
        self.image_position = start[0] - self.line.vector[0]/2 - self.image.get_width()/2, start[1] - self.line.vector[1]/2 - self.image.get_height()/2

class RelativePlatform(Platform):
    def __init__(self, planet, planet_angle, distance, width, angle, image_dict):
        center = sum(planet.circle.center, multiply(angle_to_vector(planet_angle), planet.circle.radius + PLATFORM.BORDER + distance))
        platform_vector = angle_to_vector(planet_angle+90+angle)
        start = sum(center, multiply(platform_vector, -width/2))
        start = int(round(start[0])), int(round(start[1]))
        end = sum(center, multiply(platform_vector, width/2))
        end = int(round(end[0])), int(round(end[1]))
        self.set_self(start, end, image_dict, planet.colour)
        
class Planet:
    def __init__(self, x, y, radius, mass, gravity_radius, colour):
        self.circle = Circle(x, y, radius)
        self.colour = colour
        self.mass = mass
        self.gravity_radius = gravity_radius
        count = int(math.ceil(radius/100.0)*100)
        self.image = data.load_image(str(count)+'x'+colour+'.png', True, 'planet')
        if radius % 100:
            c = float(radius) / count
            self.image = pygame.transform.smoothscale(self.image, (int(self.image.get_width()*c), int(self.image.get_height()*c)))
        self.image_position = x - self.image.get_width()/2, y - self.image.get_height()/2

class StableObject:
    def __init__(self, image_position, image):
        self.image = image
        self.image_position = image_position
        
class RelativeStableObject(StableObject):
    def __init__(self, type, image, obj, position_or_angle, altitude=0):
        h = image.get_height()
        if type == 'a': # count start_position
            center = sum(obj.circle.center, multiply(angle_to_vector(position_or_angle), obj.circle.radius + h/2 + altitude))
            angle = position_or_angle
        else:
            vector = inverse(perpendicular(normalise(obj.line.vector)))
            shift = multiply(obj.line.vector, -position_or_angle/100.0) # side shift
            center = sum(sum(obj.line.start, multiply(vector, PLATFORM.BORDER + h/2 + altitude)), shift)
            angle = vector_to_angle(vector)
        image = pygame.transform.rotozoom(image, -angle,1.)
        image_position = subtract(center, (image.get_width()/2, image.get_height()/2))
        StableObject.__init__(self, (int(round(image_position[0])), int(round(image_position[1]))), image)

        
class Checkpoint:
    def __init__(self, x, y, image_dict, radius = FLAG.RADIUS):
        self.circle = Circle(x,y,radius)
        self.image_dict = image_dict
        self.image_list = []
        self.image_position = (x - radius, y - radius)
        self.state = 'uncapped'
        self.timer = 0
        for i in range(len(image_dict['flag'])):
            self.image_list.append(image_dict['flag'][i].copy())
        self.image = self.image_list[0]
    
    def cap(self):
        if self.state != 'capped':
            self.state = 'capping'
        
    def uncap(self):
        if self.state != 'uncapped':
            self.state = 'uncapping'
    
    def update_angle(self, planets):
        closest_planet = None
        maximum = 0
        for p in planets:
            acc = [0,0]
            gx, gy = gravity_circle_circle(self.circle, p.circle, p.mass, p.gravity_radius)
            acc[0] += gx
            acc[1] += gy
            x,y = subtract(self.circle.center, p.circle.center)
            priority = pythagory(gx, gy) / pythagory(x,y) 
            if priority > maximum:
                maximum = priority
                closest_planet = p
        angle = 0
        if closest_planet:
            angle = vector_to_angle(gravity_circle_circle(closest_planet.circle, self.circle))
        for i in range(len(self.image_list)):
            self.image_list[i] = pygame.transform.rotozoom(self.image_dict['flag'][i], -angle, 1.0)
        self.image = self.image_list[0]
        self.image_position = self.circle.center[0] - self.image.get_width()/2, self.circle.center[1] - self.image.get_height()/2
        
    def update(self, delta):
        if self.state == 'capped':
            self.image = self.image_list[-1]
        elif self.state == 'uncapped':
            self.image = self.image_list[0]
        elif self.state == 'capping':
            self.timer += delta
            if self.timer > FLAG.CHANGE_TIME:
                self.timer = FLAG.CHANGE_TIME
                self.state = 'capped'
            frame = self.timer * FLAG.FRAMES / FLAG.CHANGE_TIME
            self.image = self.image_list[frame]
        elif self.state == 'uncapping':
            self.timer -= delta
            if self.timer < 0:
                self.timer = 0
                self.state = 'uncapped'
            frame = self.timer * FLAG.FRAMES / FLAG.CHANGE_TIME
            self.image = self.image_list[frame]

class RelativeCheckpoint(Checkpoint):
    def __init__(self, type, image_dict, obj, position_or_angle, altitude=-1):
        if type == 'a': # count start_position
            center = sum(obj.circle.center, multiply(angle_to_vector(position_or_angle), obj.circle.radius + FLAG.RADIUS + altitude))
            angle = position_or_angle
        else:
            vector = inverse(perpendicular(normalise(obj.line.vector)))
            shift = multiply(obj.line.vector, -position_or_angle/100.0) # side shift
            center = sum(sum(obj.line.start, multiply(vector, PLATFORM.BORDER + FLAG.RADIUS + altitude)), shift)
            angle = vector_to_angle(vector)
        Checkpoint.__init__(self, int(center[0]), int(center[1]), image_dict)
            
class Booster:
    def __init__(self, img_dict, type, obj, position_or_angle, force, radius = 30):
        if type == 'a': # count start_position
            start = sum(obj.circle.center, multiply(angle_to_vector(position_or_angle), obj.circle.radius + radius))
            angle = position_or_angle
            vector = angle_to_vector(angle)
        else:
            vector = inverse(perpendicular(normalise(obj.line.vector)))
            shift = multiply(obj.line.vector, -position_or_angle/100.0) # side shift
            start = sum(sum(obj.line.start, multiply(vector, PLATFORM.BORDER + radius + 3)), shift)
            angle = vector_to_angle(vector)
        self.circle = Circle(int(round(start[0])), int(round(start[1])), radius)
        self.force = force
        self.force_vector = multiply(vector, force)
        self.img_list = []
        for i in img_dict['geyser'][obj.colour]:
            self.img_list.append(pygame.transform.rotozoom(i, -angle,1.))
        self.frame = 0
        self.image = self.img_list[self.frame]
        self.frame_speed = BOOSTER.FRAME_SPEED + random.randint(-2,2)
        image_offset = (-self.img_list[0].get_width()/2, -self.img_list[0].get_height()/2)
        self.image_position = sum(self.circle.center, image_offset)
        
    def get_force(self, player):
        if self.circle.collide_circle(player.circle):
            return self.force_vector
        return [0,0]
        
    def update(self, delta):
        self.frame += delta * 0.001 * self.frame_speed
        if self.frame > BOOSTER.FRAMES:
            self.frame %= BOOSTER.FRAMES
        frame = int(round(self.frame))
        if frame >= BOOSTER.FRAMES or frame < 0:
            frame = frame % BOOSTER.FRAMES
        self.image = self.img_list[frame]
        
class Port:
    def __init__(self, x, y, level, image, radius = 30):
        self.circle = Circle(x,y,radius)
        self.base_image = image
        self.image = self.base_image.copy()
        self.image_position = (x - radius, y - radius) 
        self.level = level
    
    def update_angle(self, planets):
        closest_planet = None
        maximum = 0
        for p in planets:
            acc = [0,0]
            gx, gy = gravity_circle_circle(self.circle, p.circle, p.mass, p.gravity_radius)
            acc[0] += gx
            acc[1] += gy
            x,y = subtract(self.circle.center, p.circle.center)
            priority = pythagory(gx, gy) / pythagory(x,y) 
            if priority > maximum:
                maximum = priority
                closest_planet = p
        angle = 0
        if closest_planet:
            angle = vector_to_angle(gravity_circle_circle(closest_planet.circle, self.circle))
        self.image = pygame.transform.rotozoom(self.base_image, -angle, 1.0)
        self.image_position = self.circle.center[0] - self.image.get_width()/2, self.circle.center[1] - self.image.get_height()/2
        
