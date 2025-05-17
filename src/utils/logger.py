import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class SimpleLogger:
    def __init__(self, name: str, log_file: str, level: int):
        """A simple logger module

        Args:
            name (str): the logger name 
            log_file (str): the default log file path. Defaults to "app.log".
            level (int): the logger level. Defaults to 1, logging.INFO.
        """
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # The console logger handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # The file logger handler(Support rotating)
        file_handler = RotatingFileHandler(
            log_file, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger


def create_logger(logger_name, log_file="runtime/logs/app.log", level="INFO"):
    """A simple logger module

    Args:
        name (_type_): the logger name 
        log_file (str, optional): the default log file path. Defaults to "app.log".
        level (_type_, optional): the logger level. Defaults to logging.INFO.
    """
    if level == "DEBUG" or level == 0:
        log_level = logging.DEBUG
    elif level == "INFO" or level == 1:
        log_level = logging.INFO
    elif level == "WARNING" or level == 2:
        log_level = logging.WARNING
    elif level == "ERROR" or level == 3:
        log_level = logging.ERROR
    else:
        log_level = logging.ERROR

    logger = SimpleLogger(
        name=logger_name, log_file=log_file, level=log_level).get_logger()
    
    return logger


if __name__ == "__main__":
    logger_name = "Preprocess_Logger"
    log_file = "runtime/logs/preprocess.log"
    log = create_logger(logger_name=logger_name,
                        log_file=log_file, level=logging.INFO)

    log.debug("This is DEBUG level")
    log.info("This is INFO level")
    log.warning("This is WARNING level")
    log.error("This is ERROR level")
    log.critical("This is CRITICAL level")
