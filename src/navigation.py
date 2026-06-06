"""
Система навигации для бота
Использует алгоритм поиска пути A* и знание карты
"""
import math
from typing import List, Tuple, Optional
from config.de_mirage_map import KEY_POSITIONS, NAVIGATION_GRAPH, DISTANCES
from src.utils import distance, Logger

class Node:
    """Узел для алгоритма A*"""
    def __init__(self, position: str, g: float = 0, h: float = 0):
        self.position = position
        self.g = g  # Стоимость от начала
        self.h = h  # Эвристика до конца
        self.f = g + h  # Общая стоимость
        self.parent = None
    
    def __lt__(self, other):
        return self.f < other.f

class Navigation:
    """
    Система навигации для передвижения по карте
    """
    
    def __init__(self):
        self.waypoints = KEY_POSITIONS
        self.graph = NAVIGATION_GRAPH
        self.current_path: List[str] = []
        self.current_waypoint_index = 0
        
        Logger.info("Система навигации инициализирована")
    
    def find_path(self, start: str, end: str) -> List[str]:
        """
        Находит путь от start до end используя A*
        Возвращает список ключевых позиций
        """
        if start == end:
            return [start]
        
        if start not in self.waypoints or end not in self.waypoints:
            Logger.warning(f"Неверная позиция: {start} или {end}")
            return [start, end]
        
        open_set = [Node(start, 0, self._heuristic(start, end))]
        closed_set = set()
        
        while open_set:
            # Берём узел с минимальной стоимостью
            current = min(open_set)
            open_set.remove(current)
            
            if current.position == end:
                # Восстанавливаем путь
                path = []
                node = current
                while node:
                    path.insert(0, node.position)
                    node = node.parent
                return path
            
            closed_set.add(current.position)
            
            # Проверяем соседей
            for neighbor in self.graph.get(current.position, []):
                if neighbor in closed_set:
                    continue
                
                # Вычисляем стоимость пути
                if (current.position, neighbor) in DISTANCES:
                    cost = DISTANCES[(current.position, neighbor)]
                else:
                    cost = distance(
                        self.waypoints[current.position],
                        self.waypoints[neighbor]
                    )
                
                g = current.g + cost
                h = self._heuristic(neighbor, end)
                
                # Проверяем, есть ли уже путь до этого соседа
                existing = None
                for node in open_set:
                    if node.position == neighbor:
                        existing = node
                        break
                
                if existing and g >= existing.g:
                    continue
                
                if existing:
                    open_set.remove(existing)
                
                new_node = Node(neighbor, g, h)
                new_node.parent = current
                open_set.append(new_node)
        
        Logger.warning(f"Путь от {start} до {end} не найден")
        return [start, end]
    
    def _heuristic(self, pos1: str, pos2: str) -> float:
        """
        Евристика для A* (расстояние между позициями)
        """
        if pos1 not in self.waypoints or pos2 not in self.waypoints:
            return 0
        return distance(self.waypoints[pos1], self.waypoints[pos2])
    
    def set_target(self, target_position: str) -> bool:
        """
        Устанавливает целевую позицию для навигации
        """
        if target_position not in self.waypoints:
            Logger.error(f"Целевая позиция {target_position} не найдена")
            return False
        
        # Находим текущую ближайшую позицию (по умолчанию первая)
        start = self.current_path[0] if self.current_path else "T_ramp"
        
        self.current_path = self.find_path(start, target_position)
        self.current_waypoint_index = 0
        
        Logger.info(f"Путь установлен: {' -> '.join(self.current_path)}")
        return True
    
    def get_next_waypoint(self) -> Optional[Tuple[float, float, float]]:
        """
        Возвращает следующую промежуточную позицию
        """
        if not self.current_path or self.current_waypoint_index >= len(self.current_path):
            return None
        
        waypoint_key = self.current_path[self.current_waypoint_index]
        return self.waypoints[waypoint_key]
    
    def advance_waypoint(self):
        """
        Переходит к следующей промежуточной позиции
        """
        self.current_waypoint_index += 1
    
    def has_reached_destination(self) -> bool:
        """
        Проверяет, достигли ли мы конца пути
        """
        return self.current_waypoint_index >= len(self.current_path)
    
    def get_current_path(self) -> List[str]:
        """
        Возвращает текущий путь
        """
        return self.current_path
    
    def get_position_by_name(self, name: str) -> Optional[Tuple[float, float, float]]:
        """
        Получает координаты позиции по названию
        """
        return self.waypoints.get(name)
