import pygame


class Spritesheet:
    def __init__(self, filename, cols, rows, size, width=8, height=8):
        self.sheet = pygame.image.load(filename).convert()
        self.cols = cols
        self.rows = rows
        self.size = size
        self.width = width
        self.height = height
        self.frames = []
        ratio = width/height
        for row in range(rows):
            for col in range(cols):
                frame = pygame.Surface((ratio*size, size))
                pygame.transform.scale(self.get_image(col * width, row * height, width, height), (size*ratio, size), frame)
                frame.set_colorkey((0, 0, 0))
                self.frames.append(frame)

    def get_frame(self, index):
        return self.frames[index % len(self.frames)]
    
    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height))
        image.blit(self.sheet, (0, 0), (x, y, width, height))
        return image
