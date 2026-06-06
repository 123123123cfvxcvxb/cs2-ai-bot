"""
Данные карты de_mirage для навигации бота
Координаты в формате (x, y, z) - Source Engine координаты
"""

# Основные спавны
SPAWNS = {
    "T": {
        "spawn_1": (-2276, -1100, -128),
        "spawn_2": (-1844, -2400, -128),
        "spawn_3": (-1844, -800, -128),
    },
    "CT": {
        "spawn_1": (1566, 241, -128),
        "spawn_2": (1850, 600, -128),
        "spawn_3": (2090, 241, -128),
    }
}

# Бомбосайты
BOMB_SITES = {
    "A": {
        "position": (2800, 1600, -128),
        "plant_points": [
            (2900, 1700, -128),
            (2700, 1500, -128),
            (3000, 1600, -128)
        ]
    },
    "B": {
        "position": (-1400, -2300, -128),
        "plant_points": [
            (-1300, -2200, -128),
            (-1500, -2400, -128),
            (-1400, -2100, -128)
        ]
    }
}

# Ключевые позиции на карте
KEY_POSITIONS = {
    # Позиции T стороны
    "T_ramp": (-1850, -1600, -128),
    "T_lobby": (-2000, -1000, -128),
    "T_window": (-1200, -1300, -128),
    "T_mid": (400, 200, -128),
    
    # Позиции CT стороны
    "CT_main": (1600, 600, -128),
    "CT_connector": (400, 1200, -128),
    "CT_market": (1000, -800, -128),
    "CT_stairs": (1600, -600, -128),
    
    # Середина
    "mid_top": (400, 500, 100),
    "mid_main": (400, 200, -128),
    "mid_connector": (400, 1200, -128),
    
    # Позиции на А сайте
    "A_site": (2800, 1600, -128),
    "A_heaven": (2600, 1800, 200),
    "A_back": (3200, 1400, -128),
    
    # Позиции на B сайте
    "B_site": (-1400, -2300, -128),
    "B_lobby": (-1600, -2100, -128),
    "B_main": (-1200, -2400, -128),
}

# Пути навигации между точками (для алгоритма поиска пути)
NAVIGATION_GRAPH = {
    "T_ramp": ["T_lobby", "T_mid"],
    "T_lobby": ["T_ramp", "T_window"],
    "T_window": ["T_lobby", "T_mid"],
    "T_mid": ["T_ramp", "CT_connector", "mid_top"],
    
    "CT_main": ["CT_connector", "CT_stairs"],
    "CT_connector": ["T_mid", "CT_main", "mid_connector"],
    "CT_market": ["CT_stairs", "A_site"],
    "CT_stairs": ["CT_main", "CT_market"],
    
    "mid_top": ["T_mid", "A_heaven"],
    "mid_main": ["T_mid", "mid_connector"],
    "mid_connector": ["CT_connector", "mid_main"],
    
    "A_site": ["A_heaven", "A_back", "CT_market"],
    "A_heaven": ["A_site", "mid_top"],
    "A_back": ["A_site"],
    
    "B_site": ["B_lobby", "B_main"],
    "B_lobby": ["B_site", "B_main", "T_window"],
    "B_main": ["B_site", "B_lobby"],
}

# Препятствия на карте (приблизительные зоны, которые нужно избегать)
OBSTACLES = [
    # Стены и здания
    {"name": "tower", "center": (2500, 1200, 0), "radius": 400},
    {"name": "scaffolding", "center": (-800, -500, 0), "radius": 300},
    {"name": "building_ct", "center": (1800, 1000, 0), "radius": 500},
]

# Расстояния между ключевыми позициями (примерные)
DISTANCES = {
    ("T_ramp", "T_mid"): 800,
    ("T_mid", "CT_connector"): 400,
    ("CT_connector", "A_site"): 2200,
    ("CT_connector", "B_site"): 3500,
    ("T_mid", "B_site"): 2800,
    ("A_site", "B_site"): 4500,
}

# Видимость между позициями (есть ли прямая линия видимости)
LINE_OF_SIGHT = {
    "T_ramp": ["T_lobby", "T_window"],
    "T_mid": ["CT_connector", "mid_top"],
    "mid_top": ["A_heaven", "CT_connector"],
    "A_site": ["A_heaven", "CT_market"],
    "CT_main": ["CT_connector", "CT_stairs"],
}
