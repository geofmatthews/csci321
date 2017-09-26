import pygame, os, re, glob

def ReinerAnimation(animfolder, datafolder='data'):
    """
    A function to load animated sprites from Reiner's tilesets.

    The datafolder is a folder for resources.
    
    The animfolder is a folder name such as 'T_bowstan'
    or 'T grey wolf'.  All files in these folders (and their
    subfolders) are searched for anything matching the pattern:
        aname + s|sw|w|... + 0000.bmp
    where the aname is the animation name, the 's'... is
    the heading, and the 0000 is the frame index.
    Some file names have no heading, these are dealt with
    as described below.
    
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
    In this case, the image index is converted to the heading,
    and only 0 is used as an image index.

    Other such "no heading" files are special purpose,
    such as bowstan's "arrow" and the crow's "falling"
    sprites.  These have no headings, but are still meant to be
    a single animation, not a set of separate stills.
    If there are not 8 of these, it assumes
    it's one of these and stores them all under the 's'
    heading.  In this case, the animation name is stored
    in the list noheadings, and, the 's' animation is
    then copied to all other headings after the files
    have been traversed, so that changing the heading
    in the resulting animation has no effect.

    There are also some which have headings but no
    image index.  These are also stills and handled appropriately
    by adding an index=0.

    There are some insuperable problems.  For example, some
    files numbered 0000...0007 are NOT in the 's' 'sw'... order.
    crow dead and crow stopped, for example.  I renamed these
    dead s.bmp ...
    """
    folder = os.path.join(datafolder, animfolder)
    # Find the names Reiner used for his actions
    # This will find them automatically from his filenames,
    # and store them under their (stripped) names in the animations
    # dictionary
    anamepat = '(.*?)'
    headings = ['s','sw','w','nw','n','ne','e','se']
    headingpat = '(' + '|'.join([' '+h for h in headings]) + ')'
    digitpat = '(\d\d\d\d)'
    extensionpat = '(.bmp)$'

    actionpattern = anamepat + headingpat + digitpat + extensionpat
    actionpattern = re.compile(actionpattern)
    
    animationpattern = anamepat + digitpat + extensionpat
    animationpattern = re.compile(animationpattern)
    
    noindexpattern = anamepat + headingpat + extensionpat
    noindexpattern = re.compile(noindexpattern)
    
    animations = {}
    noheadings = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            m = animationpattern.match(file)
            a = actionpattern.match(file)
            n = noindexpattern.match(file)
            if m or n:
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
                            ## animated, use 's' heading
                            heading = 's'
                elif n:
                    aname = n.group(1).strip()
                    heading = n.group(2).strip()
                    index = 0
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
    # copying 's' animation to all other headings.  Assumes
    # there is an 's' animation
    for anim in animations:
        for heading in headings:
            if heading != 's' and not heading in animations[anim]:
                animations[anim][heading] = animations[anim]['s']
            
    return animations

