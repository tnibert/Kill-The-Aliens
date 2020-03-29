from gameobject import GameObject
from constants import SCREENH, SCREENW, SCROLLSPEED
from statusmodifiers import SpeedUp
from timer import Timer


# todo: add timing to stop scroll speed change
class GameMap(GameObject):
    def __init__(self, image):
        GameObject.__init__(self, image, layer=-1)
        self.changeover = 0
        self.bgoffset = 0
        self.ychng = 0
        self.scrollspeed = SCROLLSPEED
        self.statmodtimer = Timer()
        self.statmodtimer.subscribe("timeout", self.receive_signals)

    def update(self):
        self.statmodtimer.tick()

        # change offset for vertical scroll
        if self.bgoffset > 2000:
            self.bgoffset = 0
            self.changeover = 0
            self.ychng = 0
        else:
            self.bgoffset += self.scrollspeed

        if 2000 >= self.bgoffset > 2000 - SCREENH:
            self.ychng += self.scrollspeed
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

    def receive_signals(self, event):
        if isinstance(event.source, SpeedUp) and event.name == "collision":
            self.scrollspeed = 10
            # time for 15 seconds, todo: move to constant
            self.statmodtimer.startwatch(15)
        elif isinstance(event.source, Timer) and event.name == "timeout":
            print("received timeout")
            self.scrollspeed = SCROLLSPEED
