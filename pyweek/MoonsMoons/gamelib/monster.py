import pygame, random, math
from function import *
from shape import Circle, Line

class Monster:
    def __init__(self):
        self.pause = 0
        self.infinite = False
        self.move_frame = 0
        self.circle = None
        self.has_line = False
        
    def update_angle(self, delta):
        if self.pause:
            self.pause -= delta
            if self.pause <= 0:
                self.pause = 0
                self.direction = -self.direction
        else:
            self.went += delta * 0.001 * self.speed * self.direction
            if not self.infinite:
                if self.went >= self.length:
                    self.went = self.length
                    self.pause = self.pause_length
                elif self.went <= 0:
                    self.went = 0
                    self.pause = self.pause_length
        self.angle = self.angle_from + self.went
        self.circle.center = sum(self.center, multiply(angle_to_vector(self.angle), self.move_radius))
        
    def update_position(self, delta):
        if self.pause:
            self.pause -= delta
            if self.pause <= 0:
                self.pause = 0
            else:
                return
        self.went += delta * 0.001 * self.speed * self.direction
        if self.went >= self.length or self.went <= 0:
            if self.went >= self.length:
                self.went = self.length
            else:
                self.went = 0
            self.pause = self.pause_length
            self.direction = -self.direction
        self.circle.center = sum(self.start, multiply(self.vector, self.went))

class QBullet:
    def __init__(self, position, angle, image_dict):
        image = random.choice(image_dict['Qbullets'])
        self.circle = Circle(position[0], position[1], MONSTER.Q.BULLET_RADIUS)
        self.speed = MONSTER.Q.BULLET_SPEED
        self.vector = angle_to_vector(angle)
        self.angle = angle
        self.image = pygame.transform.rotozoom(image, -self.angle,1.)
        self.image_offset = (-self.image.get_width()/2, -self.image.get_height()/2)
        self.image_position = sum(self.circle.center, self.image_offset)
        
    def update(self, delta):
        self.circle.center = sum(self.circle.center, multiply(self.vector, delta * 0.001 * self.speed))
        self.image_position = sum(self.circle.center, self.image_offset)
        
class Q(Monster):
    def __init__(self, img_dict, bullets, planet, altitude, angle_from, angle_length):
        Monster.__init__(self)
        self.direction = 1 # or -1
        self.pause_length = MONSTER.Q.PAUSE + random.randint(0,500)
        self.infinite = False
        self.img_list = img_dict['Q']
        self.img_dict = img_dict
        self.shift_constant = self.img_list[0].get_height()/2 - MONSTER.Q.RADIUS
        self.went = 0
        self.bullets = bullets
        self.shoot_counter = 0
        self.shoot_time = random.randint(MONSTER.Q.SHOOT_TIME_FROM, MONSTER.Q.SHOOT_TIME_TO)
        center = planet.circle.center
        radius = planet.circle.radius + MONSTER.Q.RADIUS + altitude
        self.angle_from = angle_from
        self.angle = self.angle_from
        self.length = angle_length
        if angle_length == -1 or angle_length == 0:
                self.infinite = True
                if angle_length == 0:
                    self.direction = -1
        self.speed = to_degrees(MONSTER.Q.SPEED/float(radius)) # degrees/second
        self.move_radius = radius
        self.center = center
        self.circle = Circle(center[0], center[1], MONSTER.Q.RADIUS)
        self.extra = 0
        self.update_image(1)
        
    def update_image(self, delta):
        if self.pause:
            self.move_frame += delta * 0.001 * MONSTER.Q.MOVE_FRAME_SPEED * self.direction
            if self.move_frame > MONSTER.Q.MOVE_FRAMES:
                self.move_frame %= MONSTER.Q.MOVE_FRAMES
            move_frame = int(round(self.move_frame))
            if move_frame >= MONSTER.Q.MOVE_FRAMES or move_frame < 0:
                move_frame = move_frame % MONSTER.Q.MOVE_FRAMES
        else:
            move_frame = 0
        self.display_angle_vector = angle_to_vector(self.angle)
        if self.direction < 0:
            image = pygame.transform.flip(self.img_list[move_frame], True, False)
        else:
            image = self.img_list[move_frame]
        self.image = pygame.transform.rotozoom(image, -self.angle,1.)
        self.image_position = subtract(sum(self.circle.center, multiply(self.display_angle_vector, self.shift_constant)), (self.image.get_width()/2, self.image.get_height()/2))

    def shoot(self, delta):
        if self.shoot_time and not self.pause:
            self.shoot_time -= delta
            if self.shoot_time < 0:
                self.shoot_time = 0
                self.pause = self.pause_length
        if self.pause: # during pauses we shoot!!!
            self.shoot_counter += delta
            if self.shoot_counter > MONSTER.Q.CADENCE:
                for x in range(self.shoot_counter / MONSTER.Q.CADENCE):
                    angle = self.angle + self.direction*MONSTER.Q.SHOOT_ANGLE
                    vec = angle_to_vector(angle)
                    shift = sum(multiply(vec, self.circle.radius), multiply(perpendicular(vec), self.direction*5+random.randint(-4,4)))
                    pos = sum(self.circle.center, shift)
                    self.bullets.append(QBullet(pos, angle, self.img_dict))
                self.shoot_counter %= MONSTER.Q.CADENCE
        
    def update(self, delta):
        self.update_angle(delta)
        self.shoot(delta)
        self.extra += delta
        c = math.sin(self.extra / 100.0) * 3
        self.circle.center = sum(self.circle.center, multiply(self.display_angle_vector, c))
        self.update_image(delta)

