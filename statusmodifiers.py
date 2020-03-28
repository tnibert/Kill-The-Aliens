from moveableobject import MoveableObject
from constants import SCREENW
import math
import random


# power ups and downs, to be inherited from
class StatusModifier(MoveableObject):
    def __init__(self, img):
        MoveableObject.__init__(self, random.randrange(0, SCREENW), -100, img)
        # angle randomly ranges from 100 degrees to 260, 0 degrees is vertical axis
        self.degreeangle = random.randrange(100, 260)
        self.speed = 3

    def payload(self, target):
        print("This payload is empty...")
        return 0

    def move(self):
        # screen edge checking

        if (self.x > SCREENW - self.width and self.degreeangle > 180) or random.randrange(0, 2000) == 1467:
            self.degreeangle = random.randrange(100, 160)  # 270 - (self.degreeangle - 90)
        # print "turn left"
        elif (self.x < 0 and self.degreeangle < 180) or random.randrange(0, 2000) == 200:
            self.degreeangle = random.randrange(200, 260)  # 90 + (270 - self.degreeangle)
        # print "turn right"

        self.x -= (math.degrees(math.sin(math.radians(self.degreeangle))) * self.speed) / 40
        self.y -= (math.degrees(math.cos(math.radians(self.degreeangle))) * self.speed) / 40
        self.updatepos()

    # print "x = " + str(self.x) + ", y = " + str(self.y)
    # create movement trigonometrically like in Panzer Deathmatch


# +1 life
class OneUp(StatusModifier):
    def payload(self, target):
        # add some sort of happy animation
        target.health += 1
        return 0


# bomb booby trap, -1 life
# we'll have to make sure that the payload does not happen multiple times
class Bomb(StatusModifier):
    def payload(self, target):
        target.die()  # initiate explosion
        return 0


# double background and ship speed, need a way to undo after time
class SpeedUp(StatusModifier):
    def payload(self, target):
        target.speed = 10
        return 1


# shoot from 3 locations, need a way to undo after time
class MoreGuns(StatusModifier):
    def payload(self, target):
        # print "MOAR GUNS"
        target.bamfmode = True
        return 2