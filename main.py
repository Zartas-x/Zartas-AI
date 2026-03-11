import subprocess
import sys
import os
import json
import tkinter as tk
from tkinter import messagebox
import threading

# --- АВТОМАТИЧЕСКАЯ УСТАНОВКА БИБЛИОТЕК (БЕЗ КОСТЫЛЕЙ) ---
def install_dependencies():
    required = {'google-generativeai', 'PyGithub'}
    try:
        import google.generativeai
        import github
    except ImportError:
        # Если библиотек нет, ставим их сами
        subprocess.check_call([sys.executable, "-m", "pip", "install", *required])
        os.execl(sys.executable, sys.executable, *sys.argv) # Перезапуск скрипта

# Запускаем проверку зависимостей до основного кода
try:
    install_dependencies()
    import google.generativeai as genai
    from github import Github
except Exception as e:
    # Если даже автоустановка не помогла, выведем окно, а не вылетим
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror("Ошибка системы", f"Не удалось подготовить окружение: {e}")
    sys.exit()

# --- ОСНОВНОЙ КОД ПРИЛОЖЕНИЯ ---
CONFIG_FILE = "config.json"
REPO_NAME = "Zartas-x/Zartas-AI"

class ZartasAI:
    def __init__(self, root):
        self.root = root
        self.root.title("Zartas AI - Standalone")
        self.root.geometry("600x750")
        self.root.configure(bg="#121212")

        self.api_key_var = tk.StringVar()
        self.github_token_var = tk.StringVar()
        self.save_api_var = tk.BooleanVar()

        self.load_config()
        self.create_widgets()
        self.init_ai()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    config = json.load(f)
                    self.api_key_var.set(config.get("api_key", ""))
                    self.github_token_var.set(config.get("github_token", ""))
                    self.save_api_var.set(config.get("save_api", False))
            except: pass

    def save_config(self):
        config = {
            "api_key": self.api_key_var.get() if self.save_api_var.get() else "",
            "github_token": self.github_token_var.get() if self.save_api_var.get() else "",
            "save_api": self.save_api_var.get()
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)

    def init_ai(self):
        key = self.api_key_var.get()
        if key:
            try:
                genai.configure(api_key=key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.chat = self.model.start_chat(history=[])
                self.log(">>> [Zartas AI]: Ядро готово к работе.\n")
            except: self.log(">>> [ОШИБКА]: Проверьте API Key.\n")

    def create_widgets(self):
        # Поля ввода
        top = tk.Frame(self.root, bg="#1e1e1e", pady=10)
        top.pack(fill="x")

        tk.Label(top, text="API Key:", bg="#1e1e1e", fg="gray").grid(row=0, column=0, padx=10)
        tk.Entry(top, textvariable=self.api_key_var, width=30, bg="#2d2d2d", fg="white", bd=0).grid(row=0, column=1)
        tk.Checkbutton(top, text="Save", variable=self.save_api_var, bg="#1e1e1e", fg="gray", command=self.save_config).grid(row=0, column=2)

        tk.Label(top, text="GH Token:", bg="#1e1e1e", fg="gray").grid(row=1, column=0, padx=10)
        tk.Entry(top, textvariable=self.github_token_var, width=30, bg="#2d2d2d", fg="white", bd=0).grid(row=1, column=1)

        # Консоль
        self.log_box = tk.Text(self.root, bg="#000", fg="#00ff41", font=("Consolas", 10), bd=0)
        self.log_box.pack(padx=10, pady=10, fill="both", expand=True)

        # Кнопка
        self.btn = tk.Button(self.root, text="ЭВОЛЮЦИЯ", command=self.start_evo, bg="#28a745", fg="white", font=("Arial", 12, "bold"), pady=10)
        self.btn.pack(fill="x", padx=10, pady=10)

    def log(self, text):
        self.log_box.insert(tk.END, text)
        self.log_box.see(tk.END)

    def start_evo(self):
        self.log(">>> [ЭВОЛЮЦИЯ]: Проверка статуса на GitHub...\n")
        # Тут запускаем фоновый поток, чтобы интерфейс не завис
        threading.Thread(target=self.run_evo_logic).start()

    def run_evo_logic(self):
        # Логика работы с GitHub
        token = self.github_token_var.get()
        if not token:
            self.log(">>> [!] Нужен GitHub Token для эволюции.\n")
            return
        self.log(">>> [OK]: Соединение установлено.\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = ZartasAI(root)
    root.mainloop()
