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
            self.x = self.x - self.image.get_width()/2
            self.y = self.y - self.image.get_height()/2

            # best to not divide actions between boss and bullet
            # any scenario where the bullet explodes should be handled in this function
            event.source.health -= 1
            event.source.notify("health_down", value=-1)

    def update_explosion(self, event):
        if super().update_explosion(event):
            self.notify("remove")
