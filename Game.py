from TileMap import tileMap
import pygame
from gameObjects.Player import player
from gameObjects.Turtle import turtle
from Physics import physics
from gameObjects.Camera import camera
from World import world
from Config import config


class Game:
    """
    Classe principale du jeu : initialisation, boucle principale et rendu.
    """
    def __init__(self):
        pygame.init()
        # Configuration de la fenêtre
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption(config.SCREEN_TITLE)
        self.clock = pygame.time.Clock()
        # État du jeu
        self.running = True

        # Création des objets de jeu
        self.player = player(100, 300, 400, 100, self.screen)
        self.camera = camera(self.player)
        self.background = pygame.Surface(self.screen.get_size())
        self.world = world(self.camera, self.screen, self.background)
        self.spawning_point = config.SPAWN_POINT
        self.turtle = turtle(600, 500, self.player, self.camera, self.screen)
        self.turtle1 = turtle(1500, 500, self.player, self.camera, self.screen)
        self.turtle2 = turtle(1700, 500, self.player, self.camera, self.screen)
        self.turtle2 = turtle(1900, 500, self.player, self.camera, self.screen)
        self.turtles = [self.turtle, self.turtle1, self.turtle2]
        self.physics = physics(self.world.tile_map, self.turtles)

        # Police et affichage des vies
        self.font = pygame.font.Font('assets/fonts/Minecraft.ttf', 24)
        
    def game_over(self):
         if (self.player.chances == 0 and self.player.life_points == 0):
             self.running = False
         elif self.player.x > 3400:
             self.running = False
             print("vous avez gagner la partie !")
    
    def respawn_player(self):
        # Réapparition si chute hors de l'écran
        
        if self.player.y > self.spawning_point[1] + 720:
            self.player.on_hit()
            self.player.x, self.player.y = self.spawning_point
            self.player.collision_shape.update_collision_shape()

    def run(self):
        while self.running:
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Mise à jour de la caméra
            self.camera.update()

            # Effacement de l'écran
            self.screen.blit(self.background, (0, 0))
            self.world.draw_world()

            # Mise à jour et rendu du Gomba
            self.turtle.update(self.physics)
            self.turtle.draw()
            self.turtle1.update(self.physics)
            self.turtle1.draw()
            self.turtle2.update(self.physics)
            self.turtle2.draw()

            # Mise à jour des positions du joueur via la caméra
            render_x, render_y = self.camera.apply(self.player)
            self.player.render_x, self.player.render_y = render_x, render_y
            
            # Physique et rendu du joueur
            self.player.update(self.physics)
            self.player.draw()

            # Affichage des indicateurs de vie
            lives_surf = self.font.render(f'Lives : x{self.player.life_points}', False, (0, 0, 0))
            chances_surf = self.font.render(f'Chances : x{self.player.chances}', False, (0, 0, 0))
            self.screen.blit(lives_surf, (240, 20))
            self.screen.blit(chances_surf, (50, 20))

            self.game_over()
            self.respawn_player()
            # Rafraîchissement de l'affichage et limitation du FPS
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == '__main__':
    Game().run()
