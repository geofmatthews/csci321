import pygame, random, math
import player, camera, enviroment, data, monster, pickup, hud, text, music, button
from constants import *
from function import *

def load_level(f):
    planets = []
    planet_dict = {}
    platforms = []
    platform_dict = {}
    monsters = []
    boosters = []
    bullets = []
    player_start = [300,300]
    settings = {'update_all': False, 'song': '4'}
    checkpoints = []
    stars = []
    ports = []
    stables = []
    parts = []
    txt = text.Text()
    img_dict = data.load_images()
    level = data.load_level_file(f)
    level = level.readlines()
    for line in level:
        l = line.split()
        if len(l) == 0:
            continue
        if l[0] == "player":
            player_start = [int(l[1]), int(l[2])]
            checkpoints.insert(0, enviroment.Checkpoint(int(l[1]), int(l[2]), img_dict))
        elif l[0] == "planet":
            planets.append(enviroment.Planet(int(l[1]), int(l[2]), int(l[3]), int(l[4]), int(l[5]), l[6]))
            if len(l) > 7:
                planet_dict[l[7]] = planets[-1]
        elif l[0] == "star":
            stars.append(pickup.Star((int(l[1]), int(l[2])),img_dict))
        elif l[0] == "port":
            ports.append(enviroment.Port(int(l[1]), int(l[2]), l[3] + '.txt', img_dict['port']))
        elif l[0] == "part":
            parts.append(pickup.Part(int(l[1]), int(l[2]), img_dict['parts'][int(l[3])]))
        elif l[0] == "update_all":
            settings['update_all'] = True
        elif l[0] == "song":
            settings['song'] = l[1]
    for line in level:
        l = line.split()
        if len(l) == 0:
            continue
        elif l[0] == "platform":
            if l[1] == 'a':
                platforms.append(enviroment.Platform((int(l[2]), int(l[3])), (int(l[4]), int(l[5])), img_dict, l[6]))
                if len(l) > 7:
                    platform_dict[l[7]] = platforms[-1]
            else:
                platforms.append(enviroment.RelativePlatform(planet_dict[l[2]], int(l[3]), int(l[4]), int(l[5]), int(l[6]), img_dict))
                if len(l) > 7:
                    platform_dict[l[7]] = platforms[-1]
    for line in level:
        l = line.split()
        if len(l) == 0:
            continue
        elif l[0] == "booster":
            if l[1] == 'a':
                boosters.append(enviroment.Booster(img_dict, l[1], planet_dict[l[2]], int(l[3]), int(l[4])))
            else:
                boosters.append(enviroment.Booster(img_dict, l[1], platform_dict[l[2]], int(l[3]), int(l[4])))
        elif l[0] == "O":
            if l[1] == 'a':
                monsters.append(monster.O(l[1], img_dict, planet_dict[l[2]], int(l[3]), int(l[4])))
            else:
                monsters.append(monster.O(l[1], img_dict, platform_dict[l[2]], int(l[3]), int(l[4])))
        elif l[0] == "C":
            if l[1] == 'a':
                monsters.append(monster.C(l[1], img_dict, bullets, planet_dict[l[2]], int(l[3]), int(l[4])))
            else:
                monsters.append(monster.C(l[1], img_dict, bullets, platform_dict[l[2]], int(l[3]), int(l[4])))
        elif l[0] == "I":
            if l[1] == 'a':
                monsters.append(monster.I(l[1], img_dict, planet_dict[l[2]], int(l[3])))
            else:
                monsters.append(monster.I(l[1], img_dict, platform_dict[l[2]], int(l[3])))
        elif l[0] == "eye":
            if l[1] == 'a':
                monsters.append(monster.Eye(l[1], img_dict, planet_dict[l[2]], int(l[3])))
            else:
                monsters.append(monster.Eye(l[1], img_dict, platform_dict[l[2]], int(l[3])))
        elif l[0] == "Q":
            monsters.append(monster.Q(img_dict, bullets, planet_dict[l[1]], int(l[2]), int(l[3]), int(l[4])))
        elif l[0] == 'checkpoint': 
            if l[1] == 'a':
                if len(l) == 4:
                    checkpoints.append(enviroment.RelativeCheckpoint('a', img_dict, planet_dict[l[2]], int(l[3])))
                elif len(l) > 4:
                    checkpoints.append(enviroment.RelativeCheckpoint('a', img_dict, planet_dict[l[2]], int(l[3]), int(l[4])))
            elif l[1] == 'p':
                if len(l) == 4:
                    checkpoints.append(enviroment.RelativeCheckpoint('p', img_dict, platform_dict[l[2]], int(l[3])))
                elif len(l) > 4:
                    checkpoints.append(enviroment.RelativeCheckpoint('p', img_dict, platform_dict[l[2]], int(l[3]), int(l[4])))
            else:
                checkpoints.append(enviroment.Checkpoint(int(l[1]), int(l[2]), img_dict))
        elif l[0] == 'sign': 
            if l[1] == 'a':
                string = ''
                for i in range(len(l)):
                    if i > 4:
                        string += l[i] + ' '
                stables.append(enviroment.RelativeStableObject('a', txt.render(string, (200,200,200)), planet_dict[l[2]], int(l[3]), int(l[4])))
            elif l[1] == 'p':
                string = ''
                for i in range(len(l)):
                    if i > 4:
                        string += l[i] + ' '
                stables.append(enviroment.RelativeStableObject('p', txt.render(string, (200,200,200)), platform_dict[l[2]], int(l[3]), int(l[4])))
            else:
                string = ''
                for i in range(len(l)):
                    if i > 2:
                        string += l[i] + ' '
                stables.append(enviroment.StableObject((int(l[1]), int(l[2])), txt.render(string, (200,200,200))))
    # make gravity circles
    for p in planets:
        c = 2*p.gravity_radius*math.pi
        points = int(round(c/PLANET.POINT_DISTANCE))
        angle_dist = 360/float(points)
        for x in range(points):
            stables.append(enviroment.RelativeStableObject('a', img_dict['dash'], p, x*angle_dist, p.gravity_radius - p.circle.radius - 8))
    return player.Player(player_start, planets, platforms, img_dict), planets, platforms, checkpoints, monsters, boosters, stars, bullets, ports, stables, parts, settings

