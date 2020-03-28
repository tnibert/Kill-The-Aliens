from moveableobject import MoveableObject
from constants import UP

class Bullet(MoveableObject):
    def __init__(self, x, y, img, dir):
        MoveableObject.__init__(self, x, y, img)
        self.dir = dir
        # self.active = True
        self.speed = 13  # was 10, is now 13 for statmod speed up

    def move(self):
        # dir 0 for up, anything else for down
        if self.dir == UP:
            self.y -= self.speed
        else:
            self.y += self.speed
        self.updatepos()
