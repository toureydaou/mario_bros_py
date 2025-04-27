from interface.Animator import animator
import pygame
from interface.Object import object
from CollisionShape import CollisionShape
from Config import config
            
        
class player(object, animator):  # Classe du joueur, hérite de object et animator

    def __init__(self, x, y, render_x, render_y, screen):
        super().__init__(x, y, 32, 32, True, screen)  # Appel du constructeur de la classe parente
        self.render_x = render_x  # Position de rendu à l'écran en x
        self.render_y = render_y  # Position de rendu à l'écran en y
        self.animation_count = 0  # Compteur de frames pour l'animation
        self.animation_time = 0  # Chronomètre interne pour les animations et le état "touché"
        self.jump_limit = self.y - config.PLAYER_JUMP_POWER  # Hauteur maximale de saut
        self.life_points = config.PLAYER_LIFE_POINTS  # Points de vie initiaux
        self.chances = config.PLAYER_CHANCES  # Nombre de vies/disponibilités
        self.isDead = False  # État mort ou vivant
        self.isHit = False  # Indique si le joueur vient de subir un coup
        self.x_velocity = 0  # Vitesse horizontale actuelle
        self.y_velocity = 0  # Vitesse verticale actuelle
        self.on_ground = False  # Indique si le joueur est au sol
        self.is_jumping = False  # État de saut en cours
        self.collision_shape = CollisionShape(self, 0, 10, 22)  # Zone de collision du joueur
        self.SPRITE = self.load_spritesheet("Main Characters", "Pink Man", " (32x32).png", self.width, self.height, True)  # Chargement des sprites
        

    def move_player(self):
        keys = pygame.key.get_pressed()  # Récupère l'état du clavier

        if keys[pygame.K_LEFT]:  # Flèche gauche pressée
            self.x_velocity = config.PLAYER_SPEED * -1  # Déplacement vers la gauche
            if self.direction == True and self.isHit == False:
                 self.animation_count = 0  # Réinitialise l'animation si on change de direction
        if keys[pygame.K_RIGHT]:  # Flèche droite pressée
            self.x_velocity = config.PLAYER_SPEED  # Déplacement vers la droite
            if self.direction == False and self.isHit == False:
                self.animation_count = 0  # Réinitialise l'animation si on change de direction
        if keys[pygame.K_UP] and self.on_ground:  # Flèche haut pour sauter
            self.is_jumping = True  # Déclenchement du saut
            self.on_ground = False  # Désactive l'état "au sol"
            self.update_jump_limit()  # Met à jour la limite de saut
            if(self.isHit == False):
                self.animation_count = 0  # Réinitialise l'animation de saut
    
    def check_if_hit(self, physics):
        if(self.animation_time >= 60 and physics.characters_collision(self)):
            self.isHit = True  # Le joueur est touché
            self.animation_time = 0  # Réinitialise le chronomètre
            self.on_hit()  # Gère la perte de vie
        
        self.animation_time += 1  # Incrément du chronomètre
        
        if self.isHit == True and self.animation_time >= 18:  # Durée de l'animation "Hit"
            self.isHit = False  # Fin de l'état "touché"
            self.animation_count = 0  # Réinitialise l'animation
            
    def on_horizontal_collision_terrain(self, physics):
        self.x += self.x_velocity  # Avance horizontalement
        self.collision_shape.update_collision_shape()  # Met à jour la zone de collision
        
        horizontal_collision = physics.check_collision(self)  # Vérifie collision horizontale
        already_on_ground = False  # Mémorise si on était déjà au sol
        
        if(horizontal_collision[0] == 1):  # Collision à gauche
            self.x = horizontal_collision[1][0] + self.width - self.collision_shape.radius//2
            self.x_velocity = 0  # Arrête le mouvement horizontal
            if(self.on_ground):
                already_on_ground = True  # Conserve l'état sol

        elif(horizontal_collision[0] == 2):  # Collision à droite
            self.x = horizontal_collision[1][0] - self.width - self.collision_shape.radius
            self.x_velocity = 0  # Arrête le mouvement horizontal
            if(self.on_ground):
                already_on_ground = True  # Conserve l'état sol
        else:
            self.x = self.x - self.x_velocity  # Pas de collision : annule le déplacement
        
        return already_on_ground  # Retourne l'état sol initial
    
    def on_vertical_collision_terrain(self, physics, already_on_ground):
        self.y += self.y_velocity  # Avance verticalement
        self.collision_shape.update_collision_shape()  # Met à jour la zone de collision
        vertical_collision = physics.check_collision(self)  # Vérifie collision verticale
        
        if vertical_collision[0] == 3:  # Atterri sur un objet
            self.y = vertical_collision[1][1] - (self.width + self.collision_shape.offset_y + self.collision_shape.radius)  # Ajuste position y
            self.y_velocity = 0  # Arrête la chute
            self.on_ground = True  # Met à jour l'état sol
            
        elif vertical_collision[0] == 4:  # Heurte un plafond
            self.y = vertical_collision[1][1] - self.height + (self.width + self.collision_shape.offset_y + self.collision_shape.radius)
            self.y_velocity = 0  # Arrête le mouvement vertical
            self.is_jumping = False  # Annule l'état saut
            
        else:
            self.y -= self.y_velocity  # Pas de collision : annule le déplacement
            self.on_ground = already_on_ground  # Restaure l'état sol
            
    def update(self, physics):
        self.x_velocity = 0  # Réinitialise la vitesse horizontale
        self.move_player()  # Gère l'entrée utilisateur
        physics.apply_gravity(self)  # Applique la gravité
        self.check_if_hit(physics)  # Vérifie si le joueur est touché
            
        if self.y_velocity == 0 and self.x_velocity == 0 and self.isHit == False:
            return  # Si pas de mouvement et pas touché, rien à faire
                
        already_on_ground = self.on_horizontal_collision_terrain(physics)  # Collision horizontale
        self.on_vertical_collision_terrain(physics, already_on_ground)  # Collision verticale
        
        if self.y <= self.jump_limit:
            self.is_jumping = False  # Arrête le saut si on atteint la hauteur max
            
        self.update_direction(self.x_velocity)  # Met à jour la direction du joueur
            
        if(self.on_ground == False):
            self.y += self.y_velocity  # Applique la chute si en l'air
            
        self.x += self.x_velocity  # Applique le déplacement horizontal
        self.collision_shape.update_collision_shape()  # Met à jour la zone de collision
        
    def update_direction(self, x_velocity):
        if(self.x_velocity > 0):
            self.direction = True  # Orientation vers la droite
        elif(self.x_velocity < 0):
            self.direction = False  # Orientation vers la gauche
        
    def update_jump_limit(self):
        self.jump_limit = self.y - config.PLAYER_JUMP_POWER  # Recalcule la limite de saut
        
    def update_sprite(self):
        
        if self.direction == True:
            sprite_direction = "_right"  # Choix du suffixe direction
        else:
            sprite_direction = "_left"
            
        sprite_name = "Idle" + sprite_direction  # Animation par défaut
        
        if self.x_velocity == 0 and self.on_ground:
            sprite_name = "Idle" + sprite_direction  # Stationnaire
        elif self.x_velocity != 0 and self.on_ground:
            sprite_name = "Run" + sprite_direction  # Course
        elif self.on_ground == False and self.y_velocity < 0:
            sprite_name = "Jump" + sprite_direction  # Saut ascendant
        elif self.on_ground == False and self.y_velocity > 0:
            sprite_name = "Fall" + sprite_direction  # Chute
        if self.isHit == True:
            sprite_name = "Hit" + sprite_direction  # Animation touché
            
        sprites = self.SPRITE[sprite_name]  # Récupère la liste de frames
        sprite_index = (self.animation_count // 3) % len(sprites)  # Calcule l'index
        self.sprite = sprites[sprite_index]  # Définit le sprite courant
        self.animation_count += 1  # Incrémente le compteur d'animation
         
    def draw(self):
        self.update_sprite()  # Met à jour le sprite
        self.screen.blit(self.sprite, (self.render_x, self.render_y))  # Affiche à l'écran

    def on_hit(self):
        if (self.life_points - 1 < 0):  # Si plus de points de vie
            if (self.chances - 1 < 0):  # Si plus de vies
                self.isDead = True  # Le joueur est mort
            else:
                self.life_points = 3  # Réinitialise les points de vie
                self.chances = self.chances - 1  # Diminue les vies
        else:
            self.life_points = self.life_points - 1  # Perte d'un point de vie
        
