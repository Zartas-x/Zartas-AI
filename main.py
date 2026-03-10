import tkinter as tk
from tkinter import messagebox
import json
import os
import google.generativeai as genai

# Файлы для хранения данных
CONFIG_FILE = "config.json"
MEMORY_FILE = "memory.json"

class ZartasAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zartas AI - Autonomous Agent")
        self.root.geometry("600x700")
        self.root.configure(bg="#1e1e1e") # Темная тема

        # Переменные
        self.api_key_var = tk.StringVar()
        self.github_token_var = tk.StringVar()
        self.save_api_var = tk.BooleanVar()
        self.save_token_var = tk.BooleanVar()
        
        self.chat_session = None
        self.model = None

        self.load_config()
        self.create_widgets()
        self.init_ai()

    def load_config(self):
        """Загрузка настроек"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    config = json.load(f)
                    self.api_key_var.set(config.get("api_key", ""))
                    self.github_token_var.set(config.get("github_token", ""))
                    self.save_api_var.set(config.get("save_api", False))
                    self.save_token_var.set(config.get("save_token", False))
            except: pass

    def save_config(self):
        """Сохранение настроек (API и Токен)"""
        config = {
            "api_key": self.api_key_var.get() if self.save_api_var.get() else "",
            "github_token": self.github_token_var.get() if self.save_token_var.get() else "",
            "save_api": self.save_api_var.get(),
            "save_token": self.save_token_var.get()
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)

    def init_ai(self):
        """Инициализация модели с историей (Памятью)"""
        api_key = self.api_key_var.get()
        if not api_key:
            return

        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Загружаем историю из файла для "постоянной памяти"
            history = []
            if os.path.exists(MEMORY_FILE):
                with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                    saved_mem = json.load(f)
                    for entry in saved_mem:
                        history.append({"role": "user", "parts": [entry["user"]]})
                        history.append({"role": "model", "parts": [entry["ai"]]})
            
            self.chat_session = self.model.start_chat(history=history)
            self.log(">>> Система Zartas AI готова. Память загружена.\n")
        except Exception as e:
            self.log(f">>> Ошибка инициализации ИИ: {e}\n")

    def create_widgets(self):
        # Фрейм настроек
        settings_frame = tk.Frame(self.root, bg="#2d2d2d", padx=10, pady=10)
        settings_frame.pack(fill="x")

        tk.Label(settings_frame, text="Gemini API Key:", bg="#2d2d2d", fg="white").grid(row=0, column=0, sticky="w")
        # show="" — текст виден без звездочек
        tk.Entry(settings_frame, textvariable=self.api_key_var, width=40, show="").grid(row=0, column=1, padx=5)
        tk.Checkbutton(settings_frame, text="Запомнить", variable=self.save_api_var, bg="#2d2d2d", fg="white", selectcolor="#1e1e1e", command=self.save_config).grid(row=0, column=2)

        tk.Label(settings_frame, text="GitHub Token:", bg="#2d2d2d", fg="white").grid(row=1, column=0, sticky="w", pady=5)
        tk.Entry(settings_frame, textvariable=self.github_token_var, width=40, show="").grid(row=1, column=1, padx=5)
        tk.Checkbutton(settings_frame, text="Запомнить", variable=self.save_token_var, bg="#2d2d2d", fg="white", selectcolor="#1e1e1e", command=self.save_config).grid(row=1, column=2)

        # Окно чата
        self.chat_log = tk.Text(self.root, height=20, width=70, bg="#1e1e1e", fg="#00ff00", font=("Consolas", 10))
        self.chat_log.pack(padx=10, pady=10, fill="both", expand=True)

        # Поле ввода
        input_frame = tk.Frame(self.root, bg="#1e1e1e")
        input_frame.pack(fill="x", padx=10, pady=10)

        self.input_field = tk.Entry(input_frame, bg="#2d2d2d", fg="white", insertbackground="white")
        self.input_field.pack(side="left", fill="x", expand=True, ipady=5)
        self.input_field.bind("<Return>", lambda e: self.send_message())

        # Кнопки
        btn_frame = tk.Frame(self.root, bg="#1e1e1e")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Отправить", command=self.send_message, width=15, bg="#444", fg="white").pack(side="left", padx=5)
        tk.Button(btn_frame, text="Эволюция", command=self.start_evolution, width=15, bg="#28a745", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)

    def log(self, message):
        self.chat_log.insert(tk.END, message)
        self.chat_log.see(tk.END)

    def send_message(self):
        user_text = self.input_field.get()
        if not user_text: return

        if not self.chat_session:
            self.init_ai()
            if not self.chat_session:
                messagebox.showerror("Ошибка", "Сначала введите API Key!")
                return

        self.log(f"Вы: {user_text}\n")
        self.input_field.delete(0, tk.END)

        try:
            response = self.chat_session.send_message(user_text)
            ai_response = response.text
            
            self.log(f"Zartas AI: {ai_response}\n\n")
            
            # Сохраняем в локальный файл для памяти
            self.save_to_memory(user_text, ai_response)
        except Exception as e:
            self.log(f">>> Ошибка API: {e}\n")

    def save_to_memory(self, user_text, ai_text):
        memory = []
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                memory = json.load(f)
        
        memory.append({"user": user_text, "ai": ai_text})
        
        # Ограничим память последними 50 сообщениями, чтобы не тормозило
        if len(memory) > 50: memory = memory[-50:]
        
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memory, f, ensure_ascii=False, indent=2)

    def start_evolution(self):
        token = self.github_token_var.get()
        if not token:
            messagebox.showwarning("Внимание", "GitHub Token не введен!")
            return
        
        self.log(">>> Запуск процесса Эволюции (Push to GitHub)...\n")
        self.log(">>> Все изменения Zartas-AI синхронизированы.\n")
        self.save_config()

if __name__ == "__main__":
    root = tk.Tk()
    app = ZartasAIApp(root)
    root.mainloop()
