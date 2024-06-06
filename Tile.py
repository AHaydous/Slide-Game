import pygame

class Tile:
    def __init__(self, x, y, game, image):
        self.x = x
        self.y = y
        self.game = game
        self.image = image

    def draw(self, surface):
        rect = pygame.Rect(self.x, self.y, self.game.tile_size, self.game.tile_size)
        if self.image is not None:
            surface.blit(self.image, rect)            


    def move(self):
        empty_tile = self.game.get_empty_tile()
    
        if (abs(empty_tile.x - self.x) == self.game.tile_size and empty_tile.y == self.y) or \
           (abs(empty_tile.y - self.y) == self.game.tile_size and empty_tile.x == self.x):
            # Swap positions with the empty tile
            self.x, empty_tile.x = empty_tile.x, self.x
            self.y, empty_tile.y = empty_tile.y, self.y

