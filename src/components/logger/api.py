from .logger import Logger

def log(message : str) -> None:
    logger = Logger()
    logger.log(message)