
class Node():
    def __init__(self, n):
        self.n = n
        self.parent = None
    def __repr__(self):
        return "Node:" + repr(self.n) 

def search(openlist, closedlist, win, successors, cost, heuristic, depth=0):
    print openlist, closedlist
    if depth > 1000:
        return None
    openlist.sort(key=cost, reverse=True)
    if len(openlist) == 0:
        return None
    node = openlist.pop()
    if node in closedlist:
        updateClosedList(closedlist, node)
    if win(node):
        return node
    for child in successors(node):
        child.parent = node
        openlist.insert(0,child)
    closedlist.insert(0,node)
    return search(openlist, closedlist, win, successors, cost, heuristic, depth+1)

def win(node):
    return node.n == 11
def successors(node):
    n = node.n
    return [Node(2*n), Node(2*n+1)]
def cost(node):
    return abs(node.n - 11) + node.n

path = search([Node(1)], [], win, successors, cost)

def printPath(path):
    if path:
        print path.n, "->",
        printPath(path.parent)

printPath(path)
        
    
