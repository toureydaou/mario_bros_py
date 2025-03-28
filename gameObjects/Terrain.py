import pygame

from interface.Object import object

class terrain(object):

    def __init__(self, x, y, width, height = 500):
        super().__init__(x, y)
        self.width = width
        self.height = height

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 173, 127),
                         (self.x, self.y, self.width, self.height))
