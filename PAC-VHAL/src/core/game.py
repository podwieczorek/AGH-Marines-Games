import pygame
import os
from src.core.maze import Maze
from src.units.player import Player
from src.units.enemy import Enemy
from src.units.pickup import Pickup
from src.units.player import *
from src.core.draw import Draw
from src.core.UI.ui import UI
from src.core.UI.button import Button
from src.core.input import Input
from src.core.settings import Settings

class Game:
    
    COLORS = {
        0: (4, 105, 151),  # Background (blue)
        1: (37, 65, 23),   # Walls (green)
    }
    last_speed_change = 0    
    
    def __init__(self, settings_path):
        self.settings = Settings(settings_path)
        self.settings.load_settings()
        
        
        self.screen = pygame.display.set_mode((self.settings.s["screen_width"], self.settings.s["screen_height"]))
        self.maze = None
        self.draw = None
        self.input = Input()
        self.state = 1
        self.game_running = False
        
        self.buttons = {}
        self.buttons['start'] = Button('start', self.start_game)
        self.buttons['pause'] = Button('pause', self.pause_game)
        self.buttons['quit'] = Button('quit', self.quit_game)
        self.buttons['settings'] = Button('settings', None)
        self.buttons['resume'] = Button('resume', self.resume_game)
        
        # settings buttons
        
        
        self.current_window = 'main'
        self.current_option = 0
        self.menu_structure = {
            'main': {
                'buttons': [
                    self.buttons['start'],
                    # self.buttons['settings'],
                    self.buttons['quit'],
                ]       
            },
            'game': {
                'buttons': [
                    Button('')
                ]
            },
            'pause': {
                'buttons': [
                    self.buttons['resume'],
                    self.buttons['start'],
                    self.buttons['quit']
                    
                ]
            },
            'settings': {
                'buttons': [
                    
                ]
            }
        }
    def quit_game(self):
        self.game_running = False
        self.state = 0
        
    def pause_game(self):
        self.current_option = 0
        self.state = 1
        self.current_window = 'pause'
        
    def resume_game(self):
        self.current_option = 0
        self.state = 2
        self.current_window = 'game'
        
    def game_over(self):
        pass   
    
    #resets the game
    def tabula_rasa(self): 
        Unit.unit_list = []
        Player.player_list = []
        self.maze = None
        self.draw = None
        self.game_running = False
        
    def start_game(self):
        self.tabula_rasa()
        Player.player_list = []
        Enemy.enemy_list = []
        self.setup_maze(100, 70, 15)
        self.maze.simplex_cave(random.randrange(0,100000))
        self.maze.remove_not_connected_spaces()
        self.draw=Draw(self.screen, 15, self.maze)
        
        self.spawn_pickup(amount=10)
        self.spawn_enemy(amount=10)
        self.spawn_player('keyboard')
        
        
        self.game_running = True
        self.state = 2
        self.current_window = 'game'
        
    def spawn_player(self, tag=None):
        match tag:
            case 'keyboard':
                Keyboard_player(self.maze, self.settings.s["player_hp"], self.settings.s["player_speed"], self.settings.s["bullet_speed"])
            case 'joystick':
                Joystick_player(self.maze, self.settings.s["player_hp"], self.settings.s["player_speed"], self.settings.s["bullet_speed"])
            case _:
                raise ValueError("No type provided")
            
            
    def spawn_pickup(self, tag=Pickup, amount=10):
        for i in range(amount):
            Pickup(self.maze, self.settings.s["pickup_value"])
            
    def spawn_enemy(self, tag=Enemy, amount=10):
        for i in range(amount):
            Enemy(self.maze, 1, self.settings.s["enemy_speed"])
    
    def setup_maze(self, rows, cols, cell_size):
        self.maze = Maze(self.settings.s["maze_width"], self.settings.s["maze_height"])
        self.draw = Draw(self.screen, self.settings.s["cell_size"], self.maze)
        
        
        
    def update_settings(self):
        self.settings.load_settings()
        self.screen = pygame.display.set_mode((self.settings.s["screen_width"], self.settings.s["screen_height"]))
    
        
    
        
        
        
    def ui_loop(self):
        current_buttons = self.menu_structure[self.current_window]['buttons']
        Button.highlight(current_buttons[self.current_option])
        match self.input.get_menu_instructions():
            case 'up':
                if self.current_option == 0:
                    self.current_option = len(current_buttons) - 1
                else:
                    self.current_option -= 1
            case 'down':
                if self.current_option == len(current_buttons) - 1:
                    self.current_option = 0
                else:
                    self.current_option += 1
            case 'left':
                pass
            case 'right':
                pass
            case 'escape':
                pass
            case 'confirm':
                callback = current_buttons[self.current_option].callback
                if callback:
                    callback()
                else:
                    pass
            case _:
                pass
        
        
        Button.draw_given(self.screen, current_buttons)  
    
    def hud(self):
        pass










    def game_loop(self):
        for player in Player.player_list:
            player.input(self.input.events)
    
        current_time = pygame.time.get_ticks()
        
        self.settings.s["game_speed"] = 1000 - current_time // 200
        if self.settings.s["game_speed"] < 300:
            self.settings.s["game_speed"] = 300
        #print(game_speed)
    
        self.draw.draw_maze()
        for u in Unit.unit_list:
            u.check_colision()
            if current_time - u.last_frame > self.settings.s["game_speed"] / u.speed:
                u.step()
                u.last_frame = current_time
            self.draw.draw_unit(u)
        last_tick = current_time

    