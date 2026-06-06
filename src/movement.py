"""
Система движения для бота
Обработка движения, избегание препятствий
"""
import math
from typing import Tuple, Optional
from config.de_mirage_map import OBSTACLES
from config.bot_config import MOVEMENT_SPEED
from src.utils import distance, distance_2d, angle_between, Logger

class Movement:
    """
    Система движения и физики для бота
    """
    
    def __init__(self):
        self.position: Tuple[float, float, float] = (0, 0, 0)
        self.velocity: Tuple[float, float, float] = (0, 0, 0)
        self.target: Optional[Tuple[float, float, float]] = None
        self.speed = MOVEMENT_SPEED
        self.is_moving = False
        
        Logger.info("Система движения инициализирована")
    
    def set_position(self, position: Tuple[float, float, float]):
        """
        Устанавливает текущую позицию
        """
        self.position = position
    
    def set_target(self, target: Tuple[float, float, float]):
        """
        Устанавливает целевую позицию для движения
        """
        self.target = target
        self.is_moving = True
    
    def update(self, delta_time: float):
        """
        Обновляет состояние движения каждый фрейм
        delta_time - время между фреймами в секундах
        """
        if not self.is_moving or not self.target:
            self.velocity = (0, 0, 0)
            return
        
        # Вычисляем расстояние до цели
        dist = distance(self.position, self.target)
        
        # Если достигли цели
        if dist < 50:  # Толерантность 50 units
            self.is_moving = False
            self.velocity = (0, 0, 0)
            return
        
        # Вычисляем направление к цели
        direction = (
            (self.target[0] - self.position[0]) / dist,
            (self.target[1] - self.position[1]) / dist,
            (self.target[2] - self.position[2]) / dist
        )
        
        # Проверяем препятствия
        direction = self._avoid_obstacles(direction)
        
        # Устанавливаем скорость
        move_distance = self.speed * delta_time
        self.velocity = (
            direction[0] * move_distance,
            direction[1] * move_distance,
            direction[2] * move_distance
        )
        
        # Обновляем позицию
        self.position = (
            self.position[0] + self.velocity[0],
            self.position[1] + self.velocity[1],
            self.position[2] + self.velocity[2]
        )
    
    def _avoid_obstacles(self, direction: Tuple[float, float, float]) -> Tuple[float, float, float]:
        """
        Модифицирует направление движения для избегания препятствий
        """
        future_pos = (
            self.position[0] + direction[0] * 100,
            self.position[1] + direction[1] * 100,
            self.position[2] + direction[2] * 100
        )
        
        # Проверяем все препятствия
        for obstacle in OBSTACLES:
            if distance(future_pos, (obstacle["center"][0], obstacle["center"][1], obstacle["center"][2])) < obstacle["radius"]:
                # Вычисляем новое направление (от центра препятствия)
                dx = future_pos[0] - obstacle["center"][0]
                dy = future_pos[1] - obstacle["center"][1]
                
                length = math.sqrt(dx**2 + dy**2)
                if length > 0:
                    direction = (dx/length, dy/length, direction[2])
        
        return direction
    
    def get_position(self) -> Tuple[float, float, float]:
        """
        Возвращает текущую позицию
        """
        return self.position
    
    def get_distance_to_target(self) -> float:
        """
        Возвращает расстояние до цели
        """
        if not self.target:
            return float('inf')
        return distance(self.position, self.target)
    
    def stop(self):
        """
        Останавливает движение
        """
        self.is_moving = False
        self.velocity = (0, 0, 0)
    
    def get_direction_angle(self) -> float:
        """
        Возвращает угол направления движения в градусах
        """
        if not self.target:
            return 0
        
        return angle_between(
            (self.position[0], self.position[1]),
            (self.target[0], self.target[1])
        )