class CBullet:
    def __init__(self, position, angle, image_dict):
        self.circle = Circle(position[0], position[1], MONSTER.C.BULLET_RADIUS)
        self.speed = MONSTER.C.BULLET_SPEED
        self.vector = angle_to_vector(angle)
        self.angle = angle
        self.frame = 0
        self.image_list = []
        for i in image_dict['bullets']:
            self.image_list.append(pygame.transform.rotozoom(i, -self.angle,1.))
        self.image = self.image_list[self.frame]
        self.image_offset = (-self.image.get_width()/2, -self.image.get_height()/2)
        self.image_position = sum(self.circle.center, self.image_offset)
        
    def update(self, delta):
        self.circle.center = sum(self.circle.center, multiply(self.vector, delta * 0.001 * self.speed))
        self.image_position = sum(self.circle.center, self.image_offset)
        self.update_image(delta)
        
    def update_image(self, delta):
        self.frame += delta * 0.001 * MONSTER.C.BULLET_FRAME_SPEED
        if self.frame > MONSTER.C.BULLET_FRAMES:
            self.frame %= MONSTER.C.BULLET_FRAMES
        frame = int(round(self.frame))
        if frame >= MONSTER.C.BULLET_FRAMES or frame < 0:
            frame = frame % MONSTER.C.BULLET_FRAMES
        self.image = self.image_list[frame]

