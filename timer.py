from observe import Observable, Event
from gameobject import GameObject
import pygame


class Timer(GameObject):
    def __init__(self):
        GameObject.__init__(self, None)
        self.time = 0
        self.clock = pygame.time.Clock()
        self.fps = 30

    def update(self):
        ticktime = self.clock.tick(self.fps)  # update time in milliseconds
        self.time += ticktime

    def draw(self, screen):
        pass
