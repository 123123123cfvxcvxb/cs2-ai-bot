"""
Дерево решений для AI логики бота
Определяет, что должен делать бот в каждый момент времени
"""
from typing import Optional, Dict, Any
from enum import Enum
from config.bot_config import OBJECTIVE_PRIORITY, BOT_BEHAVIOR
from config.de_mirage_map import BOMB_SITES
from src.utils import Logger

class BotObjective(Enum):
    """Возможные цели бота"""
    STAY_ALIVE = "stay_alive"
    BUY_WEAPON = "buy_weapon"
    DEFEND_SITE = "defend_site"
    ATTACK_SITE = "attack_site"
    PEEK_ENEMY = "peek_enemy"
    ROTATE = "rotate"
    ECO = "eco"
    EXPLORE = "explore"

class DecisionTree:
    """
    Дерево решений для выбора действия бота
    """
    
    def __init__(self, game_state):
        self.game_state = game_state
        self.current_objective: Optional[BotObjective] = None
        self.target_site: Optional[str] = None  # "A" или "B"
        
        Logger.info("Decision Tree инициализировано")
    
    def make_decision(self) -> Dict[str, Any]:
        """
        Принимает решение на основе ��екущего состояния
        Возвращает словарь с командой для бота
        """
        
        # Приоритет 1: Остаться живым
        if self.game_state.is_low_health(30):
            return self._decide_retreat()
        
        # Приоритет 2: Купить оружие если нет денег
        if not self.game_state.weapons and self.game_state.can_buy():
            return self._decide_buy()
        
        # Приоритет 3: Встретить врага
        nearest_enemy = self.game_state.get_nearest_enemy()
        if nearest_enemy:
            return self._decide_engage_enemy(nearest_enemy)
        
        # Приоритет 4: Атаковать сайт
        if self.game_state.team_side == "T":
            return self._decide_attack_site()
        else:
            return self._decide_defend_site()
    
    def _decide_retreat(self) -> Dict[str, Any]:
        """
        Решение отступить и найти безопасную позицию
        """
        Logger.info("Решение: ОТСТУПЛЕНИЕ (низкое здоровье)")
        self.current_objective = BotObjective.STAY_ALIVE
        
        return {
            "action": "move",
            "target": "safe_position",
            "priority": OBJECTIVE_PRIORITY["stay_alive"],
            "description": "Ищу безопасную позицию"
        }
    
    def _decide_buy(self) -> Dict[str, Any]:
        """
        Решение купить оружие
        """
        Logger.info("Решение: ПОКУПКА ОРУЖИЯ")
        self.current_objective = BotObjective.BUY_WEAPON
        
        # Выбираем оружие в зависимости от денег
        if self.game_state.money >= 2400:
            weapon = "awp"
        elif self.game_state.money >= 1900:
            weapon = "ak47"
        elif self.game_state.money >= 1050:
            weapon = "famas"
        else:
            weapon = "pistol"
        
        return {
            "action": "buy",
            "weapon": weapon,
            "priority": OBJECTIVE_PRIORITY["buy_weapon"],
            "description": f"Покупаю {weapon}"
        }
    
    def _decide_engage_enemy(self, enemy: Dict[str, Any]) -> Dict[str, Any]:
        """
        Решение вступить в бой с врагом
        """
        Logger.info(f"Решение: БОЕВОЕ ВЗАИМОДЕЙСТВИЕ с врагом")
        self.current_objective = BotObjective.PEEK_ENEMY
        
        return {
            "action": "attack",
            "target": enemy,
            "priority": OBJECTIVE_PRIORITY["peek_enemy"],
            "description": "Вступаю в бой"
        }
    
    def _decide_attack_site(self) -> Dict[str, Any]:
        """
        Решение атаковать бомбосайт (для T)
        """
        Logger.info("Решение: АТАКА НА САЙТ")
        self.current_objective = BotObjective.ATTACK_SITE
        
        # Выбираем сайт в зависимости от стратегии
        if BOT_BEHAVIOR["aggressive"] > 0.5:
            site = "A"
        else:
            site = "B"
        
        self.target_site = site
        
        return {
            "action": "move",
            "target": f"{site}_site",
            "priority": OBJECTIVE_PRIORITY["attack_site"],
            "description": f"Атакую сайт {site}"
        }
    
    def _decide_defend_site(self) -> Dict[str, Any]:
        """
        Решение защищать сайт (для CT)
        """
        Logger.info("Решение: ЗАЩИТА САЙТА")
        self.current_objective = BotObjective.DEFEND_SITE
        
        # Выбираем сайт для защиты
        if not self.target_site:
            self.target_site = "A"
        
        return {
            "action": "move",
            "target": f"{self.target_site}_site",
            "priority": OBJECTIVE_PRIORITY["defend_site"],
            "description": f"Защищаю сайт {self.target_site}"
        }
    
    def _decide_rotate(self) -> Dict[str, Any]:
        """
        Решение ротироваться на другой сайт
        """
        Logger.info("Решение: РОТАЦИЯ")
        self.current_objective = BotObjective.ROTATE
        
        # Ротируемся на другой сайт
        new_site = "B" if self.target_site == "A" else "A"
        self.target_site = new_site
        
        return {
            "action": "move",
            "target": f"{new_site}_site",
            "priority": OBJECTIVE_PRIORITY["rotate"],
            "description": f"Ротирую на сайт {new_site}"
        }
    
    def evaluate_situation(self) -> str:
        """
        Оценивает тактическую ситуацию
        Возвращает текстовое описание
        """
        
        if self.game_state.health < 30:
            return "Критическое здоровье"
        elif self.game_state.money < 1000:
            return "Экономка"
        elif len(self.game_state.enemies) > 0:
            return "Враги видны"
        else:
            return "Позиция безопасна"
    
    def get_current_objective(self) -> Optional[BotObjective]:
        """
        Возвращает текущую цель
        """
        return self.current_objective
