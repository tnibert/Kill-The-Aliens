from trajectorymovingobject import TrajectoryMovingObject
from constants import SCREENW, SCREENH
import random


class Enemy(TrajectoryMovingObject):
    def __init__(self, x, y, img):
        TrajectoryMovingObject.__init__(self, random.randrange(0, SCREENW), -1 * img.get_height(),
                                        random.randrange(70, 110), img)

    def update(self):
        super().update()

    def respawn(self):
        self.__init__(random.randrange(0, SCREENW), random.randrange(-200, -50), self.image)

    def on_collide(self, event):
        pass
