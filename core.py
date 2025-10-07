from enum import Enum
from levels import parse_level
import random
from timer import Timer

class CellState(Enum):
    UNPROBED = "unprobed"
    PROBED = "probed"
    FLAGGED = "flagged"

class GameState(Enum):
    INITIALIZED = "initialized"
    PLAYING = "playing"
    CLEAR = "clear"
    GAMEOVER = "gameover"

class Cell:
    def __init__(self, mine: bool = False, state: CellState = CellState.UNPROBED):
        self.mine = mine
        self.state = state
    
class Game:
    def __init__(self, h: int, w: int, mines: int):
        self.h = int(h)
        self.w = int(w)
        max_mines = self.w * self.h - 1
        self.mines = max(0, min(int(mines), max_mines))
        self.field: list[list[Cell]] = [[Cell() for _ in range(self.w)] for _ in range(self.h)]

        self.flags_left = self.mines
        self.unprobed_to_clear = self.w * self.h - self.mines
        self.state = GameState.INITIALIZED
        self.probed_queue = []
        self.timer = Timer()
        self.timer.start()

    def reset(self, h: int, w: int, mines: int):
        self.h = int(h)
        self.w = int(w)
        max_mines = self.w * self.h - 1
        self.mines = max(0, min(int(mines), max_mines))
        self.field: list[list[Cell]] = [[Cell() for _ in range(self.w)] for _ in range(self.h)]

        self.flags_left = self.mines
        self.unprobed_to_clear = self.w * self.h - self.mines
        self.state = GameState.INITIALIZED
        self.probed_queue = []
        self.timer.reset()
        self.timer.start()

    def is_mine(self, x: int, y: int) -> bool:
        return self.field[y][x].mine
    
    def is_flagged(self, x: int, y: int) -> bool:
        return self.field[y][x].state == CellState.FLAGGED
    
    def is_exploded_mine(self, x: int, y: int) -> bool:
        if self.probed_queue:
            return self.probed_queue[-1] == (x, y)
        return 0

    def get_size(self):
        return (self.w, self.h)

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.w and 0 <= y < self.h
    
    def get_cell_state(self, x, y):
        if self.in_bounds(x, y):
            return self.field[y][x].state
        return None

    def neighbors(self, x: int, y: int):
        for ny in range(y - 1, y + 2):
            for nx in range(x - 1, x + 2):
                if nx == x and ny == y:
                    continue
                if self.in_bounds(nx, ny):
                    yield nx, ny, self.field[ny][nx]

    def adjacent_mines(self, x: int, y: int) -> int:
        return sum(1 for _, _, c in self.neighbors(x, y) if c.mine)

    def _init_mines_after_first_click(self, sx: int, sy: int):
        if self.state != GameState.INITIALIZED:
            return
        total = self.w * self.h
        first_idx = sy * self.w + sx

        cc = total - 1
        bc = self.mines
        offset = 0
        while bc > 0:
            if offset == first_idx:
                offset += 1 
            if random.randrange(cc) < bc:
                y = offset // self.w
                x = offset % self.w
                self.field[y][x].mine = True
                bc -= 1
            offset += 1
            cc -= 1

        self.state = GameState.PLAYING

    def flag(self, x: int, y: int):
        if self.state in (GameState.CLEAR, GameState.GAMEOVER):
            return
        cell = self.field[y][x]
        if cell.state == CellState.PROBED:
            return
        if cell.state == CellState.UNPROBED:
            if self.flags_left <= 0:
                return
            cell.state = CellState.FLAGGED
            self.flags_left -= 1
        else:  # FLAGGED -> UNPROBED
            cell.state = CellState.UNPROBED
            self.flags_left += 1

    def probe(self, x: int, y: int):
        """
        Mở ô (x,y):
            - Nếu dính mìn: state -> GAMEOVER
            - Trả về None nếu không có gì xảy ra (ô đã mở/cờ hoặc game kết thúc)
            - Khi mở hết ô safe: state -> CLEAR.
        """
        if self.state in (GameState.CLEAR, GameState.GAMEOVER):
            return None

        cell = self.field[y][x]
        if cell.state == CellState.FLAGGED or cell.state == CellState.PROBED:
            return None

        if self.state == GameState.INITIALIZED:
            self._init_mines_after_first_click(x, y)

        # Mở lan nếu không có mìn xung quanh
        stack = [(x, y)]
        while stack:
            px, py = stack.pop()
            pc = self.field[py][px]

            if pc.state != CellState.UNPROBED:
                continue

            pc.state = CellState.PROBED
            self.probed_queue.append((px, py))

            if pc.mine:
                self._gameover()
                return None

            self.unprobed_to_clear -= 1
            n = self.adjacent_mines(px, py)
            if n == 0:
                for nx, ny, nc in self.neighbors(px, py):
                    if nc.state == CellState.UNPROBED:
                        stack.append((nx, ny))

            if self.unprobed_to_clear == 0:
                self._clear()

    def click(self, x: int, y: int, right: bool = False):
        if right:
            self.flag(x, y)
            return None
        return self.probe(x, y)

    def _gameover(self):
        self.state = GameState.GAMEOVER
        self.timer.stop()

    def _clear(self):
        self.state = GameState.CLEAR
        self.timer.stop()

    def board_state(self):
        # Dùng cho debug
        out = []
        for y in range(self.h):
            row = []
            for x in range(self.w):
                c = self.field[y][x]
                if c.state == CellState.FLAGGED:
                    row.append("F")
                elif c.state == CellState.UNPROBED:
                    row.append("U")
                elif c.state == CellState.PROBED:
                    row.append(self.adjacent_mines(x, y))
                else:
                    row.append("?")
            out.append(row)

        if self.state == GameState.GAMEOVER:
            for y in range(self.h):
                for x in range(self.w):
                    if self.field[y][x].mine and self.field[y][x] != "F":
                        out[y][x] = "*"
        return out
    
# Testing
# print("chon level: easy, medium, hard, custom")
# level = input("Nhap level: ")
# if level.strip().lower() == 'custom':
#     rows = int(input("Nhap rows: "))
#     cols = int(input("Nhap cols: "))
#     mines = int(input("Nhap mines: "))
#     rows, cols, mines = parse_level(level, (rows, cols, mines))
# else:
#     rows, cols, mines = parse_level(level)

# g = Game(rows, cols, mines)
# while g.state != GameState.CLEAR and g.state != GameState.GAMEOVER:
#     x = int(input('Nhap x: '))
#     y = int(input('Nhap y: '))
#     right = int(input('Right click?(0/1): '))
#     g.click(x, y, False if right == 0 else True)
#     print(g.state)
#     for row in g.board_state():
#         print(row)
