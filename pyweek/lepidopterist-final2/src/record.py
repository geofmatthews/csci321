# Keeping track of records

import random
import settings

heightrecord = 1
comborecord = 1
collected = {}
bank = settings.money0
hiscore = {}
unlocked = 1
maxvisited = 0
seentips = set()

newheightrecord = False
newcomborecord = False
newcollections = []

catchamount = 0
bonusamount = 0

def getstate():
    return heightrecord, comborecord, collected, bank, hiscore, unlocked, maxvisited, seentips

def setstate(state):
    global heightrecord, comborecord, collected, bank, hiscore, unlocked, maxvisited, seentips
    heightrecord, comborecord, collected, bank, hiscore, unlocked, maxvisited, seentips = state

def checkheightrecord(h):
    global heightrecord, newheightrecord, bonusamount
    if int(h) > heightrecord:
        heightrecord = int(h)
        newheightrecord = True
        bonusamount += int(h)
        return int(h)
    return False

def checkcomborecord(c):
    global comborecord, newcomborecord, bonusamount
    if int(c) > comborecord:
        comborecord = int(c)
        newcomborecord = True
        bonusamount += c
        return c
    return False

def getrecords():
    global newheightrecord, newcomborecord, newcollections
    r = []
    if newheightrecord: r.append("New height record!")
    if newcomborecord: r.append("New combo record!")
    for c in newcollections:
        r.append("You caught a|%s!" % c)
    newheightrecord = False
    newcomborecord = False
    newcollections = []
    return r

def checknab(b):
    global collected, newcollections, catchamount
    catchamount += (3 * b.value if settings.easy else b.value)
    if b.name in collected:
        collected[b.name] += 1
    else:
        collected[b.name] = 1
        newcollections.append(b.fullname)
    
def checknabgrounded(b):
    global collected, catchamount
    catchamount += b.value
    if b.name in collected:
        collected[b.name] += 1
        return None
    else:
        collected[b.name] = 1
        return ["You caught a|%s!" % b.fullname]

# Should only be called when a level is actually beaten
def checkhiscore(level):
    global unlocked, hiscore
    unlocked = max(unlocked, level + 1)
    if level not in hiscore or hiscore[level] < catchamount:
        hiscore[level] = catchamount
        return ["New high score!"]
    return []

def gethighscore(level):
    return hiscore[level] if level in hiscore else None

def combinemoney():
    global bank, catchamount, bonusamount
    bank += catchamount + bonusamount
    catchamount = 0
    bonusamount = 0

def visit(level):
    global maxvisited
    maxvisited = max(maxvisited, level)

def checkvisited(level):
    return maxvisited >= level

def gettip(alltips):
    global seentips
    tips = [tip for tip in alltips if tip not in seentips]
    if tips:
        seentips.add(tips[0])
        return tips[0]
    return random.choice(alltips)

def gethcrecord():
    r = []
    if heightrecord > 1: r.append("height record: %sft" % heightrecord)
    if comborecord > 1: r.append("combo record: %sx" % comborecord)
    return "|".join(r)

