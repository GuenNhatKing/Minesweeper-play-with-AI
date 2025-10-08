from core import Game, GameState, CellState, Cell
from levels import parse_level, Level
from enum import Enum

class Action(Enum):
    PROBE = 'probe'
    FLAG = 'flag'

class AI:
    def __init__(self, game: Game):
        self.game = game  
        self.actions: list[tuple[tuple[int, int], Action]] = [] 
        
    def check_rule_1(self, x, y):
        mines_count = self.game.adjacent_mines(x, y)
        flags_count = self.game.adjacent_flagged(x, y)
        if mines_count == flags_count:
            for i, j in self.game.neighbors(x, y):
                if self.game.get_cell(i, j).state == CellState.UNPROBED:
                    self.actions.append(((i, j), Action.PROBE))
            return True
        return False

    def check_rule_2(self, x, y):
        mines_count = self.game.adjacent_mines(x, y)
        unprobed_count = self.game.adjacent_unprobed(x, y)
        flags_count = self.game.adjacent_flagged(x, y)
        if mines_count == unprobed_count + flags_count:
            for i, j in self.game.neighbors(x, y):
                if self.game.get_cell(i, j).state == CellState.UNPROBED:
                    self.actions.append(((i, j), Action.FLAG))
            return True
        return False

    def check_rule_3(self, xa, ya):
        mines_A_count = self.game.adjacent_mines(xa, ya)
        for xb, yb in self.game.neighbors(xa, ya, 2):
            if self.game.get_cell(xb, yb).state != CellState.PROBED:
                continue
            mines_B_count = self.game.adjacent_mines(xb, yb)
            unprobed_count = 0
            flags_count = 0
            for x, y in self.game.unshared_neighbors(xb, yb, xa, ya):
                if self.game.get_cell(x, y).state == CellState.UNPROBED:
                    unprobed_count += 1
                if self.game.get_cell(x, y).state == CellState.FLAGGED:
                    flags_count += 1

            if mines_A_count == (mines_B_count - unprobed_count - flags_count):  
                for x, y in self.game.unshared_neighbors(xa, ya, xb, yb):
                    if self.game.get_cell(x, y).state == CellState.UNPROBED:
                        self.actions.append(((x, y), Action.PROBE))
                for x, y in self.game.unshared_neighbors(xb, yb, xa, ya):
                    if self.game.get_cell(x, y).state == CellState.UNPROBED:
                        self.actions.append(((x, y), Action.FLAG))
                return True
        return False

    def infer(self):
        if not self.game.state == GameState.PLAYING:
            return False
        if len(self.game.probed_queue) == 0:
            return False

        probedCells = self.game.probed_queue.copy()
        while probedCells:
            x, y = probedCells.pop()
            if self.game.get_cell(x, y).state == CellState.PROBED:
                self.check_rule_1(x, y)
                self.check_rule_2(x, y)
                self.check_rule_3(x, y)
    
    def make_move(self):
        if self.game.state == GameState.INITIALIZED:
            self.actions.clear()
        if self.game.state == GameState.PLAYING:
            if len(self.actions) == 0: 
                self.infer()
            if self.game.state == GameState.PLAYING and self.actions:
                ft = self.actions.pop(0)
                x, y = ft[0]
                action = ft[1]
                if self.game.get_cell(x, y).state == CellState.UNPROBED:
                    if action == Action.PROBE:
                        # print(f'AI is PROBEDING ({x}, {y})!')
                        self.game.click(x, y)
                    elif action == Action.FLAG:
                        # print(f'AI is FLAGGING ({x}, {y})!')
                        self.game.click(x, y, right=True)    
                    