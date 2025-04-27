import pygame
from interface.Animator import animator
from interface.Object import object
from CollisionShape import CollisionShape


class Rabbit(object, animator):
    def __init__(self, x, y, player, screen):

        super().__init__(x, y, screen)
        self.width = 34
        self.height = 44

        # Références et états
        self.player = player  # Référence au joueur
        self.screen = screen  # Surface pour le rendu
        self.direction = True  # True = regard vers la droite, False = vers la gauche
        self.on_ground = False  # Indique si le lapin est au sol
        self.isDead = False  # Indique si le lapin est mort

        # Vitesse horizontale et verticale
        self.x_velocity = 0
        self.y_velocity = 0

        # Animation
        self.animation_count = 0  # Compteur pour l'index de sprite

        # Collision
        self.collision_shape = CollisionShape(self, 0, 21, 24)

        # Chargement du spritesheet : dossier "Enemies", sous-dossier "Bunny"
        self.SPRITE = self.load_spritesheet(
            "Enemies", "Bunny", " (34x44).png", self.width, self.height, True
        )

    def update_sprite(self):

        # Choix de l'animation Idle ou Run
        if self.x_velocity == 0:
            base = "Idle"
        else:
            base = "Run"

        # Suffixe selon la direction
        suffix = "_right" if self.direction else "_left"
        sprites = self.SPRITE[base + suffix]

        # Sélection et progression de la frame d'animation
        index = (self.animation_count // 3) % len(sprites)
        self.sprite = sprites[index]
        self.animation_count += 1

    def _handle_horizontal_collision(self, collision):

        code, pos = collision
        grounded = self.on_ground

        if code == 2:  # Collision à droite
            self.x = pos[0] - self.width - self.collision_shape.radius
            self.x_velocity = 0
        elif code == 1:  # Collision à gauche
            self.x = pos[0] + self.width - self.collision_shape.radius // 2
            self.x_velocity = 0
        else:
            grounded = False

        return grounded

    def _handle_vertical_collision(self, collision, grounded):

        code, pos = collision
        offset = self.width + self.collision_shape.offset_y + self.collision_shape.radius

        if code == 3:  # Atterri sur le dessus d'un objet
            self.y = pos[1] - offset - 7
            self.y_velocity = 0
            self.on_ground = True
        elif code == 4:  # Heurte le plafond
            self.y = pos[1] - self.height + offset
            self.y_velocity = 0
        else:
            # Pas de collision verticale : annule le déplacement
            self.y -= self.y_velocity
            self.on_ground = grounded

    def update(self, physics):

        # Déplacement horizontal vers le joueur
        if (self.player.x - self.x) < 0:
            self.direction = True
            self.x_velocity = -5
        else:
            self.direction = False
            self.x_velocity = 5

        # Applique la gravité
        physics.apply_gravity(self)

        # Si mouvement détecté, traiter le déplacement et les collisions
        if self.x_velocity != 0 or self.y_velocity != 0:
            # Déplacement initial
            self.x += self.x_velocity
            self.y += self.y_velocity
            self.collision_shape.update_collision_shape()

            collision = physics.check_collision(self)

            # Collision horizontale
            was_grounded = self._handle_horizontal_collision(collision)
            self.collision_shape.update_collision_shape()

            # Collision verticale
            self._handle_vertical_collision(collision, was_grounded)
            self.collision_shape.update_collision_shape()

            # Si le lapin n'est pas au sol, retomber
            if not self.on_ground:
                self.y += self.y_velocity
                self.collision_shape.update_collision_shape()

    def draw(self):

        self.update_sprite()
        self.screen.blit(self.sprite, (self.x, self.y))

        # pygame.draw.circle(self.screen, "red", (self.collision_shape.x, self.collision_shape.y), self.collision_shape.radius, 3)
