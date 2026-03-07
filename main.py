import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import requests

class ZartasAIApp(App):
    def build(self):
        # Твой личный ключ доступа
        self.api_key = "AIzaSyDi4M579p_kdmbN8tmck0SJX7STL5WL_Xg" 
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Область чата с поддержкой разметки [b], [color]
        self.scroll = ScrollView(size_hint=(1, 0.8))
        self.chat_log = Label(text="[color=00FF00][Zartas AI]:[/color] Система запущена. Я готов к работе.\n", 
                              size_hint_y=None, halign='left', valign='top', markup=True)
        self.chat_log.bind(texture_size=self.chat_log.setter('size'))
        self.scroll.add_widget(self.chat_log)
        
        # Поле ввода текста
        self.input = TextInput(hint_text="Введите ваш запрос...", size_hint=(1, 0.1), multiline=False)
        self.input.bind(on_text_validate=self.send_message)
        
        # Кнопка отправки
        btn = Button(text="ОТПРАВИТЬ", size_hint=(1, 0.1), background_color=(0.1, 0.5, 0.8, 1))
        btn.bind(on_press=self.send_message)
        
        layout.add_widget(self.scroll)
        layout.add_widget(self.input)
        layout.add_widget(btn)
        return layout

    def send_message(self, instance):
        user_text = self.input.text.strip()
        if not user_text:
            return
        
        self.chat_log.text += f"\n[b]Вы:[/b] {user_text}"
        self.input.text = ""
        
        # Небольшая задержка, чтобы интерфейс не "замерзал"
        Clock.schedule_once(lambda dt: self.fetch_ai_response(user_text), 0.1)

    def fetch_ai_response(self, text):
        try:
            # Используем модель 1.5-flash — она самая быстрая и бесплатная
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
            payload = {"contents": [{"parts": [{"text": text}]}]}
            headers = {'Content-Type': 'application/json'}
            
            response = requests.post(url, json=payload, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                answer = data['candidates'][0]['content']['parts'][0]['text']
                self.chat_log.text += f"\n[color=00FF00][b]Zartas AI:[/b][/color] {answer}\n"
            else:
                self.chat_log.text += f"\n[color=FF0000]Ошибка API ({response.status_code}): {response.text}[/color]\n"
        except Exception as e:
            self.chat_log.text += f"\n[color=FF0000]Ошибка сети: {str(e)}[/color]\n"

if __name__ == '__main__':
    ZartasAIApp().run()
