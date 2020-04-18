from moveableobject import MoveableObject
from bullet import Bullet
from constants import SCREENW, SCREENH, PLAYERHEALTH, UP, LEFT, RIGHT, PLAYERSPEED
from statusmodifiers import StatusModifier
from loadstaticres import bulletimg
from boss import Boss
from endgamesignal import EndLevel
import pygame


class Player(MoveableObject):
    def __init__(self, img, eventqueue):
        MoveableObject.__init__(self, SCREENW / 2, 450, PLAYERSPEED, img)
        self.health = PLAYERHEALTH
        self.spawnX = self.x
        self.spawnY = self.y
        # bamf mode - shoot three bullets at a time
        self.bamfmode = False

        # for more precise keyboard input
        self.goright = False
        self.goleft = False
        self.goup = False
        self.godown = False

        # for processing input events
        self.eventqueue = eventqueue
        self.statmods = []

    def update(self):
        super().update()

        # handle user input
        while not self.eventqueue.empty():
            event = self.eventqueue.get_nowait()

            if not hasattr(event, 'key'):
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.x >= 0:
                    self.goleft = True
                elif event.key == pygame.K_RIGHT and self.x + self.width <= SCREENW:
                    self.goright = True
                elif event.key == pygame.K_UP and self.y >= 0:
                    self.goup = True
                elif event.key == pygame.K_DOWN and self.y + self.height <= SCREENH:
                    self.godown = True
                elif event.key == pygame.K_SPACE:
                    self.fire(bulletimg)
                    if self.bamfmode:
                        self.fire(bulletimg, LEFT)
                        self.fire(bulletimg, RIGHT)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.goleft = False
                elif event.key == pygame.K_RIGHT:
                    self.goright = False
                elif event.key == pygame.K_UP:
                    self.goup = False
                elif event.key == pygame.K_DOWN:
                    self.godown = False

        # for smoothness and border checks
        # todo: normalize diagonals
        distance = self.speed * self.frame_tick
        if self.goright == True and self.x + self.width <= SCREENW:
            self.x += distance
        elif self.goleft == True and self.x >= 0:
            self.x -= distance
        if self.goup == True and self.y >= 0:
            self.y -= distance
        elif self.godown == True and self.y + self.height <= SCREENH:
            self.y += distance

        # handle status modifiers
        # [:] to iterate over copy of list (can remove from tick() Event handling)
        for mod in self.statmods[:]:
            mod.timer.tick()

    def fire(self, img, turret=UP):
        if turret == UP:
            bullet = Bullet(self.x + (self.image.get_width() / 2), self.y - 10, img, UP)
        if turret == LEFT:
            bullet = Bullet(self.x + 15, self.y + 40, img, UP)
        if turret == RIGHT:
            bullet = Bullet(self.x + self.image.get_width() - 15, self.y + 40, img, UP)
        # todo: ensure bullet always has a value
        self.notify("fire", bullet=bullet)

    def die(self):
        self.health -= 1
        self.start_exploding()
        self.notify("alterhealth", value=-1)

    def oneup(self):
        self.health += 1
        self.notify("alterhealth", value=1)

    def respawn(self):
        if self.health <= 0:
            self.x = -2000
            self.y = -2000
            self.speed = 0
            raise EndLevel("failure")
        else:
            self.x = self.spawnX
            self.y = self.spawnY
            self.speed = PLAYERSPEED
            self.image = self.orig_image
            self.bamfmode = False

    def update_explosion(self, event):
        if super().update_explosion(event):
            self.respawn()

    def on_collide(self, event):
        if event.kwargs.get("who") == self:
            if isinstance(event.source, StatusModifier):
                event.source.payload(self)
                event.source.subscribe("timeout", self.receive_signals)
                # todo: non timed status modifiers will never be removed
                self.statmods.append(event.source)
            elif "Enemy" in str(event.source) and not self.exploding:
                self.die()
            elif isinstance(event.source, Boss) and not self.exploding:
                self.die()

    def receive_signals(self, event):
        if event.name == "timeout" and isinstance(event.source, StatusModifier):
            event.source.reverse(self)
            self.statmods.remove(event.source)
