from enum import Enum
import random
from timer import Timer
from dataclasses import dataclass

class CellState(Enum):
    UNPROBED = "unprobed"
    PROBED = "probed"
    FLAGGED = "flagged"
    UNDEFINED = "undefined"

class GameState(Enum):
    INITIALIZED = "initialized"
    PLAYING = "playing"
    CLEAR = "clear"
    GAMEOVER = "gameover"
    UNDEFINED = "undefined"

@dataclass
class Cell:
    def __init__(self, mine: bool = False, state: CellState = CellState.UNDEFINED):
        self.mine = mine
        self.state = state
    
class Game:
    def __init__(self, h: int, w: int, mines: int):
        self.h = h
        self.w = w
        max_mines = self.w * self.h - 1
        self.mines = max(0, min(int(mines), max_mines))
        self.field: list[list[Cell]] = [[Cell(state=CellState.UNPROBED) for _ in range(self.w)] for _ in range(self.h)]
        self.flags_left = self.mines
        self.unprobed_to_clear = self.w * self.h - self.mines
        self.state = GameState.INITIALIZED
        self.probed_queue = []
        self.timer = Timer()

    def change_game_config(self, h: int, w: int, mines: int):
        self.h = h
        self.w = w
        max_mines = self.w * self.h - 1
        self.mines = max(0, min(int(mines), max_mines))
        self.field: list[list[Cell]] = [[Cell(state=CellState.UNPROBED) for _ in range(self.w)] for _ in range(self.h)]
        self.flags_left = self.mines
        self.unprobed_to_clear = self.w * self.h - self.mines
        self.state = GameState.INITIALIZED
        self.probed_queue.clear()
        self.timer.reset()

    def reset(self):
        for j in range(self.h):
            for i in range(self.w):
                self.field[j][i].mine = False
                self.field[j][i].state = CellState.UNPROBED

        self.flags_left = self.mines
        self.unprobed_to_clear = self.w * self.h - self.mines
        self.state = GameState.INITIALIZED
        self.probed_queue.clear()
        self.timer.reset()

    def is_mine(self, x: int, y: int) -> bool:
        return self.field[y][x].mine
    
    def is_exploded_mine(self, x: int, y: int) -> bool:
        if self.probed_queue:
            return self.probed_queue[-1] == (x, y)
        return False
    
    def is_probed(self, x: int, y: int) -> bool:
        return self.field[y][x].state == CellState.PROBED
    
    def is_unprobed(self, x: int, y: int) -> bool:
        return self.field[y][x].state == CellState.UNPROBED
    
    def is_flagged(self, x: int, y: int) -> bool:
        return self.field[y][x].state == CellState.FLAGGED

    def get_size(self):
        return (self.w, self.h)

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.w and 0 <= y < self.h
    
    def get_cell(self, x, y) -> Cell:
        if self.in_bounds(x, y):
            return self.field[y][x]
        return Cell()

    def neighbors(self, x: int, y: int, distance: int = 1):
        for ny in range(y - distance, y + distance + 1):
            for nx in range(x - distance, x + distance + 1):
                if nx == x and ny == y:
                    continue
                if self.in_bounds(nx, ny):
                    yield nx, ny

    def unshared_neighbors(self, x1, y1, x2, y2):
        # neighbors of (1) but not neighbors of (2)
        for x3, y3 in self.neighbors(x1, y1):
            if (abs(x3 - x2) >= 2 or abs(y3 - y2) >= 2):
                yield x3, y3

    def adjacent_mines(self, x: int, y: int) -> int:
        return sum(1 for i, j in self.neighbors(x, y) if self.is_mine(i, j))
    
    def adjacent_unprobed(self, x: int, y: int) -> int:
        return sum(1 for i, j in self.neighbors(x, y) if self.is_unprobed(i, j))

    def adjacent_flagged(self, x: int, y: int) -> int:
        return sum(1 for i, j in self.neighbors(x, y) if self.is_flagged(i, j))

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
        self.timer.start()

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
                for nx, ny in self.neighbors(px, py):
                    if self.get_cell(nx, ny).state == CellState.UNPROBED:
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
                    if self.field[y][x].mine and self.field[y][x].state != CellState.FLAGGED:
                        out[y][x] = "*"
        return out