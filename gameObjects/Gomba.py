import pygame

from interface.Object import object
from Physics import physics


class Gomba(object):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.width = 30
        self.height = 30
        self.isDead = False

    def draw(self, screen):
        pygame.draw.rect(screen, (91, 60, 17),
                         (self.x, self.y, self.width, self.height))

    def lateral_hit(self, object):
        if ((self.x + self.width) == object.get_x):
            return True

    def update(self, physics):

        direction = -1
        if self.lateral_hit(object):
            direction *= -1
        self.x += direction * 1.5
