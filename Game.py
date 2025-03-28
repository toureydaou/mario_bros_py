import pygame
from gameObjects.Player import player
from gameObjects.Gomba import Gomba
from Physics import physics
from gameObjects.Pipes import pipes
from gameObjects.Terrain import terrain


class Game:

    def __init__(self, player, gombas, pipes, terrain):
        self.player = player
        self.gombas = gombas
        self.terrain = terrain
        self.pipes = pipes
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        self.physics = physics()

    def run(self):
        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("cyan")

            # RENDER YOUR GAME HERE
            self.terrain.draw(self.screen)
            self.player.draw(self.screen)
            self.player.update(self.physics)

            self.gombas.append(Gomba(520, 520))

            gombas[0].draw(self.screen)
            gombas[0].update(self.physics)
            physics
            pipe.draw(self.screen)

            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60

        pygame.quit()


gombas = []
Terrain = terrain(0,550,2000)
pipe = pipes(400, 450)
player = player(0, 0)
game = Game(player, gombas, pipe, Terrain)
game.run()
