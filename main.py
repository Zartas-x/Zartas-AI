import tkinter as tk
from tkinter import messagebox
import os
import json

# Самый простой конфиг
CONFIG_FILE = "config_simple.json"

class TestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zartas AI - Emergency Test")
        self.root.geometry("400x300")
        
        # Переменные
        self.api_var = tk.StringVar()
        self.save_var = tk.BooleanVar()

        # Интерфейс
        tk.Label(root, text="Если ты это видишь - графика работает!").pack(pady=10)
        
        tk.Entry(root, textvariable=self.api_var, width=30).pack(pady=5)
        
        tk.Checkbutton(root, text="Сохранить API", variable=self.save_var).pack()
        
        tk.Button(root, text="ПРОВЕРИТЬ СОХРАНЕНИЕ", command=self.save_data).pack(pady=20)
        
        self.log_label = tk.Label(root, text="", fg="green")
        self.log_label.pack()

        self.load_data()

    def save_data(self):
        data = {"api": self.api_var.get(), "save": self.save_var.get()}
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f)
        self.log_label.config(text="Данные сохранены в файл!")

    def load_data(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                self.api_var.set(data.get("api", ""))
                self.save_var.set(data.get("save", False))

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = TestApp(root)
        root.mainloop()
    except Exception as e:
        # Если вылетит, эта часть попытается создать файл с текстом ошибки
        with open("CRASH_LOG.txt", "w") as f:
            f.write(str(e))
