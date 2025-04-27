import pygame

class object(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, direction, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.direction = direction

