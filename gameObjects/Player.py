import pygame
from interface.Object import object
from Physics import physics


class player(object):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.width = 50
        self.height = 50
        self.life_points = 3
        self.lives = 3
        self.isDead = False
        self.x_velocity = 10
        self.y_velocity = 0
        self.on_ground = False
        self.is_jumping = False
        self.jump_limit = self.y - 100

    def update(self, physics):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.x_velocity
        if keys[pygame.K_RIGHT]:
            self.x += self.x_velocity
        if keys[pygame.K_UP] and self.on_ground:
            self.is_jumping = True
            self.on_ground = False
            self.update_jump_limit()

        physics.apply_gravity(self)
        
        if self.y <= self.jump_limit:
            self.is_jumping = False
            
        print("-----------------------------")
        print("isJumping : " + (str)(self.is_jumping))
        print("on ground : " + (str)(self.on_ground))
        print("y position : " + (str)(self.y))
        print("-----------------------------")
            
        if self.y + self.y_velocity >= 500 :
            self.y = 500
            self.y_velocity = 0
            self.on_ground = True
            
        self.y += self.y_velocity

    
    def update_jump_limit(self):
        self.jump_limit = self.y - 100
        
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0),
                         (self.x, self.y, self.width, self.height))

    def on_hit(self):
        if (self.life_points - 1 <= 0):
            if (self.lives - 1 <= 0):
                self.isDead = True
            else:
                self.lives = self.lives - 1
        else:
            self.life_points = self.life_points - 1
