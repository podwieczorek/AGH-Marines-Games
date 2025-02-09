import pygame
from .button import Button

class UI:
    def __init__(self):
        self.buttons = []

    def add_button(self, text, x, y, width, height, color, hover_color, font, callback):
        """Add a button to the UI."""
        button = Button(text, x, y, width, height, color, hover_color, font, callback)
        self.buttons.append(button)

    def draw(self, screen):
        """Draw all UI elements."""
        for button in self.buttons:
            button.draw(screen)

    def handle_event(self, event):
        """Handle mouse events for buttons."""
        if event.type == pygame.MOUSEMOTION:
            for button in self.buttons:
                button.check_hover(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in self.buttons:
                button.check_click(event.pos)