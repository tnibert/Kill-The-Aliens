from moveableobject import MoveableObject
from constants import SCREENW, SCREENH
import random

class Enemy(MoveableObject):
    def __init__(self, x, y, img):
        MoveableObject.__init__(self, x, y, img)
        # 0 means left, 1 means right
        self.dir = random.randrange(0, 2)
        self.xspeed = random.randrange(1, 4)
        self.yspeed = random.randrange(1, 4)

    def move(self, beast):
        # check direction -- these don't match to the predefines
        if self.dir == 0:
            self.x -= self.xspeed
            self.y += self.yspeed
            self.updatepos()
        else:
            self.x += self.xspeed
            self.y += self.yspeed
            self.updatepos()
        # check horizontal border
        if self.x < 0:
            self.dir = 1
        elif self.x > SCREENW - 50:
            self.dir = 0

        # check going off bottom of screen
        if self.y > SCREENH and beast != 1:
            self.__init__(random.randrange(0, SCREENW), 0, self.image)
        elif self.y > SCREENH and beast == 1:  # do not init again, go cleanly off screen
            return beast

        self.updatepos()
        return 0

    def respawn(self):
        self.active = True
        self.__init__(random.randrange(0, SCREENW), random.randrange(-200, -50), self.image)
