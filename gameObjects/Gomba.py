import pygame

from interface.Object import object
from Physics import physics


class Gomba(object):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.width = 30
        self.height = 30
        self.isDead = False
        self.direction = -1
        

    def draw(self, screen):
        pygame.draw.rect(screen, (91, 60, 17),
                         (self.x, self.y, self.width, self.height))

    def lateral_hit(self, pipes, gombas):
        for pipe in pipes:
            if (self.x + self.width > pipe.get_x() and self.x < pipe.get_x() + pipe.width and self.y + self.height > pipe.get_y() and self.y < pipe.get_y() + pipe.height):
                return True
        for gomba in gombas:
            if ((self.x + self.width > gomba.get_x() and self.x < gomba.get_x() + gomba.width and self.y + self.height > gomba.get_y() and self.y < gomba.get_y() + gomba.height) and self != gomba):
                return True
        return False

    def update(self, pipes, gombas):

        if self.lateral_hit(pipes, gombas):
            print(self.direction)
            self.direction *= -1    
        self.x += self.direction * 1.5
