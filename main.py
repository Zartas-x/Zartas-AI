from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.utils import get_color_from_hex
import json, os, threading

class ZartasAIApp(App):
    def build(self):
        self.config_file = "config.json"
        # Основной фон — темно-серый, чтобы не было «черной дыры»
        root = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        # 1. Заголовок и Прогресс-бар (Индикатор эволюции)
        header = BoxLayout(orientation='vertical', size_hint_y=None, height=80)
        header.add_widget(Label(text="ZARTAS AI: EVOLUTION MODE", color=(0, 1, 0, 1), font_size='18sp'))
        self.progress = ProgressBar(max=100, value=0, size_hint_y=None, height=20)
        header.add_widget(self.progress)
        root.add_widget(header)

        # 2. Поля ключей (Компактно)
        keys_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        self.api_key = TextInput(hint_text="Gemini Key", password=True, multiline=False)
        self.gh_token = TextInput(hint_text="GH Token", password=True, multiline=False)
        keys_box.add_widget(self.api_key)
        keys_box.add_widget(self.gh_token)
        root.add_widget(keys_box)

        # 3. Чат / Консоль (С прокруткой)
        self.console = TextInput(readonly=True, background_color=(0.1, 0.1, 0.1, 1), 
                                foreground_color=(0, 1, 0.1, 1), text="[SYSTEM READY]\n")
        root.add_widget(self.console)

        # 4. Поле ввода для чата с Gemini
        chat_input_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=5)
        self.user_msg = TextInput(hint_text="Напиши Gemini...", multiline=False)
        send_btn = Button(text="SEND", size_hint_x=None, width=80, background_color=get_color_from_hex('#007bff'))
        send_btn.bind(on_press=self.send_to_ai)
        chat_input_box.add_widget(self.user_msg)
        chat_input_box.add_widget(send_btn)
        root.add_widget(chat_input_box)

        # 5. Кнопка Эволюции
        evo_btn = Button(text="START AUTONOMOUS EVOLUTION", size_hint_y=None, height=60,
                         background_color=get_color_from_hex('#28a745'), background_normal='')
        evo_btn.bind(on_press=self.start_evo)
        root.add_widget(evo_btn)

        self.load_settings()
        return root

    def log(self, text):
        self.console.text += f">> {text}\n"

    def load_settings(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                data = json.load(f)
                self.api_key.text = data.get("api", "")
                self.gh_token.text = data.get("gh", "")

    def save_settings(self):
        with open(self.config_file, "w") as f:
            json.dump({"api": self.api_key.text, "gh": self.gh_token.text}, f)

    def send_to_ai(self, instance):
        msg = self.user_msg.text
        if msg:
            self.log(f"YOU: {msg}")
            self.user_msg.text = ""
            # Тут будет вызов Gemini API
            self.log("AI: Думаю...")

    def start_evo(self, instance):
        self.save_settings()
        self.log("Запуск эволюции...")
        self.progress.value = 10
        threading.Thread(target=self.evo_process).start()

    def evo_process(self):
        # Имитация процесса для теста
        import time
        steps = ["Сканирование файлов...", "Связь с Gemini...", "Генерация фиксов...", "Пуш на GitHub..."]
        for i, step in enumerate(steps):
            time.sleep(1.5)
            self.log(step)
            self.progress.value += 25
        self.log("ЭВОЛЮЦИЯ ЗАВЕРШЕНА. Ждите новый билд.")
        self.progress.value = 100

if __name__ == "__main__":
    ZartasAIApp().run()
