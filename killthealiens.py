#! /usr/bin/env python
from constants import *
from loadstaticres import BG_MUSIC_FNAME, introscreen
from scene import Scene
from queue import Queue
from level import Level
from endgamesignal import EndLevel
import pygame
import sys

# todo:
# boss AI:
# add boss bum rush
#
# Currently boss can repeatedly destroy player on respawn
#
# game map speed up to reset on player death
#
# create levels for static screens
# move music control to level
#
# add hi scores screen
# add easy, medium, hard difficulty options
#
# load static resources from data structure for
# multiple level capability
#
# normalize ship diagonal movement
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

# flags
# 0 means play, 1 means user exit, 2 means death, 3 means victory
endgame = 0

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
            if event.key == pygame.K_RETURN:
                intro = 0

mylevel = Level(gamescene, player_input_queue)

# start music on endless loop
pygame.mixer.music.play(-1)

# begin main game loop
while endgame == 0:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif not hasattr(event, 'key'):
            continue
        elif event.key == pygame.K_ESCAPE:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            player_input_queue.put(event)

    try:
        mylevel.run_game()
    except EndLevel as e:
        endgame = 1
        if e.args[0] == "victory":
            disp = pygame.image.load("assets/victory1.png")
        else:
            disp = pygame.image.load("assets/dead1.png")

    pygame.display.flip()  # apply double buffer

# todo: move file loads to resource loader

# add loop to get input, continue to high scores, etc
cont = 0
while cont == 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: cont = 1
        if not hasattr(event, 'key'): continue
        if event.key == pygame.K_ESCAPE: cont = 1
    screen.blit(disp, (0, 0))
    pygame.display.flip()

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
