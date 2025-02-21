import logging


# Currently not inheriting from logging.Logger.
# Idea: to add open telemetry in the future.
class Logger:
    logger: logging.Logger

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        self.sh = logging.StreamHandler()
        self.fh = logging.FileHandler(f"{name}.log")
        self.sh.setLevel(logging.INFO)
        self.fh.setLevel(logging.INFO)
        self.formatter = logging.Formatter(
            "%(levelname)s:%(name)s:%(message)s"
        )
        self.sh.setFormatter(self.formatter)
        self.fh.setFormatter(self.formatter)
        self.logger.addHandler(self.sh)
        self.logger.addHandler(self.fh)

    def info(self, message: str, *args, **kwargs):
        self.logger.info(message, *args, **kwargs)

    def debug(self, message: str, *args, **kwargs):
        self.logger.debug(message, args, **kwargs)

    def warning(self, message: str, *args, **kwargs):
        self.logger.warning(message, args, **kwargs)

    def error(self, message: str, *args, **kwargs):
        self.logger.error(message, args, **kwargs)

    def critical(self, message: str, *args, **kwargs):
        self.logger.critical(message, args, **kwargs)
