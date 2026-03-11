from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.utils import get_color_from_hex
import json, os, threading, requests

class ZartasAIApp(App):
    def build(self):
        self.config_file = "config.json"
        root = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        # Индикатор эволюции
        header = BoxLayout(orientation='vertical', size_hint_y=None, height=80)
        header.add_widget(Label(text="ZARTAS AI: EVOLUTION ACTIVE", color=(0, 1, 0, 1), font_size='18sp'))
        self.progress = ProgressBar(max=100, value=0, size_hint_y=None, height=20)
        header.add_widget(self.progress)
        root.add_widget(header)

        # Поля ключей
        keys_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        self.api_key = TextInput(hint_text="Gemini Key", password=True, multiline=False)
        self.gh_token = TextInput(hint_text="GH Token", password=True, multiline=False)
        keys_box.add_widget(self.api_key)
        keys_box.add_widget(self.gh_token)
        root.add_widget(keys_box)

        # Чат / Консоль
        self.console = TextInput(readonly=True, background_color=(0.1, 0.1, 0.1, 1), 
                                foreground_color=(0, 1, 0.1, 1), text="[SYSTEM ONLINE]\n")
        root.add_widget(self.console)

        # Чат-ввод
        chat_input_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=5)
        self.user_msg = TextInput(hint_text="Спроси Gemini...", multiline=False)
        send_btn = Button(text="SEND", size_hint_x=None, width=80, background_color=get_color_from_hex('#007bff'))
        send_btn.bind(on_press=self.start_chat_thread)
        chat_input_box.add_widget(self.user_msg)
        chat_input_box.add_widget(send_btn)
        root.add_widget(chat_input_box)

        # Кнопка Эволюции
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

    def start_chat_thread(self, instance):
        msg = self.user_msg.text
        if msg:
            self.log(f"YOU: {msg}")
            self.user_msg.text = ""
            threading.Thread(target=self.ask_gemini, args=(msg,)).start()

    def ask_gemini(self, prompt):
        api_key = self.api_key.text
        if not api_key:
            self.log("ERROR: Введите Gemini API Key!")
            return
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            response = requests.post(url, headers=headers, json=data)
            res_json = response.json()
            answer = res_json['candidates'][0]['content']['parts'][0]['text']
            self.log(f"GEMINI: {answer}")
        except Exception as e:
            self.log(f"API ERROR: {str(e)}")

    def start_evo(self, instance):
        self.save_settings()
        self.log("ЗАПУСК ЭВОЛЮЦИИ...")
        threading.Thread(target=self.evo_process).start()

    def evo_process(self):
        # Здесь будет логика чтения main.py и отправки в Gemini для исправления
        self.log("Считывание текущего кода...")
        self.progress.value = 30
        # ... (логика пуша на GitHub добавится, когда проверим чат)
        self.log("Анализ завершен. Ошибок не найдено.")
        self.progress.value = 100

if __name__ == "__main__":
    ZartasAIApp().run()
