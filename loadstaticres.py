from utilfuncs import toframes
from boss import Boss
import pygame


introscreen = pygame.image.load("assets/intro1.png")

explosion = toframes(pygame.image.load("assets/explode1.png"), 5, 120)

shipimg = pygame.image.load("assets/spaceship1.png")
bulletimg = pygame.image.load("assets/bullet1.png")

# status modifier images
oneupimg = pygame.image.load("assets/plus102.png")
bombimg = pygame.image.load("assets/bomb.png")
speedupimg = pygame.image.load("assets/speed.png")
moregunsimg = pygame.image.load("assets/guns.png")

blank = pygame.Surface((1, 1))

# list of dicts
# each dict represents the static resources for a level
# todo: add behaviors (boss, enemies) into this config
level_configs = [
    {
        "background": pygame.image.load("assets/level1/map.png"),
        "bg_music_fname": "assets/spectre.mp3",
        "boss_image": pygame.image.load("assets/level1/boss.png"),
        "enemy_image": pygame.image.load("assets/level1/saucer.png"),
        "boss_class": Boss
    },
    # todo; saucers aren't appearing on this level
    # todo: boss erroneously appears from bottom of screen
    {
        "background": pygame.image.load("assets/level2/map.png"),
        "bg_music_fname": "assets/spectre.mp3",
        "boss_image": pygame.image.load("assets/level2/invader.png"),
        "enemy_image": pygame.image.load("assets/level2/saucer.png"),
        "boss_class": Boss
    }
]
