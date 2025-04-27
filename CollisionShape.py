class CollisionShape:
    def __init__(self, obj, offset_x, offset_y, radius):
        self.obj = obj
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.x = obj.x + self.obj.width + offset_x
        self.y = obj.y + self.obj.height + offset_y
        self.radius = radius
        
    def update_collision_shape(self):
        self.x = self.obj.x + self.obj.width + self.offset_x
        self.y = self.obj.y + self.obj.height + self.offset_y