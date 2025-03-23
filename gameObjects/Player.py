import pygame
from interface.Object import object
from Physics import physics

class player(object) :
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.width = 50
        self.height = 50
        self.life_points = 3
        self.lives = 3
        self.isDead = False
        self.y_velocity = 0
        self.on_ground = False
        
    def update(self, physics):
        
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.x -= 5
        if keys[pygame.K_d]:
            self.x += 5
        if keys[pygame.K_SPACE] and self.on_ground:
            self.y_velocity = -10
            
        physics.apply_gravity(self)

        if(self.y >= 500):
            self.on_ground = True
        else:
            self.on_ground = False

        self.y += self.y_velocity
        print(self.y)
        
        
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
        
    def on_hit(self):
        if(self.life_points - 1 <= 0):
            if(self.lives - 1 <= 0):
                self.isDead = True
            else:
                self.lives = self.lives - 1
        else:
            self.life_points = self.life_points - 1