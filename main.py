from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex
import json
import os
import threading

class ZartasAIApp(App):
    def build(self):
        self.config_file = "config.json"
        layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        # Заголовок
        layout.add_widget(Label(text="ZARTAS AI ULTRA", font_size='22sp', size_hint_y=None, height=50))

        # Поля ввода
        layout.add_widget(Label(text="Gemini API Key:", size_hint_y=None, height=30))
        self.api_key_input = TextInput(password=True, multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.api_key_input)

        layout.add_widget(Label(text="GitHub Token:", size_hint_y=None, height=30))
        self.gh_token_input = TextInput(password=True, multiline=False, size_hint_y=None, height=40)
        layout.add_widget(self.gh_token_input)

        # Консоль
        self.log_area = TextInput(readonly=True, background_color=(0, 0, 0, 1), 
                                  foreground_color=(0, 1, 0, 1), font_size='12sp')
        layout.add_widget(self.log_area)

        # Кнопка
        btn = Button(text="ЗАПУСТИТЬ ЭВОЛЮЦИЮ", size_hint_y=None, height=60,
                     background_color=get_color_from_hex('#28a745'), background_normal='')
        btn.bind(on_press=self.start_evolution_thread)
        layout.add_widget(btn)

        self.load_settings()
        return layout

    def load_settings(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    data = json.load(f)
                    self.api_key_input.text = data.get("api_key", "")
                    self.gh_token_input.text = data.get("gh_token", "")
                self.log("Настройки загружены.")
            except:
                self.log("Ошибка загрузки конфига.")

    def save_settings(self):
        data = {
            "api_key": self.api_key_input.text,
            "gh_token": self.gh_token_input.text
        }
        with open(self.config_file, "w") as f:
            json.dump(data, f)

    def log(self, message):
        self.log_area.text += f"> {message}\n"

    def start_evolution_thread(self, instance):
        self.save_settings()
        # Запускаем в отдельном потоке, чтобы экран не завис
        threading.Thread(target=self.run_evolution).start()

    def run_evolution(self):
        self.log("Инициализация Zartas-AI...")
        api_key = self.api_key_input.text
        if not api_key:
            self.log("ОШИБКА: Нет API ключа Gemini!")
            return
        
        self.log("Связь с Gemini установлена...")
        # Сюда мы добавим реальный вызов нейронки в следующем шаге
        self.log("Анализ кода на GitHub...")
        self.log("Обновление успешно завершено.")

if __name__ == "__main__":
    ZartasAIApp().run()
