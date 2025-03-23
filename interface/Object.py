class object :

    def __init__(self,x,y):
        self.x = x
        self.y = y
        
        
    def update(self):
        pass
    
    def get_x(self):
        return self.x
        
    def get_y(self):
        return self.y
     
    def set_x(self, new_x):
        self.X = new_x
        
    def set_y(self, new_y):
        self.Y = new_y
    
    def draw(self, screen):
        pass
    
    def __hash__(self):
        return hash((self.x, self.y, type(self).__name__))

    def __eq__(self, other):
        return isinstance(other, object) and self.x == other.x and self.y == other.y and type(self) == type(other)