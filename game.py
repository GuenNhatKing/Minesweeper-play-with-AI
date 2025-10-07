from levels import parse_level, Level
import pygame
from config import *
from core import Game, GameState, CellState
from ui import UI_Draw

def get_work_area_size():
    if not pygame.display.get_init():
        pygame.display.init()
    
    info = pygame.display.Info()
    width = info.current_w * 0.8
    height = info.current_h * 0.8
    return width, height

class Game_UI:
    def __init__(self, level = Level.EASY):
        self.reinit(level)
    
    def reinit(self, level: Level):
        self.level = level
        self.max_width, self.max_height = get_work_area_size()
        self.rows, self.cols, self.mines = parse_level(level.value)
        self.game = Game(self.rows, self.cols, self.mines)
        self.cell_size = CELL['size']
    
    def reset_game(self):
        self.game.reinit(self.rows, self.cols, self.mines)

    def calc_windows_size(self):
        w, h = self.game.get_size()
        height = STATUS_BAR['height'] + h * CELL['size'] + (h + 1) * BOARD['gap'] + BOARD['padding'] * 2
        width = w * CELL['size'] + (w + 1) * BOARD['gap'] + BOARD['padding'] * 2
        return (width, height)
    
    def button_motion_handle(self):
        x, y = pygame.mouse.get_pos()
        x = x // self.scale
        y = y // self.scale

        if self.ui_draw.in_board_left_clicked:
            if not self.ui_draw.is_mouse_in_board(x, y):
                self.ui_draw.in_board_left_clicked = False

        if self.ui_draw.in_board_right_clicked:
            if not self.ui_draw.is_mouse_in_board(x, y):
                self.ui_draw.in_board_right_clicked = False

        pos_x, pos_y = self.get_clicked_cell(x, y)
        if pos_x != None and pos_y != None and self.game.get_cell_state(pos_x, pos_y) == CellState.UNPROBED:
            self.ui_draw.clicked_unprobed_cell = True
        else:
            self.ui_draw.clicked_unprobed_cell = False

        if self.ui_draw.smiley_clicked:
            if not self.ui_draw.is_mouse_in_smiley_button(x, y):
                self.ui_draw.smiley_clicked = False

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

        if self.ui_draw.is_mouse_in_board(x, y):
            if pygame.mouse.get_pressed()[0]:
                self.ui_draw.in_board_left_clicked = True
            elif pygame.mouse.get_pressed()[2]:
                self.ui_draw.in_board_right_clicked = True
            pos_x, pos_y = self.get_clicked_cell(x, y)
            if pos_x != None and pos_y != None and self.game.get_cell_state(pos_x, pos_y) == CellState.UNPROBED:
                    self.ui_draw.clicked_unprobed_cell = True
        elif self.ui_draw.is_mouse_in_smiley_button(x, y):
            self.ui_draw.smiley_clicked = True

    def button_up_handle(self):
        x, y = pygame.mouse.get_pos()
        x = x // self.scale
        y = y // self.scale

        if self.ui_draw.is_mouse_in_board(x, y):
            pos_x, pos_y = self.get_clicked_cell(x, y)
            if pos_x != None and pos_y != None:
                if self.ui_draw.in_board_left_clicked:
                    self.game.click(pos_x, pos_y)
                elif self.ui_draw.in_board_right_clicked:
                    self.game.click(pos_x, pos_y, True) 
        elif self.ui_draw.is_mouse_in_smiley_button(x, y):
            self.reset_game()

        self.ui_draw.smiley_clicked = False
        self.ui_draw.in_board_left_clicked = False
        self.ui_draw.in_board_right_clicked = False
        self.ui_draw.clicked_unprobed_cell = False

    def start_ui(self):
        if not pygame.display.get_init():
            pygame.display.init()
        if not pygame.font.get_init():
            pygame.font.init()

        windows_icon = pygame.image.load('icon.png')
        pygame.display.set_icon(windows_icon)
        pygame.display.set_caption('MineSweeper')

        game_width, game_height = self.calc_windows_size()
        self.width, self.height = game_width, game_height
        self.scale = min(self.max_width / self.width, self.max_height / self.height)
        if self.scale != 1:
            self.width = int(self.width * self.scale)
            self.height = int(self.height * self.scale)

        windows = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE | pygame.SCALED | pygame.DOUBLEBUF)
        self.canvas = pygame.Surface((game_width, game_height)).convert()
        self.canvas.fill(WINDOWS['bg_color'])

        self.ui_draw = UI_Draw(surface=self.canvas, game=self.game)

        running = True
        clock = pygame.time.Clock()

        while running:
            self.ui_draw.draw_status_bar()
            self.ui_draw.draw_board()
            scaled_surface = pygame.transform.smoothscale(self.canvas, (self.width, self.height))
            windows.blit(scaled_surface, (0, 0))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEMOTION:
                    self.button_motion_handle()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.button_down_handle()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.button_up_handle()
                elif event.type == pygame.KEYUP and event.key == pygame.K_r:
                    self.reset_game()

            clock.tick(WINDOWS['fps'])

        pygame.quit()

game_ui = Game_UI(level=Level.EASY)
game_ui.start_ui()