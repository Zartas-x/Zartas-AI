import tkinter as tk
from tkinter import messagebox
import json
import os

# Используем только стандартные вещи, которые точно были в 19.1
class ZartasFinal:
    def __init__(self, root):
        self.root = root
        self.root.title("Zartas AI v19.1-MOD")
        self.root.geometry("500x600")
        
        # Переменные для хранения
        self.api_val = tk.StringVar()
        self.token_val = tk.StringVar()
        self.save_me = tk.BooleanVar()

        # Интерфейс один-в-один как в рабочей версии
        self.lbl1 = tk.Label(root, text="API KEY:")
        self.lbl1.pack(pady=5)
        
        self.api_ent = tk.Entry(root, textvariable=self.api_val, width=40)
        self.api_ent.pack()

        # Твоя галка
        self.cb = tk.Checkbutton(root, text="Запомнить меня", variable=self.save_me)
        self.cb.pack()

        self.lbl2 = tk.Label(root, text="GITHUB TOKEN:")
        self.lbl2.pack(pady=5)
        
        self.token_ent = tk.Entry(root, textvariable=self.token_val, width=40)
        self.token_ent.pack()

        self.log_box = tk.Text(root, height=15, width=55)
        self.log_box.pack(pady=10)

        self.btn = tk.Button(root, text="ЭВОЛЮЦИЯ", command=self.do_evo, bg="green", fg="white")
        self.btn.pack(pady=10)

        # Загрузка при старте
        self.load_from_file()

    def do_evo(self):
        # Логика сохранения прямо в кнопке
        if self.save_me.get():
            with open("z_config.json", "w") as f:
                json.dump({"a": self.api_val.get(), "t": self.token_val.get(), "s": True}, f)
        
        self.log_it("Запуск... Проверка токенов...")
        if not self.api_val.get():
            messagebox.showwarning("Zartas", "Пустой API!")

    def log_it(self, msg):
        self.log_box.insert(tk.END, msg + "\n")

    def load_from_file(self):
        if os.path.exists("z_config.json"):
            try:
                with open("z_config.json", "r") as f:
                    d = json.load(f)
                    self.api_val.set(d.get("a", ""))
                    self.token_val.set(d.get("t", ""))
                    self.save_me.set(d.get("s", False))
                self.log_it("Данные подтянуты из памяти.")
            except:
                pass

if __name__ == "__main__":
    root = tk.Tk()
    app = ZartasFinal(root)
    root.mainloop()
