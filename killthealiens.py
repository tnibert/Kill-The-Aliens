#! /usr/bin/env python

import pygame

# setup audio mixer
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
# initialize pygame before dependent imports
pygame.init()

from constants import SCREENW, SCREENH, PLAYERHEALTH, TEXTCOLOR, VAL_X_LOC, VAL_Y_LOC_START, VAL_TEXT_SIZE, VAL_FONT
from loadstaticres import introscreen, shipimg
from levelconfigs import level_configs
from scene import Scene
from queue import Queue
from level import Level
from player import Player
from textelement import TextElement
from endgamesignal import EndLevel
from splashpage import SplashPage
import sys

# todo:
# fix nuitka build, make linux build
# add unit tests
# setup ci
#
# add hi scores screen
# add easy, medium, hard difficulty options
#
# add a second level config:
# test with changing music between levels
# give second level boss own behavior (original boss behavior)
#
# add to score on boss death
#
# Ensure initial saucers spawn off screen
# normalize ship diagonal movement
# Replace health texts with health bars

# queues for input events
input_queue = Queue()

# set up window
screen = pygame.display.set_mode((SCREENW, SCREENH), pygame.DOUBLEBUF)
pygame.display.set_caption("KILL THE ALIENS")

# objects which will be shared between levels
shared_objects = {
    "ship": Player(shipimg, input_queue),
    "health_label": TextElement(VAL_X_LOC, VAL_Y_LOC_START, VAL_FONT, TEXTCOLOR, "Health: {}", PLAYERHEALTH),
    "score_label": TextElement(VAL_X_LOC, VAL_Y_LOC_START+VAL_TEXT_SIZE, VAL_FONT, TEXTCOLOR, "Score: {}", 0)
}

shared_objects["ship"].subscribe("alterhealth", shared_objects["health_label"].update_value)

# list of levels (including splash pages
levels = [
    SplashPage(Scene(screen), input_queue, introscreen, pygame.K_RETURN)
]

# append to list of levels for every available level configuration
for config in level_configs:
    levels.append(Level(Scene(screen), pygame.mixer, config, shared_objects))

# proceed through the levels
# NB: setup() call for SplashPage is unnecessary
while len(levels) > 0:

    # process and queue valid input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif not hasattr(event, 'key'):
            continue
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            input_queue.put(event)

    # run the level
    try:
        levels[0].run_game()

    # EndLevel exception signals end of level
    except EndLevel as e:
        # remove current level from level list
        is_splash = isinstance(levels.pop(0), SplashPage)

        # stop the game if player is out of lives
        if e.args[0].get("state") == "failure":
            levels = [SplashPage(Scene(screen), input_queue, pygame.image.load("assets/dead1.png"), pygame.K_ESCAPE)]
            continue

        # if there are still levels to go, set up the scene
        if len(levels) > 0:
            levels[0].setup()

        # handle last level finishing
        elif len(levels) == 0 and not is_splash:
            if e.args[0].get("state") == "victory":
                levels.append(SplashPage(Scene(screen), input_queue, pygame.image.load("assets/victory1.png"), pygame.K_ESCAPE))

        print("Score: {}".format(shared_objects["score_label"].get_value()))

    # apply double buffer
    pygame.display.flip()


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
