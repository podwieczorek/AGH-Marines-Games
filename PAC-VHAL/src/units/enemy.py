import random
from .unit import Unit
from .player import Player

class Enemy(Unit):
    tag='enemy'
    def __init__(self, maze, detection_radius = 10, speed = 10):
        super().__init__(maze,speed)
            
        self.direction = (0, 0)
        self.x
        self.y
        self.radius = detection_radius
        self.path = []
        self.cooldown = 100
        self.respawn()
    
    
    def step(self):
        self.ai()
        
            
    def ai(self):
        # print(self.cooldown)
        base_cooldown = 20  # cooldown after losing aggro
        probability = 0.95  # aggro probability
        target = self.player_in_radius()
        
        
        if self.path == []:
            self.path = self.get_patrol_path()
        if self.cooldown > 0:
            self.cooldown -= 1
        elif target != self:
            self.path = self.get_path_to(self.x, self.y, target, set())
            if random.random() > probability:
                self.cooldown = base_cooldown

                
        
        if self.path != []:
            self.direction = self.path.pop(0)
        
        
        self.x += self.direction[0]
        self.y += self.direction[1]
        
    def get_patrol_path(self):
        x=0
        while True:
            x+=1
            target = random.choice(Unit.unit_list)
            if target.tag == 'pickup':
                path = self.get_path_to(self.x, self.y, target, set())
                if len(path) > 5:
                    return path
            if x > 1000:
                return []

    def player_in_radius(self):
        for player in Player.player_list:
            if (player.x - self.x) ** 2 + (player.y - self.y) ** 2 <= self.radius ** 2: 
                return player
        return self
            

    def respawn(self):
        x = random.randint(0, self.maze.cols - 1)
        y = random.randint(0, self.maze.rows - 1)
        while self.maze.grid[y][x] == 1:
            x = random.randint(0, self.maze.cols - 1)
            y = random.randint(0, self.maze.rows - 1)
        #print("respawn", x, y)
        self.x = x
        self.y = y
        self.path = self.get_patrol_path()
    
    def check_colision(self):
        #self.draw_path()# so it executes every frame
        for player in Player.player_list:
            if self.does_colide(player):
                player.colides(self)
                
    def colides(self, other):
        match other.tag:
            case 'bullet':
                self.respawn()
            case _:
                pass
