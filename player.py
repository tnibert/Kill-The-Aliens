from moveableobject import MoveableObject
from bullet import Bullet
from constants import SCREENW, SCREENH, PLAYERHEALTH, UP, LEFT, RIGHT
from statusmodifiers import StatusModifier
import pygame


class Player(MoveableObject):
    def __init__(self, img, eventqueue):
        MoveableObject.__init__(self, SCREENW / 2, 450, img)
        self.health = PLAYERHEALTH
        self.spawnX = self.x
        self.spawnY = self.y
        self.speed = 5
        # bamf mode - shoot three bullets at a time
        self.bamfmode = False

        # for more precise keyboard input
        self.goright = False
        self.goleft = False
        self.goup = False
        self.godown = False

        # for processing input events
        self.eventqueue = eventqueue

    def update(self):
        # todo: multiple speed by a time interval to not lock speed to frame rate
        # user input
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
        if self.goright == True and self.x + self.width <= SCREENW:
            self.x += self.speed
        elif self.goleft == True and self.x >= 0:
            self.x -= self.speed
        if self.goup == True and self.y >= 0:
            self.y -= self.speed
        elif self.godown == True and self.y + self.height <= SCREENH:
            self.y += self.speed

        self.updatepos()

    def fire(self, img, turret=UP):
        if turret == UP:
            return Bullet(self.x + (self.image.get_width() / 2), self.y - 10, img, UP)
        if turret == LEFT:
            return Bullet(self.x + 15, self.y + 40, img, UP)
        if turret == RIGHT:
            return Bullet(self.x + self.image.get_width() - 15, self.y + 40, img, UP)
        # so, in order to implement bamf mode, we need bullets to come out from side turrets
        # but currently our fire method can only return one bullet
        # so we either return a list of bullets when we fire (a cool bit of modification to the game loop)
        # or we can check in the game loop and if bamfmode call fire two more times, I think this is better
        # we should also add something in the main loop that prevents a bullet moving upward from harming the ship

    def die(self):
        print("player dead")
        if self.active == True:
            self.active = False
            self.health -= 1

    def respawn(self, img):
        self.exploding = -1
        self.active = True
        if self.health <= 0:
            self.x = -2000
            self.y = -2000
            self.speed = 0
        else:
            self.x = self.spawnX
            self.y = self.spawnY
            self.speed = 5
            self.image = img
        self.updatepos()

    def receive_signals(self, event):
        print("player received {} from {}".format(event.name, type(event.source)))
        if event.name == "collision" and isinstance(event.source, StatusModifier):
            # todo: apply time out for payloads on speed and extra guns
            print("applying payload")
            event.source.payload(self)