class C(Monster):
    def __init__(self, type, img_dict, bullets, obj, angle_from=0, angle_length=100):
        Monster.__init__(self)
        self.type = type
        self.direction = 1 # or -1
        self.pause_length = MONSTER.C.PAUSE
        self.infinite = False
        self.img_dict = img_dict['C']
        self.shift_constant = self.img_dict['move'][0].get_height()/2 - MONSTER.C.RADIUS
        self.went = 0
        self.state = MONSTER.C.MOVING
        self.bullets = bullets
        if type == MONSTER.TYPE_ANGLE: # from to clockwise
            center, radius = obj.circle.center, obj.circle.radius + MONSTER.C.RADIUS
            self.angle_from = angle_from
            self.angle = self.angle_from
            self.length = angle_length
            if angle_length == -1 or angle_length == 0:
                self.infinite = True
                if angle_length == 0:
                    self.direction = -1
            self.speed = to_degrees(MONSTER.C.SPEED/float(radius)) # degrees/second
            self.move_radius = radius
            self.center = center
            self.circle = Circle(center[0], center[1], MONSTER.C.RADIUS)
        else: # doesn't work properly, should check out later on
            start = obj.line.start
            end = obj.line.end
            fr = angle_from
            to = angle_length
            self.vector = inverse(normalise(obj.line.vector))
            self.start = sum(start, multiply(obj.line.vector, -fr/100.0))
            end = sum(start, multiply(obj.line.vector, -to/100.0))
            dist = subtract(self.start, end)
            self.length = pythagory(dist[0], dist[1])
            angle_vector =  normalise(perpendicular(self.vector)) # angle_from means rotation coefficient and is now 1 or -1
            self.angle = vector_to_angle(angle_vector)
            self.start = sum(self.start, multiply(angle_vector, PLATFORM.BORDER + MONSTER.C.RADIUS))
            self.speed = MONSTER.C.SPEED
            # prepare images
            d = {'move': [], 'reload': [], 'bullets': []}
            for i in self.img_dict['move']:
                d['move'].append(pygame.transform.rotozoom(i, -self.angle,1.))
            for i in self.img_dict['reload']:
                d['reload'].append(pygame.transform.rotozoom(i, -self.angle,1.))
            for i in self.img_dict['bullets']:
                d['bullets'].append(pygame.transform.rotozoom(i, -self.angle,1.))
            self.circle = Circle(self.start[0], self.start[1], MONSTER.C.RADIUS)
            self.img_dict = d
            self.image_offset = subtract(multiply(angle_vector, self.shift_constant), (img_dict['C']['move'][0].get_width()/2, img_dict['C']['move'][0].get_height()/2))
            self.image_position = sum(self.circle.center, self.image_offset)
        self.update_image(1)
        
    def update(self, delta):
        if self.state != MONSTER.C.SHOOTING:
            if self.pause:
                self.state = MONSTER.C.SHOOTING
                self.shooted = False
                self.move_frame = 0
            else:
                if self.type == MONSTER.TYPE_ANGLE:
                    self.update_angle(delta)
                else:
                    self.update_position(delta)
        self.update_image(delta)
        
    def update_image(self, delta):
        if self.state == MONSTER.C.MOVING:
            self.move_frame += delta * 0.001 * MONSTER.C.MOVE_FRAME_SPEED
            if self.move_frame > MONSTER.C.MOVE_FRAMES:
                self.move_frame %= MONSTER.C.MOVE_FRAMES
            frame = int(round(self.move_frame))
            if frame >= MONSTER.C.MOVE_FRAMES:
                frame = frame % MONSTER.C.MOVE_FRAMES
        else:
            self.move_frame += delta * 0.001 * MONSTER.C.RELOAD_FRAME_SPEED
            if self.move_frame > MONSTER.C.SHOOT_FRAME and not self.shooted:
                self.shoot()
                self.shooted = True
            if self.move_frame > MONSTER.C.RELOAD_FRAMES:
                self.move_frame = 0
                self.state = MONSTER.C.MOVING
                self.pause = 0
                self.direction = -self.direction
                frame = int(round(self.move_frame))
                if frame >= MONSTER.C.MOVE_FRAMES:
                    frame = frame % MONSTER.C.MOVE_FRAMES
            else:
                frame = int(round(self.move_frame))
                if frame >= MONSTER.C.RELOAD_FRAMES:
                    frame = frame % MONSTER.C.RELOAD_FRAMES
        self.display_angle_vector = angle_to_vector(self.angle)
        if self.state == MONSTER.C.MOVING:
            image = self.img_dict['move'][frame]
        else:
            image = self.img_dict['reload'][frame]
        if self.direction < 0:
            image = pygame.transform.flip(image, True, False)
        self.image = pygame.transform.rotozoom(image, -self.angle,1.)
        self.image_position = subtract(sum(self.circle.center, multiply(self.display_angle_vector, self.shift_constant)), (self.image.get_width()/2, self.image.get_height()/2))

    def shoot(self):
        angle = self.angle + 100*self.direction
        vec = inverse(angle_to_vector(self.angle))
        pos = sum(self.circle.center, multiply(vec, 3))
        self.bullets.append(CBullet(pos, angle, self.img_dict))

