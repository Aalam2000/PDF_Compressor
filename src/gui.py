import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from src.compressor import compress_file

LANGUAGES = {
    "EN": {
        "title": "Web & PDF Optimizer",
        "formats": "Supported formats: PDF, JPG, JPEG, PNG, WEBP",
        "frame_label": " Select file (PDF or Image) ",
        "browse": "Browse...",
        "optimize": "Optimize",
        "optimizing": "Optimizing...",
        "warning_title": "Warning",
        "warning_msg": "Please select a file before optimizing.",
        "success_title": "Success",
        "success_msg": "File successfully optimized!\n\nSaved next to the original:\n",
        "error_title": "Error",
        "filetypes_all": "All supported formats",
        "filetypes_pdf": "PDF documents",
        "filetypes_img": "Images (JPG, PNG, WEBP)",
        "dialog_title": "Select file to optimize",
    },
    "RU": {
        "title": "Web & PDF Optimizer",
        "formats": "Поддерживаемые форматы: PDF, JPG, JPEG, PNG, WEBP",
        "frame_label": " Выберите файл (PDF или Изображение) ",
        "browse": "Обзор...",
        "optimize": "Оптимизировать",
        "optimizing": "Оптимизация...",
        "warning_title": "Внимание",
        "warning_msg": "Пожалуйста, выберите файл перед оптимизацией.",
        "success_title": "Успех",
        "success_msg": "Файл успешно оптимизирован!\n\nСохранен рядом с оригиналом:\n",
        "error_title": "Ошибка",
        "filetypes_all": "Все поддерживаемые форматы",
        "filetypes_pdf": "PDF документы",
        "filetypes_img": "Изображения (JPG, PNG, WEBP)",
        "dialog_title": "Выберите файл для оптимизации",
    },
    "AZ": {
        "title": "Web & PDF Optimizer",
        "formats": "Dəstəklənən formatlar: PDF, JPG, JPEG, PNG, WEBP",
        "frame_label": " Fayl seçin (PDF və ya Şəkil) ",
        "browse": "Axtar...",
        "optimize": "Optimallaşdır",
        "optimizing": "Optimallaşdırılır...",
        "warning_title": "Diqqət",
        "warning_msg": "Zəhmət olmasa optimallaşdırmadan əvvəl fayl seçin.",
        "success_title": "Uğur",
        "success_msg": "Fayl uğurla optimallaşdırıldı!\n\nOrijinalın yanında saxlanıldı:\n",
        "error_title": "Xəta",
        "filetypes_all": "Dəstəklənən bütün formatlar",
        "filetypes_pdf": "PDF sənədlər",
        "filetypes_img": "Şəkillər (JPG, PNG, WEBP)",
        "dialog_title": "Optimallaşdırmaq üçün fayl seçin",
    },
}


class PDFCompressorApp:
    def __init__(self, root):
        self.root = root
        self.current_lang = "EN"
        self.root.geometry("550x175")
        self.root.resizable(False, False)

        self.file_path_var = tk.StringVar()
        self.create_widgets()
        self.apply_lang()

    def create_widgets(self):
        # Панель языка
        lang_frame = tk.Frame(self.root)
        lang_frame.pack(anchor="ne", padx=15, pady=(5, 0))

        for lang in ["EN", "RU", "AZ"]:
            btn = tk.Button(
                lang_frame, text=lang, width=3,
                font=("Arial", 8),
                command=lambda l=lang: self.switch_lang(l)
            )
            btn.pack(side="left", padx=1)

        # Строка поддерживаемых форматов
        self.lbl_formats = tk.Label(self.root, font=("Arial", 8), fg="gray")
        self.lbl_formats.pack(anchor="w", padx=15)

        # Фрейм выбора файла
        self.file_frame = ttk.LabelFrame(self.root, padding=10)
        self.file_frame.pack(fill="x", padx=15, pady=5)

        self.entry_path = tk.Entry(self.file_frame, textvariable=self.file_path_var, width=50, state="readonly")
        self.entry_path.pack(side="left", padx=(0, 10), expand=True, fill="x")

        self.btn_browse = tk.Button(self.file_frame, command=self.browse_file)
        self.btn_browse.pack(side="right")

        self.btn_optimize = tk.Button(
            self.root,
            command=self.optimize_file,
            font=("Arial", 10, "bold"),
            bg="#2ecc71",
            fg="white",
            height=2
        )
        self.btn_optimize.pack(fill="x", padx=15, pady=(0, 10))

    def switch_lang(self, lang):
        self.current_lang = lang
        self.apply_lang()

    def apply_lang(self):
        t = LANGUAGES[self.current_lang]
        self.root.title(t["title"])
        self.lbl_formats.config(text=t["formats"])
        self.file_frame.config(text=t["frame_label"])
        self.btn_browse.config(text=t["browse"])
        self.btn_optimize.config(text=t["optimize"])

    def browse_file(self):
        t = LANGUAGES[self.current_lang]
        file_selected = filedialog.askopenfilename(
            title=t["dialog_title"],
            filetypes=[
                (t["filetypes_all"], "*.pdf;*.jpg;*.jpeg;*.png;*.webp"),
                (t["filetypes_pdf"], "*.pdf"),
                (t["filetypes_img"], "*.jpg;*.jpeg;*.png;*.webp")
            ]
        )
        if file_selected:
            self.file_path_var.set(os.path.normpath(file_selected))

    def optimize_file(self):
        t = LANGUAGES[self.current_lang]
        input_path = self.file_path_var.get()

        if not input_path:
            messagebox.showwarning(t["warning_title"], t["warning_msg"])
            return

        self.btn_optimize.config(state="disabled", text=t["optimizing"])
        self.root.update_idletasks()

        try:
            output_path = compress_file(input_path)
            messagebox.showinfo(t["success_title"], t["success_msg"] + os.path.basename(output_path))
        except Exception as e:
            messagebox.showerror(t["error_title"], str(e))
        finally:
            self.btn_optimize.config(state="normal", text=t["optimize"])


def run_app():
    root = tk.Tk()
    app = PDFCompressorApp(root)
    root.mainloop()