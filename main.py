import tkinter as tk
from tkinter import messagebox
import json
import os

# Файлы настроек
CONFIG_FILE = "zartas_config.json"
MEMORY_FILE = "zartas_memory.json"

class ZartasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zartas AI v20.0 - Stable")
        self.root.geometry("550x650")
        self.root.configure(bg="#1a1a1a")

        # Переменные (строки для ввода)
        self.api_key_var = tk.StringVar()
        self.gh_token_var = tk.StringVar()
        self.save_api_var = tk.BooleanVar()

        self.create_ui()
        self.load_settings()

    def create_ui(self):
        # Поле для API (без звездочек, как ты просил)
        tk.Label(self.root, text="GEMINI API KEY:", fg="white", bg="#1a1a1a").pack(pady=(10, 0))
        self.api_entry = tk.Entry(self.root, textvariable=self.api_key_var, width=50, bg="#333", fg="white", insertbackground="white")
        self.api_entry.pack(pady=5)
        
        # Галка сохранения
        self.save_cb = tk.Checkbutton(self.root, text="Сохранять API и Токен после выхода", 
                                      variable=self.save_api_var, bg="#1a1a1a", fg="gray", 
                                      selectcolor="#333", activebackground="#1a1a1a", command=self.save_settings)
        self.save_cb.pack()

        # Поле для GitHub Token
        tk.Label(self.root, text="GITHUB TOKEN:", fg="white", bg="#1a1a1a").pack(pady=(10, 0))
        self.gh_entry = tk.Entry(self.root, textvariable=self.gh_token_var, width=50, bg="#333", fg="white", insertbackground="white")
        self.gh_entry.pack(pady=5)

        # Консоль / Чат
        tk.Label(self.root, text="КОНСОЛЬ ZARTAS AI:", fg="#00ff00", bg="#1a1a1a").pack(pady=(10, 0))
        self.log_box = tk.Text(self.root, height=15, width=60, bg="black", fg="#00ff00", font=("Consolas", 10))
        self.log_box.pack(padx=10, pady=5)

        # Кнопка Эволюция
        self.evo_btn = tk.Button(self.root, text="ЭВОЛЮЦИЯ", width=25, height=2, 
                                 bg="#28a745", fg="white", font=("Arial", 12, "bold"),
                                 command=self.run_evolution)
        self.evo_btn.pack(pady=20)

    def log(self, text):
        self.log_box.insert(tk.END, f">>> {text}\n")
        self.log_box.see(tk.END)

    def save_settings(self):
        """Метод сохранения данных, если стоит галка"""
        if self.save_api_var.get():
            data = {
                "api": self.api_key_var.get(),
                "token": self.gh_token_var.get(),
                "save": True
            }
            with open(CONFIG_FILE, "w") as f:
                json.dump(data, f)
            self.log("Настройки сохранены.")
        else:
            if os.path.exists(CONFIG_FILE):
                os.remove(CONFIG_FILE)
            self.log("Автосохранение отключено.")

    def load_settings(self):
        """Загрузка при старте"""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                self.api_key_var.set(data.get("api", ""))
                self.gh_token_var.set(data.get("token", ""))
                self.save_api_var.set(data.get("save", False))
            self.log("Данные успешно подгружены.")

    def run_evolution(self):
        # Здесь будет логика работы с ИИ и Гитхабом
        self.log("Запуск процесса эволюции...")
        self.log("Проверка API...")
        if not self.api_key_var.get():
            messagebox.showwarning("Внимание", "Введите API Key!")
        else:
            self.log("Связь с сервером установлена (Имитация).")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = ZartasApp(root)
        root.mainloop()
    except Exception as e:
        # Если вылетит, создаст файл с ошибкой
        with open("error_report.txt", "w") as f:
            f.write(str(e))
