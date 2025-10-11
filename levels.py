from enum import Enum

class Level(Enum):
    EASY = 'Easy'
    MEDIUM = 'Medium'
    HARD = 'Hard'
    EXPERT = 'Expert'
    MASTER = 'Master'
    LEGEND = 'Legend'

LEVEL_CONFIG = {
    Level.EASY: {
        "mines": 10,
        "rows": 8,
        "cols": 8
    },
    Level.MEDIUM: {
        "mines": 40,
        "rows": 16,
        "cols": 16
    },
    Level.HARD: {
        "mines": 99,
        "rows": 16,
        "cols": 30
    },
    Level.EXPERT: {
        "mines": 150,
        "rows": 20,
        "cols": 35
    },
    Level.MASTER: {
        "mines": 220,
        "rows": 24,
        "cols": 40
    },
    Level.LEGEND: {
        "mines": 300,
        "rows": 30,
        "cols": 50
    },
}

def get_level_config(level: Level) -> tuple[int, int, int]:
    """
    Trả về (rows, cols, mines) cho Game dựa trên Level
    """
    config = LEVEL_CONFIG[level]
    return config["rows"], config["cols"], config["mines"]