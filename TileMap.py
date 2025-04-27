from interface.Animator import animator
from Config import config

class tileMap(animator):
    def __init__(self, camera, screen):
        super().__init__(screen)
        self.SKYBOX_tile_size = 128  # Taille d'une tuile de ciel
        self.GROUND_tile_size = 32   # Taille d'une tuile de sol
        self.tiles = []              # Liste des positions de tuiles terrain
        self.camera = camera         # Caméra pour le rendu décalé
        # Chargement des sprites de fond et de terrain
        self.skybox_sprite = self.load_spritesheet("Background", "", ".png", 64, 64, False)
        self.ground_sprite = self.load_spritesheet("Terrain", "", " (16x16).png", 16, 16, False)
  
    def draw_skybox(self):
        # Affiche le fond de ciel en mosaïque
        for row in range(720 // 64):
            y = row * self.SKYBOX_tile_size
            for col in range(1280 // 64):
                x = col * self.SKYBOX_tile_size
                sprite = self.skybox_sprite[config.BACKGROUND_SPRITE][0]
                self.screen.blit(sprite, (x, y))
    
    def draw_terrain(self, x, y, width, height):
        # Génère et dessine les tuiles de terrain dans la zone donnée
        for row in range(y // self.GROUND_tile_size, (y + height) // self.GROUND_tile_size):
            y_cord = row * self.GROUND_tile_size
            for col in range(x // self.GROUND_tile_size, (x + width) // self.GROUND_tile_size):
                x_cord = col * self.GROUND_tile_size
                self.tiles.append((x_cord, y_cord))  # Stocke la position pour la physique
                # Calcul du rendu selon la position relative à la caméra
                screen_x = x_cord - self.camera.camera.x
                screen_y = y_cord - self.camera.camera.y
                # Sélection du sprite selon bord/corner/interieur
                if y_cord - y < 0 and x_cord - x < 0:
                    idx = 6  # coin haut-gauche
                elif y_cord + self.GROUND_tile_size >= self.GROUND_tile_size * ((y + height) // self.GROUND_tile_size) and x_cord - x < 0:
                    idx = 50  # coin bas-gauche
                elif x_cord + self.GROUND_tile_size >= self.GROUND_tile_size * ((x + width) // self.GROUND_tile_size) and y_cord - y < 0:
                    idx = 8   # coin haut-droit
                elif x_cord + self.GROUND_tile_size >= self.GROUND_tile_size * ((x + width) // self.GROUND_tile_size) and y_cord + self.GROUND_tile_size >= self.GROUND_tile_size * ((y + height) // self.GROUND_tile_size):
                    idx = 52  # coin bas-droit
                elif y_cord - y < 0:
                    idx = 7   # bord haut
                elif x_cord - x < 0:
                    idx = 28  # bord gauche
                elif y_cord + self.GROUND_tile_size >= self.GROUND_tile_size * ((y + height) // self.GROUND_tile_size):
                    idx = 51  # bord bas
                elif x_cord + self.GROUND_tile_size >= self.GROUND_tile_size * ((x + width) // self.GROUND_tile_size):
                    idx = 30  # bord droit
                else:
                    idx = 29  # intérieur (pas de collision)
                    self.tiles.pop()  # Retire si pas collision
                # Blit du sprite choisi
                self.screen.blit(self.ground_sprite["Terrain"][idx], (screen_x, screen_y))
