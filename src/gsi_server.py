"""
GSI сервер для получения данных от CS2
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading
from typing import Dict, Any, Optional
from src.utils import Logger

class GSIHandler(BaseHTTPRequestHandler):
    """
    Обработчик GSI запросов от CS2
    """
    
    # Общая переменная для хранения последних данных
    last_game_state: Dict[str, Any] = {}
    
    def do_POST(self):
        """
        Получает POST запрос от CS2
        """
        try:
            # Читаем данные
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            # Парсим JSON
            data = json.loads(body.decode('utf-8'))
            
            # Сохраняем данные
            GSIHandler.last_game_state = data
            
            # Отправляем OK ответ
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'OK')
            
            Logger.debug("GSI данные получены и обновлены")
            
        except Exception as e:
            Logger.error(f"Ошибка при обработке GSI: {e}")
            self.send_response(500)
            self.end_headers()
    
    def log_message(self, format, *args):
        """
        Подавляем стандартные логи HTTP сервера
        """
        pass

class GSIServer:
    """
    GSI сервер для получения данных от CS2
    """
    
    def __init__(self, host: str = "127.0.0.1", port: int = 3000):
        self.host = host
        self.port = port
        self.server: Optional[HTTPServer] = None
        self.thread: Optional[threading.Thread] = None
        self.running = False
    
    def start(self):
        """
        Запускает GSI сервер
        """
        try:
            self.server = HTTPServer((self.host, self.port), GSIHandler)
            self.running = True
            
            # Запускаем сервер в отдельном потоке
            self.thread = threading.Thread(target=self._run_server, daemon=True)
            self.thread.start()
            
            Logger.info(f"GSI сервер запущен на {self.host}:{self.port}")
            return True
        except Exception as e:
            Logger.error(f"Ошибка при запуске GSI сервера: {e}")
            return False
    
    def _run_server(self):
        """
        Запускает HTTP сервер в потоке
        """
        try:
            self.server.serve_forever()
        except Exception as e:
            Logger.error(f"GSI сервер ошибка: {e}")
    
    def stop(self):
        """
        Останавливает GSI сервер
        """
        if self.server:
            self.server.shutdown()
            self.running = False
            Logger.info("GSI сервер остановлен")
    
    def get_latest_state(self) -> Dict[str, Any]:
        """
        Возвращает последнее полученное состояние игры
        """
        return GSIHandler.last_game_state.copy()
    
    def is_connected(self) -> bool:
        """
        Проверяет, подключена ли игра
        """
        return len(GSIHandler.last_game_state) > 0
