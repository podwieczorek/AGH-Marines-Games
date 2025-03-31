import pygame


class Button:
    color = (20, 0, 0)
    hover_color = (50, 50, 50)
    width = 600
    height = 50
    padding = 10
    
    buttons_list = []

    def __init__(self, text, callback=None):
        self.text = text
        self.x = 0
        self.y = 0
        self.width = self.width
        self.height = self.height
        self.font = pygame.font.Font(None, 32)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = self.color
        self.hover_color = self.hover_color
        self.callback = callback
        self.is_hovered = False
        self.buttons_list.append(self)
        
    def update_coords(buttons):
        for i, button in enumerate(buttons):
            button.x = pygame.display.get_surface().get_width() // 2 - button.width // 2
            button.y = 100 + i * (Button.height + Button.padding)
            button.rect = pygame.Rect(button.x, button.y, button.width, button.height)

    @staticmethod
    def draw_given(screen, buttons):
        Button.update_coords(buttons)
        for button in buttons:
            button.draw(screen)

    def draw(self, screen):
        """Draw the button and handle hover effect."""
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=10)
        
        # Render text
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def highlight(self):
        for button in self.buttons_list:
            button.is_hovered = False
        self.is_hovered = True
