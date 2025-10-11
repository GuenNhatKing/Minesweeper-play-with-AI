from levels import get_level_config, Level
import pygame
from config import *
from core import Game, GameState, CellState
from ui import UI_Draw
from ai import AI
from enum import Enum

def get_work_area_size():
    if not pygame.display.get_init():
        pygame.display.init()
    
    info = pygame.display.Info()
    width = info.current_w * 0.86
    height = info.current_h * 0.86
    return width, height

class Template(Enum):
    LEVEL_SELECT = 'level_select'
    MODE_SELECT = 'mode_select'
    GAMEPLAY = 'gameplay'

class Game_UI:
    def __init__(self):
        self.max_width, self.max_height = get_work_area_size()
        self.template = Template.LEVEL_SELECT

        self.cell_size = CELL['size']
        self.level: Level = None
        self.game_config: tuple[int, int, int] = None
        self.game: Game = None

        self.scale: float = None
        self.windows: pygame.Surface = None
        self.windows_size: tuple[int, int] = None
        self.canvas: pygame.Surface = None
        self.canvas_size: tuple[int, int] = None

        self.ui_draw: UI_Draw = UI_Draw()
        self.ai_enable: bool = None
        self.ai: AI = AI()

        self.running = False
        self.initialized = False

    def calc_game_size(self):
        w, h = self.game.get_size()
        height = STATUS_BAR['height'] + h * CELL['size'] + (h + 1) * BOARD['gap'] + BOARD['padding'] * 2
        width = w * CELL['size'] + (w + 1) * BOARD['gap'] + BOARD['padding'] * 2
        return (width, height)
    
    def set_level(self, level: Level):
        if self.level != level:
            self.game_config = get_level_config(level)
            if self.game:
                self.game = Game(self.game_config[0], self.game_config[1], self.game_config[2])
            else:
                self.game = Game(self.game_config[0], self.game_config[1], self.game_config[2])
            self.level = level
    
    def set_template(self, template: Template):
        self.template = template
        self.init_ui()
        if template == Template.GAMEPLAY:
            self.reset_game()
    
    def set_ai_helper(self, enable: bool):
        self.ai_enable = enable
        self.ai.game = self.game
    
    def reset_game(self):
        self.game.reset()
    
    def button_motion_handle(self):
        x, y = pygame.mouse.get_pos()
        x = x // self.scale
        y = y // self.scale
        if self.template == Template.GAMEPLAY:
            if self.ui_draw.in_board_left_clicked:
                if not self.ui_draw.is_mouse_in_board(x, y):
                    self.ui_draw.in_board_left_clicked = False

            if self.ui_draw.in_board_right_clicked:
                if not self.ui_draw.is_mouse_in_board(x, y):
                    self.ui_draw.in_board_right_clicked = False

            pos_x, pos_y = self.get_clicked_cell(x, y)
            if pos_x != None and pos_y != None and self.game.get_cell(pos_x, pos_y).state == CellState.UNPROBED:
                self.ui_draw.clicked_unprobed_cell = True
            else:
                self.ui_draw.clicked_unprobed_cell = False

            if self.ui_draw.smiley_clicked or self.ui_draw.smiley_right_clicked:
                if not self.ui_draw.is_mouse_in_smiley_button(x, y):
                    self.ui_draw.smiley_clicked = False
                    self.ui_draw.smiley_right_clicked = False

        elif self.template == Template.LEVEL_SELECT:
            for i, rect in enumerate(self.ui_draw.level_ui['rects']):
                if rect.collidepoint((x, y)):
                    if self.ui_draw.select_button_state[i] == 'normal':
                        self.ui_draw.select_button_state[i] = 'hover'
                else:
                    self.ui_draw.select_button_state[i] = 'normal'
        
        elif self.template == Template.MODE_SELECT:
            for i, rect in enumerate(self.ui_draw.mode_ui['rects']):
                if rect.collidepoint((x, y)):
                    if self.ui_draw.mode_button_state[i] == 'normal':
                        self.ui_draw.mode_button_state[i] = 'hover'
                else:
                    self.ui_draw.mode_button_state[i] = 'normal'


    def get_clicked_cell(self, x, y):
        board_x = x - BOARD['padding'] - BOARD['gap']
        board_y = y - STATUS_BAR['height'] - BOARD['padding'] - BOARD['gap']
        pos_x = int(board_x // (CELL['size'] + BOARD['gap']))
        pos_y = int(board_y // (CELL['size'] + BOARD['gap']))
        if pos_x * (CELL['size'] + BOARD['gap']) <= board_x <= pos_x * (CELL['size'] + BOARD['gap']) + CELL['size']\
            and pos_y * (CELL['size'] + BOARD['gap']) <= board_y <= pos_y * (CELL['size'] + BOARD['gap']) + CELL['size']:
            return (pos_x, pos_y)
        return (None, None)
    
    def button_down_handle(self):
        x, y = pygame.mouse.get_pos()
        x = x // self.scale
        y = y // self.scale
        self.left_mouse_down = pygame.mouse.get_pressed()[0]
        self.right_mouse_down = pygame.mouse.get_pressed()[2]
        if self.template == Template.GAMEPLAY:        

            if self.ui_draw.is_mouse_in_board(x, y):
                if pygame.mouse.get_pressed()[0]:
                    self.ui_draw.in_board_left_clicked = True
                elif pygame.mouse.get_pressed()[2]:
                    self.ui_draw.in_board_right_clicked = True
                pos_x, pos_y = self.get_clicked_cell(x, y)
                if pos_x != None and pos_y != None and self.game.get_cell(pos_x, pos_y).state == CellState.UNPROBED:
                        self.ui_draw.clicked_unprobed_cell = True
            elif self.ui_draw.is_mouse_in_smiley_button(x, y):
                if self.left_mouse_down:
                    self.ui_draw.smiley_clicked = True
                elif self.right_mouse_down:
                    self.ui_draw.smiley_right_clicked = True

        elif self.template == Template.LEVEL_SELECT:
            for i, rect in enumerate(self.ui_draw.level_ui['rects']):
                if rect.collidepoint((x, y)):
                    if self.left_mouse_down:
                        self.ui_draw.select_button_state[i] = 'active'
        
        elif self.template == Template.MODE_SELECT:
            for i, rect in enumerate(self.ui_draw.mode_ui['rects']):
                if rect.collidepoint((x, y)):
                    if self.left_mouse_down:
                        self.ui_draw.mode_button_state[i] = 'active'

    def button_up_handle(self):
        x, y = pygame.mouse.get_pos()
        x = x // self.scale
        y = y // self.scale
        if self.template == Template.GAMEPLAY:
            if self.ui_draw.is_mouse_in_board(x, y):
                pos_x, pos_y = self.get_clicked_cell(x, y)
                if pos_x != None and pos_y != None:
                    if self.ui_draw.in_board_left_clicked:
                        self.game.click(pos_x, pos_y)
                    elif self.ui_draw.in_board_right_clicked:
                        self.game.click(pos_x, pos_y, True) 
            elif self.ui_draw.is_mouse_in_smiley_button(x, y):
                if self.ui_draw.smiley_clicked:
                    self.reset_game()
                elif self.ui_draw.smiley_right_clicked:
                    self.set_template(Template.LEVEL_SELECT)

            self.ui_draw.smiley_clicked = False
            self.ui_draw.smiley_right_clicked = False
            self.ui_draw.in_board_left_clicked = False
            self.ui_draw.in_board_right_clicked = False
            self.ui_draw.clicked_unprobed_cell = False
        elif self.template == Template.LEVEL_SELECT:
            for i, rect in enumerate(self.ui_draw.level_ui['rects']):
                if rect.collidepoint((x, y)):
                    if self.ui_draw.select_button_state[i] == 'active':
                        self.ui_draw.select_button_state[i] = 'hover'
                    print(LEVEL_OPTIONS[i]['key'])
                    self.set_level(LEVEL_OPTIONS[i]['key'])
                    self.set_template(Template.MODE_SELECT)

        elif self.template == Template.MODE_SELECT:
            for i, rect in enumerate(self.ui_draw.mode_ui['rects']):
                if rect.collidepoint((x, y)):
                    if self.ui_draw.mode_button_state[i] == 'active':
                        self.ui_draw.mode_button_state[i] = 'hover'
                    if i == 0:
                        self.set_ai_helper(False)
                        print('player')
                    elif i == 1:
                        self.set_ai_helper(True)
                        print('ai')

                    self.set_template(Template.GAMEPLAY)

    def init_ui(self):
        if not pygame.display.get_init():
            pygame.display.init()

        if not pygame.font.get_init():
            pygame.font.init()

        if not self.initialized:
            windows_icon = pygame.image.load('icon.png')
            pygame.display.set_icon(windows_icon)
            pygame.display.set_caption('MineSweeper')

        if self.template == Template.GAMEPLAY:
            self.canvas_size = self.calc_game_size()
            self.ui_draw.game = self.game

        elif self.template == Template.LEVEL_SELECT:
            self.canvas_size = (LEVEL_SELECT['width'], LEVEL_SELECT['height'])

        elif self.template == Template.MODE_SELECT:
            self.canvas_size = (LEVEL_SELECT['width'], LEVEL_SELECT['height'])

        self.windows_size = self.canvas_size
        self.scale = min(self.max_width / self.windows_size[0], self.max_height / self.windows_size[1])
        if self.scale != 1:
            self.windows_size = (self.windows_size[0] * self.scale, self.windows_size[1] * self.scale)

        self.windows = pygame.display.set_mode((self.windows_size[0], self.windows_size[1]), pygame.DOUBLEBUF)
        self.canvas = pygame.Surface(self.canvas_size).convert()

        self.ui_draw.canvas = self.canvas
        self.running = True

    def draw_handle(self):
        if self.template == Template.GAMEPLAY:
            self.ui_draw.draw_gameplay()
            
        elif self.template == Template.LEVEL_SELECT:
            self.ui_draw.draw_level_select()

        elif self.template == Template.MODE_SELECT:
            self.ui_draw.draw_mode_select()

        scaled_surface = pygame.transform.smoothscale(self.canvas, (self.windows_size[0], self.windows_size[1]))
        self.windows.blit(scaled_surface, (0, 0))
        pygame.display.update()

    def event_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEMOTION:
                self.button_motion_handle()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.button_down_handle()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.button_up_handle()
            elif event.type == pygame.KEYUP and event.key == pygame.K_r:
                self.reset_game()

    def start_ui(self):
        self.init_ui()
        clock = pygame.time.Clock()
        while self.running:
            self.event_handle()
            self.draw_handle()
            clock.tick(WINDOWS['fps'])
            if self.ai_enable:
                self.ai.make_move()
        pygame.quit()

game_ui = Game_UI()
game_ui.start_ui()