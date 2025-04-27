from TileMap import tileMap

class world:
    def __init__(self, camera, screen, background):
        self.camera = camera
        self.screen = screen
        self.background = background
        self.tile_map = tileMap(self.camera, self.screen)
        self.background.fill((0, 0, 0)) 
        self.tile_map.screen = self.background
        self.tile_map.draw_skybox()
        self.tile_map.screen = screen
        
        
    def draw_world(self): # Creer le Monde ici en créants les platforms
        self.tile_map.tiles = []
        self.tile_map.draw_terrain(500, 650, 64, 600)
        self.tile_map.draw_terrain(900, 650, 160, 600)
        self.tile_map.draw_terrain(1050, 550, 100, 600)
        self.tile_map.draw_terrain(680, 950, 100, 60)
        self.tile_map.draw_terrain(400, 764, 800, 3000)
        self.tile_map.draw_terrain(-200, 600, 400, 3000)
        self.tile_map.draw_terrain(250, 430, 150, 50)
        self.tile_map.draw_terrain(500, 340, 200, 50)
        self.tile_map.draw_terrain(810, 440, 100, 50)
        self.tile_map.draw_terrain(1370, 760, 800, 3000)
        self.tile_map.draw_terrain(2310, 760, 130, 64)
        self.tile_map.draw_terrain(2600, 760, 130, 64)
        self.tile_map.draw_terrain(2900, 760, 130, 64)
        self.tile_map.draw_terrain(3100, 760, 500, 3000)
        