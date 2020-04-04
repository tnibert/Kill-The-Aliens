from moveableobject import MoveableObject
from constants import UP, BULLETSPEED, SCREENH


class Bullet(MoveableObject):
    def __init__(self, x, y, img, dir):
        MoveableObject.__init__(self, x, y, BULLETSPEED, img)
        self.dir = dir

    def move(self):
        # dir 0 for up, anything else for down
        if self.dir == UP:
            self.y -= self.speed * self.frame_tick
        else:
            self.y += self.speed * self.frame_tick
        self.updatepos()

    def update(self):
        super().update()
        self.move()
        if self.y+self.image.get_height() > SCREENH or self.y < 0:
            self.notify("remove")

    #def on_collide(self, event):
    #    if event.kwargs.get("who") == self and "Player" not in str(event.source):
    #         self.notify(Event("remove"))
