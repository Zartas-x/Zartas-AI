import tkinter as tk
from tkinter import messagebox
import json
import os

# Файлы для хранения данных
SETTING_FILE = "zartas_settings.json"

class ZartasAI:
    def __init__(self, root):
        self.root = root
        self.root.title("Zartas AI v21.0")
        self.root.geometry("500x600")
        self.root.configure(bg="#1c1c1c")

        # 1. ПЕРЕМЕННЫЕ
        self.api_key_var = tk.StringVar()
        self.gh_token_var = tk.StringVar()
        self.save_api_var = tk.BooleanVar()

        # 2. ИНТЕРФЕЙС (Строго по структуре 19.1)
        self.setup_ui()
        
        # 3. ЗАГРУЗКА ДАННЫХ
        self.load_all_data()

    def setup_ui(self):
        # Поле Gemini API (Без звездочек)
        tk.Label(self.root, text="GEMINI API KEY:", fg="#00ff00", bg="#1c1c1c", font=("Arial", 10)).pack(pady=(20, 0))
        self.entry_api = tk.Entry(self.root, textvariable=self.api_key_var, width=45, bg="#333", fg="white", bd=0)
        self.entry_api.pack(pady=5)

        # Галка сохранения
        self.check_save = tk.Checkbutton(self.root, text="Сохранять API и Token", variable=self.save_api_var,
                                         bg="#1c1c1c", fg="gray", selectcolor="#1c1c1c", 
                                         activebackground="#1c1c1c", command=self.save_all_data)
        self.check_save.pack()

        # Поле GitHub Token
        tk.Label(self.root, text="GITHUB TOKEN:", fg="#00ff00", bg="#1c1c1c", font=("Arial", 10)).pack(pady=(15, 0))
        self.entry_gh = tk.Entry(self.root, textvariable=self.gh_token_var, width=45, bg="#333", fg="white", bd=0)
        self.entry_gh.pack(pady=5)

        # Консоль логов
        tk.Label(self.root, text="SYSTEM LOG:", fg="white", bg="#1c1c1c").pack(pady=(20, 0))
        self.txt_log = tk.Text(self.root, height=12, width=55, bg="black", fg="#00ff00", font=("Consolas", 9))
        self.txt_log.pack(padx=10, pady=5)

        # Кнопка Эволюция
        self.btn_evo = tk.Button(self.root, text="ЭВОЛЮЦИЯ", bg="#28a745", fg="white", 
                                 font=("Arial", 12, "bold"), width=20, height=2, command=self.start_evo)
        self.btn_evo.pack(pady=20)

    def log(self, message):
        self.txt_log.insert(tk.END, f">> {message}\n")
        self.txt_log.see(tk.END)

    def save_all_data(self):
        """Сохранение в файл при нажатии галки"""
        if self.save_api_var.get():
            data = {
                "api": self.api_key_var.get(),
                "token": self.gh_token_var.get(),
                "is_saved": True
            }
            with open(SETTING_FILE, "w") as f:
                json.dump(data, f)
            self.log("Данные зафиксированы.")
        else:
            if os.path.exists(SETTING_FILE):
                os.remove(SETTING_FILE)
            self.log("Автосохранение отключено.")

    def load_all_data(self):
        """Загрузка при старте приложения"""
        if os.path.exists(SETTING_FILE):
            try:
                with open(SETTING_FILE, "r") as f:
                    data = json.load(f)
                    self.api_key_var.set(data.get("api", ""))
                    self.gh_token_var.set(data.get("token", ""))
                    self.save_api_var.set(data.get("is_saved", False))
                self.log("Память загружена успешно.")
            except:
                self.log("Ошибка чтения файла настроек.")

    def start_evo(self):
        self.log("Запуск протокола Эволюции...")
        # Проверка данных перед работой
        api = self.api_key_var.get()
        token = self.gh_token_var.get()
        
        if not api or not token:
            messagebox.showwarning("Внимание", "Заполните API и Token!")
            return
            
        self.log("Анализ GitHub репозитория Zartas-AI...")
        self.log("Статус: Ожидание сборки (Actions)...")
        # Здесь мы позже добавим динамику, но пока - стабильный запуск
        self.save_all_data()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = ZartasAI(root)
        root.mainloop()
    except Exception as e:
        with open("crash_report.txt", "w") as f:
            f.write(str(e))
