import os, pygame, re

class ImageManager:
    def __init__(self):
        self.dict = {}
        
    def get(self, name):
        return self.dict[name]
        
    def load_character(self, name, folder):
        folder = os.path.join('data', folder)
        imagefiles = os.listdir(folder)
        self.dict[name] = {} #dict
        for direction in ('n','ne','e','se','s','sw','w','nw'):
            self.dict[name][direction] = {} #dict
            for action in ('looking', 'walking'):
                self.dict[name][direction][action] = [] #list
                pattern = re.compile(action + ' ' + direction + '\d\d\d\d.png')
                for file in imagefiles:
                    if pattern.match(file):
                        fullname = os.path.join(folder, file)
                        try:
                            image = pygame.image.load(fullname)
                        except pygame.error as message:
                            print ('Cannot load image:', fullname)
                            raise SystemExit( message)
                        image.convert() 
                        image.set_colorkey(image.get_at((0,0)))
                        self.dict[name][direction][action].append(image)
                        
    def load_ball(self):
        folder = os.path.join('data', 'T_rolling_stone', 'rolling lavaball bitmaps')
        imagefiles = os.listdir(folder)
        self.dict['ball'] = {} #dict
        for direction in ('n','ne','e','se','s','sw','w','nw'):
            self.dict['ball'][direction] =  {} #dict
            pattern = re.compile('rolling lavaball ' + direction + '\d\d\d\d.png')
            # To make ball act like a player, all actions must be the same:
            self.dict['ball'][direction]['looking'] = [] #list
            for file in imagefiles:
                if pattern.match(file):
                    fullname = os.path.join(folder, file)
                    try:
                        image = pygame.image.load(fullname)
                    except pygame.error as message:
                        print ('Cannot load image:', fullname)
                        raise SystemExit( message)
                    image.convert() 
                    image.set_colorkey(image.get_at((0,0)))
                    self.dict['ball'][direction]['looking'].append(image)
            # Add other actions here:
            for action in ['walking']:
                self.dict['ball'][direction][action] = self.dict['ball'][direction]['looking']

    def load_image(self, name, colorkey=None):
        """Loads a single image file"""
        fullname = os.path.join('data', name)
        dictname = name[0:name.find('.')]
        try:
            image = pygame.image.load(fullname)
        except pygame.error as message:
            print ('Cannot load image:', fullname)
            raise SystemExit( message)
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        self.dict[dictname] = image

class SoundManager:
    def __init__(self):
        dict = {}
        
    def get(self, name):
        return self.dict[name]
        
    def load_sound(self, name):
        """Loads a sound from a file."""
        dictname = name[0:name.find('.')]
        class NoneSound:
            def play(self): pass
        if not pygame.mixer or not pygame.mixer.get_init():
            return NoneSound()
        fullname = os.path.join('data', name)
        try:
            sound = pygame.mixer.Sound(fullname)
        except pygame.error as message:
            print ('Cannot load sound:', fullname)
            raise SystemExit(message)
        self.dict[dictname] = sound

# Global Resource Managers:
Images = ImageManager()
Sounds = SoundManager()
