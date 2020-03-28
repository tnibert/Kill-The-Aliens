from moveableobject import MoveableObject
from bullet import Bullet
from constants import *
import random


class Boss(MoveableObject):
    def __init__(self, x, y, img, time):
        MoveableObject.__init__(self, x, y, img)
        self.health = BOSSHEALTH
        self.inittime = time

        # state indicator for boss
        # 0 is still, 1 is aimless moving
        # 2 is chase ship, 3 is fire at ship
        self.mode = 0

        # counts number of steps in a given direction
        self.step = 0
        self.maxstep = 4
        self.stepdist = 4
        # initial direction
        self.dir = random.randrange(0, 4)
        self.active = True
        # for mode 2
        self.alreadygoing = 0

    def move(self, foe, time):
        # so this is going to need a little AI
        # and maybe some smoothing of the movement
        # and tracking of foe
        # and discrimination of shooting

        # update mode based on timer
        if time - self.inittime > 1000:
            self.inittime = time
            if self.mode < 3:
                self.mode += 1
            else:
                self.mode = 0

        if self.mode == 0:
            return

        elif self.mode == 1:
            if self.step < self.maxstep:
                self.step += 1
            else:
                self.dir = random.randrange(0, 4)
                self.step = 0
                self.maxstep = random.randrange(2, 6)

        elif self.mode == 2:
            test = self.infirerange(foe)
            if test == -3 and self.alreadygoing == 0:  # if ship is in middle
                self.dir = random.randrange(0, 2)
                self.alreadygoing = 1
            elif test == -1 and self.alreadygoing == 0:
                self.dir = LEFT
                self.alreadygoing = 1
            elif test == -2 and self.alreadygoing == 0:
                self.dir = RIGHT
                self.alreadygoing = 1
            elif test > 0:
                self.mode = 0
                self.alreadygoing = 0

        # MODE 3 HAS NOT BEEN IMPLEMENTED


        # check for screen boundaries
        if self.y + self.height > foe.y - 60:
            self.dir = UP
            self.step = 0
        if self.y < 0:
            self.dir = DOWN
            self.step = 0
        if self.x < -50:
            self.dir = RIGHT
            self.step = 0
        if self.x + self.width - 50 > SCREENW:
            self.dir = LEFT
            self.step = 0

        # self.dir = random.randrange(2,4)
        if self.dir == DOWN:  # move down
            self.y += self.stepdist
        elif self.dir == UP:  # move up
            self.y -= self.stepdist
        elif self.dir == LEFT:  # move left
            self.x -= self.stepdist
        elif self.dir == RIGHT:  # move right
            self.x += self.stepdist

        self.updatepos()

    def fire(self, img, side):
        if side == LEFT:
            return Bullet(self.x, self.y + self.height, img, DOWN)
        else:
            return Bullet(self.x + self.width, self.y + self.height, img, DOWN)

    def infirerange(self, foe):
        # self.x is left turret, self.x+self.width is right turret
        # return 1 if left turret, return 2 if right
        # return -1 if too far left, -2 if too far right, -3 if in center
        if foe.x + foe.width > self.x and foe.x < self.x: return 1
        if foe.x + foe.width > self.x + self.width and foe.x < self.x + self.width: return 2
        if foe.x + foe.width < self.x: return -1
        if foe.x > self.x + self.width: return -2
        if foe.x + foe.width < self.x + self.width and foe.x > self.x: return -3

    def die(self):
        # print "dead"
        self.active = False
