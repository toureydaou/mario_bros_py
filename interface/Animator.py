import pygame
from os import listdir
from os.path import isfile, join


class animator(pygame.sprite.Sprite):  # classe pour gérer les animations, hérite de Sprite
    
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)  # initialisation du Sprite parent
        self.screen = screen  # référence à la surface d'affichage
        
    def load_spritesheet(self, dir1, dir2, prefix, width, height, direction=False):
        # construit le chemin vers le dossier contenant les sprites
        path = join("assets", dir1, dir2)
        # récupère tous les fichiers du répertoire
        images = [f for f in listdir(path) if isfile(join(path, f))]
        
        all_sprites = {}  # dictionnaire pour stocker les animations par nom
        for image in images:
            # charge le spritesheet avec canal alpha pour la transparence
            sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()
            sprites = []  # liste des surfaces représentant chaque frame
            
            # découpe le spritesheet en tuiles de taille (width x height)
            for i in range(0, sprite_sheet.get_height() // height):  # lignes
                for j in range(0, sprite_sheet.get_width() // width):  # colonnes
                    # crée une surface transparente de taille (width, height)
                    surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
                    # définit la zone à copier depuis le spritesheet
                    rect = pygame.Rect(j * width, i * height, width, height)
                    # copie la région définie sur la nouvelle surface
                    surface.blit(sprite_sheet, (0, 0), rect)
                    # ajoute la frame mise à l'échelle (scale2x)
                    sprites.append(pygame.transform.scale2x(surface))
                
            if direction:
                # si on veut gérer direction, on stocke deux animations : droite et gauche
                key = image.replace(prefix, "") + "_right"
                all_sprites[key] = sprites
                # crée la version retournée (miroir horizontal)
                flipped = [pygame.transform.flip(sprite, True, False) for sprite in sprites]
                all_sprites[image.replace(prefix, "") + "_left"] = flipped
            else:
                # sinon, on stocke l'animation sans distinction de direction
                all_sprites[image.replace(prefix, "")] = sprites
                
        return all_sprites  # renvoie le dictionnaire de toutes les animations
