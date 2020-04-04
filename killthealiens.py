#! /usr/bin/env python
from moveableobject import MoveableObject
from enemy import Enemy
from bullet import Bullet
from player import Player
from statusmodifiers import *
from boss import Boss
from utilfuncs import switch, toframes, collide
from constants import *
from loadstaticres import *
from scene import Scene
from gamemap import GameMap
from timer import Timer
from queue import Queue
import pygame
import sys
import random

# todo:
# ok, now this is getting hairy
# We still need to test the explosion of the ship
# But to do that, we need to move the bullets and the saucers to the new architecture
# (because new arch handles the collisions)
# explosions should be implemented for bullets and saucers if it is working
# we also need to push events to the game_mgmt_queue and process in Scene
#
# currently the only object not framerate locked is the player, need to add this
# to all other GameObjects, including the gamemap
#
# at the end of all of that, we will move the boss to the new architecture
# we also need to fix the bug in the boss with infirerange() returning None

# queues for input events
player_input_queue = Queue()
game_mgmt_queue = Queue()

# well, we added music but it makes the game hang :\
# these two lines before pygame.init() fix hang problem slightly, but don't completely fix
# may have to somehow run mixer in a separate process
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

pygame.init()

speedupstarttime = -1
moregunsstarttime = -1

# set up window
screen = pygame.display.set_mode((SCREENW, SCREENH), pygame.DOUBLEBUF)
pygame.display.set_caption("KILL THE ALIENS")

gamescene = Scene(game_mgmt_queue, screen)

# image conversions
map_bg = background.convert()
bulletimg = bulletimg.convert()     # todo: change name

game_map = GameMap(map_bg)
gamescene.attach(game_map)

# set text font
myfont = pygame.font.SysFont("monospace", 15)

# load up music
pygame.mixer.music.load(BG_MUSIC_FNAME)

# actually transparent square
blacksquare = pygame.Surface((explosion[0].get_width() - 15, explosion[0].get_height() - 15), pygame.SRCALPHA, 32)

# set up game objects
ship = Player(shipimg, player_input_queue)
gamescene.attach(ship)

# sprite groups
#saucers = []
bullets = []
# gone = False
# killed = pygame.sprite.Group()

# create enemies
for x in range(0, 3):
    gamescene.attach(Enemy(saucerimg))

# create boss
#boss = Boss(100, -1200, bossimg, 0)

# create boss explosions
# maybe move this later in the code and don't create it in memory until we need it
#boom = []
#boom.append(MoveableObject(0, 0, pygame.Surface((1, 1))))

clock = pygame.time.Clock()

# flags
# 0 means play, 1 means user exit, 2 means death, 3 means victory
endgame = 0
# 0 means no boss, 1 means clear out shop for boss, 2 means boss entering,
# 3 means boss is out, 4 means dying, 5 means dead
BEASTMODE = 0

BLACK = (0, 0, 0)
blacksquare.fill(BLACK)

score = 0
time = 0  # total play time
endtime = 0

deadindex = -10

intro = 1

# opening screen
while intro == 1:
    screen.fill(BLACK)
    screen.blit(introscreen, (0, 0))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if not hasattr(event, 'key'): continue
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN: intro = 0

# start music on endless loop
pygame.mixer.music.play(-1)

