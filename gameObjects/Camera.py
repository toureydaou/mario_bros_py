import pygame
from Config import config

class camera:
    def __init__(self, player, smoothing_factor=0.05):

        self.player = player  # Référence à l'objet joueur
        # Dimensions de l'écran
        self.screen_width = config.SCREEN_WIDTH  # Largeur de la fenêtre de jeu
        self.screen_height = config.SCREEN_HEIGHT  # Hauteur de la fenêtre de jeu
        # Rectangle représentant la zone visible (viewport)
        self.camera = pygame.Rect(0, 0, self.screen_width, self.screen_height)
        # Facteur de lissage pour amortir le mouvement de la caméra
        self.smoothing_factor = smoothing_factor

    def update(self):

        # Position cible pour centrer la caméra sur le joueur
        target_camera_x = self.player.x - self.screen_width // 2
        target_camera_y = self.player.y - self.screen_height // 2

        # Interpolation linéaire : rapprochement progressif vers la position cible
        self.camera.x += (target_camera_x - self.camera.x) * self.smoothing_factor
        self.camera.y += (target_camera_y - self.camera.y) * self.smoothing_factor

        # Limitation : empêcher la caméra de sortir des bords du monde
        world_width, world_height = config.WORLD_SIZE[0], config.WORLD_SIZE[1]

        self.camera.x = max(0, min(self.camera.x, world_width - self.screen_width))

        self.camera.y = max(0, min(self.camera.y, world_height - self.screen_height))

    def apply(self, entity):
        # Calcul de la position relative à la viewport
        return entity.x - self.camera.x, entity.y - self.camera.y
