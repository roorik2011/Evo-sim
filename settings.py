# settings.py
WIDTH, HEIGHT = 1280, 720
TILE_SIZE = 10
UI_WIDTH = 250
FPS = 60

EXPERIMENTAL_MODE = True 

# Типы клеток
EMPTY, WALL, PLANT, MEAT, AGENT = 0, 1, 2, 3, 4
ACTIONS = ["MOVE", "TURN_L", "TURN_R", "EAT", "ATTACK", "REPRODUCE", "PHOTOSYNTHESIS", "EXPLODE", "NOTHING", "SHARE", "STEAL"]
VIEW_TYPES = {EMPTY: "Empty", PLANT: "Plant", MEAT: "Meat", AGENT: "Friend", "ENEMY": "Enemy"}

COLORS = {
    "BG": (255, 255, 255),
    EMPTY: (255, 255, 255),
    PLANT: (0, 100, 0),
    MEAT: (200, 0, 0),
    "AGENT": (255, 215, 0),
    "TEXT": (50, 50, 50),
    "UI": (220, 220, 220),
    "SELECT": (0, 0, 255),
    "GRAPH": (0, 150, 255),
    "OUTLINE": (0, 0, 0),
    "EXPLOSION": (255, 100, 0)
}

START_AGENTS = 80
START_PLANTS = 200 # Начальные кусты
PLANT_REPRODUCTION_CHANCE = 0.001 # Шанс растения размножиться за тик
RANDOM_PLANT_SPAWN_CHANCE = 0.01 # Шанс появления "семени" извне