from enum import Enum
import random

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
    def __init__(self, bomb: bool = False, state: CellState = CellState.UNPROBED):
        self.bomb = bomb
        self.state = state
    
class Game:
    def __init__(self, h: int, w: int, bombs: int):
        self.reinit(h, w, bombs)

    def reinit(self, h: int, w: int, bombs: int):
        self.h = int(h)
        self.w = int(w)
        max_bombs = self.w * self.h - 1
        self.bombs = max(0, min(int(bombs), max_bombs))
        self.field: list[list[Cell]] = [[Cell() for _ in range(self.w)] for _ in range(self.h)]

        self.flags_left = self.bombs
        self.unprobed_to_clear = self.w * self.h - self.bombs
        self.state = GameState.INITIALIZED
        self.probed_queue = []

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.w and 0 <= y < self.h

    def neighbors(self, x: int, y: int):
        for ny in range(y - 1, y + 2):
            for nx in range(x - 1, x + 2):
                if nx == x and ny == y:
                    continue
                if self.in_bounds(nx, ny):
                    yield nx, ny, self.field[ny][nx]

    def adjacent_bombs(self, x: int, y: int) -> int:
        return sum(1 for _, _, c in self.neighbors(x, y) if c.bomb)

    def _init_bombs_after_first_click(self, sx: int, sy: int):
        if self.state != GameState.INITIALIZED:
            return
        total = self.w * self.h
        first_idx = sy * self.w + sx

        cc = total - 1
        bc = self.bombs
        offset = 0
        while bc > 0:
            if offset == first_idx:
                offset += 1 
            if random.randrange(cc) < bc:
                y = offset // self.w
                x = offset % self.w
                self.field[y][x].bomb = True
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
            self._init_bombs_after_first_click(x, y)

        # Mở lan nếu không có mìn xung quanh
        stack = [(x, y)]
        while stack:
            px, py = stack.pop()
            pc = self.field[py][px]

            if pc.state != CellState.UNPROBED:
                continue

            pc.state = CellState.PROBED
            self.probed_queue.append((px, py))

            if pc.bomb:
                self._gameover(last_boom=(px, py))
                return None

            self.unprobed_to_clear -= 1
            n = self.adjacent_bombs(px, py)
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

    def _clear(self):
        self.state = GameState.CLEAR

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
                    row.append(self.adjacent_bombs(x, y))
                else:
                    row.append("?")
            out.append(row)

        if self.state == GameState.GAMEOVER:
            for y in range(self.h):
                for x in range(self.w):
                    if self.field[y][x].bomb and self.field[y][x] != "F":
                        out[y][x] = "*"
        return out
    
# Testing
g = Game(8, 8, 10)
print(g.state)
for row in g.board_state():
    print(row)
while g.state != GameState.CLEAR and g.state != GameState.GAMEOVER:
    x = int(input('Nhap x: '))
    y = int(input('Nhap y: '))
    right = int(input('Right click?(0/1): '))
    g.click(x, y, False if right == 0 else True)
    print(g.state)
    for row in g.board_state():
        print(row)
