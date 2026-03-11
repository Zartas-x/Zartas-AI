import tkinter as tk
from tkinter import messagebox

class ZartasAI:
    def __init__(self, root):
        self.root = root
        self.root.title("Zartas AI v19.1")
        self.root.geometry("400x500")
        
        # Заголовок
        self.label = tk.Label(root, text="Zartas AI Console", font=("Arial", 14))
        self.label.pack(pady=10)
        
        # Поле вывода (Логи)
        self.log_area = tk.Text(root, height=15, width=45)
        self.log_area.pack(padx=10, pady=10)
        
        # Кнопка действия
        self.btn = tk.Button(root, text="ЭВОЛЮЦИЯ", command=self.evolve, bg="green", fg="white", width=20)
        self.btn.pack(pady=20)
        
    def log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        
    def evolve(self):
        self.log("Запуск процесса эволюции...")
        self.log("Проверка системы...")
        self.log("Готов к работе.")
        messagebox.showinfo("Zartas AI", "Версия 19.1 активна")

if __name__ == "__main__":
    root = tk.Tk()
    app = ZartasAI(root)
    root.mainloop()
