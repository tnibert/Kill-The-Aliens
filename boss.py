from moveableobject import MoveableObject
from timer import Timer
from constants import BOSS_DEATH_SCORE_INC, BOSSHEALTH, NUM_BOSS_EXPLOSIONS, UP, DOWN, LEFT, RIGHT, BOSS_SPEED, SCREENW, SCREENH
from loadstaticres import blank, explosion
from endgamesignal import EndLevel
from loadstaticres import bulletimg
import random
import bullet

"""
This file defines all boss behaviors
"""

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

# for rush attack
RUSH_START = 0
RUSH_DOWN = 1
RUSH_SIDE = 2
RUSH_UP = 3
RUSH_RECENTER = 4


class Boss(MoveableObject):
    """
    State machine for the boss behavior
    Allow for identification of bosses by one type and define base functionality.
    Combat strategies will differ.
    """

    def __init__(self, x, y, img, foe):
        MoveableObject.__init__(self, x, y, BOSS_SPEED, img)

        self.health = BOSSHEALTH
        self.foe = foe

        # initial direction
        self.dir = random.randrange(0, 4)

        # counts number of steps in a given direction
        self.step = 0

        # overarching state
        self.game_state = BOSS_STATE_ENTERING

        self.combat_state_timer = Timer()
        self.combat_state_change_time = 5
        self.combat_state_timer.subscribe("timeout", self.update_combat_mode)

        # create boss explosions
        self.boom = []
        self.trigger_index = 0
        for i in range(NUM_BOSS_EXPLOSIONS):
            self.boom.append(MoveableObject(random.randrange(self.image.get_width() - explosion[0].get_width()),
                                            random.randrange(self.image.get_height() - explosion[0].get_height()),
                                            0, blank))

    def update_combat_mode(self, event):
        """
        interface
        """
        pass

    def combat_move(self):
        """
        interface
        """
        pass

    def detect_foe_loc_relative(self):
        """
        interface
        """
        pass

    def update(self):
        """
        All bosses will have the same overarching state changes, but not combat strategies.
        """

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
                self.notify("death", value=BOSS_DEATH_SCORE_INC)

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
            raise EndLevel({"state": "victory"})

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

    def start_exploding(self):
        self.exploding = True
        self.image = self.image.copy()
        self.boom[self.trigger_index].start_exploding()


class InvaderBossBehave(Boss):
    def __init__(self, x, y, img, foe):
        super().__init__(x, y, img, foe)

        # combat move mode
        self.mode = MOVE_MODE_STILL

        self.maxstep = 10

        self.alreadygoing = 0

        self.bullet_start_locs = [-1 * self.width/2, 0, self.width/2]

    def update_combat_mode(self, event):
        """
        Event handler for the combat state timer
        Cycle through combat states
        :param event:
        :return:
        """
        if self.mode < MOVE_MODE_CHASING:
            self.mode += 1
        else:
            self.mode = MOVE_MODE_STILL

        self.combat_state_timer.startwatch(self.combat_state_change_time)

    def combat_move(self):

        if self.mode == MOVE_MODE_STILL:
            return

        elif self.mode == MOVE_MODE_AIMLESS:
            if self.step < self.maxstep:
                self.step += 1
            else:
                self.dir = random.randrange(0, 4)
                self.step = 0
                self.maxstep = random.randrange(20, 60)

        elif self.mode == MOVE_MODE_CHASING:
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
                self.mode = 0
                self.alreadygoing = 0

        # 1 in 100 chance of shooting
        # todo: this is currently frame rate dependent
        if random.randrange(100) == 2:
            loc = random.randrange(len(self.bullet_start_locs))
            self.notify("fire", bullet=bullet.Bullet(self.x + self.width/2 + self.bullet_start_locs[loc],
                                                     self.y + self.height + bulletimg.get_height(),
                                                     bulletimg,
                                                     DOWN,
                                                     self))

        self.adjust_for_boundaries()
        self.general_motion()

    def infirerange(self):
        # todo: examine this logic and improve
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


class MagykalBossBehave(Boss):

    def __init__(self, x, y, img, foe):
        super().__init__(x, y, img, foe)

        # combat move mode
        self.mode = MOVE_MODE_STILL

        self.maxstep = 10

        self.rush_phase = RUSH_START

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
            return

        elif self.mode == MOVE_MODE_AIMLESS:
            if self.step < self.maxstep:
                self.step += 1
            else:
                self.dir = random.randrange(0, 4)
                self.step = 0
                # todo: define a constant here, larger
                self.maxstep = random.randrange(5, 10)

            self.adjust_for_boundaries()
            self.general_motion()

        elif self.mode == MOVE_MODE_CHASING:
            self.dir = self.detect_foe_loc_relative()

            self.adjust_for_boundaries()
            self.general_motion()

        elif self.mode == MOVE_MODE_FIRE:
            bullet_start_locs = [-10, 0, 10]
            for loc in bullet_start_locs:
                self.notify("fire", bullet=bullet.Bullet(self.x + self.width/2 + loc,
                                                         self.y + self.height + bulletimg.get_height(),
                                                         bulletimg,
                                                         DOWN,
                                                         self))
            # to fire while moving
            self.adjust_for_boundaries()
            self.general_motion()

        elif self.mode == MOVE_MODE_RUSH:
            if self.rush_phase == RUSH_START:
                self.speed *= 3
                self.combat_state_timer.stopwatch()
                self.dir = DOWN
                self.rush_phase = RUSH_DOWN
            elif self.rush_phase == RUSH_DOWN and self.y >= SCREENH - self.height:
                self.rush_phase = RUSH_SIDE
                self.dir = random.choice((LEFT, RIGHT))
            elif (self.x <= 0 or self.x + self.width >= SCREENW) and self.rush_phase == RUSH_SIDE:
                self.rush_phase = RUSH_UP
                self.dir = UP
            elif self.rush_phase == RUSH_UP and self.y < SCREENH/2 - self.height:
                self.rush_phase = RUSH_RECENTER
                if self.x < SCREENW/2 - self.width/2:
                    self.dir = RIGHT
                else:
                    self.dir = LEFT
            elif self.rush_phase == RUSH_RECENTER and self.x < SCREENW/2 - self.width/2 + 15 and self.x > SCREENW/2 - self.width/2 - 15:
                self.speed /= 3
                self.rush_phase = RUSH_START
                self.update_combat_mode(None)

            self.general_motion()

    def detect_foe_loc_relative(self):
        """
        Determine the location of the player relative to the boss
        :return: LEFT or RIGHT
        """
        if self.foe.x + self.foe.width/2 > self.x + self.width/2:
            return RIGHT
        else:
            return LEFT
