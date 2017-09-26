import pygame, math
from constants import *
from function import *
from collision import *
from shape import Line, Circle
from enviroment import Platform, Planet

class Player:#(MovingObject):
    def __init__(self, position, planets, platforms, image_dict):
        #super(Player, self).__init__()
        self.image_dict = image_dict['player']

#        self.old_image = pygame.Surface([PLAYER.SIZE, PLAYER.SIZE])
#        self.old_image.fill((255, 100, 0))
#        self.old_image = self.old_image.convert_alpha()
#        self.basic_old_image = self.old_image.copy()
#        self.basic_image = self.image.convert_alpha()
        self.shift_constant = self.image_dict['body'][0].get_height()/2 - PLAYER.SIZE/2
        self.x = position[0]
        self.y = position[1]
        self.circle = Circle(self.x, self.y, PLAYER.SIZE/2)
        self.image_position = [0,0]
        self.last_center = position
        self.angle = 0 # up
        self.display_angle = self.angle
        self.angle_vector = [0,-1]
        self.display_angle_vector = [0,-1]
        self.gravity_angle = 0
        self.gravity_angle_vector = [0,-1]
        self.speed = [0,0] #x,y
        self.acc = [0,0]
        self.planets = planets
        self.platforms = platforms
        self.on_ground = False
        self.closest_planet = planets[0]
        self.move_frame = 0 # for moving with body
        self.eye_frame = 0 # moving with eyes
        self.movement = False
        self.jump_available = False
        self.ground_speed = 0
        self.was_on_ground = False
        self.move_eyes = False
        self.vacuum_time = 0
        
        #self.keep_keys = {'l':None, 'r':None, 'j':None}
        self.keep_keys = []
        self.update_image(1)
        
    def set_camera(self, cam):
        self.cam = cam    
    
    def respawn(self, position):
        self.circle.set_center(position[0], position[1])
        self.on_ground = False
        self.speed = [0,0]
        self.acc = [0,0]
        self.vacuum_time = 0
        
    def set_angle(self, angle):
        self.angle = angle
        self.angle_vector = angle_to_vector(angle)
        
    def set_angle_vector(self, vector):
        if vector != [0,0]:
            self.angle_vector = normalise(vector)
            self.angle = vector_to_angle(self.angle_vector)

    def set_gravity_angle(self, angle):
        self.gravity_angle = angle
        self.gravity_angle_vector = angle_to_vector(angle)
        
    def set_gravity_angle_vector(self, vector):
        if vector != [0,0]:
            self.gravity_angle_vector = normalise(vector)
            self.gravity_angle = vector_to_angle(vector)  
        
    def update(self, keys, delta, external):
        # move (use keys against PLAYER.CONTROLS)
        return self.move(keys, delta, external)

    def update_image(self, delta):
        diff = self.display_angle - self.angle
        while abs(diff) > 180:
            if diff > 0:
                diff -= 360
            else:
                diff += 360
        self.display_angle -= diff * PLAYER.TURN_RATIO * delta * 0.001
        if abs(diff) > delta * PLAYER.TURN_SPEED * 0.001:
            if diff > 0:
                self.display_angle -= delta * PLAYER.TURN_SPEED * 0.001
            else:
                self.display_angle += delta * PLAYER.TURN_SPEED * 0.001
        else:
            self.display_angle = self.angle
        movement = self.on_ground and self.movement
        if not movement and self.move_frame:
            c = 1
            if self.move_frame < PLAYER.MOVE_FRAMES/2:
                c = -1
            self.move_frame += delta * 0.001 * PLAYER.MOVE_FRAME_SPEED * c
            if self.move_frame < 0 or self.move_frame > PLAYER.MOVE_FRAMES:
                self.move_frame = 0
        if movement:
            self.move_frame += delta * 0.001 * PLAYER.MOVE_FRAME_SPEED
            if self.move_frame > PLAYER.MOVE_FRAMES:
                self.move_frame %= PLAYER.MOVE_FRAMES
        
        eye_frame = 0
        if self.move_eyes:
            self.eye_frame += delta * 0.001 * PLAYER.EYE_FRAME_SPEED
            if self.eye_frame > PLAYER.EYE_FRAMES:
                self.eye_frame = 0
                self.move_eyes = False
            eye_frame = int(round(self.eye_frame))
            if eye_frame >= PLAYER.EYE_FRAMES:
                eye_frame = eye_frame % PLAYER.EYE_FRAMES

        move_frame = int(round(self.move_frame))
        if move_frame >= PLAYER.MOVE_FRAMES:
            move_frame = move_frame % PLAYER.MOVE_FRAMES
        
        image = self.image_dict['eyes'][eye_frame].copy()
        image.blit(self.image_dict['body'][move_frame], (0,0))
        
        if diff:
            self.display_angle_vector = angle_to_vector(self.display_angle)
        self.image = pygame.transform.rotozoom(image, -self.display_angle,1.)
        self.image_position = subtract(sum(self.circle.center, multiply(self.display_angle_vector, self.shift_constant)), (self.image.get_width()/2, self.image.get_height()/2))
        
    def apply_keys(self, left, right, jump, delta):
        if self.on_ground and not self.was_on_ground:
            self.ground_speed = -tangent_size(self.speed, perpendicular(self.angle_vector))
            normal_speed = pythagory(self.speed[0], self.speed[1])
            if normal_speed > CAMERA.SHAKE_THRESHOLD:
                self.cam.shake((normal_speed - CAMERA.SHAKE_THRESHOLD)*CAMERA.SHAKE_RATIO)
            else:
                self.move_eyes = True
        if self.on_ground:
            self.was_on_ground = True
            self.movement = right or left
            if right:
                self.ground_speed += PLAYER.GROUND_ACCELERATION*delta*0.001
            if left:
                self.ground_speed -= PLAYER.GROUND_ACCELERATION*delta*0.001
            if self.ground_speed > PLAYER.MAX_GROUND_SPEED:
                self.ground_speed = PLAYER.MAX_GROUND_SPEED
            if self.ground_speed < -PLAYER.MAX_GROUND_SPEED:
                self.ground_speed = -PLAYER.MAX_GROUND_SPEED 
            if not right and not left:
                if self.ground_speed > 0:
                    self.ground_speed -= PLAYER.BRAKE_ACC*delta*0.001
                    if self.ground_speed < 0:
                        self.ground_speed = 0
                else:
                    self.ground_speed += PLAYER.BRAKE_ACC*delta*0.001
                    if self.ground_speed > 0:
                        self.ground_speed = 0
            self.speed[0] = (self.ground_speed) * -self.angle_vector[1]
            self.speed[1] = (self.ground_speed) * self.angle_vector[0]
            if jump and self.jump_available:
                self.jump_available = False
                self.speed[0] += PLAYER.JUMP_ACC * (self.angle_vector[0] + self.gravity_angle_vector[0]) /2
                self.speed[1] += PLAYER.JUMP_ACC * (self.angle_vector[1] + self.gravity_angle_vector[1]) /2
        else:
            self.was_on_ground = False
            if pythagory(self.speed[0], self.speed[1]) > PLAYER.MAX_AIR_SPEED:
                limiter = True
            else:
                limiter = False
            pom = 0
            if self.speed != [0,0]:
                pom = tangent_size([-self.gravity_angle_vector[1], self.gravity_angle_vector[0]], self.speed)
            if right and (not limiter or pom < 0):
                self.acc[0] += PLAYER.AIR_ACCELERATION * -self.gravity_angle_vector[1]
                self.acc[1] += PLAYER.AIR_ACCELERATION * self.gravity_angle_vector[0]
            if left and (not limiter or pom > 0):
                self.acc[0] += PLAYER.AIR_ACCELERATION * self.gravity_angle_vector[1]
                self.acc[1] += PLAYER.AIR_ACCELERATION * -self.gravity_angle_vector[0]
        if not jump:
            self.jump_available = True               
        
    
    def move(self, keys, delta, external):
        # calculate gravity
        strongest = None
        maximum = -1
        self.acc = [0.0, 0.0]
        for p in self.planets:
            gx, gy = gravity_circle_circle(self.circle, p.circle, p.mass, p.gravity_radius)
            if not self.on_ground:
                self.acc[0] += gx
                self.acc[1] += gy
            x,y = subtract(self.circle.center, p.circle.center)
            priority = pythagory(gx, gy) / pythagory(x,y) 
            if priority > maximum:
                maximum = priority
                self.closest_planet = p
        # check keys and add player acceleration
        left, right, jump = self.check_keys(keys)
        # determine speed based on given commands
        self.apply_keys(left, right, jump, delta)
        if self.on_ground:
            gx, gy = gravity_circle_circle(self.circle, self.closest_planet.circle, self.closest_planet.mass, self.closest_planet.gravity_radius)
            self.acc[0] += gx
            self.acc[1] += gy
        if self.acc == [0,0]:
            self.vacuum_time += delta
            if self.vacuum_time > PLAYER.VACUUM_TIME:
                return 'dead'
        self.speed[0] += self.acc[0]*delta*0.001
        self.speed[1] += self.acc[1]*delta*0.001 
        if external != [0,0]:
            diff = subtract(external, self.speed)
            self.speed = sum(self.speed, multiply(diff, PLAYER.BOOST_RATIO))       
        #move circle
        self.circle.move((self.speed[0]*delta*0.001, self.speed[1]*delta*0.001))
        
        if self.closest_planet:
            vector = gravity_circle_circle(self.circle, self.closest_planet.circle)
            self.set_gravity_angle_vector(inverse(vector))
            
        self.on_ground = False
        # checkout collision with surfaces
        self.colliding_planets = []
        for p in self.planets:
            if self.circle.collide_circle(p.circle):
                self.colliding_planets.append(p)

        self.colliding_platforms = []
        self.above_platform = None
        min_distance = 0
        for p in self.platforms:
            if self.circle.collide_line(p.line, PLATFORM.BORDER):
                self.colliding_platforms.append(p)
            is_above = collide_line_line(self.circle.center, self.closest_planet.circle.center, p.line.start, p.line.end)
            if is_above and self.above_platform == None:
                point = collide_line_line_extended(self.circle.center, self.closest_planet.circle.center, p.line.start, p.line.end)
                min_distance = pythagory(self.circle.center[0] - point[0], self.circle.center[1] - point[1])
                self.above_platform = p
            elif is_above:
                point = collide_line_line_extended(self.circle.center, self.closest_planet.circle.center, p.line.start, p.line.end)
                distance = pythagory(self.circle.center[0] - point[0], self.circle.center[1] - point[1])
                if min_distance > distance:
                    self.above_platform = p
                    min_distance = distance
        
        # workout angle
        
        if self.above_platform != None:
            vector = perpendicular(self.above_platform.line.vector)
            angle = vector_to_angle(vector)
            if 90 < abs(angle - self.gravity_angle) < 270:
                vector = inverse(vector)
            self.set_angle_vector(vector)
        else:
            self.set_angle(self.gravity_angle)
        
        self.handle_collision()

        self.update_image(delta)
        self.last_center = multiply(self.circle.center,1)
        
    def handle_collision(self):
        if len(self.colliding_platforms) == 1:
            self.handle_single_platform_collision(self.colliding_platforms[0])
        elif len(self.colliding_planets) == 1:
            planet = self.colliding_planets[0]
            vector = self.circle.collide_circle_extended(planet.circle)
            self.circle.move(vector)
            self.set_angle_vector(vector)
            self.on_ground = True           
        elif len(self.colliding_platforms) > 1:
            self.handle_multiple_collisions()
            
    def handle_single_platform_collision(self, platform):
        vector = self.circle.collide_line_extended(platform.line, PLATFORM.BORDER)
        if vector == [0,0]:
            return
        self.circle.move(vector)
        angle = vector_to_angle(vector)
        if PLATFORM.MIN_ANGLE < abs(angle - self.gravity_angle) < PLATFORM.MAX_ANGLE:
            self.on_ground = False
            if 90 < abs(angle - self.gravity_angle) < 270:
                x, y = tangent(vector, platform.line.vector)
                self.speed = [x,y]
        else:
            self.on_ground = True
        self.set_angle_vector(vector)
        self.ground_speed = -tangent_size(self.speed, perpendicular(self.angle_vector))
            
    def handle_multiple_collisions(self):
        platforms = []
        if len(self.colliding_platforms) == 0:
            return
        for platform in self.colliding_platforms:
            distance = 1
            if not self.circle.collide_line(platform.line, PLATFORM.BORDER):
                return
            vector = self.circle.collide_line_extended(platform.line, PLATFORM.BORDER)
            perpendicular_v = perpendicular(vector)
            if tangent_size(perpendicular_v, self.speed) < 0:
                perpendicular_v = inverse(perpendicular_v)
            pom = sum(self.circle.center, vector)
            point = collide_line_line_extended(self.last_center, self.circle.center, pom, subtract(pom, perpendicular_v))
            if point == self.last_center:
                distance = 0
            elif self.circle.center != self.last_center:
                distance = pythagory(point[0] - self.last_center[0], point[1] - self.last_center[1])/pythagory(self.circle.center[0] - self.last_center[0], self.circle.center[1] - self.last_center[1])
            platforms.append([platform, distance, point, perpendicular_v])
        platforms = sorted(platforms, key=lambda student: student[1])
        min_ground_speed = None
        for platform in platforms:
            self.handle_single_platform_collision(platform[0])
            if min_ground_speed == None:
                min_ground_speed = self.ground_speed
            elif abs(min_ground_speed) > abs(self.ground_speed):
                min_ground_speed = self.ground_speed
        self.ground_speed = min_ground_speed
            
    def check_keys(self, keys): # u,l,d,r
        d = {'u': keys[PLAYER.CONTROLS[0]],
             'l': keys[PLAYER.CONTROLS[1]],
             'd': keys[PLAYER.CONTROLS[2]],
             'r': keys[PLAYER.CONTROLS[3]]}
        left = right = jump = False
        jump_affected = False
        
        if self.keep_keys:
            if d[self.keep_keys[0]]:
                if self.keep_keys[2] == 'l':
                    left = True
                else:
                    right = True
                d[self.keep_keys[0]] = False
                
                # jump
                if d[self.keep_keys[1]]:
                    jump = True
                    d[self.keep_keys[1]] = False
            else:
                self.keep_keys = None

        if 315 <= self.angle or self.angle < 45 or 1:
            if d['u']:
                jump = True
            if d['l']:
                left = True
                self.keep_keys = ['l', 'u', 'l'] # the key to hold, jump key to remember and use, direction of movement
            if d['r']:
                right = True
                self.keep_keys = ['r', 'u', 'r']
            if d['d'] and not (right or left or jump):
                if 315 <= self.angle:
                    left = True
                    self.keep_keys = ['d', 'l', 'l']
                else:
                    right = True
                    self.keep_keys = ['d', 'r', 'r']
                
        elif 45 <= self.angle < 135:
            if d['r']:
                jump = True
            if d['u']:
                left = True
                self.keep_keys = ['u', 'r', 'l']
            if d['d']:
                right = True
                self.keep_keys = ['d', 'r', 'r']
            if d['l'] and not (right or left or jump):
                if self.angle < 90:
                    left = True
                    self.keep_keys = ['l', 'u', 'l']
                else:
                    right = True
                    self.keep_keys = ['l', 'd', 'r']
        elif 135 <= self.angle < 225:
            if d['d']:
                jump = True
            if d['r']:
                left = True
                self.keep_keys = ['r', 'd', 'l']
            if d['l']:
                right = True
                self.keep_keys = ['l', 'd', 'r']
            if d['u'] and not (right or left or jump):
                if self.angle < 180:
                    left = True
                    self.keep_keys = ['u', 'r', 'l']
                else:
                    right = True
                    self.keep_keys = ['u', 'l', 'r']
        elif 225 <= self.angle < 315:
            if d['l']:
                jump = True
            if d['d']:
                left = True
                self.keep_keys = ['d', 'l', 'l']
            if d['u']:
                right = True
                self.keep_keys = ['u', 'l', 'r']
            if d['r'] and not (right or left or jump):
                if self.angle < 270:
                    left = True
                    self.keep_keys = ['r', 'd', 'l']
                else:
                    right = True
                    self.keep_keys = ['r', 'u', 'r']
        return left, right, jump