import pygame
from Button import Button
import tkinter as tk

class HomePage:
    def __init__(self):
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 600
        
        self.running = True

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (150, 150, 150)

        self.window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Slide Puzzle Game")

        self.buttons = [
            Button(300, 200, 200, 50, "3x3"),
            Button(300, 270, 200, 50, "4x4"),
            Button(300, 340, 200, 50, "5x5")
        ]

        self.select_options = ["nature", "volcano", "fish"]
        self.selected_option = self.select_options[0]

        self.select_rect = pygame.Rect(300, 410, 200, 30)
        self.select_color = self.WHITE
        self.select_border_color = (0, 163, 163)
        pygame.font.init()
        self.select_font = pygame.font.Font(None, 20)

        self.arrow_rect = pygame.Rect(self.select_rect.right - 20, self.select_rect.y + 10, 10, 10)
        self.arrow_color = (0, 163, 163)

        self.title_font = pygame.font.Font(None, 72)
        self.title_text = self.title_font.render("Sliding Puzzle Game", True, (0, 163, 163))
        self.title_rect = self.title_text.get_rect(center=(self.WINDOW_WIDTH // 2, 100))

    def run(self):
        from Game import Game
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.is_clicked(event):
                            if button.text == "3x3":
                                game = Game(self.selected_option + ".jpg", 3)
                            elif button.text == "4x4":
                                game = Game(self.selected_option + ".jpg", 4)
                            elif button.text == "5x5":
                                game = Game(self.selected_option + ".jpg", 5)
                            else:
                                game = None
    
                            if game is not None:
                                game.run()
                                self.running = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.select_rect.collidepoint(event.pos):
                        self.show_select_options()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.arrow_rect.collidepoint(event.pos):
                        self.show_select_options()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, option in enumerate(self.select_options):
                        option_rect = self.select_rect.copy()
                        option_rect.y += (i + 1) * self.select_rect.height
                        if option_rect.collidepoint(event.pos):
                            self.selected_option = option
                            print("Selected option:", self.selected_option)

            self.window.fill((220, 234, 234))
            
            self.window.blit(self.title_text, self.title_rect)

            for button in self.buttons:
                button.draw(self.window)

            pygame.draw.rect(self.window, self.select_color, self.select_rect)
            pygame.draw.rect(self.window, self.select_border_color, self.select_rect, 2)

            label_surface = self.select_font.render(self.selected_option, True, self.select_border_color)
            label_rect = label_surface.get_rect(midleft=(self.select_rect.x + 5, self.select_rect.centery))
            self.window.blit(label_surface, label_rect)

            pygame.draw.polygon(self.window, self.arrow_color, [(self.arrow_rect.x, self.arrow_rect.y),
                                                                 (self.arrow_rect.x + self.arrow_rect.width // 2,
                                                                  self.arrow_rect.y + self.arrow_rect.height),
                                                                 (self.arrow_rect.x + self.arrow_rect.width,
                                                                  self.arrow_rect.y)])

            pygame.display.update()

        pygame.quit()

    def show_select_options(self):
        option_rects = []
        options_visible = True
    
        while options_visible:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.select_rect.collidepoint(event.pos):
                        options_visible = False
                        break
    
                    for i, option_rect in enumerate(option_rects):
                        if option_rect.collidepoint(event.pos):
                            self.selected_option = self.select_options[i]
                            options_visible = False
                            break
    
            self.window.fill((220, 234, 234))
            
            self.window.blit(self.title_text, self.title_rect)
    
            for button in self.buttons:
                button.draw(self.window)
    
            pygame.draw.rect(self.window, self.select_color, self.select_rect)
            pygame.draw.rect(self.window, self.select_border_color, self.select_rect, 2)
    
            label_surface = self.select_font.render(self.selected_option, True, self.select_border_color)
            label_rect = label_surface.get_rect(midleft=(self.select_rect.x + 5, self.select_rect.centery))
            self.window.blit(label_surface, label_rect)
    
            pygame.draw.polygon(self.window, self.arrow_color, [(self.arrow_rect.x, self.arrow_rect.y),
                                                                 (self.arrow_rect.x + self.arrow_rect.width // 2,
                                                                  self.arrow_rect.y + self.arrow_rect.height),
                                                                 (self.arrow_rect.x + self.arrow_rect.width,
                                                                  self.arrow_rect.y)])
    
            option_rects.clear()
            for i, option in enumerate(self.select_options):
                option_rect = self.select_rect.copy()
                option_rect.y += (i + 1) * self.select_rect.height
                pygame.draw.rect(self.window, self.select_color, option_rect)
                pygame.draw.rect(self.window, self.select_border_color, option_rect, 2)
                option_surface = self.select_font.render(option, True, self.select_border_color)
                option_rect = option_surface.get_rect(center=option_rect.center)
                self.window.blit(option_surface, option_rect)
                option_rects.append(option_rect)
    
            pygame.display.update()
