
def fringeNodes(depth, branch=8):
    return branch**depth

def totalNodes(depth, branch=8):
    sum = 0
    for i in range(depth+1):
        sum += fringeNodes(i, branch)
    return sum

def totalNodesN(depth, branch=8):
    return (branch**(depth+1)-1)/(branch-1)

def deepeningNodes(depth, branch = 8):
    sum = 0
    for i in range(depth+1):
        sum += totalNodes(i)
    return sum

for i in range(21):
    fn = fringeNodes(i)
    tn = totalNodes(i)
    dn = deepeningNodes(i)
    print i, fn, tn, dn

print i, fn/float(fn), tn/float(fn), dn/float(fn)

        
