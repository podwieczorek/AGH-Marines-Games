from .unit import Unit


class Bullet(Unit):
    tag='bullet'
    def __init__(self, maze, x, y, direction, speed = 30):
        super().__init__(maze, speed)
        self.state = 'moving'
        self.x = x
        self.y = y
        self.direction = direction
        
    def step(self):
        
        if self.direction not in self.maze.get_valid_directions(self.x, self.y):
            self.die()
            return
            
        x = self.direction[0] + self.x
        y = self.direction[1] + self.y

        self.x = x
        self.y = y
    
    def colides(self, other):
        match other.tag:
            case 'player':
                pass
            case _:   
                 self.die()
