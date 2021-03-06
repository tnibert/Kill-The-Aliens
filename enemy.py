from trajectorymovingobject import TrajectoryMovingObject
from constants import SCREENW, SCREENH, SAUCER_DEATH_SCORE_INC
from player import Player
from bullet import Bullet
import random


class Enemy(TrajectoryMovingObject):
    def __init__(self, img):
        TrajectoryMovingObject.__init__(self, random.randrange(0, SCREENW), # x location
                                        -3 * img.get_height(),              # y location
                                        random.randrange(60, 100),          # speed
                                        img)
        self.exit_stage = False

    def update(self):
        super().update()
        if self.y > SCREENH:
            self.respawn()

    def respawn(self):
        """
        Respawn if not set to exit
        :return:
        """
        if not self.exit_stage:
            self.image = self.orig_image
            self.x = random.randrange(0, SCREENW)
            self.y = -3 * self.image.get_height()
            self.speed = random.randrange(60, 100)
        else:
            self.notify("remove")

    def update_explosion(self, event):
        if super().update_explosion(event):
            # if the explosion is complete
            self.notify("score_up", value=SAUCER_DEATH_SCORE_INC)
            self.respawn()

    def on_collide(self, event):
        if event.kwargs.get("who") == self:
            if not self.exploding:
                if isinstance(event.source, Player):
                        self.start_exploding()
                elif isinstance(event.source, Bullet):
                        self.start_exploding()
                        event.source.notify("remove")

    def leave(self):
        """
        Set flag to leave the game scene on screen exit
        :return:
        """
        self.exit_stage = True