class O(Monster):
    def __init__(self, type, img_dict, obj, angle_from=0, angle_length=100):
        Monster.__init__(self)
        self.type = type
        self.direction = 1 # or -1
        self.pause_length = MONSTER.O.PAUSE + random.randint(0,500)
        self.infinite = False
        self.img_dict = img_dict['O']
        self.shift_constant = self.img_dict['body'][0].get_height()/2 - MONSTER.O.RADIUS
        self.went = 0
        self.eye_frame = 0
        if type == MONSTER.TYPE_ANGLE: # from to clockwise
            center, radius = obj.circle.center, obj.circle.radius + MONSTER.O.RADIUS
            self.angle_from = angle_from
            self.angle = self.angle_from
            self.length = angle_length
            if angle_length == -1 or angle_length == 0:
                self.infinite = True
                if angle_length == 0:
                    self.direction = -1
            self.speed = to_degrees(MONSTER.O.SPEED/float(radius)) # degrees/second
            self.move_radius = radius
            self.center = center
            self.circle = Circle(center[0], center[1], MONSTER.O.RADIUS)
        else:
            start = obj.line.start
            end = obj.line.end
            fr = angle_from
            to = angle_length
            self.vector = inverse(normalise(obj.line.vector))
            self.start = sum(start, multiply(obj.line.vector, -fr/100.0))
            end = sum(start, multiply(obj.line.vector, -to/100.0))
            dist = subtract(self.start, end)
            self.length = pythagory(dist[0], dist[1])
            angle_vector =  normalise(perpendicular(self.vector)) # angle_from means rotation coefficient and is now 1 or -1
            angle = vector_to_angle(angle_vector)
            self.start = sum(self.start, multiply(angle_vector, PLATFORM.BORDER + MONSTER.O.RADIUS))
            self.speed = MONSTER.O.SPEED
            # prepare images
            d = {'eyes': [], 'body': []}
            for i in self.img_dict['eyes']:
                d['eyes'].append(pygame.transform.rotozoom(i, -angle,1.))
            for i in self.img_dict['body']:
                d['body'].append(pygame.transform.rotozoom(i, -angle,1.))
            self.circle = Circle(self.start[0], self.start[1], MONSTER.O.RADIUS)
            self.img_dict = d
            self.image_offset = subtract(multiply(angle_vector, self.shift_constant), (self.img_dict['body'][0].get_width()/2, self.img_dict['body'][0].get_height()/2))
            self.image_position = sum(self.circle.center, self.image_offset)
        self.update_image(1)
        
    def update(self, delta):
        if self.type == MONSTER.TYPE_ANGLE:
            self.update_angle(delta)
        else:
            self.update_position(delta)
        self.update_image(delta)
            
    def update_image(self, delta):
        if not self.pause:
            self.move_frame += delta * 0.001 * MONSTER.O.MOVE_FRAME_SPEED * self.direction
            if self.move_frame > MONSTER.O.MOVE_FRAMES:
                self.move_frame %= MONSTER.O.MOVE_FRAMES
        move_frame = int(round(self.move_frame))
        if move_frame >= MONSTER.O.MOVE_FRAMES or move_frame < 0:
            move_frame = move_frame % MONSTER.O.MOVE_FRAMES
        self.eye_frame += delta * 0.001 * MONSTER.O.MOVE_FRAME_SPEED
        if self.eye_frame > MONSTER.O.EYE_FRAMES + MONSTER.O.KEEP_NORMAL:
            self.eye_frame %= MONSTER.O.EYE_FRAMES + MONSTER.O.KEEP_NORMAL
        eye_frame = int(round(self.eye_frame - MONSTER.O.KEEP_NORMAL))
        if eye_frame < 0 or eye_frame >= MONSTER.O.EYE_FRAMES:
            eye_frame = 0
        
        if self.type == MONSTER.TYPE_ANGLE: # do rotation
            self.display_angle_vector = angle_to_vector(self.angle)
            image = self.img_dict['eyes'][eye_frame].copy()
            image.blit(self.img_dict['body'][move_frame], (0,0))
            self.image = pygame.transform.rotozoom(image, -self.angle,1.)
            self.image_position = subtract(sum(self.circle.center, multiply(self.display_angle_vector, self.shift_constant)), (self.image.get_width()/2, self.image.get_height()/2))
        else:
            self.image = self.img_dict['eyes'][eye_frame].copy()
            self.image.blit(self.img_dict['body'][move_frame], (0,0))
            self.image_position = sum(self.circle.center, self.image_offset)
            
