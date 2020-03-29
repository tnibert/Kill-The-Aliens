from observe import Observable
import pygame


class GameObject(pygame.sprite.Sprite, Observable):
    def __init__(self, img, layer=0):
        pygame.sprite.Sprite.__init__(self)
        Observable.__init__(self)
        # todo: may be better to not having GameObject tied to rendering
        self.image = img
        self.layer = layer

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
