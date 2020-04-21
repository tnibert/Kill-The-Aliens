import boss
import pygame

"""
This list of dicts represents the static resources for
the various levels.
"""

# todo: add behaviors (boss, enemies) into this config
level_configs = [
    {
        "background": pygame.image.load("assets/level1/map.png"),
        "bg_music_fname": "assets/spectre.mp3",
        "boss_image": pygame.image.load("assets/level1/boss.png"),
        "enemy_image": pygame.image.load("assets/level1/saucer.png"),
        "boss_class": boss.Boss
    },
    # todo; saucers aren't appearing on this level
    # todo: boss erroneously appears from bottom of screen
    {
        "background": pygame.image.load("assets/level2/map.png"),
        "bg_music_fname": "assets/spectre.mp3",
        "boss_image": pygame.image.load("assets/level2/invader.png"),
        "enemy_image": pygame.image.load("assets/level2/saucer.png"),
        "boss_class": boss.Boss
    }
]