def start(jukebox, level, first_time = False):
    menu = False
    if level == "menu.txt":
        menu = True
    next_level = None
    pygame.display.set_caption("Moon's moons")
    screen = pygame.display.set_mode((SCREEN.WIDTH, SCREEN.HEIGHT)) #, pygame.FULLSCREEN)
    if first_time and level in STORY:
        story(screen, STORY[level])
    dim = screen.copy().convert_alpha()
    dim.fill((0,0,0,200))
    screen_rect = screen.get_rect()
    background = data.load_image('background.png')

    img_dict = data.load_images()
    overlay = hud.Hud(SCREEN.WIDTH, SCREEN.HEIGHT, img_dict)
    pl, planets, platforms, checkpoints, monsters, boosters, stars, bullets, ports, stables, parts, settings = load_level(level)
    last_checkpoint = checkpoints.pop(0).circle.center
    cam = camera.Camera(pl)
    pl.set_camera(cam)
    decaying = []
    star_counter = 0
    tries = 1
    buttons = []
    buttons.append(button.Button(750, 50, 'esc', data.load_image('cross.png', True), data.load_image('cross_over.png', True)))
    buttons.append(button.Button(680, 50, 'sound', data.load_image('sound.png', True), data.load_image('sound_over.png', True)))
    for c in checkpoints:
        c.update_angle(planets)
    for p in ports:
        p.update_angle(planets)
    jukebox.play_song(settings['song'])
    running = True
    start_time = last_time = pygame.time.get_ticks()
    clock = pygame.time.Clock()
    shown = False
    slowed = False
    won = False
    while running:
        clock.tick(100)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                pl.respawn(last_checkpoint)
            if e.type == pygame.KEYDOWN and e.key == pygame.K_e:
                if shown:
                    shown = False
                else:
                    shown = True
            if e.type == pygame.KEYDOWN and e.key == pygame.K_s:
                if slowed:
                    slowed = False
                else:
                    slowed = True
        time = pygame.time.get_ticks()
        delta = time - last_time
        if slowed:
            delta /= 10
        if delta > 300:
            delta = delta % 300
        external = [0,0]    
        for b in boosters:
            external = sum(external, b.get_force(pl))
        state = pl.update(pygame.key.get_pressed(), delta, external)
        if state == 'dead':
            pl.respawn(last_checkpoint)
            tries += 1
        for m in monsters:
            if settings['update_all']:
                m.update(delta)
            else:
                if m.has_line:
                    point = m.line.start
                else:
                    point = m.circle.center
                if cam.rect.collidepoint(point):
                    m.update(delta)
        for b in bullets:
            b.update(delta)
        for b in boosters:
            b.update(delta)
        
        cam.update()
        last_time = time
        
        screen_rect.x = cam.x/10 + SCREEN.WIDTH/2
        screen_rect.y = cam.y/10 + SCREEN.HEIGHT/2
        screen.blit(background, (0,0), screen_rect)
        for ds in decaying:  
            if ds.update(pl, delta):
                decaying.remove(ds)
            show(ds, screen, cam)
        for s in stars:
            if s.update(pl, delta):
                star_counter += 1
                decaying.append(stars.pop(stars.index(s)))
            show(s, screen, cam)
        for p in parts:
            if p.update(pl, delta):
                decaying.append(parts.pop(parts.index(p)))
            show(p, screen, cam)
            if shown:
                pygame.draw.circle(screen, (150,150,150), cam.shift(p.circle.center), p.circle.radius)
        
        bullets[:] = [b for b in bullets if cam.rect.collidepoint(b.circle.center)]
        blen = len(bullets) - 1
        for b in range(len(bullets)):
            c = False
            for p in planets:
                if p.circle.collide_circle(bullets[blen-b].circle):
                    c = True
                    break
            if not c:
                for p in platforms:
                    if p.line.collide_circle(bullets[blen-b].circle, PLATFORM.BORDER):
                        c = True
                        break
            if c:
                del bullets[blen-b]
        blen = len(bullets) - 1
        for b in range(len(bullets)):
            if bullets[blen-b].circle.collide_circle(pl.circle):
                pl.respawn(last_checkpoint)
                tries += 1
                del bullets[blen-b]
                
                
        ##########################
        ######### DRAW ###########
        ##########################
        for s in stables:
            show(s, screen, cam)
        for p in ports:
            show(p, screen, cam)
            if len(parts) == 0 and p.circle.collide_circle(pl.circle):
                next_level = p.level
                running = False
                won = True
        for b in boosters:
            show(b, screen, cam)
        for c in checkpoints:
            if c.circle.collide_circle(pl.circle) and last_checkpoint != c.circle.center:
                last_checkpoint = c.circle.center
                for cp in checkpoints:
                    cp.uncap()
                c.cap()
            c.update(delta)
            screen.blit(c.image, (c.image_position[0] - cam.x, c.image_position[1] - cam.y))
        for b in bullets:
            show(b, screen, cam)
        for m in monsters:
            kill = False
            if m.has_line:
                if m.line.collide_circle(pl.circle, m.border):
                    kill = True
            else:
                if m.circle.collide_circle(pl.circle):
                    kill = True
            if kill:
                pl.respawn(last_checkpoint)
                tries += 1
            show(m, screen, cam)
            if shown:
                if m.has_line:
                    pygame.draw.line(screen, (150,50,255), cam.shift(m.line.start), cam.shift(m.line.end), m.border*2)
                else:
                    pygame.draw.circle(screen, (150,50,255), cam.shift(m.circle.center), m.circle.radius)
        show(pl, screen, cam)
        if shown:
            pygame.draw.circle(screen, (150,50,255), cam.shift(pl.circle.center), pl.circle.radius)
        for p in planets:
            show(p, screen, cam)
            if shown:
                pygame.draw.circle(screen, (50,150,255), cam.shift(p.circle.center), p.circle.radius)
        for p in platforms:
            screen.blit(p.image, (p.image_position[0] - cam.x, p.image_position[1] - cam.y))
        for b in buttons:
            e = b.update()
            if e == 'esc':
                running = False
            elif e == 'sound':
                jukebox.toggle()
            screen.blit(b.image, b.image_position)
            
        if not menu:
            overlay.update(delta, star_counter, tries)
            screen.blit(overlay.image, (0,0))
        if shown:
            screen.blit(dim, (0,0))
        pygame.display.flip()
    if not menu:
        if won:
            data.save_level(star_counter, tries, level)
        else:
            data.save_level(0, 0, level)
    return next_level
    
