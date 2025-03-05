import pygame
from .button import Button

class UI:
    def __init__(self, root):
        self.root = root
    
    def death_screen(self, screen, points):
        # Set up font and size
        font = pygame.font.Font(None, 72)
        small_font = pygame.font.Font(None, 36)
        
        # Define the text to display
        death_text = "Game Over"
        points_text = f"Points Collected: {points}"
        restart_text = "Press 'R' to Restart"
        
        # Render the text
        death_surface = font.render(death_text, True, (255, 0, 0))
        points_surface = small_font.render(points_text, True, (255, 255, 255))
        restart_surface = small_font.render(restart_text, True, (255, 255, 255))
        
        # Get the text rectangles
        death_rect = death_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
        points_rect = points_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        restart_rect = restart_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
        
        # Blit the text to the screen
        screen.blit(death_surface, death_rect)
        screen.blit(points_surface, points_rect)
        screen.blit(restart_surface, restart_rect)
        
        # Update the display
        pygame.display.flip()
    
    
    def instructions(self, screen):
        # Set up font and size
        font = pygame.font.Font(None, 36)
        
        # Define the text to display
        instructions_text = [
            "Instructions:",
            "Use arrow keys to move",
            "Press 'ESC' to pause",
            "WSAD to move",
            "Space to shoot",
            
        
        ]
        
        # Set the starting position for the text
        start_y = 100
        line_height = 40
        
        # Render each line of text
        for i, line in enumerate(instructions_text):
            text = font.render(line, True, (255, 255, 255))
            screen.blit(text, (50, start_y + i * line_height))
        
        # Update the display
        pygame.display.flip()