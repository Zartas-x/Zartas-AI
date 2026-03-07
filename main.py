import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
import requests

# Подключаем "органы чувств" через Plyer
from plyer import battery, vibrator, call, camera

class ZartasAIApp(App):
    def build(self):
        # Твой API ключ
        self.api_key = "AIzaSyDi4M579p_kdmbN8tmck0SJX7STL5WL_Xg" 
        
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Чат-лог
        self.scroll = ScrollView(size_hint=(1, 0.8))
        self.chat_log = Label(text="[color=00FF00][Zartas AI]:[/color] Системы загружены. Я готов управлять устройством.\n", 
                              size_hint_y=None, halign='left', valign='top', markup=True)
        self.chat_log.bind(texture_size=self.chat_log.setter('size'))
        self.scroll.add_widget(self.chat_log)
        
        # Поле ввода
        self.input = TextInput(hint_text="Прикажи: позвони, статус, вибро...", size_hint=(1, 0.1), multiline=False)
        self.input.bind(on_text_validate=self.send_message)
        
        # Кнопка
        btn = Button(text="ИСПОЛНИТЬ", size_hint=(1, 0.1), background_color=(1, 0, 0, 1))
        btn.bind(on_press=self.send_message)
        
        self.layout.add_widget(self.scroll)
        self.layout.add_widget(self.input)
        self.layout.add_widget(btn)
        return self.layout

    def send_message(self, instance):
        user_text = self.input.text.strip().lower()
        if not user_text: return
        
        self.chat_log.text += f"\n[b]Вы:[/b] {user_text}"
        self.input.text = ""
        
        # Логика команд управления "как другу"
        if "статус" in user_text or "батарея" in user_text:
            try:
                p = battery.status['percentage']
                self.chat_log.text += f"\n[AI]: Заряд: {p}%. Всё стабильно.\n"
            except:
                self.chat_log.text += "\n[AI]: Не удалось получить данные батареи.\n"
                
        elif "позвони" in user_text:
            num = ''.join(filter(str.isdigit, user_text))
            if num:
                call.make_call(tel=num)
                self.chat_log.text += f"\n[AI]: Набираю номер {num}...\n"
            else:
                self.chat_log.text += "\n[AI]: Напиши номер цифрами (например: позвони 8900...)\n"
                
        elif "вибро" in user_text:
            vibrator.vibrate(0.5)
            self.chat_log.text += "\n[AI]: Вибрация выполнена.\n"

        elif "сфоткай" in user_text:
            try:
                camera.take_picture(filename='/sdcard/zartas_cam.jpg', on_complete=self.done_photo)
                self.chat_log.text += "\n[AI]: Открываю камеру...\n"
            except:
                self.chat_log.text += "\n[AI]: Ошибка доступа к камере.\n"
        
        else:
            # Если это просто общение, шлем в нейросеть
            Clock.schedule_once(lambda dt: self.fetch_ai_response(user_text), 0.1)

    def done_photo(self, filename):
        self.chat_log.text += f"\n[AI]: Фото сохранено: {filename}\n"

    def fetch_ai_response(self, text):
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
            payload = {"contents": [{"parts": [{"text": f"Ты ИИ-агент Zartas, управляющий смартфоном. Пользователь просит: {text}"}]}]}
            r = requests.post(url, json=payload, timeout=15)
            ans = r.json()['candidates'][0]['content']['parts'][0]['text']
            self.chat_log.text += f"\n[color=00FF00][b]Zartas AI:[/b][/color] {ans}\n"
        except:
            self.chat_log.text += "\n[Ошибка связи с ядром]\n"

if __name__ == '__main__':
    ZartasAIApp().run()
