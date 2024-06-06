import pygame
import os
import random
import time
from Tile import Tile
from Button import Button
from Home import HomePage

class Game:
    def __init__(self, image_name, size):
        self.grid_width = 400
        self.grid_height = 400
        self.size = size

        self.tile_size = self.grid_width // size

        self.gap_size = self.grid_width - (size * self.tile_size)
        
        directory = "images"
        image_path = os.path.join(directory, image_name)

        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.grid_width, self.grid_height))

        self.tiles = []
        for y in range(size):
            for x in range(size):
                tile_rect = pygame.Rect(
                    (x * self.tile_size) + self.gap_size // 2,
                    (y * self.tile_size) + self.gap_size // 2,
                    self.tile_size,
                    self.tile_size
                )
                if x == size - 1 and y == size - 1:
                    tile = Tile(x, y, self, None)
                    self.empty_tile = tile
                else:
                    tile_image = pygame.Surface((self.tile_size, self.tile_size))
                    tile_image.blit(self.image, (0, 0), tile_rect)
                    tile = Tile(x, y, self, tile_image)

                tile.x += 200
                tile.y += 60

                self.tiles.append(tile)

        self.shuffle()

        self.back_button = Button(240, 500, 100, 50, "Back")
        self.start_button = Button(360, 500, 100, 50, "Start")
        self.reset_button = Button(480, 500, 100, 50, "Reset")

        self.font = pygame.font.Font(None, 36)
        self.start_time = None
        self.end_time = None
        self.stopwatch_running = False
        self.puzzle_solved = False

    def start_stopwatch(self):
        self.start_time = time.time()
        self.stopwatch_running = True

    def stop_stopwatch(self):
        self.end_time = time.time()
        self.stopwatch_running = False

    def get_elapsed_time(self):
        if self.start_time is None:
            return 0
        elif self.stopwatch_running:
            return time.time() - self.start_time
        else:
            return self.end_time - self.start_time

    def get_empty_tile(self):
        for tile in self.tiles:
            if tile.image is None:
                return tile

    def shuffle(self):
        num_tiles = self.size * self.size
        positions = [(x, y) for x in range(self.size) for y in range(self.size)]
        random.shuffle(positions)

        for i, tile in enumerate(self.tiles):
            if i < num_tiles:
                tile.x = (positions[i][0] * self.tile_size) + 200
                tile.y = (positions[i][1] * self.tile_size) + 70

    def check_win(self):
        for i, tile in enumerate(self.tiles):
            if tile.x != ((i % self.size) * self.tile_size) + 200 or tile.y != ((i // self.size) * self.tile_size) + 70:
                return False
    
        self.puzzle_solved = True
        return True



    def reset(self):
        self.stop_stopwatch()
        self.start_time = None
        self.end_time = None
        self.puzzle_solved = False

        for i, tile in enumerate(self.tiles):
            tile.x = ((i % self.size) * self.tile_size) + 200
            tile.y = ((i // self.size) * self.tile_size) + 70

    def back(self):
        pygame.quit()
        home_page = HomePage()
        home_page.run()

    def high_score(self):
        if self.check_win():
            elapsed_time = self.get_elapsed_time()

            high_score = self.read_high_score()
    
            if high_score is None or elapsed_time < high_score:
                self.save_high_score(elapsed_time)
                message = "NEW HIGH SCORE!!"
            else:
                message = "YOU WON!"
    
            self.reset() 
    
            return message


    def read_high_score(self):
        try:
            with open("HighScore.txt", "r") as file:
                high_score = float(file.read())
                return high_score
        except FileNotFoundError:
            return None

    def save_high_score(self, time):
        with open("HighScore.txt", "w") as file:
            file.write(str(time))

    def run(self):
        pygame.init()
        window = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Slide Puzzle Game")
        clock = pygame.time.Clock()
    
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.is_clicked(event):
                        self.back()
                    elif self.start_button.is_clicked(event):
                        if not self.stopwatch_running and not self.puzzle_solved:
                            self.start_stopwatch()
                        self.shuffle()
                        self.puzzle_solved = False
                    elif self.reset_button.is_clicked(event):
                        self.reset()
    
                    tile_moved = False

                    for tile in self.tiles:
                        if pygame.Rect(tile.x, tile.y, self.tile_size, self.tile_size).collidepoint(event.pos):
                            tile.move()
                            tile_moved = True
        
                    if tile_moved and self.check_win():
                        self.stop_stopwatch()
                        message = self.high_score()
                        if message:
                            font = pygame.font.Font(None, 36)
                            text = font.render(message, True, (0, 163, 163))
                            window.blit(text, (300, 40))
                            pygame.display.flip()
                            time.sleep(3)
                            self.reset()
    
            window.fill((220, 234, 234))
    
            for tile in self.tiles:
                tile.draw(window)
    
            self.back_button.draw(window)
            self.start_button.draw(window)
            self.reset_button.draw(window)
    
            elapsed_time = self.get_elapsed_time()
            stopwatch_label = self.font.render(f"Time: {elapsed_time:.2f} seconds", True, (0, 0, 0))
            window.blit(stopwatch_label, (20, 20))
    
            pygame.display.flip()
            clock.tick(60)
    
        pygame.quit()

