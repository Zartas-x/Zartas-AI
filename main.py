import os
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from plyer import battery, vibrator

class ZartasAIApp(App):
    def build(self):
        # Твой текущий API ключ
        self.api_key = "AIzaSyDi4M579p_kdmbN8tmck0SJX7STL5WL_Xg" 
        self.history = [] # ПАМЯТЬ ДЛЯ ОБЩЕНИЯ
        
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.scroll = ScrollView(size_hint=(1, 0.8))
        self.chat_log = Label(text="[color=00FF00][Zartas AI]:[/color] Я подключен к ядру. Чем помочь?\n", 
                              size_hint_y=None, halign='left', valign='top', markup=True)
        self.chat_log.bind(texture_size=self.chat_log.setter('size'))
        self.scroll.add_widget(self.chat_log)
        
        self.input = TextInput(hint_text="Напиши сообщение...", size_hint=(1, 0.1), multiline=False)
        self.input.bind(on_text_validate=self.send_message)
        
        btn = Button(text="ОТПРАВИТЬ", size_hint=(1, 0.1), background_color=(0.1, 0.5, 0.8, 1))
        btn.bind(on_press=self.send_message)
        
        self.layout.add_widget(self.scroll)
        self.layout.add_widget(self.input)
        self.layout.add_widget(btn)
        return self.layout

    def send_message(self, instance):
        user_text = self.input.text.strip()
        if not user_text: return
        
        self.chat_log.text += f"\n[b]Вы:[/b] {user_text}"
        self.input.text = ""
        
        # Локальная команда без интернета
        if "статус" in user_text.lower():
            p = battery.status.get('percentage', '???')
            self.chat_log.text += f"\n[AI]: Заряд: {p}%. Связь с системой активна.\n"
            vibrator.vibrate(0.1)
        else:
            Clock.schedule_once(lambda dt: self.fetch_response(user_text), 0.1)

    def fetch_response(self, text):
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
            
            # Обновляем память (держим последние 4 сообщения для контекста)
            self.history.append({"role": "user", "parts": [{"text": text}]})
            payload = {"contents": self.history[-5:]}
            
            # Делаем запрос с таймаутом
            r = requests.post(url, json=payload, timeout=10)
            
            if r.status_code == 200:
                data = r.json()
                ans = data['candidates'][0]['content']['parts'][0]['text']
                self.chat_log.text += f"\n[color=00FF00][b]Zartas AI:[/b][/color] {ans}\n"
                self.history.append({"role": "model", "parts": [{"text": ans}]})
            else:
                self.chat_log.text += f"\n[Ошибка]: Сервер ответил кодом {r.status_code}\n"
        except Exception as e:
            self.chat_log.text += f"\n[Ошибка связи]: Проверь интернет или API-ключ.\n"

if __name__ == '__main__':
    ZartasAIApp().run()