class I(Monster):
    def __init__(self, type, img_dict, obj, position_or_angle):
        Monster.__init__(self)
        self.type = type
        self.speed = 0
        self.circle = Circle(0, 0, MONSTER.I.RADIUS)
        self.state = MONSTER.I.PREPARING
        self.frame = 0
        self.position = 0 # linear expression of position (px)
        if self.type == MONSTER.TYPE_ANGLE: # count start_position
            self.start = sum(obj.circle.center, multiply(angle_to_vector(position_or_angle), obj.circle.radius + self.circle.radius))
            self.angle = position_or_angle
            self.vector = angle_to_vector(self.angle)
        else:
            self.vector = inverse(perpendicular(normalise(obj.line.vector)))
            shift = multiply(obj.line.vector, -position_or_angle/100.0) # side shift
            self.start = sum(sum(obj.line.start, multiply(self.vector, PLATFORM.BORDER + self.circle.radius)), shift)
            self.angle = vector_to_angle(self.vector)
        self.circle.center = self.start[0], self.start[1]
        self.img_list = []
        for i in img_dict['I']:
            self.img_list.append(pygame.transform.rotozoom(i, -self.angle,1.))
        self.shift_constant = img_dict['I'][0].get_height()/2 - MONSTER.I.RADIUS
        self.image_offset = subtract(multiply(self.vector, self.shift_constant), (self.img_list[0].get_width()/2, self.img_list[0].get_height()/2))
        self.image_position = sum(self.circle.center, self.image_offset)
        self.image = self.img_list[0]
        
    def update(self, delta):
        if self.state == MONSTER.I.JUMPING:
            self.move(delta)
        elif self.state == MONSTER.I.PREPARING:
            self.update_frames(delta)
        self.image_position = sum(self.circle.center, self.image_offset)

    def move(self, delta):
        self.speed -= 0.001 * delta * MONSTER.I.JUMP_ACC
        self.position += self.speed * delta * 0.001
        if self.position < 0:
            self.position = 0
            self.state = MONSTER.I.PREPARING
        self.circle.center = sum(self.start, multiply(self.vector, self.position))
        
    def update_frames(self, delta):
        self.frame += delta * 0.001 * MONSTER.I.FRAME_SPEED
        if self.frame > MONSTER.I.FRAMES:
            self.frame = 0
            self.state = MONSTER.I.JUMPING
            self.speed = MONSTER.I.JUMP_SPEED
        move_frame = int(round(self.frame))
        if move_frame >= MONSTER.I.FRAMES or move_frame < 0:
            move_frame = move_frame % MONSTER.I.FRAMES
        self.image = self.img_list[move_frame]
        
class Eye(Monster):
    def __init__(self, type, img_dict, obj, position_or_angle):
        Monster.__init__(self)
        self.type = type
        self.has_line = True
        self.border = MONSTER.EYE.RADIUS
        self.frame = 0
        if self.type == MONSTER.TYPE_ANGLE: # count start_position
            self.start = sum(obj.circle.center, multiply(angle_to_vector(position_or_angle), obj.circle.radius + MONSTER.EYE.RADIUS))
            self.angle = position_or_angle
            self.vector = angle_to_vector(self.angle)
        else:
            self.vector = inverse(perpendicular(normalise(obj.line.vector)))
            shift = multiply(obj.line.vector, -position_or_angle/100.0) # side shift
            self.start = sum(sum(obj.line.start, multiply(self.vector, PLATFORM.BORDER - 3 + MONSTER.EYE.RADIUS)), shift)
            self.angle = vector_to_angle(self.vector)
        end = sum(self.start, multiply(self.vector, MONSTER.EYE.LINE_LENGTH))
        self.line = Line(self.start, end)
        self.img_list = []
        for i in img_dict['eye']:
            self.img_list.append(pygame.transform.rotozoom(i, -self.angle,1.))
        self.shift_constant = img_dict['eye'][0].get_height()/2 - MONSTER.EYE.RADIUS
        self.image_offset = subtract(multiply(self.vector, self.shift_constant), (self.img_list[0].get_width()/2, self.img_list[0].get_height()/2))
        self.image_position = sum(self.start, self.image_offset)
        self.image = self.img_list[0]
        
    def update(self, delta):
        self.frame += delta * 0.001 * MONSTER.EYE.FRAME_SPEED
        if self.frame > MONSTER.I.FRAMES:
            self.frame = 0
        move_frame = int(round(self.frame))
        if move_frame >= MONSTER.EYE.FRAMES or move_frame < 0:
            move_frame = move_frame % MONSTER.EYE.FRAMES
        self.image = self.img_list[move_frame]