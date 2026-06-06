"""
Точка входа для CS2 AI Bot
"""
import time
import sys
from src.bot import CS2Bot
from src.utils import Logger

def main():
    """
    Главная функция
    """
    print("=" * 50)
    print("CS2 Autonomous AI Bot")
    print("de_mirage Edition")
    print("=" * 50)
    print()
    
    # Создаём бота
    bot = CS2Bot()
    
    # Инициализируем на спавне T
    bot.initialize((-2276, -1100, -128))
    
    # Запускаем бота
    bot.start()
    
    # Симуляция
    print("Симуляция запущена. Бот будет работать 30 секунд...")
    print()
    
    try:
        simulation_time = 0
        max_simulation_time = 30
        last_status_log = 0
        
        while simulation_time < max_simulation_time and bot.running:
            # Основной цикл обновления
            bot.update()
            
            # Логируем статус каждые 5 секунд
            if simulation_time - last_status_log >= 5:
                print()
                bot.log_status()
                print()
                last_status_log = simulation_time
            
            # Симулируем 60 FPS
            time.sleep(0.016)
            simulation_time += 0.016
        
        print()
        print("=" * 50)
        print("Симуляция завершена!")
        print("=" * 50)
        
        # Финальный статус
        bot.log_status()
        
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")
    finally:
        bot.stop()

if __name__ == "__main__":
    main()