def show(obj, screen, cam):
    screen.blit(obj.image, cam.shift(obj.image_position))
    
def story(screen, text_list):
    txt = text.Text()
    running = True
    screen.fill((0,0,0))
    dim = screen.convert()
    text_surf = screen.copy()
    base_surf = text_surf.copy()
    page = 0
    next = True
    alpha = 255
    dim.set_alpha(alpha)
    last_time = pygame.time.get_ticks()
    clock = pygame.time.Clock()
    state = 'darken'
    while running:
        clock.tick(100)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False
            elif e.type == pygame.KEYDOWN:
                state = 'darken'
            elif e.type == pygame.MOUSEBUTTONDOWN:
                state = 'darken'
        time = pygame.time.get_ticks()
        delta = time - last_time
        last_time = time

        if state != 'waiting':
            if state == 'darken':
                alpha += int(delta * 0.2)
                if alpha >= 255:
                    alpha = 255
                    if page == len(text_list):
                        running = False
                    else:
                        y = 0
                        text_surf = base_surf.copy()
                        for line in text_list[page]:
                            t = txt.render(line)
                            text_surf.blit(t, (150,y*40 + 200))
                            y += 1
                        page += 1
                        state = 'lighten'
            elif state == 'lighten':
                alpha -= int(delta * 0.2)
                if alpha <= 0:
                    alpha = 0
                    state = 'waiting'
            dim.set_alpha(alpha)
            screen.blit(text_surf, (0,0))
            screen.blit(dim, (0,0))
            pygame.display.flip()