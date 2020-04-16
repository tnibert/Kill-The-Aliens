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
# remove bullet when boss is hit
# boss firing - in middle, multiple bullets in stream next to each other like laser
# boss or player final death to end game
# player collision with boss does not work
#
# add boss bum rush
#
# normalize ship diagonal movement
# move static resources to subdirectory
# load static resources from file
# multiple level capability
# increase speed of speed up power up, and match speed on map and ship
#
# Replace health texts with health bars

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

# load up music
pygame.mixer.music.load(BG_MUSIC_FNAME)

# actually transparent square
blacksquare = pygame.Surface((explosion[0].get_width() - 15, explosion[0].get_height() - 15), pygame.SRCALPHA, 32)

# flags
# 0 means play, 1 means user exit, 2 means death, 3 means victory
endgame = 0

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
            pygame.quit()
            sys.exit()
        if not hasattr(event, 'key'): continue
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN: intro = 0

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

    # for final player death
    # if ship.health <= 0 and endtime == 0:
    #     endtime = time
    #
    # # for time delay after death
    # if time >= endtime + 4000 and endtime != 0:
    #     # print "game over"
    #     endgame = 2

    # text rendering
    #healthlbl = myfont.render("Health: " + str(ship.health), 1, (255, 255, 0))
    #scorelbl = myfont.render("Score: " + str(score), 1, (255, 255, 0))

    mylevel.run_game()

    #screen.blit(healthlbl, (SCREENW - 100, 20))
    #screen.blit(scorelbl, (SCREENW - 100, 35))

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
