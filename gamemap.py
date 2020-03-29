from gameobject import GameObject
from constants import SCREENH, SCREENW, SCROLLSPEED


class GameMap(GameObject):
    def __init__(self, image):
        GameObject.__init__(self, image, layer=-1)
        self.changeover = 0
        self.bgoffset = 0
        self.ychng = 0

    def update(self):
        # change offset for vertical scroll
        if self.bgoffset > 2000:
            self.bgoffset = 0
            self.changeover = 0
            self.ychng = 0
        else:
            self.bgoffset += SCROLLSPEED

        if 2000 >= self.bgoffset > 2000 - SCREENH:
            self.ychng += SCROLLSPEED
            self.changeover = 1

    def draw(self, screen):
        # for seamless vertical scrolling
        if self.changeover == 0:
            screen.blit(self.image, (0, 0), (0, 2000 - SCREENH - self.bgoffset, SCREENW, 2000 - self.bgoffset))
        elif self.changeover == 1:
            # print "ychng: " + str(ychng)
            # print "bgoffset: " + str(bgoffset)
            screen.blit(self.image, (0, 0), (0, self.image.get_height() - self.ychng, SCREENW, 2000))
            screen.blit(self.image, (0, self.ychng), (0, 0, SCREENW, SCREENH - self.ychng))
