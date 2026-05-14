import glob
import os
import subprocess
import sys

from PIL import Image


def find_ghostscript() -> str:
    """
    Ищет исполняемый файл Ghostscript внутри упакованного .exe
    или в локальной папке разработки 'bin'.
    """
    # Если приложение запущено как скомпилированный .exe файл PyInstaller
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        bundle_dir = sys._MEIPASS
        embedded_path = os.path.join(bundle_dir, "bin", "gswin64c.exe")
        if os.path.exists(embedded_path):
            return embedded_path

    # Если приложение запущено из среды разработки (в PyCharm)
    local_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bin", "gswin64c.exe")
    if os.path.exists(local_path):
        return local_path

    # Резервный вариант поиска в системе
    standard_path_pattern = r"C:\Program Files\gs\gs*\bin\gswin64c.exe"
    found_paths = glob.glob(standard_path_pattern)
    if found_paths:
        return found_paths[-1]

    return "gswin64c.exe"


def compress_image(input_path: str, output_path: str):
    """Сжимает и оптимизирует графические файлы для веб-страниц."""
    with Image.open(input_path) as img:
        # Конвертируем в RGB (необходимо для сохранения PNG/WEBP с прозрачностью в JPEG)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        # Сохраняем с оптимизацией и качеством 80% (золотая середина для веб)
        img.save(output_path, "JPEG", optimize=True, quality=80)


def compress_file(input_path: str) -> str:
    """
    Определяет тип файла и запускает соответствующий метод сжатия.
    Новый файл сохраняется в той же папке с суффиксом '_compressed'.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Исходный файл не найден: {input_path}")

    # Формирование пути для выходного файла рядом с оригиналом
    file_dir, file_name = os.path.split(input_path)
    name_part, ext_part = os.path.splitext(file_name)
    ext_lower = ext_part.lower()

    # Для графических файлов принудительно меняем расширение на .jpg для веб-оптимизации
    if ext_lower in [".jpg", ".jpeg", ".png", ".webp"]:
        output_name = f"{name_part}_compressed.jpg"
    else:
        output_name = f"{name_part}_compressed{ext_part}"

    output_path = os.path.join(file_dir, output_name)

    # Логика сжатия в зависимости от расширения
    if ext_lower == ".pdf":
        gs_executable = find_ghostscript()
        args = [
            gs_executable, "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
            "-dPDFSETTINGS=/ebook", "-dNOPAUSE", "-dQUIET", "-dBATCH",
            f"-sOutputFile={output_path}", input_path
        ]
        try:
            result = subprocess.run(
                args, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            if result.returncode != 0:
                raise RuntimeError(f"Ошибка Ghostscript: {result.stderr}")
        except FileNotFoundError:
            raise RuntimeError("Ghostscript не найден в C:\\Program Files\\gs\\")

    elif ext_lower in [".jpg", ".jpeg", ".png", ".webp"]:
        try:
            compress_image(input_path, output_path)
        except Exception as e:
            raise RuntimeError(f"Ошибка сжатия изображения: {str(e)}")

    else:
        raise ValueError(f"Неподдерживаемый формат файла: {ext_part}")

    return output_path
