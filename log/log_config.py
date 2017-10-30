import logging
import logging.handlers


# Создаем логгеры все в одном месте, потом будем их получить по имени
# Клиентский и серверный логгеры
def setup_logger(logger_name, log_file, level=logging.WARNING):
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    if logger_name.startswith('server'):
        file_handler = logging.handlers.TimedRotatingFileHandler(log_file, encoding='utf-8', when='d')
    else:
        file_handler = logging.FileHandler(log_file, encoding='utf-8', mode='w')
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
