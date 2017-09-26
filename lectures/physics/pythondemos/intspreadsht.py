from numpy import *

def prlatex(ls):
    for x in ls:
        print round(x,1),"&",
    print "\\\\"

def step(t,x,v,dt,k,m):
    a = -k*x/m
    x += v*dt
    v += a*dt
    a = -k*x/m
    t += dt
    return (t,x,v,a)
    
def euler(start=0.0, stop=5.0, dt=1.0, x = 20.0, v = 0.0, k = 5.0, m = 10.0):
    a = -k*x/m
    for t in arange(start, stop+dt, dt):
        prlatex ((t,x,v,a))
        t,x,v,a = step(t,x,v,dt,k,m)
    print "--------------------"

def midpoint(start=0.0, stop=5.0, dt=1.0, x = 20.0, v = 0.0, k = 5.0, m = 10.0):
    a = -k*x/m
    for t in arange(start, stop+dt, dt):
        prlatex ((t,x,v,a))
        t1,x1,v1,a1 = step(t,x,v,dt/2.0,k,m)
        prlatex((t1,x1,v1,a1))
        x += v1*dt
        v += a1*dt
        a = -k*x/m
        t += dt
    print "-----------------------"
    
    
    

euler()
euler(dt=0.5)
midpoint()

    