# begin main game loop
# this should have all been put in a function T_T
while endgame == 0:

    # determine if we should have a status modifier
    # so apparently there's no switch/case in python >_>
    # choose a random number, determine which powerup based on number, if not 1 - 6 just continue on w/ no stat mod
    for case in switch(random.randrange(0, 10000)):
        statmod = None
        if case(1):
            statmod = OneUp(oneupimg)
        elif case(90):
            statmod = Bomb(bombimg)
        elif case(1337):
            statmod = SpeedUp(speedupimg)
            statmod.subscribe("collision", game_map.receive_signals)
        elif case(511):
            statmod = MoreGuns(moregunsimg)
        if statmod is not None:
            # todo: make the receiving function more specific
            print("statmod created")
            statmod.subscribe("collision", ship.receive_signals)
            gamescene.attach(statmod)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: endgame = 1
        elif not hasattr(event, 'key'): continue
        elif event.key == pygame.K_ESCAPE: endgame = 1
        #elif event.key == pygame.K_SPACE and ship.active:
        #    bullets.append(ship.fire(bulletimg))
        #    if ship.bamfmode:
        #        bullets.append(ship.fire(bulletimg, LEFT))
        #        bullets.append(ship.fire(bulletimg, RIGHT))
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            player_input_queue.put(event)

    gamescene.update_cycle()

    #if BEASTMODE == 3:  # if boss is out
    #    if boss.infirerange(ship) > 0:
    #        if random.randrange(0, 10) == 1 and ship.exploding == -1:  # and if ship is not exploding
    #            bullets.append(boss.fire(bulletimg, LEFT))
    #        if random.randrange(0, 10) == 1 and ship.exploding == -1:
    #            bullets.append(boss.fire(bulletimg, RIGHT))

    #
    # # move bullets, check for collisions with player or boss or off screen
    # # explosions as well
    # # just an iteration through all bullets
    # for bullet in bullets:
    #     bullet.move()
    #     # -60 to go a little off screen, for high up explosions
    #     if bullet.y < -60 or bullet.y > SCREENH: bullet.active = False
    #     if collide(ship, bullet) and bullet.dir != UP:
    #         ship.die()
    #         bullet.active = False
    #     elif BEASTMODE == 3 and collide(boss, bullet):
    #         boss.health -= 5
    #         if boss.health <= 0:
    #             boss.die()
    #             BEASTMODE += 1
    #         bullet.active = False
    #     if -1 < bullet.exploding < 4: bullet.explode(time)
    #     if bullet.active == False: bullets.remove(bullet)

    # maybe it would be best to have a section just to handle explosions across the board
    # perhaps an explosion object, eg just kill the sprite and have explosion obj take over
    #
    #     for bullet in bullets:
    #         if collide(saucer, bullet):
    #             bullet.x = saucer.x
    #             bullet.y = saucer.y
    #             bullet.updatepos()
    #             # respawn saucer off screen and increment score
    #             if BEASTMODE != 1:
    #                 saucer.respawn()
    #             else:
    #                 deadindex = saucers.index(saucer)
    #                 dietest = 1
    #             bullet.explode(time)
    #             # saucers.remove(saucer)		#this removes the actual object from the list
    #             score += 5
    #     if saucer.active == False: saucer.respawn()

    # for final player death
    # if ship.health <= 0 and endtime == 0:
    #     endtime = time
    #
    # # for time delay after death
    # if time >= endtime + 4000 and endtime != 0:
    #     # print "game over"
    #     endgame = 2

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

    # text rendering
    healthlbl = myfont.render("Health: " + str(ship.health), 1, (255, 255, 0))
    scorelbl = myfont.render("Score: " + str(score), 1, (255, 255, 0))
#    bosslbl = myfont.render("Boss Health: " + str(boss.health), 1, (255, 255, 0))

    # render images

    screen.fill(BLACK)

    gamescene.render_cycle()

    # if BEASTMODE >= 2: screen.blit(boss.image, (boss.x, boss.y))
    #
    # if BEASTMODE >= 4:
    #     for splat in boom:
    #         screen.blit(splat.image, (splat.x, splat.y))

    screen.blit(healthlbl, (SCREENW - 100, 20))
    screen.blit(scorelbl, (SCREENW - 100, 35))
    # if BEASTMODE >= 3: screen.blit(bosslbl, (SCREENW / 2, 20))

    pygame.display.flip()  # apply double buffer

# end game loop

# display end screens
# todo: move file loads to resource loader
if BEASTMODE == 5:
    disp = pygame.image.load("victory1.png")
else:
    disp = pygame.image.load("dead1.png")

# add loop to get input, continue to high scores, etc
cont = 0
while cont == 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: cont = 1
        if not hasattr(event, 'key'): continue
        if event.key == pygame.K_ESCAPE: cont = 1
    screen.blit(disp, (0, 0))
    pygame.display.flip()
# elif(endgame == 1): continue

# update and view high scores
# open file
# scores = []
# f = open('scores', 'rw')
# for line in f:
#	scores.append(line)
# print scores
# read scores into list
# compare score to list
# display high scores


pygame.quit()
sys.exit()
