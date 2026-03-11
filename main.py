import tkinter as tk
from tkinter import messagebox
import json
import os
import time
import threading
import google.generativeai as genai
from github import Github

# --- КОНФИГУРАЦИЯ ---
CONFIG_FILE = "config.json"
MEMORY_FILE = "memory.json"
REPO_NAME = "Zartas-x/Zartas-AI"

# Код для GitHub Actions, который приложение создаст само
GITHUB_WORKFLOW_CODE = """
name: Zartas AI Auto-Build
on:
  push:
    branches: [ main ]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install google-generativeai PyGithub
      - name: Check Syntax
        run: python -m py_compile main.py
"""

class ZartasAIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zartas AI - One File System")
        self.root.geometry("700x850")
        self.root.configure(bg="#121212")

        self.api_key_var = tk.StringVar()
        self.github_token_var = tk.StringVar()
        self.save_api_var = tk.BooleanVar()
        self.save_token_var = tk.BooleanVar()
        
        self.chat_session = None
        self.setup_local_env() # Создаем нужные файлы при старте
        self.load_config()
        self.create_widgets()
        self.init_ai()

    def setup_local_env(self):
        """Создает структуру папок для GitHub прямо из кода"""
        if not os.path.exists(".github/workflows"):
            os.makedirs(".github/workflows", exist_ok=True)
            with open(".github/workflows/main.yml", "w") as f:
                f.write(GITHUB_WORKFLOW_CODE.strip())
        
        if not os.path.exists("requirements.txt"):
            with open("requirements.txt", "w") as f:
                f.write("google-generativeai\nPyGithub\n")

    def load_config(self):
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
        config = {
            "api_key": self.api_key_var.get() if self.save_api_var.get() else "",
            "github_token": self.github_token_var.get() if self.save_token_var.get() else "",
            "save_api": self.save_api_var.get(),
            "save_token": self.save_token_var.get()
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)

    def init_ai(self):
        api_key = self.api_key_var.get()
        if api_key:
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.chat_session = self.model.start_chat(history=[])
                self.log(">>> [SYSTEM]: ИИ подключен к ядру.\n")
            except: self.log(">>> [ERROR]: Ошибка ключа API.\n")

    def create_widgets(self):
        # Панель управления
        ctrl_frame = tk.Frame(self.root, bg="#1e1e1e", pady=15)
        ctrl_frame.pack(fill="x")

        tk.Label(ctrl_frame, text="Gemini API Key:", bg="#1e1e1e", fg="#888").grid(row=0, column=0, padx=10, sticky="w")
        tk.Entry(ctrl_frame, textvariable=self.api_key_var, width=35, bg="#2d2d2d", fg="white", insertbackground="white", bd=0).grid(row=0, column=1)
        tk.Checkbutton(ctrl_frame, text="Save", variable=self.save_api_var, bg="#1e1e1e", fg="gray", command=self.save_config).grid(row=0, column=2)

        tk.Label(ctrl_frame, text="GitHub Token:", bg="#1e1e1e", fg="#888").grid(row=1, column=0, padx=10, sticky="w")
        tk.Entry(ctrl_frame, textvariable=self.github_token_var, width=35, bg="#2d2d2d", fg="white", insertbackground="white", bd=0).grid(row=1, column=1)
        tk.Checkbutton(ctrl_frame, text="Save", variable=self.save_token_var, bg="#1e1e1e", fg="gray", command=self.save_config).grid(row=1, column=2)

        # Индикатор Actions
        self.status_canvas = tk.Canvas(ctrl_frame, width=30, height=30, bg="#1e1e1e", highlightthickness=0)
        self.status_canvas.grid(row=0, column=3, rowspan=2, padx=20)
        self.status_light = self.status_canvas.create_oval(5, 5, 25, 25, fill="gray")
        self.status_label = tk.Label(ctrl_frame, text="Actions: Idle", bg="#1e1e1e", fg="white", font=("Consolas", 8))
        self.status_label.grid(row=2, column=3)

        # Консоль
        self.chat_log = tk.Text(self.root, bg="#000", fg="#00ff41", font=("Consolas", 10), bd=0, padx=10, pady=10)
        self.chat_log.pack(fill="both", expand=True, padx=10, pady=5)

        # Кнопка эволюции
        self.evolve_btn = tk.Button(self.root, text="ЗАПУСТИТЬ ЭВОЛЮЦИЮ", command=self.start_evolution, 
                                   bg="#28a745", fg="white", font=("Arial", 12, "bold"), pady=10)
        self.evolve_btn.pack(fill="x", padx=10, pady=10)

    def log(self, text):
        self.chat_log.insert(tk.END, text)
        self.chat_log.see(tk.END)

    def update_status(self, status):
        colors = {"success": "#28a745", "in_progress": "#ffc107", "failure": "#dc3545", "idle": "gray"}
        self.status_canvas.itemconfig(self.status_light, fill=colors.get(status, "gray"))
        self.status_label.config(text=f"Actions: {status}")

    def start_evolution(self):
        self.save_config()
        threading.Thread(target=self.evolution_loop).start()

    def evolution_loop(self):
        token = self.github_token_var.get()
        if not token: 
            self.log(">>> [!] Введите GitHub Token!\n")
            return

        try:
            g = Github(token)
            repo = g.get_repo(REPO_NAME)
            self.log(f">>> [EVO]: Начало цикла сборки {REPO_NAME}...\n")
            self.update_status("in_progress")

            # Мониторим GitHub Actions
            while True:
                runs = repo.get_workflow_runs()
                if runs.totalCount > 0:
                    last_run = runs[0]
                    if last_run.status == "completed":
                        if last_run.conclusion == "success":
                            self.update_status("success")
                            self.log(">>> [OK]: Сборка завершена успешно!\n")
                            break
                        else:
                            self.update_status("failure")
                            self.log(">>> [FAIL]: Сбой сборки. Запрос к ИИ на исправление...\n")
                            self.handle_auto_fix(repo)
                            break
                time.sleep(15)
        except Exception as e:
            self.log(f">>> [ERROR]: {e}\n")

    def handle_auto_fix(self, repo):
        # Имитируем получение ошибки для Gemini
        prompt = "Мой код в main.py вызвал ошибку при сборке на GitHub. Проанализируй код и исправь возможные ошибки синтаксиса или логики."
        try:
            response = self.chat_session.send_message(prompt)
            new_code = response.text
            
            # Чистим ответ от Markdown (если Gemini добавил ```python)
            if "```python" in new_code:
                new_code = new_code.split("```python")[1].split("```")[0].strip()

            contents = repo.get_contents("main.py")
            repo.update_file(contents.path, "Zartas AI: Auto-Correction", new_code, contents.sha)
            self.log(">>> [REPAIR]: Исправленный код отправлен в репозиторий. Перезапуск сборки...\n")
            self.evolution_loop()
        except Exception as e:
            self.log(f">>> [CRITICAL]: Не удалось исправить автоматически: {e}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = ZartasAIApp(root)
    root.mainloop()
