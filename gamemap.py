from gameobject import GameObject
from constants import SCREENH, SCREENW, SCROLLSPEED, MAXSCROLLSPEED
from statusmodifiers import SpeedUp
from player import Player


class GameMap(GameObject):
    def __init__(self, image):
        GameObject.__init__(self, 0, 0, image, layer=-1)
        self.changeover = 0
        self.bgoffset = 0
        self.ychng = 0
        self.scrollspeed = SCROLLSPEED
        self.statmodtimer = None

    def update(self):
        super().update()

        if self.statmodtimer is not None:
            self.statmodtimer.tick()

        # change offset for vertical scroll
        # todo: make 2000 a constant
        if self.bgoffset > 2000:
            self.bgoffset = 0
            self.changeover = 0
            self.ychng = 0
        else:
            self.bgoffset += (self.scrollspeed * self.frame_tick)

        if 2000 >= self.bgoffset > 2000 - SCREENH:
            self.ychng += (self.scrollspeed * self.frame_tick)
            self.changeover = 1

    def render(self, screen):
        # for seamless vertical scrolling
        if self.changeover == 0:
            screen.blit(self.image, (0, 0), (0, 2000 - SCREENH - self.bgoffset, SCREENW, 2000 - self.bgoffset))
        elif self.changeover == 1:
            screen.blit(self.image, (0, 0), (0, self.image.get_height() - self.ychng, SCREENW, 2000))
            screen.blit(self.image, (0, self.ychng), (0, 0, SCREENW, SCREENH - self.ychng))

    def increase_speed(self, event):
        if isinstance(event.kwargs.get("who"), Player):
            self.scrollspeed = MAXSCROLLSPEED
            self.statmodtimer = event.source.timer
            event.source.subscribe("timeout", self.reset_speed)

    def reset_speed(self, event):
        self.scrollspeed = SCROLLSPEED
        self.statmodtimer = None
