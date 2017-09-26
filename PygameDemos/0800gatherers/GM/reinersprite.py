import pygame, os, re, glob

def ReinerSprite(animfolder, datafolder='data'):
    """
    A function to load animated sprites from Reiner's tilesets.
    Images are returned in nested dictionaries as
        animations[action][heading][index]
    The headings are 's', 'sw', 'w' etc.
    The action names are whatever Reiner called them in the folder.
    Some of them may be in German.  To see what they are just
    ask for
        animations.keys()
    This class assumes that file names without headings and
    exactly 8 subimages are 'stills',
    usually s, sw, w, ... se, and numbered 0, 1, 2 ... 7

    Other such "no heading" files are special purpose,
    such as bowstan's "arrow" and the crow's "falling"
    sprites.  If there are not 8 of these, it assumes
    it's one of these and stores them all under the 's'
    heading.  In this case, the animation name is stored
    in the list noheadings, and, the 's' animation is
    then copied to all other headings after the files
    have been traversed.
    """
    folder = os.path.join(datafolder, animfolder)
    # Find the names Reiner used for his actions
    # This will find them automatically from his filenames,
    # and store them under their (stripped) names in the animations
    # dictionary
    headings = ['s','sw','w','nw','n','ne','e','se']
    headingpattern = '(' + '|'.join([' '+h for h in headings]) + ')'
    actionpattern = '(.*?)' + headingpattern + '(\d\d\d\d)(.bmp)$'
    actionpattern = re.compile(actionpattern)
    animationpattern = '(.*?)(\d\d\d\d)(.bmp)$'
    animationpattern = re.compile(animationpattern)
    animations = {}
    noheadings = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            m = animationpattern.match(file)
            a = actionpattern.match(file)
            if m:
                # Find name, heading, and index from filename:
                if a:
                    aname = a.group(1).strip()
                    heading = a.group(2).strip()
                    index = int(a.group(3))
                else:
                    aname = m.group(1).strip()
                    index = int(m.group(2))
                    # No headings.  Find out if there are 8 of them:
                    pattern = os.path.join(root, aname + '*.*')
                    matchingfiles = glob.glob(pattern)
                    if len(matchingfiles) == 8:
                    ## nonanimated images, but assume
                    ## numbered 0,1,2,... = s,sw,w,...
                        heading = {0:'s',1:'sw',2:'w',3:'nw',
                                   4:'n',5:'ne',6:'e',7:'se'}[index%8]
                        index = 0
                    else:
                        noheadings.append(aname)
                        heading = 's'
                # If no dictionary entry yet, add it:
                if not aname in animations:
                    animations[aname] = {}
                if not heading in animations[aname]:
                    animations[aname][heading] = {}
                # Load the image
                fullname = os.path.join(root, file)
                try:
                    image = pygame.image.load(fullname)
                except pygame.error, message:
                    print 'Cannot load image: ', fullname
                    raise SystemExit, message
                image.convert()
                image.set_colorkey(image.get_at((0,0)))
                animations[aname][heading][index] = image
    # Finished walking through folders, fix up noheadings by
    # copying 's' animation to all other headings.
    for aname in noheadings:
        for heading in headings[1:]:
            animations[aname][heading] = animations[aname]['s']
            
    return animations

