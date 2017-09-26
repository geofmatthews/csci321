import pygame, math, random
from pygame.locals import *
import data, combo, effect, vista, feat, sprite, settings, record, loadlevel, noise, game

level = 1

def main():
    global level
    pygame.mixer.pre_init(11025, -16, 2, 256)
    pygame.init()
    vista.init()
    noise.init()
    sprite.load()
    level = record.unlocked
    while True:
        if record.maxvisited:
            noise.play("girl")
            worldmap()
            noise.stop()
        if level in (1,4):
            noise.play("gnos")
        if level in (2,5):
            noise.play("one")
        if level in (3,6):
            noise.play("xylo")
        cutscene()
        record.visit(level)
        showtip()
        action()
        game.save()
        effect.savecache()
        if record.unlocked > 6:  # Ending sequence
            level = 7
            cutscene()
            record.unlocked = 6
            level = 6
            game.save()
            theend()
        shop()
        game.save()
        noise.stop()

def worldmap():
    global level
    if settings.unlockall:
        record.unlocked = 6
    vista.mapinit()
    levelnames = ["Stage 1: Mortimer's backyard", "Stage 2: Dojo of the Royal Lepidopteral Society",
        "Stage 3: Bucolic Meadow of Doom", "Stage 4: Some field you have to cross",
        "Stage 5: Imperial palace of|the Royal Society of Lepidopterists",
        "Final stage:|The Lost Buttefly Garden of Verdania"]
    levelps = [(150, 90), (250, 130), (350, 110), (450, 150), (550, 130), (650,170)]
    clock = pygame.time.Clock()
    teffect = effect.LevelNameEffect("")
    speffect = effect.PressSpaceEffect(["Press Space to choose level"])
    speffect.position(vista.screen)
    hseffect = effect.HighScoreEffect("")
    hceffect = effect.HCRecord([record.gethcrecord()])
    hceffect.position(vista.screen)
    updateteffect = True
    udseq = []
    esign = None
    while True:
        dt = clock.tick(60) * 0.001
        if settings.printfps and random.random() < dt:
            print clock.get_fps()

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                exit()
            elif event.type == KEYDOWN and event.key == K_F12:
                pygame.image.save(vista.screen, "screenshot.png")
            elif event.type == KEYDOWN and event.key == K_RIGHT:
                udseq = []
                if level < record.unlocked:
                    level += 1
                    updateteffect = True
            elif event.type == KEYDOWN and event.key == K_LEFT:
                udseq = []
                if level > 1:
                    level -= 1
                    updateteffect = True
            elif event.type == KEYDOWN and event.key in (K_UP, K_DOWN):
                udseq.append(0 if event.key == K_UP else 1)
                if len(udseq) >= 8 and tuple(udseq[-8:]) == (0,0,1,1,0,0,1,1) and not settings.easy:
                    settings.easy = True
                    esign = effect.EasyModeIndicator(["Easy Mode Activated!"])
                    esign.position(vista.screen)
                    udseq = []
                    noise.play("cha-ching")
            elif event.type == KEYDOWN and event.key == K_SPACE:
                return

        if updateteffect:
            teffect.update(levelnames[level-1])
            teffect.position(vista.screen)
            updateteffect = False

        hstext = u"high score: \u00A3%s" % record.hiscore[level] if level in record.hiscore else ""
        hseffect.update(hstext)
        hseffect.position(vista.screen)
        if esign:
            esign.think(dt)

        vista.mapclear()
        for j in range(1,record.unlocked):
            x0, y0 = levelps[j-1]
            x1, y1 = levelps[j]
            vista.line((x0, y0-6), (x1, y1-6), (0,0,0), (200,200,200))
        for p in levelps:
            sprite.frames["leveldisk"].draw(p)
        sprite.frames["stand"].draw(levelps[level-1])
        teffect.draw(vista.screen)
#        speffect.draw(vista.screen)
        hseffect.draw(vista.screen)
        hceffect.draw(vista.screen)
        if esign:
            esign.draw(vista.screen)
        pygame.display.flip()

