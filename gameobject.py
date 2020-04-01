from observe import Observable
from timer import Timer
import pygame


class GameObject(pygame.sprite.Sprite, Observable):
    def __init__(self, img, layer=0):
        pygame.sprite.Sprite.__init__(self)
        Observable.__init__(self)
        # todo: may be better to not having GameObject tied to rendering
        self.image = img
        self.layer = layer
        self.frame_timer = Timer()
        self.frame_tick = 0

    def update(self):
        self.frame_tick = self.frame_timer.tick()

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))
