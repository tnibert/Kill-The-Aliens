from observe import Observable
import pygame


class GameObject(pygame.sprite.Sprite, Observable):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        Observable.__init__(self)
        self.image = img

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