def cutscene():
    global level
    if record.checkvisited(level) and not (settings.alwaysshow or level == 7):
        return
    clock = pygame.time.Clock()
    dlines = loadlevel.getdialogue(level)
    dialogue = None
    background = pygame.Surface(vista.screen.get_size())
    background.fill((0,0,0))
    def drawbackgroundline(y):
        if speaker == "m":
            r = random.randint(0, 144)
            color = r,r,144
        elif speaker == "e":
            r = random.randint(0, 64)
            color = 192-r,192-2*r,0
        elif speaker == "s":
            r = random.randint(64, 192)
            color = r,r,r
        elif speaker == "v":
            r = random.randint(0,64)
            color = r,128+r,r
        pygame.draw.line(background, color,(0,y),(9999,y))
    speaker = None
    while dlines or dialogue:
        dt = clock.tick(60) * 0.001
        if settings.printfps and random.random() < dt:
            print clock.get_fps()

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN and event.key == K_SPACE:
                dialogue = None
            elif event.type == KEYDOWN and event.key == K_F12:
                pygame.image.save(vista.screen, "screenshot.png")

        if not dialogue:
            if not dlines: return
            newspeaker, _, line = dlines[0].partition("|")
            dialogue = effect.Dialogue(line, newspeaker)
            if newspeaker != speaker:
                speaker = newspeaker
                for y in range(100, 300):
                    drawbackgroundline(y)
            del dlines[0]

        dialogue.think(dt)
        
        for j in range(100):
            if random.random() < dt:
                drawbackgroundline(random.randint(100, 299))

        vista.screen.blit(background, (0,0))
        sprite.frames["head-%s" % speaker].place((0,0))
        dialogue.draw(vista.screen)
        pygame.display.flip()
    

def showtip():
    alltips = open(data.filepath("tips.txt")).readlines()
    alltips = [tip[4:] for tip in alltips if int(tip[0]) <= record.unlocked <= int(tip[2])]
    tiptext = record.gettip(alltips)
    tip = effect.Tip([tiptext])
    clock = pygame.time.Clock()
    while True:
        dt = clock.tick(60) * 0.001
        if settings.printfps and random.random() < dt:
            print clock.get_fps()

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN and event.key in (K_ESCAPE, K_SPACE):
                vista.screen.fill((0,0,0))
                pygame.display.flip()
                return
            elif event.type == KEYDOWN and event.key == K_F12:
                pygame.image.save(vista.screen, "screenshot.png")

        tip.think(dt)

        vista.screen.fill((0,0,0))
        tip.draw(vista.screen)
        pygame.display.flip()
        if not tip: return

def shop():
    # TODO: show species collected
    record.combinemoney()
    vista.mapinit()
    feat.startlevel()
    clock = pygame.time.Clock()
    speffect = effect.PressSpaceEffect(["Press Space to upgrade"])
    speffect.position(vista.screen)
    ueffect = effect.UpgradeTitle(["Upgrade abilities"])
    ueffect.position(vista.screen)
    deffect = effect.ContinueIndicator()
    deffect.position(vista.screen)
    beffect = effect.BankIndicator(record.bank)
    beffect.position(vista.screen)
    pointer = 0
    nfeat = len(feat.known) + 1
    pointerys = [82 + int(32 * j) for j in list(range(len(feat.known))) + [7.5]]
    feats = [f for f in feat.allfeats if f in feat.known]
    pricetags = [effect.CostIndicator(feat.getupgradecost(f), j) for j,f in enumerate(feats)]
    while True:
        dt = clock.tick(60) * 0.001
        if settings.printfps and random.random() < dt:
            print clock.get_fps()

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            elif event.type == KEYDOWN and event.key == K_F12:
                pygame.image.save(vista.screen, "screenshot.png")
            elif event.type == KEYDOWN and event.key == K_UP:
                pointer -= 1
                pointer %= nfeat
            elif event.type == KEYDOWN and event.key == K_DOWN:
                pointer += 1
                pointer %= nfeat
            elif event.type == KEYDOWN and event.key == K_SPACE:
                if pointer == nfeat - 1:
                    return
                cost = feat.getupgradecost(feats[pointer])
                if cost and record.bank >= cost:
                    record.bank -= cost
                    feat.known[feats[pointer]] += 1
                    feat.bars[feats[pointer]] = feat.known[feats[pointer]]
                    pricetags[pointer].update(feat.getupgradecost(feats[pointer]))
                    beffect.update(record.bank)
                    beffect.position(vista.screen)
                    noise.play("cha-ching")

        vista.mapclear()
        feat.draw(shopping = True)
        pygame.draw.circle(vista.screen, (255, 128, 0), (152, pointerys[pointer]), 4)
        if pointer != nfeat - 1:
            speffect.draw(vista.screen)
        deffect.draw(vista.screen)
        beffect.draw(vista.screen)
        ueffect.draw(vista.screen)
        for tag in pricetags: tag.draw(vista.screen)
        pygame.display.flip()

