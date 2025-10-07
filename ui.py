import pygame
from config import *
from core import Game, CellState, GameState

class GameImage:
    def __init__(self):
        self.image_srcs = [
            {'name': 'number_1', 'src': 'assets/icons/Minesweeper_tile_number_1.png'},
            {'name': 'number_2', 'src': 'assets/icons/Minesweeper_tile_number_2.png'},
            {'name': 'number_3', 'src': 'assets/icons/Minesweeper_tile_number_3.png'},
            {'name': 'number_4', 'src': 'assets/icons/Minesweeper_tile_number_4.png'},
            {'name': 'number_5', 'src': 'assets/icons/Minesweeper_tile_number_5.png'},
            {'name': 'number_6', 'src': 'assets/icons/Minesweeper_tile_number_6.png'},
            {'name': 'number_7', 'src': 'assets/icons/Minesweeper_tile_number_7.png'},
            {'name': 'number_8', 'src': 'assets/icons/Minesweeper_tile_number_8.png'},

            {'name': 'flag', 'src': 'assets/icons/Minesweeper_flag.png'},
            {'name': 'tile_probed', 'src': 'assets/icons/Minesweeper_tile_probed.png'},
            {'name': 'tile_unprobed', 'src': 'assets/icons/Minesweeper_tile_unprobed.png'},

            {'name': 'mine', 'src': 'assets/icons/Minesweeper_mine.png'},
            {'name': 'mine_red', 'src': 'assets/icons/Minesweeper_mine_red.png'},
            {'name': 'not_mine', 'src': 'assets/icons/Minesweeper_not_mine.png'},

            {'name': 'smiley_happy', 'src': 'assets/icons/Minesweeper_smiley__happy.png'},
            {'name': 'smiley_dead', 'src': 'assets/icons/Minesweeper_smiley__dead.png'},
            {'name': 'smiley_cool', 'src': 'assets/icons/Minesweeper_smiley__cool.png'},
            {'name': 'smiley_shocked', 'src': 'assets/icons/Minesweeper_smiley__shocked.png'},
            {'name': 'smiley_clicked', 'src': 'assets/icons/Minesweeper_smiley__clicked.png'},
        ]
        self.images = {}
        for x in self.image_srcs:
            self.images[x['name']] = pygame.transform.scale(pygame.image.load(x['src']), (CELL['size'], CELL['size']))

    def get_surface(self, name):
        return self.images[name]

