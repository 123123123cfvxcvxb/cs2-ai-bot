"""
Получение и обработка состояния игры через Game State Integration (GSI)
"""
import json
from typing import Dict, Optional, Any
from config.bot_config import GSI_HOST, GSI_PORT
from src.utils import Logger

class GameState:
    """
    Хранит и управляет информацией о состоянии игры
    """
    
    def __init__(self):
        self.player_state: Dict[str, Any] = {}
        self.round_state: Dict[str, Any] = {}
        self.map_name: str = "de_mirage"
        self.team_side: str = "T"  # T или CT
        self.health: int = 100
        self.armor: int = 0
        self.money: int = 800
        self.weapons: list = []
        self.position: tuple = (0, 0, 0)
        self.enemies: list = []
        self.teammates: list = []
        
        Logger.info("Game State инициализирован")
    
    def update_from_gsi(self, data: Dict[str, Any]):
        """
        Обновляет состояние игры из данных GSI
        """
        try:
            # Информация о игроке
            if "player" in data:
                player = data["player"]
                self.player_state = player
                
                # Здоровье и броня
                if "state" in player:
                    state = player["state"]
                    self.health = state.get("health", 100)
                    self.armor = state.get("armor", 0)
                
                # Деньги
                if "match_stats" in player:
                    stats = player["match_stats"]
                    self.money = stats.get("money", 800)
                
                # Позиция (приблизительная)
                if "state" in player and "position" in player["state"]:
                    pos = player["state"]["position"]
                    self.position = tuple(pos)
            
            # Информация о раунде
            if "round" in data:
                self.round_state = data["round"]
            
            # Информация о карте
            if "map" in data:
                map_data = data["map"]
                self.map_name = map_data.get("name", "de_mirage")
                self.team_side = map_data.get("team_ct", {}).get("score", 0)  # Примерная логика
            
            return True
        except Exception as e:
            Logger.error(f"Ошибка при обновлении Game State: {e}")
            return False
    
    def is_alive(self) -> bool:
        """
        Проверяет, живого ли бот
        """
        return self.health > 0
    
    def is_low_health(self, threshold: int = 30) -> bool:
        """
        Проверяет, низкое ли здоровье
        """
        return self.health < threshold
    
    def has_money_for_weapon(self, weapon_cost: int) -> bool:
        """
        Проверяет, хватает ли денег на оружие
        """
        return self.money >= weapon_cost
    
    def can_buy(self) -> bool:
        """
        Проверяет, может ли бот покупать в текущем раунде
        """
        # Покупка возможна в начале раунда (первые 15 секунд)
        return True  # Упрощённо
    
    def get_health_percentage(self) -> float:
        """
        Возвращает процент здоровья
        """
        return (self.health / 100) * 100
    
    def set_enemies(self, enemies: list):
        """
        Устанавливает список врагов
        """
        self.enemies = enemies
    
    def set_teammates(self, teammates: list):
        """
        Устанавливает список товарищей по команде
        """
        self.teammates = teammates
    
    def get_nearest_enemy(self) -> Optional[Dict[str, Any]]:
        """
        Возвращает ближайшего врага
        """
        if not self.enemies:
            return None
        
        from src.utils import distance
        nearest = min(self.enemies, key=lambda e: distance(self.position, e.get("position", (0, 0, 0))))
        return nearest
    
    def get_round_info(self) -> Dict[str, Any]:
        """
        Возвращает информацию о текущем раунде
        """
        return self.round_state
    
    def log_state(self):
        """
        Логирует текущее состояние для отладки
        """
        Logger.debug(f"Health: {self.health}, Armor: {self.armor}, Money: {self.money}")
        Logger.debug(f"Position: {self.position}")
        Logger.debug(f"Enemies: {len(self.enemies)}, Teammates: {len(self.teammates)}")