def theend():
    clock = pygame.time.Clock()
    pygame.event.get()
    endthing = effect.Effect(["THE END"])
    total = sum(record.hiscore.values())
    hsthing = effect.HighScoreTotal([u"High score total: \u00A3%s" % total])
    endthing.position(vista.screen)
    hsthing.position(vista.screen)
    while True:
        dt = clock.tick(60) * 0.001
        if settings.printfps and random.random() < dt:
            print clock.get_fps()

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN and event.key in (K_ESCAPE, K_SPACE):
                exit()
            elif event.type == KEYDOWN and event.key == K_F12:
                pygame.image.save(vista.screen, "screenshot.png")
        vista.screen.fill((0,0,0))
        endthing.draw(vista.screen)
        hsthing.draw(vista.screen)
        pygame.display.flip()



# TODO: show level goal
def action():
    global level
    vista.levelinit(level)

    butterflies, goal, timeout = loadlevel.load(level)

    clock = pygame.time.Clock()
    facingright = True
    x, y, g, vy = 200, 0, (250 if settings.easy else 500), 0
    leapvx, leapvy = 200., 200.
    twirlvy = 200.
    nabvx = 400.
    runvx = 300.
    rollvx, rollvy = 250., 250.
    dartvx, dartvy = 250., 300.
    boundvx, boundvy = -100., 250.
    nabtick, nabtime = 0, 0.25
    nabradius = 50
    twirlradius = 80
    rollradius = 80
    leaping = 0
    runtick = 0
    twirltick = 0
    rolltick = 0
    currentfeat = ""
    combocount = 0
    grounded = True
    paused = False
    title = effect.Effect(["READY", "SET", "COLLECT"])
    endtitle = True
    ending = False
    effects = []
    heffect = effect.HeightIndicator()
    ceffect = effect.ComboIndicator()
    peffect = effect.ProgressIndicator(goal)
    cdeffect = effect.CountdownIndicator(timeout)
    seffect = effect.StageNameEffect(level, goal, timeout)
    feat.startlevel()
    pygame.event.get()
    while True:
        dt = clock.tick(60) * 0.001
        if settings.printfps and random.random() < dt:
            print clock.get_fps()

        if paused:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    ending = True
                    endtitle = None
                    feat.checknewfeat(len(record.collected))
                    if record.catchamount >= goal:
                        unlocked = record.unlocked
                        record.checkhiscore(level)
                        if record.unlocked > unlocked:
                            level = record.unlocked
                    paused = False
                elif event.type == KEYDOWN and event.key == K_F12:
                    pygame.image.save(vista.screen, "screenshot.png")
                elif event.type == KEYDOWN and event.key == K_RETURN:
                    paused = False
            vista.screen.blit(pausescreen, (0,0))
            pygame.display.flip()
            continue
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                paused = True
                pausescreen = pygame.Surface(vista.screen.get_size()).convert_alpha()
                fade = pygame.Surface(vista.screen.get_size()).convert_alpha()
                fade.fill((0,0,0,128))
                pausescreen.blit(vista.screen,(0,0))
                pausescreen.blit(fade,(0,0))
                pausetitle = effect.PauseTitle(["PAUSED"])
                pauseinfo = effect.PauseInfo(["Press Enter to resume|or Esc to exit level"])
                pausetitle.position(pausescreen)
                pauseinfo.position(pausescreen)
                pausetitle.draw(pausescreen)
                pauseinfo.draw(pausescreen)
            elif event.type == KEYDOWN and event.key == K_F12:
                pygame.image.save(vista.screen, "screenshot.png")
            elif event.type == KEYDOWN and event.key == K_TAB:
                settings.hidefeatnames = not settings.hidefeatnames
                feat.startlevel(False)

        k = pygame.key.get_pressed()
        kcombo = combo.check(k)

        if grounded:
            dx = 0
            if k[K_RIGHT]:
                dx += runvx * dt
            if k[K_LEFT]:
                dx -= runvx * dt
            if nabtick:
                dx = 0

            if not cdeffect:
                dx = 0
                kcombo = ""

            if dx:
                facingright = dx > 0
                currentfeat = "run"
                x += dx
            elif not nabtick:
                currentfeat = ""

            if kcombo == "leap" and "leap" in feat.known:
                if feat.attempt("leap"):
                    vx = leapvx if facingright else -leapvx
                    vy = leapvy
                    combocount = 1
                    grounded = False
                    currentfeat = "leap"
                    noise.play("hop")
            elif kcombo == "twirl" and "twirl" in feat.known:
                if feat.attempt("twirl"):
                    combocount = 1
                    grounded = False
                    currentfeat = "twirl"
                    vx = 0
                    vy = twirlvy
                    twirltick = 1
                    noise.play("rotor")
            elif kcombo == "nab" and "nab" in feat.known:
                if feat.attempt("nab"):
                    currentfeat = "nab"
                    nabtick = nabtime
                    noise.play("woosh")
            elif kcombo == ("roll-r" if facingright else "roll-l") and "roll" in feat.known:
                if feat.attempt("roll"):
                    grounded = False
                    currentfeat = "roll"
                    vx = (rollvx if facingright else -rollvx)
                    vy = rollvy
                    combocount = 1
                    rolltick = 1
                    twirltick = 0
                    noise.play("rotor")
            elif kcombo == ("dart-r" if facingright else "dart-l") and "dart" in feat.known:
                if feat.attempt("dart"):
                    grounded = False
                    currentfeat = "dart"
                    vx = (dartvx if facingright else -dartvx)
                    vy = dartvy
                    combocount = 1
                    rolltick = 0
                    twirltick = 0
                    noise.play("hop")
            elif kcombo == ("dart-l" if facingright else "dart-r") and "bound" in feat.known:
                if feat.attempt("bound"):
                    grounded = False
                    currentfeat = "bound"
                    vx = (boundvx if facingright else -boundvx)
                    vy = boundvy
                    combocount = 1
                    rolltick = 0
                    twirltick = 0
                    noise.play("hop")
        else:
            if kcombo == "leap" and "leap" in feat.known:
                if feat.attempt("leap"):
                    vx = leapvx if facingright else -leapvx
                    vy = leapvy
                    combocount += 1
                    currentfeat = "leap"
                    twirltick = 0
                    noise.play("hop")
            elif kcombo == ("turn-r" if facingright else "turn-l") and "turn" in feat.known:
                if feat.attempt("turn"):
                    facingright = not facingright
                    vx = leapvx if facingright else -leapvx
                    vy = leapvy
                    combocount += 1
                    twirltick = 0
                    rolltick = 0
                    currentfeat = "leap"
                    noise.play("hop")
            elif kcombo == "nab" and "nab" in feat.known:
                if feat.attempt("nab"):
                    currentfeat = "nab"
                    nabtick = nabtime
                    vx = nabvx if facingright else -nabvx
                    combocount += 1
                    twirltick = 0
                    rolltick = 0
                    noise.play("woosh")
            elif kcombo == "twirl" and "twirl" in feat.known:
                if feat.attempt("twirl"):
                    currentfeat = "twirl"
                    vx = 0
                    vy = twirlvy
                    combocount += 1
                    twirltick = 1
                    rolltick = 0
                    noise.play("rotor")
            elif kcombo == ("roll-r" if facingright else "roll-l") and "roll" in feat.known:
                if feat.attempt("roll"):
                    currentfeat = "roll"
                    vx = (rollvx if facingright else -rollvx)
                    vy = rollvy
                    combocount += 1
                    rolltick = 1
                    twirltick = 0
                    noise.play("rotor")
            elif kcombo == ("dart-r" if facingright else "dart-l") and "dart" in feat.known:
                if feat.attempt("dart"):
                    currentfeat = "dart"
                    vx = (dartvx if facingright else -dartvx)
                    vy = dartvy
                    combocount += 1
                    rolltick = 0
                    twirltick = 0
                    noise.play("hop")
            elif kcombo == ("dart-l" if facingright else "dart-r") and "bound" in feat.known:
                if feat.attempt("bound"):
                    currentfeat = "bound"
                    vx = (boundvx if facingright else -boundvx)
                    vy = boundvy
                    combocount += 1
                    rolltick = 0
                    twirltick = 0
                    noise.play("hop")

            if nabtick:
                x += vx * dt
            else:
                x += vx * dt
                y += vy * dt - 0.5 * g * dt ** 2
                vy -= g * dt
            if y < 0:
                y = 0
                vy = 0
                grounded = True
                combocount = 0
                feat.land()
                ach = record.getrecords()
                if ach: effects.append(effect.AchievementEffect(ach))
                currentfeat = ""
                twirltick = 0
                rolltick = 0

        x, y = vista.constrain(x, y, 30)

        nx, ny, nr = None, None, None
        if nabtick:
            nabtick = max(nabtick - dt, 0)
            if not nabtick:
                currentfeat = "" if grounded else "leap"
            nx, ny = x + (40 if facingright else -40), y + 80
            nr = nabradius
        elif currentfeat == "twirl":
            nx, ny = x, y + 80
            nr = twirlradius
        elif currentfeat == "roll":
            nx, ny = x, y + 50
            nr = rollradius
        if nx is not None:
            for b in list(butterflies):
                adx, ady = b.x - nx, b.y - ny
                if adx ** 2 + ady ** 2 < nr ** 2:
                    b.nabbed = True
                    butterflies.remove(b)
                    value = 3 * b.value if settings.easy else b.value
                    effects.append(effect.NabBonusIndicator(value, (b.x, b.y)))
                    if grounded:
                        ach = record.checknabgrounded(b)
                        if ach:
                            effects.append(effect.AchievementEffect(ach))
                    else:
                        record.checknab(b)

        heffect.update(y/25.)
        heffect.position(vista.screen)
        ceffect.update(combocount)
        ceffect.position(vista.screen)
        peffect.update(record.catchamount)
        cdeffect.position(vista.screen)

        hbonus = record.checkheightrecord(y/25.)
        if hbonus:
            effects.append(effect.HeightBonusIndicator(hbonus))
        cbonus = record.checkcomborecord(combocount)
        if cbonus:
            effects.append(effect.ComboBonusIndicator(cbonus))

        if currentfeat == "leap":
            picname = "run2"
        elif currentfeat == "run":
            picname = ("run0", "run1", "run2", "run1")[int(4 * runtick / 0.5)]
            runtick += dt
            runtick %= 0.5
        elif currentfeat == "nab":
            picname = ("nab3", "nab2", "nab1", "nab0")[int(4. * nabtick / nabtime)]
            if not grounded:
                picname = "sky" + picname
        elif currentfeat == "twirl":
            twirltick += dt
            picname = ("twirl0", "twirl1", "twirl2", "twirl3")[int(4 * twirltick / 0.25) % 4]
        elif currentfeat == "roll":
            rolltick += dt
            picname = "roll%s" % (int(8 * rolltick / 0.35) % 8)
        elif currentfeat == "dart":
            picname = "dart"
        elif currentfeat == "bound":
            picname = "bound"
        else:
            picname = "stand"
        if "twirl" not in picname and not facingright:
            picname = picname + "-b"
        vista.position((x, y), facingright, vy)

        butterflies += loadlevel.newbutterflies(level, dt)
        
        feat.think(dt)
        vista.think(dt)
        for b in butterflies: b.think(dt)
        seffect.think(dt)
        if not seffect:
            title.think(dt)
        for e in effects:
            e.think(dt)
        effects = [e for e in effects if e]
        ceffect.think(dt)
        if not title:
            cdeffect.think(dt)
        if grounded and not cdeffect and not effects and not ending:
            ending = True
            if record.catchamount >= goal:
                w = ["Stage complete!"]
                unlocked = record.unlocked
                w += record.checkhiscore(level)
                if record.unlocked > unlocked:
                    level = record.unlocked
            else:
                w = ["Stage incomplete"]
            w += feat.checknewfeat(len(record.collected))
            endtitle = effect.EndEffect(w)
        if ending and endtitle:
            endtitle.think(dt)
            
        
        vista.clear()
        sprite.frames[picname].draw((x, y))
        for b in butterflies:
            b.draw()
        if nr is not None and settings.showdots:
            vista.circle((int(nx), int(ny)), int(nr))
        feat.draw(facingright=facingright)
        heffect.draw(vista.screen)
        ceffect.draw(vista.screen)
        cdeffect.draw(vista.screen)
        peffect.draw(vista.screen)
        for e in effects:
            e.draw(vista.screen)
        seffect.draw(vista.screen)
        if not seffect:
            title.draw(vista.screen)
        if ending and endtitle:
            endtitle.draw(vista.screen)
        pygame.display.flip()
        if not endtitle:
            return

