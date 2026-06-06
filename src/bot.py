"""
Основной класс бота CS2
Интегрирует все компоненты вместе
"""
import time
from typing import Dict, Any, Optional
from config.bot_config import AI_UPDATE_INTERVAL
from src.utils import Logger
from src.navigation import Navigation
from src.movement import Movement
from src.game_state import GameState
from src.decision_tree import DecisionTree

class CS2Bot:
    """
    Главный класс автономного бота для CS2
    """
    
    def __init__(self):
        self.name = "AutoBot_AI"
        self.running = False
        self.last_update_time = time.time()
        
        # Компоненты бота
        self.game_state = GameState()
        self.navigation = Navigation()
        self.movement = Movement()
        self.decision_tree = DecisionTree(self.game_state)
        
        # Состояние
        self.current_decision: Optional[Dict[str, Any]] = None
        self.current_target: Optional[str] = None
        
        Logger.info(f"Бот {self.name} создан")
    
    def initialize(self, start_position: tuple = (-2276, -1100, -128)):
        """
        Инициализирует бота на карте
        """
        self.movement.set_position(start_position)
        self.game_state.position = start_position
        Logger.info(f"Бот инициализирован на позиции {start_position}")
    
    def start(self):
        """
        Запускает осн��вной цикл бота
        """
        self.running = True
        Logger.info("Бот запущен")
    
    def stop(self):
        """
        Останавливает бота
        """
        self.running = False
        self.movement.stop()
        Logger.info("Бот остановлен")
    
    def update(self):
        """
        Основной цикл обновления бота
        """
        if not self.running:
            return
        
        current_time = time.time()
        delta_time = current_time - self.last_update_time
        self.last_update_time = current_time
        
        # Обновляем физику движения
        self.movement.update(delta_time)
        self.game_state.position = self.movement.get_position()
        
        # Проверяем, должны ли мы принять новое решение
        if delta_time >= AI_UPDATE_INTERVAL or not self.movement.is_moving:
            self._make_ai_decision()
        
        # Проверяем, достигли ли цели
        if self.movement.get_distance_to_target() < 100:
            self.navigation.advance_waypoint()
            next_waypoint = self.navigation.get_next_waypoint()
            
            if next_waypoint:
                self.movement.set_target(next_waypoint)
                Logger.info(f"Переходу к следующей точке: {next_waypoint}")
            else:
                self._make_ai_decision()
    
    def _make_ai_decision(self):
        """
        Принимает решение на основе AI
        """
        decision = self.decision_tree.make_decision()
        self.current_decision = decision
        
        # Выполняем действие
        if decision["action"] == "move":
            target_name = decision["target"]
            self._move_to_target(target_name)
        elif decision["action"] == "buy":
            self._execute_buy(decision["weapon"])
        elif decision["action"] == "attack":
            self._execute_attack(decision["target"])
    
    def _move_to_target(self, target_name: str):
        """
        Движется к целевой позиции
        """
        if self.navigation.set_target(target_name):
            next_waypoint = self.navigation.get_next_waypoint()
            if next_waypoint:
                self.movement.set_target(next_waypoint)
                Logger.info(f"Направляюсь к {target_name}")
    
    def _execute_buy(self, weapon: str):
        """
        Выполняет покупку оружия
        """
        Logger.info(f"Покупаю {weapon} за {self.game_state.money} денег")
        # В реальной игре здесь было бы взаимодействие с покупкой
        self.game_state.weapons.append(weapon)
    
    def _execute_attack(self, enemy: Dict[str, Any]):
        """
        Выполняет атаку на врага
        """
        Logger.info(f"Атакую врага!")
        # В реальной игре здесь было бы кликанье мышки
    
    def get_status(self) -> Dict[str, Any]:
        """
        Возвращает статус бота
        """
        return {
            "name": self.name,
            "running": self.running,
            "position": self.movement.get_position(),
            "health": self.game_state.health,
            "money": self.game_state.money,
            "current_objective": str(self.decision_tree.get_current_objective()),
            "current_path": self.navigation.get_current_path(),
            "is_moving": self.movement.is_moving,
            "situation": self.decision_tree.evaluate_situation()
        }
    
    def log_status(self):
        """
        Логирует статус бота
        """
        status = self.get_status()
        Logger.info(f"=== Статус бота ===")
        Logger.info(f"Позиция: {status['position']}")
        Logger.info(f"Здоровье: {status['health']}")
        Logger.info(f"Деньги: {status['money']}")
        Logger.info(f"Цель: {status['current_objective']}")
        Logger.info(f"Ситуация: {status['situation']}")
