import requests, json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard  # Для копирования

class ZartasAIApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 1. Поле для ключа
        self.api_input = TextInput(hint_text="Вставь API Key", size_hint=(1, 0.1), password=True)
        
        # 2. Окно чата (логи)
        self.scroll = ScrollView(size_hint=(1, 0.7))
        self.chat_log = Label(
            text="[color=00FF00][Zartas AI]:[/color] Система логирования активна. Жду ключ...\n", 
            size_hint_y=None, markup=True, halign='left', valign='top'
        )
        self.chat_log.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        self.chat_log.bind(texture_size=self.chat_log.setter('size'))
        self.scroll.add_widget(self.chat_log)
        
        # 3. Кнопка копирования логов
        self.copy_btn = Button(text="СКОПИРОВАТЬ ВСЕ ЛОГИ", size_hint=(1, 0.08), background_color=(0.2, 0.6, 1, 1))
        self.copy_btn.bind(on_press=self.copy_to_clipboard)
        
        # 4. Поле ввода сообщения
        self.input = TextInput(hint_text="Напиши что-нибудь...", size_hint=(1, 0.1), multiline=False)
        self.input.bind(on_text_validate=self.send_message)
        
        self.layout.add_widget(self.api_input)
        self.layout.add_widget(self.scroll)
        self.layout.add_widget(self.copy_btn)
        self.layout.add_widget(self.input)
        return self.layout

    def copy_to_clipboard(self, instance):
        # Копируем чистый текст без тегов [color] для меня
        clean_text = self.chat_log.text.replace("[color=00FF00]", "").replace("[/color]", "").replace("[b]", "").replace("[/b]", "")
        Clipboard.copy(clean_text)
        self.copy_btn.text = "ЛОГИ СКОПИРОВАНЫ!"
        Clock.schedule_once(lambda dt: setattr(self.copy_btn, 'text', "СКОПИРОВАТЬ ВСЕ ЛОГИ"), 2)

    def send_message(self, instance):
        user_text = self.input.text.strip()
        key = self.api_input.text.replace(" ", "").strip()
        if not user_text or not key: return
        self.chat_log.text += f"\n[b]Вы:[/b] {user_text}"
        self.input.text = ""
        Clock.schedule_once(lambda dt: self.fetch_ai_response(user_text, key), 0.1)

    def fetch_ai_response(self, text, key):
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        params = {'key': key}
        headers = {'Content-Type': 'application/json'}
        payload = {"contents": [{"parts": [{"text": text}]}]}
        
        try:
            self.chat_log.text += f"\n[LOG]: Отправка на {url}..."
            session = requests.Session()
            session.trust_env = False 
            
            r = session.post(url, params=params, headers=headers, json=payload, timeout=15)
            
            self.chat_log.text += f"\n[LOG]: Статус ответа: {r.status_code}"
            
            if r.status_code == 200:
                ans = r.json()['candidates'][0]['content']['parts'][0]['text']
                self.chat_log.text += f"\n[color=00FF00][b]Zartas AI:[/b][/color] {ans}\n"
            else:
                self.chat_log.text += f"\n[КРИТИЧЕСКАЯ ОШИБКА]:\n{r.text}\n"
        except Exception as e:
            self.chat_log.text += f"\n[ОШИБКА СЕТИ]: {str(e)}\n"

if __name__ == '__main__':
    ZartasAIApp().run()
