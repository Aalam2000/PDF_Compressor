import os

# Определение структуры проекта
structure = [
    "src/__init__.py",  # Папка для исходного кода приложения
    "src/gui.py",  # Модуль графического интерфейса (Tkinter)
    "src/compressor.py",  # Модуль взаимодействия с Ghostscript
    "tests/__init__.py",  # Папка для тестов
    "requirements.txt",  # Список зависимостей
    "README.md",  # Описание проекта для Git
    ".gitignore"  # Исключения для Git
]

for path in structure:
    # Получаем имя родительской папки
    dirname = os.path.dirname(path)

    # Создаем папки, только если путь к папке не пустой
    if dirname:
        os.makedirs(dirname, exist_ok=True)

    # Создаем пустой файл
    with open(path, "w", encoding="utf-8") as f:
        if path == ".gitignore":
            f.write(".venv/\n.idea/\n__pycache__/\n*.pyc\n")
        elif path == "README.md":
            f.write("# PDF Compressor App\nПриложение для сжатия PDF через Ghostscript.\n")

print("Структура проекта успешно создана!")
