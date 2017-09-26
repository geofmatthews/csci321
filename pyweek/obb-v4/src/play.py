import pygame, random
from pygame.locals import *
import vista, context, body, settings, panel, status, noise, twinkler, enemy, graphics, tip, mechanics

class Play(context.Context):
    def __init__(self):
        self.body = body.Body()
        self.panel = panel.Panel(self.body)
        self.status = status.Status(self.body)
        self.edgepoint = None
        self.twinklers = []
        self.shots = []
        self.paused = False
        self.target = None
        self.healmode = False
        self.clearselections()
        self.clickat = None

    def __getstate__(self):
        d = dict(self.__dict__)
        d["paused"] = False
        d["pscreen"] = None
        return d

    def think(self, dt, events, keys, mousepos, buttons):

        if self.paused:
            if any(e.type == KEYDOWN or e.type == MOUSEBUTTONDOWN for e in events):
                self.resume()
            return


        if vista.vrect.collidepoint(mousepos):
            edge = vista.grid.nearestedge(vista.screentoworld(mousepos))
            if edge != self.edgepoint:
                if self.panel.selected is not None:
                    appspec = self.panel.tiles[self.panel.selected]
                    self.parttobuild = self.body.canplaceapp(edge, appspec)
                elif self.status.selected is not None:
                    otype = self.status.selected
                    self.parttobuild = self.body.canplaceorgan(edge, otype)
                if self.parttobuild is not None:
                    worldpos = vista.HexGrid.edgeworld(*edge)
                    visible = self.body.mask.isvisible(worldpos)
                    self.canbuild = self.body.canaddpart(self.parttobuild) and visible
                    self.parttobuild.status = "ghost" if self.canbuild else "badghost"
        else:
            edge = None
            self.parttobuild = None
        self.edgepoint = edge

        for event in events:
            if event.type == KEYDOWN and event.key == K_SPACE:
                if settings.debugkeys:
                    self.body.addrandompart()
            if event.type == KEYDOWN and event.key == K_BACKSPACE:
                if settings.debugkeys:
                    self.body.addrandompart(20)
            if event.type == KEYDOWN and event.key == K_v:
                if settings.debugkeys:
                    wpos = vista.screentoworld(mousepos)
                    print "Visibility:", self.body.mask.visibility(wpos)
            if event.type == KEYUP and event.key == K_x:
                if settings.debugkeys:
                    if self.target is not None:
                        self.target.die()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                self.clickat = event.pos
            if event.type == MOUSEBUTTONUP and event.button == 1:
                self.handleleftclick(mousepos)
            if event.type == MOUSEBUTTONUP and event.button == 3:
                self.handlerightclick(mousepos)
            if event.type == MOUSEBUTTONUP and event.button == 4 and settings.zoomonscroll:
                vista.zoomin()
            if event.type == MOUSEBUTTONUP and event.button == 5 and settings.zoomonscroll:
                vista.zoomout()
            if event.type == MOUSEMOTION and event.buttons[0]:
                self.handleleftdrag(event.pos, event.rel)

        if settings.showtips:
            tip.settip(self.choosetip(mousepos))

        if keys[K_F5] and settings.debugkeys:
            self.body.addrandompart()

        if (keys[K_x] and settings.debugkeys) or self.cutmode:
            newtarget = self.pointchildbyedge(mousepos)
            if newtarget != self.target:
                if self.target is not None:
                    self.target.setbranchstatus()
                self.target = newtarget
                if self.target is not None:
                    self.target.setbranchstatus("target")
        elif self.healmode:
            self.body.sethealstatus()
            self.target = self.body.nearestorgan(vista.screentoworld(mousepos))
        elif self.target is not None:
            self.target.setbranchstatus()
            self.target = None

        vista.think(dt, mousepos, keys)
        vista.icons["cut"].selected = self.cutmode
        vista.icons["heal"].selected = self.healmode

        self.body.think(dt, self.status.healmeter)
        self.panel.think(dt)
        self.status.think(dt, mousepos)
        self.twinklers += twinkler.newtwinklers(self.body.mask, dt)
        for t in self.twinklers:
            t.think(dt)
        self.twinklers = [t for t in self.twinklers if t.alive()]
        self.body.claimtwinklers(self.twinklers)
        self.body.attackenemies(self.shots)
        if random.random() < dt:
            self.shots += enemy.newshots(self.body)
        for s in self.shots: s.think(dt)
        self.shots = [s for s in self.shots if s.alive()]
        self.status.setheights(self.body.maxmutagen, self.body.maxplaster)
        self.status.mutagenmeter.amount += self.body.checkmutagen()
        self.status.healmeter.amount += self.body.checkplaster()
        tip.think(dt)
        self.twinklers += enemy.spoils
        del enemy.spoils[:]
        self.shots += enemy.spawnedshots
        del enemy.spawnedshots[:]

    def pause(self):
        self.paused = True
        self.pscreen = graphics.ghostify(vista._screen)
        noise.pause()

    def resume(self):
        self.paused = False
        self.pscreen = None
        noise.resume()

    def clearselections(self, clearpanel = True, clearstatus = True, clearheal = True, clearcut = True):
        if self.target is not None:
            self.target.setbranchstatus()
        self.target = None
        self.parttobuild = None
        self.iconclicked = None
        if clearpanel:
            self.panel.selecttile()
        if clearstatus:
            self.status.select()
        if clearheal:
            if self.healmode:
                self.body.core.setbranchstatus()
            self.healmode = False
        if clearcut:
            self.cutmode = False

    def handleleftclick(self, mousepos):

        if self.clickat is None:  # It's a drag
            return
        (x0, y0), (x1, y1) = self.clickat, mousepos
        if abs(x0-x1) + abs(y0-y1) > 25:
            return
    
        bicon = self.status.iconpoint(mousepos)  # Any build icons pointed to
        vicon = vista.iconhit(mousepos)  # Any vista icons pointed to
        if vicon == "trash":
            if self.panel.selected is not None:
                self.panel.claimtile()
                noise.play("trash")
            self.clearselections()
        elif vicon == "zoomin":
            vista.zoomin()
        elif vicon == "zoomout":
            vista.zoomout()
        elif vicon == "pause":
            self.pause()
        elif vicon == "music":
            noise.nexttrack()
        elif vicon == "heal":
            self.body.core.setbranchstatus()
            if self.healmode:
                self.clearselections()
            else:
                self.clearselections()
                if vista.icons["heal"].active:
                    self.healmode = True
        elif vicon == "cut":
            if self.cutmode:
                self.clearselections()
            else:
                self.clearselections()
                if vista.icons["cut"].active:
                    self.cutmode = True
        elif vista.prect.collidepoint(mousepos):  # Click on panel
            self.clearselections(clearpanel = False)
            jtile = self.panel.iconp(mousepos)
            if jtile in (None, 0, 1, 2, 3, 4, 5):
                self.panel.selecttile(jtile)
        elif bicon is not None:
            self.clearselections(clearstatus = False)
            self.status.select(bicon.name)
        elif vista.vrect.collidepoint(mousepos):
            if self.cutmode and self.target is not None:
                self.target.die()
                self.clearselections()
            elif self.healmode and self.target is not None:
                self.target.autoheal = not self.target.autoheal
            elif self.parttobuild is not None and self.canbuild and self.body.canaddpart(self.parttobuild):
                if self.panel.selected is not None:
                    self.panel.claimtile()
                if self.status.selected is not None:
                    self.status.build()
                self.body.addpart(self.parttobuild)
                self.clearselections()
            else:
                worldpos = vista.screentoworld(mousepos)
                if vista.HexGrid.nearesttile(worldpos) == (0,0):
                    settings.showtips = not settings.showtips
                    noise.play("addpart")


    def choosetip(self, mousepos):
        bicon = self.status.iconpoint(mousepos)  # Any build icons pointed to
        vicon = vista.iconhit(mousepos)  # Any vista icons pointed to
        if vicon == "trash":
            if self.panel.selected is not None:
                return "click this to get rid of stalk and get new one"
            else:
                return "if you no like a stalk, click on stalk then click here to get new one. or you can right-click on stalk, it faster"
        elif vicon == "zoomin":
            return
        elif vicon == "zoomout":
            return
        elif vicon == "pause":
            return "click to pause game. it okay. me wait"
        elif vicon == "music":
            return "click to hear new song or turn off"
        elif vicon == "heal":
            if self.healmode:
                return "click on organs to change them so they don't heal by self. no want to waste ooze on non-vital organs"
            return "me organs will use ooze to heal when they get hurt. if you want some organs not to take ooze, click here to change them"
        elif vicon == "cut":
            return "no like a stalk or a organ on me body? use this to get rid of it! it okay, me not get hurt"
        elif vista.prect.collidepoint(mousepos):
            jtile = self.panel.iconp(mousepos)
            if jtile in (0, 1, 2, 3, 4, 5):
                return "these me stalk options, har har har! can grow stalks where colors match. try make lots of branches."
            else:
                return self.panel.choosetip(mousepos)
        elif bicon is not None:
            return mechanics.info[bicon.name]
        elif vista.vrect.collidepoint(mousepos):
            worldpos = vista.screentoworld(mousepos)
            if vista.HexGrid.nearesttile(worldpos) == (0,0):
                return "click me mouth to turn me tips on or off"
            organ = self.body.nearestorgan(worldpos)
        elif vista.rrect.collidepoint(mousepos):
            return self.status.choosetip(mousepos)

    def handlerightclick(self, mousepos):
        if vista.prect.collidepoint(mousepos):  # Click on panel
            self.clearselections()
            if settings.trashonrightclick:
                jtile = self.panel.iconp(mousepos)
                if jtile in (0, 1, 2, 3, 4, 5):
                    self.panel.selecttile(jtile)
                    self.panel.claimtile()
                    noise.play("trash")
        elif vista.vrect.collidepoint(mousepos):  # Click on main window
            if settings.panonrightclick:
                vista.jumptoscreenpos(mousepos)
            else:
                self.clearselections()

    def handleleftdrag(self, pos, rel):
        if self.clickat is not None:
            (x0, y0), (x1, y1) = self.clickat, pos
            if abs(x0-x1) + abs(y0-y1) > 25:
                self.clickat = None

        if settings.panondrag:
            if vista.vrect.collidepoint(pos):
                vista.scoot(rel)


    def pointchildbyedge(self, screenpos):
        edge = vista.grid.nearestedge(vista.screentoworld(screenpos))
        edge = vista.grid.normedge(*edge)
        if edge not in self.body.takenedges:
            return None
        parent = self.body.takenedges[edge]
        if edge not in parent.buds:
            edge = vista.grid.opposite(*edge)
        return parent.buds[edge]
        

    def draw(self):
        if self.paused:
            vista._screen.blit(self.pscreen, (0,0))
            pygame.display.flip()
            return
        vista.clear()
        if self.panel.selected is not None or self.status.selected is not None:
            self.body.tracehexes()
        self.body.draw()
        if self.parttobuild is not None:
            self.parttobuild.draw()
        for t in self.twinklers: t.draw()
        for s in self.shots: s.draw()
        vista.addmask(self.body.mask)
        self.panel.draw()
        self.status.draw()
        vista.flip()


