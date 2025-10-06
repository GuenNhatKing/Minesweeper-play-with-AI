import pygame
from config import *
from core import Game, CellState, GameState

numbers = {}
for n in range(1, 9):
    img = pygame.image.load(f'assets/icons/Minesweeper_tile_number_{n}.png')
    numbers[n] = pygame.transform.scale(img, (CELL['size'], CELL['size']))

img = pygame.image.load('assets/icons/Minesweeper_flag.png')
flag = pygame.transform.scale(img, (CELL['size'], CELL['size']))

img = pygame.image.load('assets/icons/Minesweeper_tile_probed.png')
tile_probed = pygame.transform.scale(img, (CELL['size'], CELL['size']))

img = pygame.image.load('assets/icons/Minesweeper_tile_unprobed.png')
tile_unprobed = pygame.transform.scale(img, (CELL['size'], CELL['size']))

img = pygame.image.load('assets/icons/Minesweeper_mine.png')
mine = pygame.transform.scale(img, (CELL['size'], CELL['size']))

img = pygame.image.load('assets/icons/Minesweeper_mine_red.png')
mine_red = pygame.transform.scale(img, (CELL['size'], CELL['size']))

img = pygame.image.load('assets/icons/Minesweeper_not_mine.png')
not_mine = pygame.transform.scale(img, (CELL['size'], CELL['size']))

# Calculate functions
def calc_windows_size(game: Game):
    w, h = game.get_size()
    height = STATUS_BAR['height'] + h * CELL['size'] + (h + 1) * BOARD['gap'] + BOARD['padding'] * 2
    width = w * CELL['size'] + (w + 1) * BOARD['gap'] + BOARD['padding'] * 2
    return (width, height)

def click_handle(x, y, windows: pygame.Surface, game: Game):
    width, height = windows.get_size()
    if BOARD['padding'] + BOARD['gap'] <= x <= width - BOARD['padding'] \
        and STATUS_BAR['height'] + BOARD['padding'] + BOARD['gap'] <= y <= height - BOARD['padding']:
        board_x = x - BOARD['padding'] - BOARD['gap']
        board_y = y - STATUS_BAR['height'] - BOARD['padding'] - BOARD['gap']
        pos_x = board_x // (CELL['size'] + BOARD['gap'])
        pos_y = board_y // (CELL['size'] + BOARD['gap'])
        if pos_x * (CELL['size'] + BOARD['gap']) <= board_x <= pos_x * (CELL['size'] + BOARD['gap']) + CELL['size']\
        and pos_y * (CELL['size'] + BOARD['gap']) <= board_y <= pos_y * (CELL['size'] + BOARD['gap']) + CELL['size']:
            if pygame.mouse.get_pressed()[0]:
                game.click(pos_x, pos_y)
            elif  pygame.mouse.get_pressed()[2]:
                game.click(pos_x, pos_y, True)

