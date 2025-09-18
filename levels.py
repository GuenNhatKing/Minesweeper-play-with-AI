from enum import Enum

class Level(Enum):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'
    CUSTOM = 'custom'

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
    Level.CUSTOM: {
        "mines": 0,
        "rows": 0,
        "cols": 0
    }
}

def get_level_config(level: Level) -> tuple[int, int, int]:
    """
    Trả về (rows, cols, mines) cho Game dựa trên Level
    """
    config = LEVEL_CONFIG[level]
    return config["rows"], config["cols"], config["mines"]

def parse_level(name: str, custom: tuple[int, int, int] = None) -> tuple[int, int, int]:
    """
    Parse từ string -> (rows, cols, mines)
    Ví dụ: 'easy', 'medium', 'hard', 'custom'
    Nếu custom thì cần truyền vào tuple (rows, cols, mines)
    """
    name = name.strip().lower()
    try:
        level = Level(name)
    except ValueError:
        raise ValueError(f"Invalid level name: {name}")
    if level == Level.CUSTOM:
        if custom is None:
            raise ValueError("Custom level requires (rows, cols, mines) tuple")
        return custom
    return get_level_config(level)