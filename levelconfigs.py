import boss
import pygame

"""
This list of dicts represents the static resources for
the various levels.
"""

# todo: add enemy behavior into this config
# todo: add boss health to this config
level_configs = [
    {
        "background": pygame.image.load("assets/simple_level/map.png"),
        "bg_music_fname": "assets/spectre.mp3",
        "boss_image": pygame.image.load("assets/simple_level/invader.png"),
        "enemy_image": pygame.image.load("assets/simple_level/saucer.png"),
        "boss_class": boss.BossL1Behave
    },
    {
        "background": pygame.image.load("assets/magykal_level/map.png"),
        "bg_music_fname": "assets/spectre.mp3",
        "boss_image": pygame.image.load("assets/magykal_level/boss.png"),
        "enemy_image": pygame.image.load("assets/magykal_level/saucer.png"),
        "boss_class": boss.BossL2Behave
    }
]