# Draw functions
def draw_status_bar(windows: pygame.Surface, game: Game):
    width = windows.get_width()
    rect = pygame.Rect(0, 0, width, STATUS_BAR['height'])
    pygame.draw.rect(windows, STATUS_BAR['bg_color'], rect)

    mine_counter_font = pygame.font.Font(MINE_COUNTER['font'], min(MINE_COUNTER['font-size'], STATUS_BAR['height'] - 2 * STATUS_BAR['padding-horizontal']))
    mine_counter_text = mine_counter_font.render(f'{game.flags_left:03d}', True, MINE_COUNTER['color'], MINE_COUNTER['bg-color'])

    mine_counter_rect = pygame.Rect(STATUS_BAR['padding-vertical'], STATUS_BAR['padding-horizontal'], MINE_COUNTER['width'], STATUS_BAR['height'] - 2 * STATUS_BAR['padding-horizontal'])
    pygame.draw.rect(windows, MINE_COUNTER['bg-color'], mine_counter_rect)
    
    mine_counter_text_rect = mine_counter_text.get_rect()
    mine_counter_text_rect.center = (STATUS_BAR['padding-vertical'] + MINE_COUNTER['width'] // 2, STATUS_BAR['height'] // 2)
    windows.blit(mine_counter_text, mine_counter_text_rect)

    timer_font = pygame.font.Font(TIMER['font'], min(TIMER['font-size'], STATUS_BAR['height'] - 2 * STATUS_BAR['padding-horizontal']))
    timer_text = timer_font.render(f'{game.flags_left:03d}', True, TIMER['color'], TIMER['bg-color'])

    timer_rect = pygame.Rect(width - STATUS_BAR['padding-vertical'] - TIMER['width'], STATUS_BAR['padding-horizontal'], TIMER['width'], STATUS_BAR['height'] - 2 * STATUS_BAR['padding-horizontal'])
    pygame.draw.rect(windows, TIMER['bg-color'], timer_rect)
    
    timer_text_rect = timer_text.get_rect()
    timer_text_rect.center = (width - STATUS_BAR['padding-vertical'] - TIMER['width'] // 2, STATUS_BAR['height'] // 2)
    windows.blit(timer_text, timer_text_rect)
    
    # smiley_button_rect = pygame.Rect()
    
def draw_board(windows: pygame.Surface, game: Game): 
    w, h = game.get_size()

    board_offset_x = BOARD['padding']
    board_offset_y = STATUS_BAR['height'] + BOARD['padding']
    board_width = h * CELL['size'] + (h + 1) * BOARD['gap']
    board_height = w * CELL['size'] + (w + 1) * BOARD['gap']

    board_rect = pygame.Rect(board_offset_x, board_offset_y, board_width, board_height)
    pygame.draw.rect(windows, BOARD['bg_color'], board_rect)

    offset_y = board_offset_y + BOARD['gap']

    for i in range(h):
        offset_x = board_offset_x + BOARD['gap']
        for j in range(w):
            state = game.get_cell_state(j, i)
            cell_rect = pygame.Rect(offset_x, offset_y, CELL['size'], CELL['size'])
            offset_x += CELL['size'] + BOARD['gap']

            if state == CellState.UNPROBED:
                pygame.draw.rect(windows, CELL['unprobed_color'], cell_rect)
                windows.blit(tile_unprobed, cell_rect)
            elif state == CellState.FLAGGED:
                pygame.draw.rect(windows, CELL['unprobed_color'], cell_rect)
                windows.blit(flag, cell_rect)
            elif state == CellState.PROBED:
                pygame.draw.rect(windows, CELL['probed_color'], cell_rect)
                adj = game.adjacent_mines(j, i)
                if 1 <= adj <= 8:
                    windows.blit(numbers[adj], cell_rect)
                if adj == 0:
                    windows.blit(tile_probed, cell_rect)
        offset_y += CELL['size'] + BOARD['gap']
    
    offset_y = board_offset_y + BOARD['gap']
    if game.state == GameState.GAMEOVER:
        for y in range(h):
            offset_x = board_offset_x + BOARD['gap']
            for x in range(w):
                cell_rect = pygame.Rect(offset_x, offset_y, CELL['size'], CELL['size'])
                offset_x += CELL['size'] + BOARD['gap']

                is_mine = game.is_mine(x, y)
                is_flagged = game.is_flagged(x, y)
                is_exploded_mine = game.is_exploded_mine(x, y)
                if is_mine and not is_flagged:
                    windows.blit(mine, cell_rect)
                
                if not is_mine and is_flagged:
                    windows.blit(not_mine, cell_rect)

                if is_mine and is_exploded_mine:
                    windows.blit(mine_red, cell_rect)
                
            offset_y += CELL['size'] + BOARD['gap']      

# Start pygame
def start_ui(game: Game):
    pygame.init()
    pygame.font.init()

    windows_icon = pygame.image.load('icon.png')
    pygame.display.set_icon(windows_icon)
    pygame.display.set_caption('MineSweeper')

    width, height = calc_windows_size(game)
    windows = pygame.display.set_mode((width, height))
    windows.fill(WINDOWS['bg_color'])

    running = True
    clock = pygame.time.Clock()

    while running:
        draw_status_bar(windows, game)
        draw_board(windows, game)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                click_handle(x, y, windows, game)

        clock.tick(WINDOWS['fps'])

    pygame.quit()