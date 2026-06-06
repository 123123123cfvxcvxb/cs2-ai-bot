"""
Конфигурация бота CS2
"""

# Уровень сложности (1-5)
DIFFICULTY = 3

# Скорость движения бота (units/sec)
MOVEMENT_SPEED = 250

# Расстояние, на котором бот замечает врага (units)
ENEMY_DETECTION_RANGE = 1500

# Расстояние для атаки (units)
ATTACK_RANGE = 400

# Поведение бота
BOT_BEHAVIOR = {
    "aggressive": 0.6,      # Агрессивность (0-1)
    "caution": 0.4,         # Осторожность (0-1)
    "economy": True,        # Экономный режим
    "team_play": True       # Командная игра
}

# Интервал обновления AI (секунды)
AI_UPDATE_INTERVAL = 0.1

# GSI (Game State Integration) сервер
GSI_HOST = "127.0.0.1"
GSI_PORT = 3000

# Приоритет целей
OBJECTIVE_PRIORITY = {
    "stay_alive": 100,
    "buy_weapon": 90,
    "defend_site": 80,
    "attack_site": 75,
    "peek_enemy": 60,
    "rotate": 50,
    "eco": 40
}
