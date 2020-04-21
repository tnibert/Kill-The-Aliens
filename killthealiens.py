#! /usr/bin/env python
from constants import *
from loadstaticres import BG_MUSIC_FNAME, introscreen
from scene import Scene
from queue import Queue
from level import Level
from endgamesignal import EndLevel
from splashpage import SplashPage
import pygame
import sys

# todo:
# fix nuitka build, make linux build
# add unit tests
# setup ci
#
# add hi scores screen
# add easy, medium, hard difficulty options
#
# load static resources from data structure for
# multiple level capability
#
# Ensure initial saucers spawn off screen
# normalize ship diagonal movement
# Replace health texts with health bars

# queues for input events
input_queue = Queue()

# setup audio mixer
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

pygame.init()

# set up window
screen = pygame.display.set_mode((SCREENW, SCREENH), pygame.DOUBLEBUF)
pygame.display.set_caption("KILL THE ALIENS")

# load up music
pygame.mixer.music.load(BG_MUSIC_FNAME)

levels = [
    SplashPage(Scene(screen), input_queue, introscreen, pygame.K_RETURN),
    Level(Scene(screen), input_queue, pygame.mixer)
]

while len(levels) > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif not hasattr(event, 'key'):
            continue
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            input_queue.put(event)

    try:
        levels[0].run_game()
    except EndLevel as e:
        levels.pop(0)
        if e.args[0].get("state") == "victory":
            levels.append(SplashPage(Scene(screen), input_queue, pygame.image.load("assets/victory1.png"), pygame.K_ESCAPE))
        elif e.args[0].get("state") == "failure":
            levels.append(SplashPage(Scene(screen), input_queue, pygame.image.load("assets/dead1.png"), pygame.K_ESCAPE))

        score = e.args[0].get("score")
        if score is not None:
            print("Score: {}".format(score))

    pygame.display.flip()  # apply double buffer

# todo: move file loads to resource loader

# pseudocode to update and view high scores:
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
sys.exit(0)
