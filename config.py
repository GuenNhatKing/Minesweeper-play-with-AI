from levels import Level, LEVEL_CONFIG
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
    'gap': 0
}

CELL = {
    'size': 40,
    'unprobed_color': (220, 220, 220),
    'probed_color': (192, 192, 192)
}

MINE_COUNTER = {
    'font': FONT['helvetica-bold'],
    'font-size': 28,
    'color': (255, 0, 0),
    'bg-color': (0, 0, 0),
    'width': 60
}

TIMER = {
    'font': FONT['helvetica-bold'],
    'font-size': 28,
    'color': (255, 0, 0),
    'bg-color': (0, 0, 0),
    'width': 60
}

LEVEL_SELECT = {
    'bg-color': (171, 171, 171),
    'width': 400,
    'height': 400
}

LEVEL_BUTTON = {
    'font': FONT['helvetica-bold'],
    'font-size': 20,
    'color': (0, 0, 0),
    'bg-color': (255, 255, 255),
    'bg-color-hover': (238, 238, 238),
    'bg-color-active': (190, 190, 190),
    'width': 300,
    'height': 44,
    'margin': 8,
    'radius': 8
}

LEVEL_OPTIONS: list = []
for i in Level:
    LEVEL_OPTIONS.append({'key': i, 'label': f'{i.value} ({LEVEL_CONFIG[i]['rows']}x{LEVEL_CONFIG[i]['cols']}, {LEVEL_CONFIG[i]['mines']})'})

MODE_SELECT = {
    'bg-color': (171, 171, 171),
    'width': 400,
    'height': 300
}

MODE_BUTTON = {
    'font': FONT['helvetica-bold'],
    'font-size': 20,
    'color': (0, 0, 0),
    'bg-color': (255, 255, 255),
    'bg-color-hover': (238, 238, 238),
    'bg-color-active': (190, 190, 190),
    'width': 220,
    'height': 44,
    'margin': 8,
    'radius': 8
}

MODE_OPTIONS = [
    {'key': 'PLAYER', 'label': 'Player'},
    {'key': 'AI',      'label': 'AI'},
]