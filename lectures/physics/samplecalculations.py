import numpy

def force(x):
#    k = 5.0
#    return -k*x
    return 4.0*x
def accel(x):
    m = 2.0
    return force(x)/m


def initialize(newdt,newstop):
    global t,x,v,a,dt,stop
    t = 0.0
    x = 8.0
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
        print round(item,3), " & ",
    print "\\\\"

def run(updateFunction):
    print "\\begin{tabular}{r|rrrr}"
    print "$t$ & $x$ & $v$ & $a$ \\\\\\hline"
    texrow([t,x,v,accel(x)])
    while t <= stop:
        updateFunction()
        texrow([t, x, v, accel(x)])
    print "\\end{tabular}"

initialize(0.5, 2.0)
#run(Euler)


initialize(0.5, 1.0)
run(Midpoint)
initialize(0.25, 1.0)
run(Midpoint)

initialize(0.5, 2.0)
#run(RungeKutta)

def sequence(updateFunction):
    initialize(4.0,8)
    run(updateFunction)
    initialize(2.0,6)
    run(updateFunction)
    initialize(1.0,5)
    run(updateFunction)

#sequence(RungeKutta)
