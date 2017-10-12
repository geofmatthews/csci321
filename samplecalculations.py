import numpy
dt = 0.5
m = 10.0
k = 5.0
def force(x):
    global k
    return -k*x
def accel(x):
    global m
    return force(x)/m

t = 0.0
x = 20.0
v = 0.0
a = None

def update():
    global dt,a,x,v,t
    t += dt
    a = accel(x)
    x += v*dt
    v += a*dt

def texrow(ls):
    for item in ls:
        print round(item,1), " & ",
    print "\\\\"

print "\\begin{tabular}{r|rrrr}"
print "$t$ & $x$ & $v$ & $a$ \\\\\\hline"
for step in range(10):
    texrow([t, x, v, accel(x)])
    update()
print "\\end{tabular}"
    
