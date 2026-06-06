"""
Утилиты для бота
"""
import math
from typing import Tuple

def distance(p1: Tuple[float, float, float], p2: Tuple[float, float, float]) -> float:
    """
    Вычисляет расстояние между двумя точками
    """
    return math.sqrt(
        (p1[0] - p2[0])**2 + 
        (p1[1] - p2[1])**2 + 
        (p1[2] - p2[2])**2
    )

def distance_2d(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """
    Вычисляет расстояние между двумя точками (2D)
    """
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def angle_between(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """
    Вычисляет угол между двумя точками (в градусах)
    """
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    angle = math.atan2(dy, dx)
    return math.degrees(angle)

def normalize_angle(angle: float) -> float:
    """
    Нормализует угол к диапазону (-180, 180)
    """
    while angle > 180:
        angle -= 360
    while angle < -180:
        angle += 360
    return angle

def point_in_circle(point: Tuple[float, float], center: Tuple[float, float], radius: float) -> bool:
    """
    Проверяет, находится ли точка внутри круга
    """
    return distance_2d(point, center) <= radius

def lerp(a: float, b: float, t: float) -> float:
    """
    Линейная интерполяция между a и b
    t должен быть в диапазоне [0, 1]
    """
    return a + (b - a) * max(0, min(1, t))

def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    Ограничивает значение в диапазоне [min_val, max_val]
    """
    return max(min_val, min(max_val, value))

def vector_normalize(v: Tuple[float, float, float]) -> Tuple[float, float, float]:
    """
    Нормализует вектор
    """
    length = math.sqrt(v[0]**2 + v[1]**2 + v[2]**2)
    if length == 0:
        return (0, 0, 0)
    return (v[0]/length, v[1]/length, v[2]/length)

def vector_scale(v: Tuple[float, float, float], scale: float) -> Tuple[float, float, float]:
    """
    Масштабирует вектор
    """
    return (v[0]*scale, v[1]*scale, v[2]*scale)

class Logger:
    """
    Простой логгер для отладки
    """
    DEBUG = True
    
    @staticmethod
    def log(message: str, level: str = "INFO"):
        if Logger.DEBUG:
            print(f"[{level}] {message}")
    
    @staticmethod
    def debug(message: str):
        Logger.log(message, "DEBUG")
    
    @staticmethod
    def info(message: str):
        Logger.log(message, "INFO")
    
    @staticmethod
    def warning(message: str):
        Logger.log(message, "WARNING")
    
    @staticmethod
    def error(message: str):
        Logger.log(message, "ERROR")
