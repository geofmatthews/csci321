
import pygame, time
from pygame.locals import *
from pygame.color import *
import numpy as N
from VerletPhysics import ParticleSystem

#### Globals
pygame.init()
screen = pygame.display.set_mode((int(640*3/2),int(480*3/2)))
backcolor = (128,128,255)
background = pygame.Surface(screen.get_size())
background.fill(backcolor)
myfont = pygame.font.Font(None, 24)
euler = False
eulerDamping = False
collisions = False

#### Utilities

def curtainSystem(n=12):
    global euler, collisions, screen
    n 
    w,h = screen.get_size()
    xstep = w/float(n)
    ystep = h/float(n)
    positions = []
    velocities = []
    masses = []
    for j in range(n):
        for i in range(n):
            positions.extend([i*xstep, j*ystep, 0.0])
            velocities.extend([0.0,0.0,0.0])
            masses.append(5.0)
    psystem = ParticleSystem(positions, velocities, masses)
    down = N.array((0.0,1.0,0.0))
    for j in range(n):
        for i in range(n):
            p1 = i+j*n
            psystem.makeConstant(p1, down, 32.0)
            p2 = i+(j+1)*n
            p3 = (i+1)+j*n
            p4 = (i+1) + (j+1)*n
            if j+1 < n:
                psystem.makeStick(p1, p2)
            if i+1 < n:
                psystem.makeStick(p1, p3)
    psystem.setVel((n/2)*n-1, N.array((1000+N.random.random()*1000.0, 0.0, 0.0)))

    for i in range(n):
        psystem.makePin(i)
    return psystem
            
def gridSystem(n=8):
    global euler, collisions, screen
    w,h = screen.get_size()
    xstep = w/float(n)
    ystep = h/float(n)
    positions = []
    velocities = []
    masses = []
    for i in range(n):
        for j in range(n):
            positions.extend([i*xstep, j*ystep, 0.0])
            velocities.extend([0.0, 0.0, 0.0])
            masses.append(5.0+N.random.random())
    psystem = ParticleSystem(positions, velocities, masses)
    for i in range(n):
        for j in range(n):
            p1 = i+j*n
            p2 = i+(j+1)*n
            p3 = (i+1)+j*n
            p4 = (i+1) + (j+1)*n
            if j+1 < n:
                psystem.computeForces.append(("spring", p1, p2, 1.0,
                                             psystem.dist(p1, p2)*1))
            if i+1 < n:
                psystem.computeForces.append(("spring", p1, p3, 1.0,
                                             psystem.dist(p1, p3)*1))
            if i+1 < n and j+1 < n:
                psystem.computeForces.append(("spring", p2, p3, 1.0,
                                              psystem.dist(p2,p3)))
                psystem.computeForces.append(("spring", p1, p4, 1.0,
                                              psystem.dist(p1, p4)))
    #for i in range(n):
        #psystem.setVel(i, N.array((8.0, 8.0, 0.0)))
        #psystem.setVel(i+n, N.array((0.0, -10.0, 0.0)))
    psystem.incPos(n*n-1, N.array((30.0, 30.0, 0.0)))

    return psystem

def randomSystem(n, connect="stick"):
    global euler, collisions, screen
    w,h = screen.get_size()
    size = min(w,h)
    positions = N.random.random(3*n)*size/2.0 + size/3.0
    positions[2::3] = 0.0
    velocities = N.random.random(3*n)*10.0 - 5.0
    velocities[2::3] = 0.0
    masses = N.random.random(n)*10.0 + 5.0
    psystem = ParticleSystem(positions, velocities, masses)
    psystem.collisions = collisions
    psystem.euler = euler
    psystem.makePin(0)
    psystem.makePin(n-1)
    for i in range(0, psystem.n-3, 3):
        psystem.makeTriangle(i, i+1, i+2)
        if connect == "spring":
            psystem.computeForces.append(("spring", i+2, i+3, 1.0, 100.0))
        else:
            psystem.constraints.append(("stick", i+2, i+3,
                                          psystem.dist(i+2, i+3)))
    for i in range(psystem.n):
        psystem.computeForces.append(("drag", i, 0.1))
    psystem.computeForces.append(("constant", 0, N.array((1.0, 0.0, 0.0)), 1.0))
    psystem.computeForces.append(("constant", n-1, N.array((1.0, 0.0, 0.0)), -1.0))
    return psystem

