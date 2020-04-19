from moveableobject import MoveableObject
from timer import Timer
from constants import *
from loadstaticres import blank, explosion
from endgamesignal import EndLevel
from loadstaticres import bulletimg
import random
import bullet


# overarching boss states
BOSS_STATE_ENTERING = 0
BOSS_STATE_FIGHTING = 1
BOSS_STATE_DYING = 2
BOSS_STATE_DEAD = 3

# combat states
MOVE_MODE_STILL = 0
MOVE_MODE_AIMLESS = 1
MOVE_MODE_CHASING = 2
MOVE_MODE_FIRE = 3
MOVE_MODE_RUSH = 4


class Boss(MoveableObject):
    """
    State machine for the boss behavior
    """
    def __init__(self, x, y, img, foe):
        MoveableObject.__init__(self, x, y, BOSS_SPEED, img)
        self.health = BOSSHEALTH
        self.combat_state_timer = Timer()
        self.combat_state_change_time = 5
        self.combat_state_timer.subscribe("timeout", self.update_combat_mode)

        self.game_state = BOSS_STATE_ENTERING
        # move mode
        self.mode = MOVE_MODE_STILL

        self.foe = foe

        # counts number of steps in a given direction
        self.step = 0
        self.maxstep = 10
        # initial direction
        self.dir = random.randrange(0, 4)

        self.alreadygoing = 0

        # create boss explosions
        self.boom = []
        self.trigger_index = 0
        for i in range(NUM_BOSS_EXPLOSIONS):
            self.boom.append(MoveableObject(random.randrange(self.image.get_width() - explosion[0].get_width()),
                                            random.randrange(self.image.get_height() - explosion[0].get_height()),
                                            0, blank))

    def update(self):
        super().update()
        if self.game_state == BOSS_STATE_ENTERING:
            if self.y < 5:
                self.y += self.speed * self.frame_tick
            else:
                self.game_state = BOSS_STATE_FIGHTING
                self.combat_state_timer.startwatch(self.combat_state_change_time)

        elif self.game_state == BOSS_STATE_FIGHTING:
            if self.health <= 0:
                self.game_state = BOSS_STATE_DYING
                return

            self.combat_state_timer.tick()
            self.combat_move()

        elif self.game_state == BOSS_STATE_DYING:
            if not self.exploding:
                self.start_exploding()

            for e in self.boom:
                e.update()

            # start next explosion if the previous is finished
            if not self.boom[self.trigger_index].exploding and self.trigger_index < len(self.boom)-1:
                self.trigger_index += 1
                self.boom[self.trigger_index].start_exploding()

            # render explosions onto boss
            # todo: make sections of boss transparent after explosions
            self.image = self.orig_image.copy()
            for e in self.boom:
                e.render(self.image)

            # check if all explosions are finished
            if self.trigger_index == len(self.boom)-1 and not self.boom[self.trigger_index].exploding:
                self.game_state = BOSS_STATE_DEAD
                self.exploding = False

        elif self.game_state == BOSS_STATE_DEAD:
            raise EndLevel("victory")

    def start_exploding(self):
        self.exploding = True
        self.image = self.image.copy()
        self.boom[self.trigger_index].start_exploding()

    def update_combat_mode(self, event):
        """
        Event handler for the combat state timer
        Cycle through combat states
        :param event:
        :return:
        """
        if self.mode < MOVE_MODE_RUSH:
            self.mode += 1
        else:
            self.mode = MOVE_MODE_STILL

        self.combat_state_timer.startwatch(self.combat_state_change_time)

    def combat_move(self):
        """
        Handle movement while in BOSS_STATE_FIGHTING
        :return:
        """

        if self.mode == MOVE_MODE_STILL:
            #print("move mode still")
            return

        elif self.mode == MOVE_MODE_AIMLESS:
            #print("move mode aimless")
            if self.step < self.maxstep:
                self.step += 1
            else:
                self.dir = random.randrange(0, 4)
                self.step = 0
                self.maxstep = random.randrange(2, 6)

            self.adjust_for_boundaries()
            self.general_motion()

        elif self.mode == MOVE_MODE_CHASING:
            #print("move mode chasing")
            test = self.infirerange()
            if test == -3 and self.alreadygoing == 0:  # if ship is in middle
                self.dir = random.randrange(0, 2)
                self.alreadygoing = 1
            elif test == -1 and self.alreadygoing == 0:
                self.dir = LEFT
                self.alreadygoing = 1
            elif test == -2 and self.alreadygoing == 0:
                self.dir = RIGHT
                self.alreadygoing = 1
            elif test > 0:
                self.alreadygoing = 0

            self.adjust_for_boundaries()
            self.general_motion()

        elif self.mode == MOVE_MODE_FIRE:
            #print("in fire mode")
            bullet_start_locs = [-10, 0, 10]
            for loc in bullet_start_locs:
                self.notify("fire", bullet=bullet.Bullet(self.x + self.width/2 + loc,
                                                         self.y + self.height + bulletimg.get_height(),
                                                         bulletimg,
                                                         DOWN,
                                                         self))

        elif self.mode == MOVE_MODE_RUSH:
            #print("move mode rush")
            pass

    def adjust_for_boundaries(self):
        """
        Check for boundaries and change direction if necessary
        """
        if self.y + self.height > self.foe.y - 60:
            self.dir = UP
            self.step = 0
        if self.y < 0:
            self.dir = DOWN
            self.step = 0
        if self.x < -50:
            self.dir = RIGHT
            self.step = 0
        if self.x + self.width - 50 > SCREENW:
            self.dir = LEFT
            self.step = 0

    def general_motion(self):
        """
        Adjust position based on direction specified
        """
        if self.dir == DOWN:  # move down
            self.y += self.speed * self.frame_tick
        elif self.dir == UP:  # move up
            self.y -= self.speed * self.frame_tick
        elif self.dir == LEFT:  # move left
            self.x -= self.speed * self.frame_tick
        elif self.dir == RIGHT:  # move right
            self.x += self.speed * self.frame_tick

    def infirerange(self):
        """
        The logic here isn't really relevant anymore since we got rid of the turrets
        But it seems to add an interesting dynamic, so we'll keep it for the moment
        :return: an int which determines the behavior in the calling function
        """
        # todo: examine this logic more closely
        # self.x is left turret, self.x+self.width is right turret
        # return 1 if left turret, return 2 if right
        # return -1 if too far left, -2 if too far right, -3 if in center
        if self.foe.x + self.foe.width >= self.x and self.foe.x <= self.x:
            return 1
        if self.foe.x + self.foe.width >= self.x + self.width and self.foe.x <= self.x + self.width:
            return 2
        if self.foe.x + self.foe.width <= self.x:
            return -1
        if self.foe.x >= self.x + self.width:
            return -2
        if self.foe.x + self.foe.width <= self.x + self.width and self.foe.x >= self.x:
            return -3

        # default to center
        return -3
