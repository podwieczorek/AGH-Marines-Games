import pygame
from .button import Button

class UI:
    def __init__(self, root):
        self.root = root
    
    def death_screen(self, screen, score, top_scores):
        font = pygame.font.Font(None, 74)
        text = font.render(f"Game Over! Score: {score}", True, (255, 255, 255))
        restart_text = font.render("Press R to Restart", True, (255, 255, 255))
        quit_text = font.render("Press ESC to Quit", True, (255, 255, 255))

        screen.fill((0, 0, 0))
        screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, 100))

        # Display the top 5 scores
        font_small = pygame.font.Font(None, 50)
        for i, high_score in enumerate(top_scores):
            high_score_text = font_small.render(f"{i + 1}. {high_score}", True, (255, 255, 255))
            screen.blit(high_score_text, (screen.get_width() // 2 - high_score_text.get_width() // 2, 200 + i * 50))

        screen.blit(restart_text, (screen.get_width() // 2 - restart_text.get_width() // 2, 500))
        screen.blit(quit_text, (screen.get_width() // 2 - quit_text.get_width() // 2, 600))
        
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