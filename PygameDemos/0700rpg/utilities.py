import os, pygame
def loadImage(name, folder=os.path.join("data","images"),colorkey=-1):
    fullname = os.path.join(folder, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print "Cannot load image:", fullname
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey)
    return image
