from utilfuncs import toframes
import pygame


introscreen = pygame.image.load("assets/intro1.png")

explosion = toframes(pygame.image.load("assets/explode1.png"), 5, 120)

shipimg = pygame.image.load("assets/spaceship1.png")
saucerimg = pygame.image.load("assets/saucer1.png")
bulletimg = pygame.image.load("assets/bullet1.png")
bossimg = pygame.image.load("assets/invader2.png")

# status modifier images
oneupimg = pygame.image.load("assets/plus102.png")
bombimg = pygame.image.load("assets/bomb.png")
speedupimg = pygame.image.load("assets/speed.png")
moregunsimg = pygame.image.load("assets/guns.png")

background = pygame.image.load("assets/map1.png")

BG_MUSIC_FNAME = "assets/spectre.mp3"

blank = pygame.Surface((1, 1))
