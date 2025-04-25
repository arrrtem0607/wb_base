import logging
import sys

logger = logging.getLogger("supplier_app")
logger.setLevel(logging.INFO)

# Консольный вывод
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s", "%Y-%m-%d %H:%M:%S"
))

# Очистим, чтобы не было дублирования
logger.handlers.clear()
logger.addHandler(console_handler)
