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
        
        # Поле для твоего НОВОГО ключа (без варнингов)
        self.api_input = TextInput(hint_text="Вставь свой рабочий Google API Key", size_hint=(1, 0.1), password=True)
        
        self.scroll = ScrollView(size_hint=(1, 0.8))
        self.chat_log = Label(text="[color=00FF00][Zartas AI]:[/color] Жду ключ. Проверь, работает ли VPN в браузере LDPlayer!\n", 
                              size_hint_y=None, halign='left', valign='top', markup=True)
        self.chat_log.bind(texture_size=self.chat_log.setter('size'))
        self.scroll.add_widget(self.chat_log)
        
        self.input = TextInput(hint_text="Пиши тут...", size_hint=(1, 0.1), multiline=False)
        self.input.bind(on_text_validate=self.send_message)
        
        self.layout.add_widget(self.api_input)
        self.layout.add_widget(self.scroll)
        self.layout.add_widget(self.input)
        return self.layout

    def send_message(self, instance):
        user_text = self.input.text.strip()
        key = self.api_input.text.strip()
        if not user_text or not key: return
        self.chat_log.text += f"\n[b]Вы:[/b] {user_text}"
        self.input.text = ""
        Clock.schedule_once(lambda dt: self.fetch_ai_response(user_text, key), 0.1)

    def fetch_ai_response(self, text, key):
        try:
            # Используем самый базовый URL
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
            headers = {'Content-Type': 'application/json'}
            payload = {"contents": [{"parts": [{"text": text}]}]}
            
            # Добавим лог отправки
            self.chat_log.text += "\n[Система]: Отправляю запрос..."
            
            r = requests.post(url, headers=headers, json=payload, timeout=15)
            
            if r.status_code == 200:
                ans = r.json()['candidates'][0]['content']['parts'][0]['text']
                self.chat_log.text += f"\n[color=00FF00][b]Zartas AI:[/b][/color] {ans}\n"
            else:
                # ВЫВОДИМ ПОЛНЫЙ ТЕКСТ ОШИБКИ
                self.chat_log.text += f"\n[!] Ошибка {r.status_code}: {r.text[:100]}\n"
        except Exception as e:
            self.chat_log.text += f"\n[!] Сбой сети: {str(e)}\n"

if __name__ == '__main__':
    ZartasAIApp().run()
