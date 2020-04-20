from moveableobject import MoveableObject
from constants import SCREENW
import math
import random


class TrajectoryMovingObject(MoveableObject):
    """
    A gameobject that moves on a trajectory
    """
    def __init__(self, x, y, speed, img):
        MoveableObject.__init__(self, x, y, speed, img)
        self.degreeangle = random.randrange(100, 260)

    def move(self):
        # screen edge checking
        if (self.x > SCREENW - self.width and self.degreeangle > 180) or random.randrange(0, 2000) == 1467:
            self.degreeangle = random.randrange(100, 160)

        elif (self.x < 0 and self.degreeangle < 180) or random.randrange(0, 2000) == 200:
            self.degreeangle = random.randrange(200, 260)

        self.x -= (((math.degrees(math.sin(math.radians(self.degreeangle))) * self.speed) / 40) * self.frame_tick)
        self.y -= (((math.degrees(math.cos(math.radians(self.degreeangle))) * self.speed) / 40) * self.frame_tick)

    def update(self):
        super().update()
        self.move()
