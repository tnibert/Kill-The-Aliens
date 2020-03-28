from constants import EXTIMELAPSE
from loadstaticres import explosion
from gameobject import GameObject


# all sprites inherit from this class
class MoveableObject(GameObject):
    def __init__(self, x, y, img):
        GameObject.__init__(self, img)
        self.x = x
        self.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.updatepos()
        self.exploding = -1
        self.timestack = []
        self.active = True

    def updatepos(self):  # this lets us play nice with pygame, collision detection
        self.pos = (self.x, self.y)
        self.rect.x = self.x
        self.rect.y = self.y

    def explode(self, time):  # yes, everything can explode
        self.timestack.append(time)
        self.speed = 0
        if len(self.timestack) < 2:
            difftime = EXTIMELAPSE + 1
        elif len(self.timestack) >= 2:
            newtime = self.timestack.pop()
            oldtime = self.timestack.pop()
            difftime = newtime - oldtime
            # print "newtime: " + str(newtime) + " oldtime: " + str(oldtime) + " diff: " + str(difftime)
            if difftime <= EXTIMELAPSE:
                self.timestack.append(oldtime)
            else:
                self.timestack.append(newtime)
        if self.exploding < len(explosion) - 1 and difftime > EXTIMELAPSE:
            self.exploding += 1
            self.image = explosion[self.exploding]
        if self.exploding >= len(explosion) - 1:
            # self.image.fill(BLACK)
            self.exploding += 1
            self.image = explosion[len(explosion) - 1]
            self.active = False
            return True  # we're done
        return False

    # then return to main for cleanup
    # print self.active
    # print self.timestack
