from moveableobject import MoveableObject
from constants import UP, BULLETSPEED, SCREENH
import boss


class Bullet(MoveableObject):
    def __init__(self, x, y, img, dir):
        super().__init__(x, y, BULLETSPEED, img)
        self.dir = dir

    def move(self):
        # dir 0 for up, anything else for down
        if self.dir == UP:
            self.y -= self.speed * self.frame_tick
        else:
            self.y += self.speed * self.frame_tick

    def update(self):
        super().update()
        self.move()
        if self.y+self.image.get_height() > SCREENH or self.y < 0:
            self.notify("remove")

    def on_collide(self, event):
        if isinstance(event.source, boss.Boss) and event.kwargs.get("who") is self and not self.exploding:
            self.start_exploding()

    def update_explosion(self, event):
        print("in bullet update_explosion()")
        if super().update_explosion(event):
            self.notify("remove")
