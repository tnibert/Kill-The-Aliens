from moveableobject import MoveableObject
from bullet import Bullet
from constants import SCREENW, PLAYERHEALTH, UP, LEFT, RIGHT


class Player(MoveableObject):
    def __init__(self, img):
        MoveableObject.__init__(self, SCREENW / 2, 450, img)
        self.health = PLAYERHEALTH
        self.spawnX = self.x
        self.spawnY = self.y
        self.speed = 5
        self.bamfmode = False

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
        if (self.health <= 0):
            self.x = -2000
            self.y = -2000
            self.speed = 0
        else:
            self.x = self.spawnX
            self.y = self.spawnY
            self.speed = 5
            self.image = img
        self.updatepos()
