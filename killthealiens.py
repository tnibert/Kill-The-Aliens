#! /usr/bin/env python
from enemy import Enemy
from constants import *
from loadstaticres import *
from scene import Scene
from queue import Queue
from level import Level
import pygame
import sys

# todo:
# ship death on saucer impact
#
# move the boss to the new architecture
# we also need to fix the bug in the boss with infirerange() returning None
# have boss signal saucers to clear out when entering
#
# normalize ship diagonal movement
#
# add score keeping and add text elements to scene
# load static resources from file
# multiple level capability
# increase speed of speed up power up, and match speed on map and ship

# queues for input events
player_input_queue = Queue()

# setup audio mixer
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

pygame.init()

# set up window
screen = pygame.display.set_mode((SCREENW, SCREENH), pygame.DOUBLEBUF)
pygame.display.set_caption("KILL THE ALIENS")

gamescene = Scene(screen)

# set text font
myfont = pygame.font.SysFont("monospace", 15)

# load up music
pygame.mixer.music.load(BG_MUSIC_FNAME)

# actually transparent square
blacksquare = pygame.Surface((explosion[0].get_width() - 15, explosion[0].get_height() - 15), pygame.SRCALPHA, 32)

# create boss
#boss = Boss(100, -1200, bossimg, 0)

# create boss explosions
# maybe move this later in the code and don't create it in memory until we need it
#boom = []
#boom.append(MoveableObject(0, 0, pygame.Surface((1, 1))))

#clock = pygame.time.Clock()

# flags
# 0 means play, 1 means user exit, 2 means death, 3 means victory
endgame = 0
# 0 means no boss, 1 means clear out shop for boss, 2 means boss entering,
# 3 means boss is out, 4 means dying, 5 means dead
#BEASTMODE = 0

#blacksquare.fill(BLACK)

score = 0

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

# create enemies
for x in range(0, 3):
    gamescene.attach(Enemy(saucerimg))

mylevel = Level(gamescene, player_input_queue)

# start music on endless loop
pygame.mixer.music.play(-1)

# begin main game loop
# this should have all been put in a function T_T
while endgame == 0:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif not hasattr(event, 'key'):
            continue
        elif event.key == pygame.K_ESCAPE:
            endgame = 1
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            player_input_queue.put(event)

    #if BEASTMODE == 3:  # if boss is out
    #    if boss.infirerange(ship) > 0:
    #        if random.randrange(0, 10) == 1 and ship.exploding == -1:  # and if ship is not exploding
    #            bullets.append(boss.fire(bulletimg, LEFT))
    #        if random.randrange(0, 10) == 1 and ship.exploding == -1:
    #            bullets.append(boss.fire(bulletimg, RIGHT))

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
    #healthlbl = myfont.render("Health: " + str(ship.health), 1, (255, 255, 0))
    #scorelbl = myfont.render("Score: " + str(score), 1, (255, 255, 0))
#    bosslbl = myfont.render("Boss Health: " + str(boss.health), 1, (255, 255, 0))

    mylevel.run_game()

    # if BEASTMODE >= 2: screen.blit(boss.image, (boss.x, boss.y))
    #
    # if BEASTMODE >= 4:
    #     for splat in boom:
    #         screen.blit(splat.image, (splat.x, splat.y))

    #screen.blit(healthlbl, (SCREENW - 100, 20))
    #screen.blit(scorelbl, (SCREENW - 100, 35))
    # if BEASTMODE >= 3: screen.blit(bosslbl, (SCREENW / 2, 20))

    pygame.display.flip()  # apply double buffer

# end game loop

# display end screens
# todo: move file loads to resource loader
BEASTMODE = 5
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
