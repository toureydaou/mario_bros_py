class physics:
    def __init__(self, terrain=500, gravity=2, velocity=20):
        self.gravity = gravity
        self.velocity = velocity
        self.ground_level = 500

    def apply_gravity(self, obj):

        if not obj.on_ground:
            obj.y_velocity += self.gravity
            obj.y_velocity = min(obj.y_velocity, self.velocity)
        
        else:
            obj.y_velocity = 0
        
        if obj.is_jumping:
            obj.y_velocity += -5

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
