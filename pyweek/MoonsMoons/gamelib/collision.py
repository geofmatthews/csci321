from function import *

def collide_line_line(start1, end1, start2, end2):
    a, b = collide_line_line_core(start1, end1, start2, end2)
    if 0 < a < 1 and 0 < b < 1:
        return True
    return False
    
def collide_line_line_extended(start1, end1, start2, end2):
    [a, b] = collide_line_line_core(start1, end1, start2, end2)
    if [a,b] == [None,None]:
        return [None,None]
    else:
        vectA = (start1[0] - end1[0], start1[1] - end1[1])
        offset = multiply(vectA, a)
        return sum(start1, offset)

def collide_line_line_core(start1, end1, start2, end2):
    vectA = (start1[0] - end1[0], start1[1] - end1[1])
    vectB = (end2[0] - start2[0], end2[1] - start2[1])
    point = (start1[0] - start2[0], start1[1] - start2[1])
    if vectA[0] == 0 or vectA[1] == 0 or vectB[0] == 0 or vectB[1] == 0:
        if (vectA[0] == 0 and vectA[1] == 0) or (vectB[0] == 0 and vectB[1] == 0):
            a, b = collide_circle_line_extended(point, 1, [0,0], sum(vectA, vectB))
            return [a, 0]
        if vectA[0] == 0 and vectB[1] == 0:
            return [point[0]/vectB[0], point[1]/vectA[1]]
        if vectB[0] == 0 and vectA[1] == 0:
            return [point[0]/vectA[0], point[1]/vectB[1]]
        if vectA[0] == 0 and vectB[0] == 0:    
            return [1,1]
        if vectA[1] == 0 and vectB[1] == 0:    
            return [1,1]
        if vectA[0] == 0:
            b_coord = point[0]/vectB[0]
            a_coord = (point[1] - b_coord*vectB[1])/vectA[1]
            return a_coord, b_coord
        if vectA[1] == 0:
            b_coord = point[1]/vectB[1]
            a_coord = (point[0] - b_coord*vectB[0])/vectA[0]
            return a_coord, b_coord
        if vectB[0] == 0:
            a_coord = point[0]/vectA[0]
            b_coord = (point[1] - a_coord*vectA[1])/vectB[1]
            return a_coord, b_coord
        if vectB[1] == 0:
            a_coord = point[1]/vectA[1]
            b_coord = (point[0] - a_coord*vectA[0])/vectB[0]
            return a_coord, b_coord
        return [None,None]
    pom = -1.0*vectB[0]/vectB[1]
    a_coord, b_coord = None, None
    if (vectA[0]+vectA[1]*pom) != 0:
        a_coord = (point[0] + point[1]*pom)/(vectA[0]+vectA[1]*pom)
    else:
        return [None,None]
    pom = -1.0*vectA[0]/vectA[1]
    b_coord = (point[0] + point[1]*pom)/(vectB[0]+vectB[1]*pom)
    return [a_coord, b_coord]

def collide_circle_point(pos1, r, pos2):
    if pythagory(pos1[0] - pos2[0], pos1[1] - pos2[1]) < r:
        return True
    return False
    
def collide_circle_circle(pos1, r1 ,pos2, r2):
    r = r1 + r2
    if pythagory(pos1[0] - pos2[0], pos1[1] - pos2[1]) < r:
        return True
    return False
    
def collide_circle_line(pos, radius, start, end, border = 0):
    r = radius + border
    if collide_circle_circle(pos, r, start, 0):
        return True
    if collide_circle_circle(pos, r, end, 0):
        return True
    vectA = (end[0] - start[0], end[1] - start[1])
    deltax = pos[0] - start[0]
    deltay = pos[1] - start[1]
    if vectA[0] == 0 or vectA[0] == -0.0:
        if vectA[1] > 0:
            if 0 < deltay < vectA[1] and -r < deltax < r:
                return True
        else:
            if 0 > deltay > vectA[1] and -r < deltax < r:
                return True
        return False
    elif vectA[1] == 0 or vectA[1] == -0.0:
        if vectA[0] > 0:
            if 0 < deltax < vectA[0] and -r < deltay < r:
                return True
        else:
            if 0 > deltax > vectA[0] and -r < deltay < r:
                return True
        return False
    else:
        ratio = r/pythagory(vectA[0], vectA[1])
        vectB = ((start[1] - end[1])*ratio, (end[0] - start [0])*ratio)
        pom = - vectB[0]/vectB[1]
        parallel = (deltax + deltay*pom)/(vectA[0]+vectA[1]*pom)
        perpendicular = (deltax - parallel*vectA[0])/vectB[0]
        if 0 < parallel < 1 and -1 < perpendicular < 1:
            return True
    return False

def collide_circle_circle_extended(pos1, r1 ,pos2, r2):
    r = r1 + r2
    distance = pythagory(pos1[0] - pos2[0], pos1[1] - pos2[1])
    if distance < r:
        return normalise([pos1[0] - pos2[0], pos1[1] - pos2[1]], r - distance)
    return [0, 0]
    
def collide_circle_line_extended(pos, radius, start, end, border = 0):
    r = radius + border
    return_vector = [0,0]
    vector = collide_circle_circle_extended(pos, r, start, 0)
    if vector != [0,0]:
        return_vector = vector
    vector = collide_circle_circle_extended(pos, r, end, 0)    
    if vector != [0,0]:
        return_vector = vector
    vectA = (end[0] - start[0], end[1] - start[1])
    deltax = pos[0] - start[0]
    deltay = pos[1] - start[1]
    if vectA[0] == 0 or vectA[0] == -0.0:
        if vectA[1] > 0:
            if 0 < deltay < vectA[1] and -r < deltax < 0:
                return_vector = [-r-deltax, 0]
            elif 0 < deltay < vectA[1] and 0 < deltax < r:
                return_vector = [r-deltax, 0]
        else:
            if 0 > deltay > vectA[1] and -r < deltax < 0:
                return_vector = [-r-deltax, 0]
            elif 0 > deltay > vectA[1] and 0 < deltax < r:
                return_vector = [r-deltax, 0]
    elif vectA[1] == 0 or vectA[1] == -0.0:
        if vectA[0] > 0:
            if 0 < deltax < vectA[0] and -r < deltay < 0:
                return_vector = [0, -r-deltay]
            elif 0 < deltax < vectA[0] and 0 < deltay < r:
               return_vector = [0, r-deltay]
        else:
            if 0 > deltax > vectA[0] and -r < deltay < 0:
                return_vector = [0, -r-deltay]
            elif 0 > deltax > vectA[0] and 0 < deltay < r:
               return_vector = [0, r-deltay]
    else:
        ratio = r/pythagory(vectA[0], vectA[1])
        vectB = ((start[1] - end[1])*ratio, (end[0] - start [0])*ratio)
        pom = - vectB[0]/vectB[1]
        parallel = (deltax + deltay*pom)/(vectA[0]+vectA[1]*pom)
        perpendicular = (deltax - parallel*vectA[0])/vectB[0]
        if 0 < parallel < 1 and 0 < perpendicular < 1:
            return_vector = normalise(vectB, r*(1-perpendicular))
        if 0 < parallel < 1 and -1 < perpendicular < 0:
            return_vector = normalise(vectB, r*(-1-perpendicular))
    return return_vector

