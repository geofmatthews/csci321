import math
from constants import *

   
def pythagory(x,y):
	return (x**2 + y**2) ** 0.5
    
def gravity_circle_circle(circle1, circle2, mass2 = 0, radius = -1): 
    "returns vector of gravity force on circle1 caused by circle2"
    pos1 = circle1.center
    pos2 = circle2.center
    if mass2 == 0:
        mass2 = circle2.radius
    return gravity_constant(pos1, pos2, mass2, radius)
    
def gravity(pos1, pos2, mass2, radius):
    deltax = pos2[0] - pos1[0]
    deltay = pos2[1] - pos1[1]
    distance = pythagory(deltax, deltay)
    force_zero = G*(16*mass2)
    forcenorm = gravity_constant(distance, force_zero, radius)
    force = normalise([deltax,deltay], forcenorm)
    return force
    
def gravity_function1(x, p):
    y = 0
    if x < p*G_RANGE:
        y = p
    elif x < 2*p*G_RANGE:
        y = (2*p - x/G_RANGE)
    return y
    
def gravity_constant(pos1, pos2, mass2, radius):
    deltax = pos2[0] - pos1[0]
    deltay = pos2[1] - pos1[1]
    distance = pythagory(deltax, deltay)
    forcenorm = 0
    if radius == -1 or distance < radius:
        forcenorm = mass2
    force = normalise([deltax,deltay], forcenorm)
    return force
    
def to_radians(angle):
    return angle*0.017453292
    
def to_degrees(angle):
    return angle*57.295779513
    
def normalise(vector, norm = 1):
    size = pythagory(vector[0], vector[1])
    if size == 0:
        return [0,0]
    x = norm*vector[0]/size
    y = norm*vector[1]/size
    return [x,y]
    
def inverse(vector):
    return [-vector[0], -vector[1]]
    
def multiply(vector, number):
    return [number*vector[0], number*vector[1]]
    
def sum(vector1, vector2):
    return [vector1[0] + vector2[0], vector1[1] + vector2[1]]

def subtract(vector1, vector2):
    return [vector1[0] - vector2[0], vector1[1] - vector2[1]]
    
def perpendicular(vector):
    return [vector[1], -vector[0]]
    
def tangent(vector, direction):
    size = (vector[0]*direction[0] + vector[1]*direction[1])/pythagory(direction[0], direction[1])
    return normalise(direction, size)
    
def tangent_size(vector, direction):
    return(vector[0]*direction[0] + vector[1]*direction[1])/pythagory(direction[0], direction[1])
    
def normal(vector, direction):
    x, y = tangent(vector, direction)
    return subtract(vector, [x,y])
    
def vector_to_angle(vector):
    x, y = vector
    if y == 0:
        if x > 0:
            return 90
        else:
            return 270
    angle = to_degrees(math.atan(1.0*x/-y))
    if y > 0:
        angle += 180
    if angle < 0:
        angle += 360
    return angle
    
def angle_to_vector(angle):
    angle_rad = to_radians(angle)
    return [math.sin(angle_rad),-math.cos(angle_rad)]
