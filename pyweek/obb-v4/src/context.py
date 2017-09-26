import vista

class Context(object):
    def think(self, dt, events, keys, mousepos, buttons):
        pass
        
    def draw(self):
        vista.clear()


cstack = []

def push(con):
    cstack.append(con)

def pop(n = 1):
    for _ in range(n):
        if cstack:
            del cstack[-1]

def top():
    return cstack[-1] if cstack else None


