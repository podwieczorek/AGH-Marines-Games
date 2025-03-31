import pygame


class Input:
    def __init__(self):
        self.events = []
        
        self.menu_key = {
            pygame.K_UP: 'up',
            pygame.K_w: 'up',
            pygame.K_DOWN: 'down',
            pygame.K_s: 'down',
            pygame.K_LEFT: 'left',
            pygame.K_a: 'left',
            pygame.K_RIGHT: 'right',
            pygame.K_d: 'right',
            pygame.K_RETURN: 'confirm',
            pygame.K_SPACE: 'confirm',
            pygame.K_ESCAPE: 'escape'
        }
           
    def get_menu_instructions(self):
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key in self.menu_key:
                    return self.menu_key[event.key]

    def update(self, events):
        self.events = events
        return self.events
        