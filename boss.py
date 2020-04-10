from moveableobject import MoveableObject
from bullet import Bullet
from constants import *
from loadstaticres import blank, explosion
from functools import reduce
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
    def __init__(self, x, y, img, time):
        MoveableObject.__init__(self, x, y, BOSS_SPEED, img)
        self.health = BOSSHEALTH
        self.inittime = time

        self.game_state = BOSS_STATE_ENTERING
        # move mode
        self.mode = MOVE_MODE_STILL

        # counts number of steps in a given direction
        self.step = 0
        self.maxstep = 4
        self.stepdist = 4
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
                self.game_state = BOSS_STATE_DYING

        elif self.game_state == BOSS_STATE_FIGHTING:
            pass

        elif self.game_state == BOSS_STATE_DYING:
            for e in self.boom:
                e.update()
            if not self.exploding:
                self.start_exploding()
            else:
                for e in self.boom:
                    e.render(self.image)

                # check if all explosions are finished
                if len([e for e in self.boom if e.exploding == True]) == 0:
                    self.game_state = BOSS_STATE_DEAD
                    self.exploding = False

        elif self.game_state == BOSS_STATE_DEAD:
            pass

    def start_exploding(self):
        self.exploding = True
        for e in self.boom:
            e.start_exploding()

    def move(self, foe, time):
        # update mode based on timer
        if time - self.inittime > 1000:
            self.inittime = time
            if self.mode < 3:
                self.mode += 1
            else:
                self.mode = 0

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
            test = self.infirerange(foe)
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
                #Traceback (most recent call last):
                # File "/home/tim/code/Kill-The-Aliens/killthealiens.py", line 374, in <module>
                #   boss.move(ship, time)
                # File "/home/tim/code/Kill-The-Aliens/boss.py", line 64, in move
                #   elif test > 0:
                #TypeError: '>' not supported between instances of 'NoneType' and 'int'
                # wtf?
                self.mode = 0
                self.alreadygoing = 0

        # MODE 3 HAS NOT BEEN IMPLEMENTED

        # check for screen boundaries
        if self.y + self.height > foe.y - 60:
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
            self.y += self.stepdist
        elif self.dir == UP:  # move up
            self.y -= self.stepdist
        elif self.dir == LEFT:  # move left
            self.x -= self.stepdist
        elif self.dir == RIGHT:  # move right
            self.x += self.stepdist

        self.updatepos()

    def fire(self, img, side):
        if side == LEFT:
            return Bullet(self.x, self.y + self.height, img, DOWN)
        else:
            return Bullet(self.x + self.width, self.y + self.height, img, DOWN)

    def infirerange(self, foe):
        # self.x is left turret, self.x+self.width is right turret
        # return 1 if left turret, return 2 if right
        # return -1 if too far left, -2 if too far right, -3 if in center
        if foe.x + foe.width > self.x and foe.x < self.x: return 1
        if foe.x + foe.width > self.x + self.width and foe.x < self.x + self.width: return 2
        if foe.x + foe.width < self.x: return -1
        if foe.x > self.x + self.width: return -2
        if foe.x + foe.width < self.x + self.width and foe.x > self.x: return -3
        # todo: this can return None and crash the program
        # e.g.
        # Traceback (most recent call last):
        #   File "/home/tim/code/Kill-The-Aliens/killthealiens.py", line 213, in <module>
        #     if boss.infirerange(ship) > 0:
        # TypeError: '>' not supported between instances of 'NoneType' and 'int'

    def die(self):
        # print "dead"
        self.active = False

    # if BEASTMODE == 3:  # if boss is out
    #    if boss.infirerange(ship) > 0:
    #        if random.randrange(0, 10) == 1 and ship.exploding == -1:  # and if ship is not exploding
    #            bullets.append(boss.fire(bulletimg, LEFT))
    #        if random.randrange(0, 10) == 1 and ship.exploding == -1:
    #            bullets.append(boss.fire(bulletimg, RIGHT))

    # if boss got killed make Sonic style boss death explosion
    # explode is called multiple times over several main loops to advance the explosion frame
    # if BEASTMODE == 4:
    #     for splat in boom:
    #         # if first pass, initialize explosion sequence
    #         if len(boom) == 1 and splat.exploding == -1:
    #             splat.x = random.randrange(boss.x, boss.x + boss.width - explosion[
    #                 0].get_width())  # subtract explosion width
    #             splat.y = random.randrange(boss.y, boss.y + boss.height - explosion[0].get_height())
    #             explosion.append(blacksquare)  # to take chunks out of boss
    #         splat.explode(time)
    #     if boom[-1].exploding == 2 and len(boom) < 8:
    #         boom.append(MoveableObject(random.randrange(boss.x, boss.x + boss.width - explosion[0].get_width()),
    #                                        random.randrange(boss.y,
    #                                                         boss.y + boss.height - explosion[0].get_height()),
    #                                        pygame.Surface((1, 1))))
    #     # if boss is done exploding
    #     if len(boom) == 8 and boom[-1].exploding == len(explosion):
    #         BEASTMODE = 5
    #         score += 1000
    #         endtime = time

    # this may have to be reexamined, testing beastmode < 3
    # if boss.y > 0 and BEASTMODE < 3: BEASTMODE = 3
    #
    # # if boss is displayed
    # if 4 > BEASTMODE >= 2:
    #     boss.move(ship, time)
    #     # if ship collides with boss, lose life
    #     if collide(ship, boss):
    #         # print "boss collision"
    #         ship.die()  # evaluation of death is earlier in the code


    # if BEASTMODE >= 2: screen.blit(boss.image, (boss.x, boss.y))
    #
    # if BEASTMODE >= 4:
    #     for splat in boom:
    #         screen.blit(splat.image, (splat.x, splat.y))

    # bosslbl = myfont.render("Boss Health: " + str(boss.health), 1, (255, 255, 0))
    # if BEASTMODE >= 3: screen.blit(bosslbl, (SCREENW / 2, 20))
