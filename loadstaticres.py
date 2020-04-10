from utilfuncs import toframes
import pygame


introscreen = pygame.image.load("intro1.png")

explosion = toframes(pygame.image.load("explode1.png"), 5, 120)

shipimg = pygame.image.load("spaceship1.png")
saucerimg = pygame.image.load("saucer1.png")
bulletimg = pygame.image.load("bullet1.png")
bossimg = pygame.image.load("invader2.png")

# status modifier images
oneupimg = pygame.image.load("plus102.png")
bombimg = pygame.image.load("bomb.png")
speedupimg = pygame.image.load("speed.png")
moregunsimg = pygame.image.load("guns.png")

background = pygame.image.load("map1.png")

BG_MUSIC_FNAME = "spectre.mp3"

blank = pygame.Surface((1, 1))
