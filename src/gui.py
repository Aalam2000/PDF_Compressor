import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from src.compressor import compress_file  # Изменили импорт функции


class PDFCompressorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Web & PDF Optimizer")  # Обновили заголовок окна
        self.root.geometry("550x150")
        self.root.resizable(False, False)

        self.file_path_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        file_frame = ttk.LabelFrame(self.root, text=" Выберите файл (PDF или Изображение) ", padding=10)
        file_frame.pack(fill="x", padx=15, pady=15)

        self.entry_path = tk.Entry(file_frame, textvariable=self.file_path_var, width=50, state="readonly")
        self.entry_path.pack(side="left", padx=(0, 10), expand=True, fill="x")

        self.btn_browse = tk.Button(file_frame, text="Обзор...", command=self.browse_file)
        self.btn_browse.pack(side="right")

        self.btn_optimize = tk.Button(
            self.root,
            text="Оптимизировать",
            command=self.optimize_file,
            font=("Arial", 10, "bold"),
            bg="#2ecc71",
            fg="white",
            height=2
        )
        self.btn_optimize.pack(fill="x", padx=15, pady=(0, 15))

    def browse_file(self):
        """Открывает диалоговое окно с поддержкой PDF и графических форматов"""
        file_selected = filedialog.askopenfilename(
            title="Выберите файл для оптимизации",
            filetypes=[
                ("Все поддерживаемые форматы", "*.pdf;*.jpg;*.jpeg;*.png;*.webp"),
                ("PDF документы", "*.pdf"),
                ("Изображения (JPG, PNG, WEBP)", "*.jpg;*.jpeg;*.png;*.webp")
            ]
        )
        if file_selected:
            self.file_path_var.set(os.path.normpath(file_selected))

    def optimize_file(self):
        input_path = self.file_path_var.get()

        if not input_path:
            messagebox.showwarning("Внимание", "Пожалуйста, выберите файл перед оптимизацией.")
            return

        self.btn_optimize.config(state="disabled", text="Оптимизация...")
        self.root.update_idletasks()

        try:
            # Вызов обновленной функции сжатия
            output_path = compress_file(input_path)

            messagebox.showinfo(
                "Успех",
                f"Файл успешно оптимизирован!\n\nСохранен рядом с оригиналом:\n{os.path.basename(output_path)}"
            )
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
        finally:
            self.btn_optimize.config(state="normal", text="Оптимизировать")


def run_app():
    root = tk.Tk()
    app = PDFCompressorApp(root)
    root.mainloop()
