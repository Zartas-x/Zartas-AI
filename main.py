from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.utils import get_color_from_hex
from kivy.clock import Clock # Добавил для безопасного вывода из потока
import json, os, threading, requests

class ZartasAIApp(App):
    def build(self):
        self.config_file = "config.json"
        root = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        header = BoxLayout(orientation='vertical', size_hint_y=None, height=80)
        header.add_widget(Label(text="ZARTAS AI: DEBUG MODE", color=(0, 1, 0, 1), font_size='18sp'))
        self.progress = ProgressBar(max=100, value=0, size_hint_y=None, height=20)
        header.add_widget(self.progress)
        root.add_widget(header)

        keys_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
        self.api_key = TextInput(hint_text="Gemini Key", password=True, multiline=False)
        self.gh_token = TextInput(hint_text="GH Token", password=True, multiline=False)
        keys_box.add_widget(self.api_key)
        keys_box.add_widget(self.gh_token)
        root.add_widget(keys_box)

        self.console = TextInput(readonly=True, background_color=(0.1, 0.1, 0.1, 1), 
                                foreground_color=(0, 1, 0.1, 1), text="[SYSTEM READY]\n")
        root.add_widget(self.console)

        chat_input_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=5)
        self.user_msg = TextInput(hint_text="Пиши сюда...", multiline=False)
        send_btn = Button(text="SEND", size_hint_x=None, width=80, background_color=get_color_from_hex('#007bff'))
        send_btn.bind(on_press=self.start_chat_thread)
        chat_input_box.add_widget(self.user_msg)
        chat_input_box.add_widget(send_btn)
        root.add_widget(chat_input_box)

        evo_btn = Button(text="START EVOLUTION", size_hint_y=None, height=60,
                         background_color=get_color_from_hex('#28a745'))
        evo_btn.bind(on_press=self.start_evo)
        root.add_widget(evo_btn)

        self.load_settings()
        return root

    def log(self, text):
        # Безопасный вывод в консоль из любого потока
        Clock.schedule_once(lambda dt: self._update_log(text))

    def _update_log(self, text):
        self.console.text += f">> {text}\n"

    def load_settings(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    data = json.load(f)
                    self.api_key.text = data.get("api", "")
                    self.gh_token.text = data.get("gh", "")
            except: pass

    def start_chat_thread(self, instance):
        msg = self.user_msg.text.strip()
        if msg:
            self.log(f"YOU: {msg}")
            self.user_msg.text = ""
            threading.Thread(target=self.ask_gemini, args=(msg,)).start()

    def ask_gemini(self, prompt):
        api_key = self.api_key.text.strip()
        if not api_key:
            self.log("ОШИБКА: Нет ключа!")
            return
        
        self.log("Запрос отправлен...")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        try:
            # Отключаем верификацию SSL (костыль для эмуляторов) + таймаут 10 сек
            res = requests.post(url, 
                               json={"contents": [{"parts": [{"text": prompt}]}]},
                               headers={'Content-Type': 'application/json'},
                               verify=False, 
                               timeout=10)
            
            if res.status_code == 200:
                ans = res.json()['candidates'][0]['content']['parts'][0]['text']
                self.log(f"GEMINI: {ans}")
            else:
                self.log(f"ОШИБКА СЕРВЕРА {res.status_code}: {res.text[:50]}")
        
        except Exception as e:
            # Ловим ВООБЩЕ всё
            self.log(f"КРИТИЧЕСКАЯ ОШИБКА: {type(e).__name__}")
            self.log(f"ДЕТАЛИ: {str(e)[:100]}")

    def start_evo(self, instance):
        self.log("Эволюция пока в разработке...")

if __name__ == "__main__":
    ZartasAIApp().run()
