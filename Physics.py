class physics:
    def __init__(self, gravity=0.5, velocity=10):
        self.gravity = gravity
        self.velocity = velocity

    def apply_gravity(self, obj):
        
        if not obj.on_ground:
            obj.y_velocity += self.gravity
            obj.y_velocity = min(obj.y_velocity, self.velocity)
        else:
            obj.y_velocity = 0

    def check_collision(self, obj, platforms):
        obj.on_ground = False

        for platform in platforms:
            if (obj.x < platform.x + platform.width and
                obj.x + obj.width > platform.x and
                obj.y + obj.height > platform.y and
                obj.y + obj.height - obj.y_velocity < platform.y):
                
                obj.y = platform.y - obj.height
                obj.y_velocity = 0
                obj.on_ground = True
            
