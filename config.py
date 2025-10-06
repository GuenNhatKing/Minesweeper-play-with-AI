FONT = {
    'helvetica': 'assets/fonts/Helvetica.ttf',
    'helvetica-bold': 'assets/fonts/Helvetica-Bold.ttf'
}

WINDOWS = {
    'fps': 60,
    'bg_color': (171, 171, 171)
}

STATUS_BAR = {
    'height': 60,
    'padding-vertical': 20,
    'padding-horizontal': 10,
    'bg_color': (100, 100, 100)
}

BOARD = {
    'padding': 20,
    'bg_color': (108, 108, 108),
    'gap': 4
}

CELL = {
    'size': 40,
    'unprobed_color': (220, 220, 220),
    'probed_color': (192, 192, 192)
}

MINE_COUNTER = {
    'font': FONT['helvetica'],
    'font-size': 28,
    'color': (255, 0, 0),
    'bg-color': (0, 0, 0),
    'width': 60
}

TIMER = {
    'font': FONT['helvetica'],
    'font-size': 28,
    'color': (255, 0, 0),
    'bg-color': (0, 0, 0),
    'width': 60
}

LEVELS = {
    # Beginner
    "1": {"height": 9,  "width": 9,  "mines": 10},
    # Easy
    "2": {"height": 12, "width": 12, "mines": 20},
    # Intermediate
    "3": {"height": 16, "width": 16, "mines": 40},
    # Hard
    "4": {"height": 20, "width": 24, "mines": 80},
    # Expert
    "5": {"height": 16, "width": 30, "mines": 99},
}