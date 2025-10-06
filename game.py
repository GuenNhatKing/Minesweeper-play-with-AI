from core import Game
from config import LEVELS
from ui import start_ui

height, width, mines = LEVELS['1']['height'], LEVELS['1']['width'], LEVELS['1']['mines']

print(height, width, mines)
game = Game(height, width, mines)
start_ui(game)