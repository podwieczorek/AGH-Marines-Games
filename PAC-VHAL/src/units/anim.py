from src.core.spriesheet import Spritesheet
from src.units.unit import Unit

class Anim(Unit):
    def __init__(self, maze, speed):
        super().__init__(maze, speed)
        self.state = 'idle'
        self.animation = Spritesheet('static/images/units/pacvhal-base.png', 4, 1, self.maze.size, 8, 8)
        self.index = 0
        
    def step(self):
        self.index += 1
        if self.index >= 4:
            self.index = 0
            
    def colides(self, other):
        pass

    def die(self):
        pass

    def get_frame(self):
        return self.animation.get_frame(self.index)
    
    def get_size(self):
        return self.maze.size
#