def triangleSystem():
    global euler, collisions, screen
    w,h = screen.get_size()
    
    tris = [0.1, 0.4, 0.0,
            0.1, 0.1, 0.0,
            0.4, 0.1, 0.0,
            
            0.6, 0.1, 0.0,
            0.9, 0.1, 0.0,
            0.9, 0.4, 0.0,
            
            0.9, 0.6, 0.0,
            0.9, 0.9, 0.0,
            0.6, 0.9, 0.0,
            
            0.4, 0.9, 0.0,
            0.1, 0.9, 0.0,
            0.1, 0.6, 0.0]
    scale = [float(w),float(h),0.0] * int(len(tris)/3)
    
    positions = N.array(tris) * N.array(scale)
    n = len(positions)/3
    velocities = N.random.random(3*n)*10.0 - 5.0
    velocities[2::3] = 0.0
    masses = N.array([16.0, 4.0, 4.0]*int(n/3)) + N.random.random(n)*4.0
    N.random.shuffle(masses)
    psystem = ParticleSystem(positions, velocities, masses)
    psystem.collisions = collisions
    psystem.euler = euler
    for i in range(0,12,3):
        psystem.constraints.append(("triangle",i+0,i+1,i+2,
                                    psystem.dist(i+0,i+1),
                                    psystem.dist(i+1,i+2),
                                    psystem.dist(i+2,i+0)))
    springk = 0.1
    springl = 0.25
    psystem.computeForces.append(("spring", 2, 3, springk, psystem.dist(2,3)*springl))
    psystem.computeForces.append(("spring", 5, 6, springk, psystem.dist(5,6)*springl))
    psystem.computeForces.append(("spring", 8, 9, springk, psystem.dist(8,9)*springl))
    if True:
        psystem.computeForces.append(("spring", 11, 0, springk, psystem.dist(11,0)*springl))   
    else:
        psystem.constraints.append(("stick", 11, 0, psystem.dist(11,0)))   
    for i in range(psystem.n):
        if True:
            psystem.computeForces.append(("drag", i, 0.075))
    psystem.makePin(0)
    return psystem                       

def textout(txt, pos, txtcolor = (0,0,0)):
    rtext = myfont.render(txt, 1, txtcolor, backcolor)
    textrec = rtext.get_rect()
    textrec.topright = (screen.get_width(), pos)
    screen.blit(rtext, textrec)

def fpsout(fps):
    textout("fps: %f" % fps, 0)
    

def newSystem(n, systemtype):
    if systemtype == 0:
        return randomSystem(n, "stick")
    elif systemtype == 1:
        return randomSystem(n, "spring")
    elif systemtype == 2:
        return triangleSystem()
    elif systemtype == 3:
        return gridSystem()
    elif systemtype == 4:
        return curtainSystem()
    else:
        print "Unknown system type: " , systemtype
        exit(0)

systems = ("Random stick",
           "Random spring",
           "Four triangles",
           "Grid of springs",
           "Curtain")
    
def main():
    global  euler, collisions, eulerDamping
    systemtype = 0
    nParticles = 4 + 5*2
    plotTime = False
    mysystem = newSystem(nParticles, systemtype)

    clock = pygame.time.Clock()
    running = 1
    framesPerSecond = 30
    stepsPerFrame = 2
    deltaT = 1/4.0
    screen.blit(background, (0,0))

    frames = 0
    elapsedtime = 0.0
    fps = 0.0

    while running:
        frametime = clock.tick(framesPerSecond)
        frames += 1
        elapsedtime += frametime
        if frames >= 100:
            fps = 1000.0*float(frames)/(elapsedtime)
            frames = 0
            elapsedtime = 0.0
            
        for event in pygame.event.get():
            if event.type == QUIT:
                running = 0
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = 0
                elif event.key == K_F1:
                    systemtype -= 1
                    systemtype %= 5
                    mysystem = newSystem(nParticles, systemtype)
                elif event.key == K_F2:
                    systemtype += 1
                    systemtype %= 5
                    mysystem = newSystem(nParticles, systemtype)                    
                elif event.key == K_F3:
                    euler = not euler
                    mysystem.euler = euler
                elif event.key == K_F4:
                    eulerDamping = not eulerDamping
                    mysystem.eulerDamping = eulerDamping
                elif event.key == K_F5:
                    collisions = not collisions
                    mysystem.collisions = collisions
                elif event.key == K_F12:
                    mysystem = newSystem(nParticles, systemtype)
        mysystem.euler = euler
        mysystem.eulerDamping = eulerDamping
        mysystem.collisions = collisions

        for i in range(stepsPerFrame):
            mysystem.Step(deltaT)
                    
        screen.blit(background, (0,0))
        mysystem.Draw(screen)
        fpsout(fps)
        textout("F1/2: " + systems[systemtype], 22)
        if mysystem.euler:
            textout("F3: Euler", 22*2)
        else:
            textout("F3: Verlet", 22*2)
        if mysystem.eulerDamping:
            textout("F4: Euler damping", 22*3)
        else:
            textout("F4: No Euler damping", 22*3)
        if mysystem.collisions:
            textout("F5: Collisions", 22*4)
        else:
            textout("F5: No collisions", 22*4)
        textout("F12: New system", 22*5)
        pygame.display.flip()

if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.quit()

    
    
    
