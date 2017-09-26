import os, pygame

def load_music(name):
    fullname = os.path.join('data', 'music', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load music:', name
        raise SystemExit, message
    return sound
    
def first_time(level):
    fullname = os.path.join('data', 'save', 'save.txt')
    f = open(fullname, 'r')
    lines = f.readlines()
    for l in lines:
        a = l.split()
        if len(a) == 0:
            continue
        if a[0] == level:
            return False
    return True
    
def save_level(stars, tries, level):
    fullname = os.path.join('data', 'save', 'save.txt')
    new_lines = []
    try:
        f = open(fullname, 'r')
        lines = f.readlines()
        f.close()
        found = False
        for l in lines:
            a = l.split()
            if len(a) == 0:
                continue
            if a[0] == level:
                found = True
                if int(a[1]) < stars or (int(a[1]) == stars and int(a[2]) < tries):
                    new_lines.append(level + ' ' + str(stars) + ' ' + str(tries))
                else:
                    new_lines.append(a[0] + ' ' + a[1] + ' ' + a[2])
            else:
                new_lines.append(a[0] + ' ' + a[1] + ' ' + a[2])
        if not found:
            new_lines.append(level + ' ' + str(stars) + ' ' + str(tries))
    except IOError:
        new_lines.append(level + ' ' + str(stars) + ' ' + str(tries))
    try:
        f = file(fullname, 'w')
    except IOError:
        raise SystemExit, "Couldn't load file "+fullname
    s = ""
    for l in new_lines:
        s += l + '\n'
    f.write(s)
    f.close()
    

def load_image(name, alpha=False, dir = ""):
    if dir:
        fullname = os.path.join('data', 'images', dir, name)
    else:
        fullname = os.path.join('data', 'images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    if alpha:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image
    
def load_music(name):
    fullname = os.path.join('data', 'music', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load music:', name
        raise SystemExit, message
    return sound
    
def load_images():
    d = {}
    ############ PLAYER ##############
    d['player'] = {'body': [], 'eyes': []}
    d['player']['body'].append(load_image('body1.png', True, 'player'))
    d['player']['body'].append(load_image('body2.png', True, 'player'))
    d['player']['body'].append(load_image('body3.png', True, 'player'))
    d['player']['body'].append(load_image('body4.png', True, 'player'))
    #d['player']['body'].append(load_image('body5.png', True, 'player'))
    #d['player']['body'].append(load_image('body5.png', True, 'player'))
    d['player']['body'].append(load_image('body4.png', True, 'player'))
    d['player']['body'].append(load_image('body3.png', True, 'player'))
    d['player']['body'].append(load_image('body2.png', True, 'player'))
    for x in range(12):
        d['player']['eyes'].append(load_image('oci' + str(x+1) + '.png', True, 'player'))
    
    ############ MONSTERS #############
    ## Q ##
    d['Q'] = []
    d['Q'].append(load_image('body1.png', True, 'Q'))
    d['Q'].append(load_image('body2.png', True, 'Q'))
    # bullets
    d['Qbullets'] = []
    d['Qbullets'].append(load_image('bullet1.png', True, 'Q'))
    
    ## C ##
    d['C'] = {'move': [], 'reload': [], 'bullets': []}
    for x in range(12):
        d['C']['reload'].append(load_image('reload' + str(x+1) + '.png', True, 'C'))
    for x in range(7):
        d['C']['move'].append(load_image('move' + str(x+1) + '.png', True, 'C'))
    for x in range(4):
        d['C']['bullets'].append(load_image('bullet' + str(x+1) + '.png', True, 'C'))
    
    ## O ##
    d['O'] = {'body': [], 'eyes': []}
    d['O']['body'].append(load_image('body1.png', True, 'O'))
    d['O']['body'].append(load_image('body2.png', True, 'O'))
    d['O']['body'].append(load_image('body3.png', True, 'O'))
    for x in range(6):
        d['O']['eyes'].append(load_image('eyes' + str(x+1) + '.png', True, 'O'))
    
    ## I ##
    d['I'] = []
    for x in range(10):
        d['I'].append(load_image('icko' + str(x+1) + '.png', True, 'I'))
    
    ## EYE ##
    d['eye'] = []
    for x in range(10):
        d['eye'].append(load_image('oko' + str(x+1) + '.png', True, 'eye'))
        
    ## GEYSER ##
    d['geyser'] = {'1': [], '2': [], '3': []}
    for x in range(17):
        d['geyser']['1'].append(load_image('gejzir' + str(x) + '.png', True, 'geyser'))
    for x in range(17):
        d['geyser']['2'].append(load_image('gejzir_azure' + str(x) + '.png', True, 'geyser'))
    for x in range(17):
        d['geyser']['3'].append(load_image('gejzir_red' + str(x) + '.png', True, 'geyser'))

    d['flag'] = []
    for x in range(7):
        d['flag'].append(load_image('flag' + str(x) + '.png', True, 'flag'))

    d['star'] = load_image('star1.png', True, 'pickup')
    d['star_empty'] = load_image('star2.png', True, 'pickup')
    
    d['parts'] = []
    d['parts'].append(load_image('belts.png', True, 'parts'))
    d['parts'].append(load_image('exhaust.png', True, 'parts'))
    d['parts'].append(load_image('igloo.png', True, 'parts'))
    d['parts'].append(load_image('joystick.png', True, 'parts'))
    d['parts'].append(load_image('metal_plate.png', True, 'parts'))
    d['parts'].append(load_image('metal_plate2.png', True, 'parts'))
    d['parts'].append(load_image('radar.png', True, 'parts'))
    d['parts'].append(load_image('top.png', True, 'parts'))
    d['parts'].append(load_image('wheel.png', True, 'parts'))
    d['parts'].append(load_image('wing.png', True, 'parts'))
    
    d['port'] = load_image('port60.png', True)
    
    d['dash'] = load_image('dash.png', True, 'extra')
    d['platform1-left'] = load_image('side1.png', True, 'platform')
    d['platform1-middle'] = load_image('middle1.png', True, 'platform')
    d['platform1-right'] = pygame.transform.flip(d['platform1-left'], True, False)
    d['platform2-left'] = load_image('side2.png', True, 'platform')
    d['platform2-middle'] = load_image('middle2.png', True, 'platform')
    d['platform2-right'] = pygame.transform.flip(d['platform2-left'], True, False)
    d['platform3-left'] = load_image('side3.png', True, 'platform')
    d['platform3-middle'] = load_image('middle3.png', True, 'platform')
    d['platform3-right'] = pygame.transform.flip(d['platform3-left'], True, False)
    return d

def load_font(path, size):
    fullname = os.path.join('data', 'fonts', path)
    return pygame.font.Font(fullname, size)
    
def load_level_file(f):
    return file(os.path.join('data', 'levels', f), 'r')

