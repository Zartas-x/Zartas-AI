import requests, json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

class ZartasAIApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Поле для ключа с авто-очисткой пробелов
        self.api_input = TextInput(hint_text="Вставь Google API Key здесь", size_hint=(1, 0.1), password=True)
        
        self.scroll = ScrollView(size_hint=(1, 0.8))
        self.chat_log = Label(text="[color=00FF00][Zartas AI]:[/color] Раз браузер работает — мы у цели!\n1. Создай НОВЫЙ ключ в AI Studio.\n2. Вставь его сюда.\n", 
                              size_hint_y=None, halign='left', valign='top', markup=True)
        self.chat_log.bind(texture_size=self.chat_log.setter('size'))
        self.scroll.add_widget(self.chat_log)
        
        self.input = TextInput(hint_text="Пиши...", size_hint=(1, 0.1), multiline=False)
        self.input.bind(on_text_validate=self.send_message)
        
        self.layout.add_widget(self.api_input)
        self.layout.add_widget(self.scroll)
        self.layout.add_widget(self.input)
        return self.layout

    def send_message(self, instance):
        user_text = self.input.text.strip()
        # Убираем все лишние пробелы вокруг ключа автоматически!
        key = self.api_input.text.replace(" ", "").strip()
        
        if not user_text or not key: 
            self.chat_log.text += "\n[!] Нужен ключ и текст!"
            return
            
        self.chat_log.text += f"\n[b]Вы:[/b] {user_text}"
        self.input.text = ""
        Clock.schedule_once(lambda dt: self.fetch_ai_response(user_text, key), 0.1)

    def fetch_ai_response(self, text, key):
        try:
            # Используем стабильный адрес
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
            payload = {"contents": [{"parts": [{"text": text}]}]}
            
            self.chat_log.text += "\n[Система]: Связь с Google установлена. Жду ответ..."
            
            r = requests.post(url, json=payload, timeout=20)
            
            if r.status_code == 200:
                res_data = r.json()
                ans = res_data['candidates'][0]['content']['parts'][0]['text']
                self.chat_log.text += f"\n[color=00FF00][b]Zartas AI:[/b][/color] {ans}\n"
            else:
                # Показываем причину прямо в чате
                error_msg = r.json().get('error', {}).get('message', 'Неизвестная ошибка')
                self.chat_log.text += f"\n[Ошибка {r.status_code}]: {error_msg}\n"
                if "API key not valid" in error_msg:
                    self.chat_log.text += "[Подсказка]: Ключ неверный. Удали старый в AI Studio и создай НОВЫЙ.\n"
        except Exception as e:
            self.chat_log.text += f"\n[Сбой]: {str(e)}\n"

if __name__ == '__main__':
    ZartasAIApp().run()
