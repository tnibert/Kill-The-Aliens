from observe import Observable
from constants import GAMEOBJ_LAYER


class GameObject(Observable):
    """
    A renderable object in the game
    """
    def __init__(self, x, y, img, layer=GAMEOBJ_LAYER):
        Observable.__init__(self)

        self.x = x
        self.y = y
        self.image = img
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.layer = layer

        # allows for movement speed independent of frame rate
        self.frame_tick = 0

    def update(self):
        pass

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def on_tick(self, event):
        """
        Event handler for clock ticks
        :param event:
        :return:
        """
        diff = event.kwargs.get("diff")
        if diff is not None:
            self.frame_tick = diff
        else:
            self.frame_tick = 0

    def on_collide(self, event):
        """
        Event handler for collisions
        :param event:
        :return:
        """
        pass
