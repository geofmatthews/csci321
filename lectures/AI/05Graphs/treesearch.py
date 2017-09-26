
def treeSearch(problem):
    fringe = [makeNode(problem.initialState())]
    while fringe:
        node = fringe.pop(0)
        if problem.goalTest(node):
            return node
        fringe.extend(expand(node, problem))
        fringe.sort(key = problem.cost, reverse=True)
    return None

def expand(node, problem):
    successors = []
    for (action, result) in problem.successors(node):
        s = makeNode()
        s.parent = node
        s.action = action
        s.state = result
        s.pathCost = node.pathCost + problem.stepCost(node, action, s)
        s.depth = node.depth + 1
        successors.append(s)
    return successors

def 
