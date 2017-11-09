import numpy

def force(x):
    k = 5.0
    return 4*x
def accel(x):
    m = 2.0
    return force(x)/m

def initialize(start,newdt,newstop):
    global t,x,v,a,dt,stop,xPrevious
    t = start
    x = 8.0
    xPrevious = x
    v = 0.0
    a = None
    dt = newdt
    stop = newstop

def Euler():
    global dt,a,x,v,t
    a = accel(x)
    x += v*dt
    v += a*dt
    t += dt

def SymplecticEuler():
    global dt,a,x,v,t
    a = accel(x)
    v += a*dt
    x += v*dt
    t += dt

def Verlet():
    global dt,a,x,v,t,xPrevious
    a = accel(x)
    xNew = 2*x - xPrevious + a*dt*dt
    x, xPrevious = xNew, x
    t += dt
    v = x - xPrevious
    
    
def Midpoint():
    global dt,a,x,v,t
    a = accel(x)
    vHalf = v + a*dt/2.0
    xHalf = x + v*dt/2.0
    aHalf = accel(xHalf)
    tHalf = t + dt/2.0
    texrow([tHalf,xHalf,vHalf,aHalf])
    v = v + aHalf*dt
    x = x + vHalf*dt
    t += dt

def RungeKutta():
    global dt,a,x,v,t
    a = accel(x)
    vA = v + a*dt/2.0
    xA = x + v*dt/2.0
    aA = accel(xA)
    tA = t + dt/2.0
    texrow([tA,xA,vA,aA])
    vB = v + aA*dt/2.0
    xB = x + vA*dt/2.0
    aB = accel(xB)
    tB = t + dt/2.0
    texrow([tB,xB,vB,aB])
    vC = v + aB*dt
    xC = x + vB*dt
    aC = accel(xC)
    tC = t + dt
    texrow([tC,xC,vC,aC])
    v = v + (a/6.0 + aA/3.0 + aB/3.0 + aC/6.0)*dt
    x = x + (v/6.0 + vA/3.0 + vB/3.0 + vC/6.0)*dt
    t += dt

def texrow(ls):
    for item in ls:
        print round(item,2), " & ",
    print "\\\\"

def run(updateFunction):
    print "\\begin{tabular}{r|rrrr}"
    print "$t$ & $x$ & $v$ & $a$ \\\\\\hline"
    texrow([t,x,v,accel(x)])
    while t <= stop:
        updateFunction()
        texrow([t, x, v, accel(x)])
    print "\\end{tabular}"



initialize(0.0, 0.5, .99)
run(Midpoint)
initialize(0.0, 0.5, 1.99)
run(Verlet)

def sequence(updateFunction):
    initialize(1,16)
    run(updateFunction)
    initialize(0.5,8)
    run(updateFunction)
    initialize(0.25,4)
    run(updateFunction)
