import sys
import os

# Добавляем корневую директорию проекта в пути поиска модулей,
# чтобы гарантировать корректный импорт папки src при любых условиях запуска
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.gui import run_app

if __name__ == "__main__":
    run_app()
