from moveableobject import MoveableObject
import bullet
from timer import Timer
from constants import *
from loadstaticres import blank, explosion
import random


BOSS_STATE_ENTERING = 0
BOSS_STATE_FIGHTING = 1
BOSS_STATE_DYING = 2
BOSS_STATE_DEAD = 3

MOVE_MODE_STILL = 0
MOVE_MODE_AIMLESS = 1
MOVE_MODE_CHASING = 2
MOVE_MODE_FIRE = 3


class Boss(MoveableObject):
    """
    State machine for the boss behavior
    0 means no boss, 1 means clear out shop for boss, 2 means boss entering,
    3 means boss is out, 4 means dying, 5 means dead
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
        self.maxstep = 4
        # initial direction
        self.dir = random.randrange(0, 4)
        self.active = True
        # for mode 2
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
                print("starting explosion {}".format(self.trigger_index))
                self.boom[self.trigger_index].start_exploding()

            # render explosions onto boss
            # todo: make sections of boss transparent after explosions
            self.image = self.orig_image.copy()
            for e in self.boom:
                e.render(self.image)

            # check if all explosions are finished
            if self.trigger_index == len(self.boom)-1 and not self.boom[self.trigger_index].exploding:
                print("boss dead")
                self.game_state = BOSS_STATE_DEAD
                self.exploding = False

        elif self.game_state == BOSS_STATE_DEAD:
            pass

    def start_exploding(self):
        self.exploding = True
        self.image = self.image.copy()
        self.boom[self.trigger_index].start_exploding()

    def update_combat_mode(self, event):
        if self.mode < MOVE_MODE_FIRE:
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
                self.maxstep = random.randrange(2, 6)

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

        # MODE 3 HAS NOT BEEN IMPLEMENTED

        # check for screen boundaries
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

        # self.dir = random.randrange(2,4)
        if self.dir == DOWN:  # move down
            self.y += self.speed * self.frame_tick
        elif self.dir == UP:  # move up
            self.y -= self.speed * self.frame_tick
        elif self.dir == LEFT:  # move left
            self.x -= self.speed * self.frame_tick
        elif self.dir == RIGHT:  # move right
            self.x += self.speed * self.frame_tick

    def on_collide(self, event):
        """
        Handle bullet collision with boss
        :param event:
        :return:
        """
        if isinstance(event.source, bullet.Bullet) and event.kwargs.get("who") is self:
            self.health -= 1
            self.notify("health_down", value=-1)

    def fire(self, img, side):
        if side == LEFT:
            return bullet.Bullet(self.x, self.y + self.height, img, DOWN)
        else:
            return bullet.Bullet(self.x + self.width, self.y + self.height, img, DOWN)

    def infirerange(self):
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

    def die(self):
        # print "dead"
        self.active = False

    # if BEASTMODE == 3:  # if boss is out
    #    if boss.infirerange(ship) > 0:
    #        if random.randrange(0, 10) == 1 and ship.exploding == -1:  # and if ship is not exploding
    #            bullets.append(boss.fire(bulletimg, LEFT))
    #        if random.randrange(0, 10) == 1 and ship.exploding == -1:
    #            bullets.append(boss.fire(bulletimg, RIGHT))

    #     # if boss is done exploding
    #     if len(boom) == 8 and boom[-1].exploding == len(explosion):
    #         BEASTMODE = 5
    #         score += 1000
    #         endtime = time

    # bosslbl = myfont.render("Boss Health: " + str(boss.health), 1, (255, 255, 0))
    # if BEASTMODE >= 3: screen.blit(bosslbl, (SCREENW / 2, 20))
