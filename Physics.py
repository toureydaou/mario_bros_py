import math
from gameObjects.Player import player


class physics:

    def __init__(self, tile_map, ennemies, gravity=2):
        self.tile_map = tile_map            # les tiles du monde
        self.ennemies = ennemies            # Référence à l'ennemi pour collision
        self.gravity = gravity              # Accélération gravitationnelle
        self.max_y_velocity = 25            # Vitesse de chute maximale

    def apply_gravity(self, obj):
        # Applique la gravité si l'objet n'est pas au sol
        if not obj.on_ground:
            obj.y_velocity = min(obj.y_velocity + self.gravity, self.max_y_velocity)
        else:
            obj.y_velocity = 0

        # Bonus de saut pour le joueur
        if isinstance(obj, player) and obj.is_jumping:
            obj.y_velocity -= 5

    def check_collision(self, obj):
        tile_size = 32
        nearest_tile = None
        min_dist_sq = float('inf')

        # Parcours des tuiles pour trouver la plus proche en collision
        for tile in self.tile_map.tiles:
            # Coordonnée la plus proche sur la tuile
            cx = max(tile[0], min(obj.collision_shape.x, tile[0] + tile_size))
            cy = max(tile[1], min(obj.collision_shape.y, tile[1] + tile_size))
            dx = obj.collision_shape.x - cx
            dy = obj.collision_shape.y - cy
            dist_sq = dx*dx + dy*dy

            if dist_sq <= obj.collision_shape.radius**2 and dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                nearest_tile = tile
                closest_dx, closest_dy = dx, dy

        if nearest_tile:
            angle = math.degrees(math.atan2(closest_dy, closest_dx))
            # Collision selon l'angle d'impact
            if 30 <= angle <= 160:
                return 4, nearest_tile  # collision dessous
            if -160 <= angle <= -30:
                return 3, nearest_tile  # collision dessus
            if angle > 160 or angle < -160:
                return 2, nearest_tile  # collision droite
            if -30 < angle < 30:
                return 1, nearest_tile  # collision gauche

        return 0, None  # pas de collision

    def characters_collision(self, character): # Collision entre joueur et ennemies
        
        for enm in self.ennemies:
            dx = character.collision_shape.x - enm.collision_shape.x
            dy = character.collision_shape.y - enm.collision_shape.y
            dist_sq = dx*dx + dy*dy
            r_sum = character.collision_shape.radius + enm.collision_shape.radius
            if (dist_sq <= r_sum*r_sum):
                return True
