import logging
import sys

def setup_logging():
    log_format = "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    formatter = logging.Formatter(log_format)
    
    # Корневой логгер
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    # 1. Обработчик для записи в файл в корне проекта
    file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 2. Обработчик для вывода в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Перехватываем логи самого uvicorn, чтобы запросы из /docs тоже шли в файл
    uvicorn_loggers = ["uvicorn", "uvicorn.error", "uvicorn.access"]
    for logger_name in uvicorn_loggers:
        uv_logger = logging.getLogger(logger_name)
        uv_logger.addHandler(file_handler)
        uv_logger.addHandler(console_handler)
        uv_logger.propagate = False

# Вызываем функцию сразу при импорте файла
setup_logging()