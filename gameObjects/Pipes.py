import pygame

from interface.Object import object
from Physics import physics


class Pipes(object):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.width = 100
        self.height = 150

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0),
                         (self.x, self.y, self.width, self.height))
