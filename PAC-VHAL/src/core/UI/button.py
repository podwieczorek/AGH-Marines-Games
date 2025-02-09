import pygame

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, font, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.font = font
        self.callback = callback
        self.is_hovered = False

    def draw(self, screen):
        """Draw the button and handle hover effect."""
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)
        
        # Render text
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        """Check if the mouse is over the button."""
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos):
        """Trigger event if clicked."""
        if self.rect.collidepoint(mouse_pos):
            self.callback()



