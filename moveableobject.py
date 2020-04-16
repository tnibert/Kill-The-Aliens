from constants import EXPLOSION_FRAME_UPDATE_WAIT
from loadstaticres import explosion
from gameobject import GameObject
from timer import Timer


# all sprites inherit from this class
class MoveableObject(GameObject):
    def __init__(self, x, y, speed, img):
        GameObject.__init__(self, x, y, img)
        self.orig_image = self.image
        self.speed = speed
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.exploding = False
        self.explosion_index = 0
        self.explosion_timer = Timer()
        self.explosion_timer.subscribe("timeout", self.update_explosion)

    def update(self):
        super().update()
        if self.exploding:
            self.explosion_timer.tick()

    def start_exploding(self):
        self.exploding = True
        self.image = explosion[self.explosion_index]
        self.speed = 0
        self.explosion_timer.startwatch(EXPLOSION_FRAME_UPDATE_WAIT)

    def update_explosion(self, event):
        """
        Event handler to update the explosion, called from the explosion timer
        :param event: the timer notify event
        :return: True if explosion is complete, False if not
        """
        if self.explosion_index < len(explosion)-1:
            self.explosion_index += 1
            self.image = explosion[self.explosion_index]
            self.explosion_timer.startwatch(EXPLOSION_FRAME_UPDATE_WAIT)
            return False
        else:
            self.explosion_index = 0
            self.exploding = False
            return True
