import pygame

class Game :
    

    def __init__(self, player):
        self.player = player
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        
    def detect_keys():
        keys = pygame.key.get_pressed()
        #### a continuer ####
        # if keys[K_w]:
        #     self.player.get_x()
            
        
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

            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60

        pygame.quit()
        
        
test = Game()
test.run()