from moveableobject import MoveableObject
from trajectorymovingobject import TrajectoryMovingObject
from observe import Event
from constants import SCREENW, SCREENH, STATMOD_DURATION, PLAYERSPEED, PLAYERMAXSPEED, STATMOD_SPEED
from timer import Timer
import random


# todo: handling of timers with acquisition of multiple power ups in player and gamemap
# is a bit out of whack
# If you receive multiple power ups, the status will be reset at the end of the timer of
# the first power up received

# power ups and downs, to be inherited from
class StatusModifier(TrajectoryMovingObject):
    def __init__(self, img):
        TrajectoryMovingObject.__init__(self, random.randrange(0, SCREENW), -1 * img.get_height(), STATMOD_SPEED, img)
        # angle randomly ranges from 100 degrees to 260, 0 degrees is vertical axis
        self.timer = Timer(self)

    def payload(self, target):
        self.notify(Event("remove"))

    def update(self):
        super().update()
        if self.y > SCREENH:
            self.notify(Event("remove"))


# +1 life
class OneUp(StatusModifier):
    def payload(self, target):
        # add some sort of happy animation
        target.health += 1
        super().payload(target)
        return 0


# bomb booby trap, -1 life
# we'll have to make sure that the payload does not happen multiple times
class Bomb(StatusModifier):
    def payload(self, target):
        target.die()  # initiate explosion
        super().payload(target)
        return 0


# double background and ship speed, need a way to undo after time
class SpeedUp(StatusModifier):
    def payload(self, target):
        target.speed = PLAYERMAXSPEED
        self.timer.startwatch(STATMOD_DURATION)
        super().payload(target)
        return 1

    def reverse(self, target):
        target.speed = PLAYERSPEED


# shoot from 3 locations, need a way to undo after time
class MoreGuns(StatusModifier):
    def payload(self, target):
        # print "MOAR GUNS"
        target.bamfmode = True
        self.timer.startwatch(STATMOD_DURATION)
        super().payload(target)
        return 2

    def reverse(self, target):
        target.bamfmode = False
