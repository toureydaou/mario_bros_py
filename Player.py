import pygame

class Player :
    
    def __init__(self, X, Y):
        self.life_points = 3
        self.lives = 3
        self.speed = 10
        self.jump = 5
        self.isDead = False
        self.X = X
        self.Y = Y
        
        
    def on_hit(self):
        if(self.life_points - 1 <= 0):
            if(self.lives - 1 <= 0):
                self.isDead = True
            else:
                self.lives = self.lives - 1
        else:
            self.life_points = self.life_points - 1
            
    def set_x(self, new_x):
        self.x = new_x
        
    def set_y(self, new_y):
        self.y = new_y
        
    def get_positions(self):
        return (self.x, self.y)