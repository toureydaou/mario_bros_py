import pygame
from interface.Animator import animator
from interface.Object import object
from CollisionShape import CollisionShape


class turtle(object, animator):
    def __init__(self, x, y, player, camera, screen):
        super().__init__(x, y, 44, 26, True, screen)
        self.player = player
        self.camera = camera

        # Physique et état
        self.x_velocity = 0  # Vitesse en x
        self.y_velocity = 0  # Vitesse en y
        self.on_ground = False  # Indique si Gomba est au sol
        self.isDead = False  # Indique si Gomba est mort

        # Animation
        self.animation_count = 0  # Compteur d'images
        self.spike_timer = 0  # Chronomètre pour l'état des piquants
        self.state = "idle_2"  # États possibles : idle_2, spikes_out, idle_1, spikes_in

        # Collision
        self.collision_shape = CollisionShape(self, 0, 0, 24)

        # Chargement du spritesheet : dossier "Enemies", sous-dossier "Turtle", fichier " (44x26).png"
        self.SPRITE = self.load_spritesheet(
            "Enemies", "Turtle", " (44x26).png", self.width, self.height, True
        )

    def update_sprite(self):

        # Détermination du nom de l'animation en fonction de l'état
        if self.state == "idle_2":
            base = "Idle 2"
        elif self.state == "spikes_out":
            base = "Spikes out"
        elif self.state == "idle_1":
            base = "Idle 1"
        elif self.state == "spikes_in":
            base = "Spikes in"
        else:
            base = "Idle 2"

        # Ajout du suffixe de direction
        suffix = "_right" if self.direction else "_left"
        sprite_list = self.SPRITE[base + suffix]

        # Avance la frame de l'animation
        index = (self.animation_count // 3) % len(sprite_list)
        self.sprite = sprite_list[index]
        self.animation_count += 1

    def _handle_horizontal_collision(self, collision):

        code, pos = collision
        already_on_ground = self.on_ground

        if code == 2:  # collision à droite
            self.x = pos[0] - self.width - self.collision_shape.radius
            self.x_velocity = 0
        elif code == 1:  # collision à gauche
            self.x = pos[0] + self.width - self.collision_shape.radius // 2
            self.x_velocity = 0
        else:
            already_on_ground = False

        return already_on_ground

    def _handle_vertical_collision(self, collision, already_on_ground):

        code, pos = collision

        if code == 3:  # atterri sur le dessus
            # Ajuste la position pour être exactement sur la surface
            offset = self.width + self.collision_shape.offset_y + self.collision_shape.radius
            self.y = pos[1] - offset + 16
            self.y_velocity = 0
            self.on_ground = True

        elif code == 4:  # collision avec le plafond
            offset = self.width + self.collision_shape.offset_y + self.collision_shape.radius
            self.y = pos[1] - self.height + offset
            self.y_velocity = 0
            self.is_jumping = False

        else:
            # Pas de collision verticale : annule le déplacement
            self.y -= self.y_velocity
            self.on_ground = already_on_ground

    def update(self, physics):

        # Oriente Gomba vers le joueur
        self.direction = (self.player.x - self.x) < 0

        # Applique la gravité
        physics.apply_gravity(self)

        # Ne bouge que s'il y a une vitesse
        if self.x_velocity or self.y_velocity:
            # Déplacement et mise à jour du collision_shape
            self.x += self.x_velocity
            self.y += self.y_velocity
            self.collision_shape.update_collision_shape()

            # Vérification des collisions
            collision = physics.check_collision(self)

            # Résolution horizontale
            already_on_ground = self._handle_horizontal_collision(collision)
            self.collision_shape.update_collision_shape()

            # Résolution verticale
            self._handle_vertical_collision(collision, already_on_ground)
            self.collision_shape.update_collision_shape()

            # Si en l'air, ré-applique vitesse verticale
            if not self.on_ground:
                self.y += self.y_velocity
                self.collision_shape.update_collision_shape()

        # Machine à états pour les piquants
        self.spike_timer += 1
        dist = abs(self.player.x - self.x)

        if self.state == "idle_2":
            # Affiche les piquants si le joueur est très proche
            if dist < 50:
                self.state = "spikes_out"
                self.animation_count = 0
            self.spike_timer = 0

        elif self.state == "spikes_out" and self.spike_timer > 21:
            self.state = "idle_1"
            self.animation_count = 0
            self.spike_timer = 0

        elif self.state == "idle_1" and self.spike_timer >= 100:
            # Cache les piquants lorsque le joueur s'éloigne
            if dist >= 50:
                self.state = "spikes_in"
                self.animation_count = 0
            self.spike_timer = 0

        elif self.state == "spikes_in" and self.spike_timer > 21:
            # Retour à l'état initial
            self.state = "idle_2"
            self.animation_count = 0
            self.spike_timer = 0

    def draw(self):

        self.update_sprite()
        screen_x = self.x - self.camera.camera.x
        screen_y = self.y - self.camera.camera.y
        self.screen.blit(self.sprite, (screen_x, screen_y))

        # pygame.draw.circle(self.screen, "red", (self.collision_shape.x, self.collision_shape.y), self.collision_shape.radius, 3)
