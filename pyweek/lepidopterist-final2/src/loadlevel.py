# Level loading, duh

import random
import sprite, data, settings

levelset = {}
levelset[1] = dict((
  (sprite.BlueButterfly, 8),
  (sprite.YellowButterfly, 8),
  (sprite.RedButterfly, 8),
))
levelset[2] = dict((
  (sprite.YellowButterfly, 8),
  (sprite.WhiteButterfly, 8),
  (sprite.PurpleButterfly, 8),
))
levelset[3] = dict((
  (sprite.BlueButterfly, 6),
  (sprite.RedButterfly, 6),
  (sprite.WhiteButterfly, 6),
  (sprite.GreenButterfly, 8),
  (sprite.BlueFairy, 6),
))
levelset[4] = dict((
  (sprite.YellowButterfly, 6),
  (sprite.WhiteButterfly, 6),
  (sprite.GreyButterfly, 6),
  (sprite.BlueFairy, 6),
  (sprite.RedFairy, 6),
))
levelset[5] = dict((
  (sprite.RedButterfly, 4),
  (sprite.WhiteButterfly, 6),
  (sprite.GreyButterfly, 10),
  (sprite.GreenFairy, 12),
))
levelset[6] = dict((
  (sprite.BlueButterfly, 8),
  (sprite.YellowButterfly, 8),
  (sprite.RedButterfly, 8),
  (sprite.WhiteButterfly, 8),
  (sprite.GreyButterfly, 8),
  (sprite.PurpleButterfly, 8),
  (sprite.GreenButterfly, 8),
  (sprite.BlueFairy, 8),
  (sprite.RedFairy, 8),
  (sprite.GreenFairy, 8),
))

def load(level):
    if not 1 <= level <= 6:
        return [], 0, 0
    if level == 1:
        goal = 12
        timeout = 60
    if level == 2:
        goal = 40
        timeout = 60
    if level == 3:
        goal = 100
        timeout = 90
    if level == 4:
        goal = 250
        timeout = 120
    if level == 5:
        goal = 300
        timeout = 60
    if level == 6:
        goal = 600
        timeout = 90
        
    butterflies = []
    for kind, number in levelset[level].items():
        butterflies += [kind() for j in range(number)]

    return butterflies, goal, timeout

def newbutterflies(level, dt):
    if not 1 <= level <= 6: return []
    newbs = []
    for kind, number in levelset[level].items():
        if random.uniform(0, (60. if settings.easy else 120.)/number) < dt:
            newbs.append(kind())
    return newbs

def getbox(level):
    if level == 1:
        return 0, 1000, -40, 600
    if level == 2:
        return 0, 800, -40, 1000
    if level == 3:
        return 0, 1400, -40, 1200
    if level == 4:
        return 0, 1400, -40, 1200
    if level == 5:
        return 0, 800, -40, 1600
    if level == 6:
        return 0, 1000, -40, 2000
    return 0, 1000, -40, 600

def getdialogue(level = ""):
    lines = [line.strip() for line in open(data.filepath("dialogue.txt")) if line.startswith(str(level))]
    return [line.partition("|")[2] for line in lines if line]


