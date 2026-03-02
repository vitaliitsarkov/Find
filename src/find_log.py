import os
from datetime import datetime


class ErrorLogger:
    def __init__(self, log_filename="find_error_log.txt"):
        # Получаем директорию пользователя
        home_dir = os.path.expanduser("~")
        self.log_file_path = os.path.join(home_dir, log_filename)

    def log_error(self, exception: Exception):
        """Записывает текст ошибки в лог-файл с временной меткой"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_message = f"[{timestamp}] {str(exception)}\n"

        with open(self.log_file_path, "a", encoding="utf-8") as log_file:
            log_file.write(error_message)