class UI_Draw:
    def __init__(self, surface: pygame.Surface, game: Game):
        self.game_image = GameImage()
        self.canvas = surface
        self.game = game
        self.in_board_left_clicked = False
        self.in_board_right_clicked = False
        self.clicked_unprobed_cell = False
        self.smiley_clicked = False

    # Draw functions
    def draw_status_bar(self):
        width = self.canvas.get_width()
        rect = pygame.Rect(0, 0, width, STATUS_BAR['height'])
        pygame.draw.rect(self.canvas, STATUS_BAR['bg_color'], rect)

        mine_counter_font = pygame.font.Font(MINE_COUNTER['font'], min(MINE_COUNTER['font-size'], STATUS_BAR['height'] - 2 * STATUS_BAR['padding-horizontal']))
        mine_counter_text = mine_counter_font.render(f'{self.game.flags_left:03d}', True, MINE_COUNTER['color'], MINE_COUNTER['bg-color'])

        mine_counter_rect = pygame.Rect(STATUS_BAR['padding-vertical'], STATUS_BAR['padding-horizontal'], MINE_COUNTER['width'], STATUS_BAR['height'] - 2 * STATUS_BAR['padding-horizontal'])
        pygame.draw.rect(self.canvas, MINE_COUNTER['bg-color'], mine_counter_rect)
        
        mine_counter_text_rect = mine_counter_text.get_rect()
        mine_counter_text_rect.center = (STATUS_BAR['padding-vertical'] + MINE_COUNTER['width'] // 2, STATUS_BAR['height'] // 2)
        self.canvas.blit(mine_counter_text, mine_counter_text_rect)

        timer_font = pygame.font.Font(TIMER['font'], min(TIMER['font-size'], STATUS_BAR['height'] - 2 * STATUS_BAR['padding-horizontal']))
        timer_text = timer_font.render(f'{self.game.flags_left:03d}', True, TIMER['color'], TIMER['bg-color'])

        timer_rect = pygame.Rect(width - STATUS_BAR['padding-vertical'] - TIMER['width'], STATUS_BAR['padding-horizontal'], TIMER['width'], STATUS_BAR['height'] - 2 * STATUS_BAR['padding-horizontal'])
        pygame.draw.rect(self.canvas, TIMER['bg-color'], timer_rect)
        
        timer_text_rect = timer_text.get_rect()
        timer_text_rect.center = (width - STATUS_BAR['padding-vertical'] - TIMER['width'] // 2, STATUS_BAR['height'] // 2)
        self.canvas.blit(timer_text, timer_text_rect)
        
        smiley_width = STATUS_BAR['height'] - 2 * STATUS_BAR['padding-horizontal'] # Square
        smiley_button_rect = pygame.Rect((width - smiley_width) // 2, STATUS_BAR['padding-horizontal'], smiley_width, STATUS_BAR['height'] - 2 * STATUS_BAR['padding-horizontal'])
        
        if self.game.state == GameState.CLEAR:
            self.canvas.blit(self.game_image.get_surface('smiley_cool'), smiley_button_rect)
        elif self.game.state == GameState.GAMEOVER:
            self.canvas.blit(self.game_image.get_surface('smiley_dead'), smiley_button_rect)
        elif self.in_board_left_clicked and self.clicked_unprobed_cell\
            and (self.game.state == GameState.INITIALIZED or self.game.state == GameState.PLAYING):
            self.canvas.blit(self.game_image.get_surface('smiley_shocked'), smiley_button_rect)
        else:
            self.canvas.blit(self.game_image.get_surface('smiley_happy'), smiley_button_rect)
        
        if self.smiley_clicked:
            self.canvas.blit(self.game_image.get_surface('smiley_clicked'), smiley_button_rect)

    def draw_board(self): 
        w, h = self.game.get_size()

        board_offset_x = BOARD['padding']
        board_offset_y = STATUS_BAR['height'] + BOARD['padding']
        board_width = w * CELL['size'] + (w + 1) * BOARD['gap']
        board_height = h * CELL['size'] + (h + 1) * BOARD['gap']

        board_rect = pygame.Rect(board_offset_x, board_offset_y, board_width, board_height)
        pygame.draw.rect(self.canvas, BOARD['bg_color'], board_rect)

        offset_y = board_offset_y + BOARD['gap']

        for j in range(h):
            offset_x = board_offset_x + BOARD['gap']
            for i in range(w):
                state = self.game.get_cell_state(i, j)
                cell_rect = pygame.Rect(offset_x, offset_y, CELL['size'], CELL['size'])
                offset_x += CELL['size'] + BOARD['gap']

                if state == CellState.UNPROBED:
                    pygame.draw.rect(self.canvas, CELL['unprobed_color'], cell_rect)
                    self.canvas.blit(self.game_image.get_surface('tile_unprobed'), cell_rect)
                elif state == CellState.FLAGGED:
                    pygame.draw.rect(self.canvas, CELL['unprobed_color'], cell_rect)
                    self.canvas.blit(self.game_image.get_surface('flag'), cell_rect)
                elif state == CellState.PROBED:
                    pygame.draw.rect(self.canvas, CELL['probed_color'], cell_rect)
                    adj = self.game.adjacent_mines(i, j)
                    if 1 <= adj <= 8:
                        self.canvas.blit(self.game_image.get_surface(f'number_{adj}'), cell_rect)
                    if adj == 0:
                        self.canvas.blit(self.game_image.get_surface('tile_probed'), cell_rect)
            offset_y += CELL['size'] + BOARD['gap']
        
        offset_y = board_offset_y + BOARD['gap']
        if self.game.state == GameState.GAMEOVER:
            for y in range(h):
                offset_x = board_offset_x + BOARD['gap']
                for x in range(w):
                    cell_rect = pygame.Rect(offset_x, offset_y, CELL['size'], CELL['size'])
                    offset_x += CELL['size'] + BOARD['gap']

                    is_mine = self.game.is_mine(x, y)
                    is_flagged = self.game.is_flagged(x, y)
                    is_exploded_mine = self.game.is_exploded_mine(x, y)
                    if is_mine and not is_flagged:
                        self.canvas.blit(self.game_image.get_surface('mine'), cell_rect)
                    
                    if not is_mine and is_flagged:
                        self.canvas.blit(self.game_image.get_surface('not_mine'), cell_rect)

                    if is_mine and is_exploded_mine:
                        self.canvas.blit(self.game_image.get_surface('mine_red'), cell_rect)
                    
                offset_y += CELL['size'] + BOARD['gap']      

    def is_mouse_in_board(self, x, y):
        width, height = self.canvas.get_size()
        return BOARD['padding'] + BOARD['gap'] <= x <= width - BOARD['padding'] \
            and STATUS_BAR['height'] + BOARD['padding'] + BOARD['gap'] <= y <= height - BOARD['padding']

    def is_mouse_in_smiley_button(self, x, y):
        width, height = self.canvas.get_size()
        smiley_width = STATUS_BAR['height'] - 2 * STATUS_BAR['padding-horizontal']
        return (width - smiley_width) // 2 <= x <= (width - smiley_width) // 2 + smiley_width\
            and STATUS_BAR['padding-horizontal'] <= y <= STATUS_BAR['height'] - STATUS_BAR['padding-horizontal']
