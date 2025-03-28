import pygame
from gameObjects.Player import player
from gameObjects.Gomba import Gomba
from Physics import physics
from gameObjects.Pipes import Pipe
import random


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
        self.gombas.append(Gomba(520, 535))
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

            if len(self.gombas) < 3:
                self.gombas.append(Gomba(random.randint(600, 860), 535))

            for gomba in self.gombas:
                gomba.draw(self.screen)
                gomba.update(self.pipes, self.gombas)

            for pipe in self.pipes:
                pipe.draw(self.screen)
            
            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60

        pygame.quit()


gombas = []

pipes = []
pipe1 = Pipe(400, 400)
pipe2 = Pipe(900, 400)
player = player(0, 0)
pipes.append(pipe1)
pipes.append(pipe2)
game = Game(player, gombas, pipes)
game.run()
