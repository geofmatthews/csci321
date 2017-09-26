import os, pygame, re

class _ImageManager(object):
    def __init__(self):
        self.animations = {}
        self.static = {}

    def getAnimations(self, name):
        return self.animations[name]
    
    def getStatic(self, name):
        return self.static[name]

    def loadAnimations(self, folder, name,
                       actions=('looking', 'walking'),
                       directions=('n','ne','e','se','s','sw','w','nw'),
                       colorkey = True):
        if name in self.animations:
            return
        self.animations[name] = {}
        for d in directions:
            self.animations[name][d] = {}
            for a in actions:
                self.animations[name][d][a] = []
                pattern = re.compile(a + ' ' + d + '\d\d\d\d.bmp')
                for f in os.listdir(folder):
                    if pattern.match(f):
                        try:
                            image = pygame.image.load(os.path.join(folder,f))
                        except pygame.error as message:
                            print ('Cannot load image:', f)
                            raise (SystemExit, message)
                        image.convert()
                        if colorkey:
                            image.set_colorkey(image.get_at((0,0)))
                        self.animations[name][d][a].append(image)
        
    def loadStatic(self, filename, name, colorkey=True):
        try:
            image = pygame.image.load(filename)
        except pygame.error as message:
            print ('Cannot load image:', filename)
            raise (SystemExit, message)
        image.convert()
        if colorkey:
            image.set_colorkey(image.get_at((0,0)))
        self.static[name] = image

# Singleton interface:
_imagemanager = _ImageManager()
def ImageManager(): return _imagemanager
        
                       
        
