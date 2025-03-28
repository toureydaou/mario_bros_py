import pygame
from gameObjects.Player import player
from gameObjects.Gomba import Gomba
from Physics import physics
from gameObjects.Pipes import Pipes


class Game:

    def __init__(self, player, gombas, pipes):
        self.player = player
        self.gombas = gombas
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
            self.player.draw(self.screen)
            self.player.update(self.physics)

            self.gombas.append(Gomba(520, 535))

            gombas[0].draw(self.screen)
            gombas[0].update(self.physics)

            pipe.draw(self.screen)

            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60

        pygame.quit()


gombas = []
pipe = Pipes(400, 300)
player = player(0, 0)
game = Game(player, gombas, pipe)
game.run()
