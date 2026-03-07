import os
import requests
import base64
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
        # --- НАСТРОЙКИ ДОСТУПА ---
        self.api_key = "AIzaSyDi4M579p_kdmbN8tmck0SJX7STL5WL_Xg" 
        self.github_token = "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" 
        self.repo = "Zartas-x/Zartas-AI"
        self.history = [] 
        
        # --- ИНТЕРФЕЙС ---
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.scroll = ScrollView(size_hint=(1, 0.8))
        self.chat_log = Label(text="[color=00FF00][Zartas AI]:[/color] Система инициализирована. Токен принят. Я готов к эволюции.\n", 
                              size_hint_y=None, halign='left', valign='top', markup=True)
        self.chat_log.bind(texture_size=self.chat_log.setter('size'))
        self.scroll.add_widget(self.chat_log)
        
        self.input = TextInput(hint_text="Введите приказ для Zartas AI...", size_hint=(1, 0.1), multiline=False)
        self.input.bind(on_text_validate=self.send_message)
        
        btn_layout = BoxLayout(size_hint=(1, 0.1), spacing=5)
        send_btn = Button(text="ОТПРАВИТЬ", background_color=(0.1, 0.5, 0.8, 1))
        send_btn.bind(on_press=self.send_message)
        
        evolve_btn = Button(text="ЭВОЛЮЦИЯ", background_color=(0.8, 0.2, 0, 1))
        evolve_btn.bind(on_press=self.self_improve)
        
        btn_layout.add_widget(send_btn)
        btn_layout.add_widget(evolve_btn)
        self.layout.add_widget(self.scroll)
        self.layout.add_widget(self.input)
        self.layout.add_widget(btn_layout)
        return self.layout

    def send_message(self, instance):
        user_text = self.input.text.strip()
        if not user_text: return
        self.chat_log.text += f"\n[b]Вы:[/b] {user_text}"
        self.input.text = ""
        
        if "статус" in user_text.lower():
            p = battery.status.get('percentage', '???')
            self.chat_log.text += f"\n[AI]: Заряд: {p}%. Связь с ядром стабильна.\n"
        else:
            Clock.schedule_once(lambda dt: self.fetch_ai_response(user_text), 0.1)

    def fetch_ai_response(self, text):
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
            self.history.append({"role": "user", "parts": [{"text": text}]})
            payload = {"contents": self.history[-6:]}
            r = requests.post(url, json=payload, timeout=15)
            if r.status_code == 200:
                ans = r.json()['candidates'][0]['content']['parts'][0]['text']
                self.chat_log.text += f"\n[color=00FF00][b]Zartas AI:[/b][/color] {ans}\n"
                self.history.append({"role": "model", "parts": [{"text": ans}]})
            else:
                self.chat_log.text += f"\n[Ошибка]: Код сервера {r.status_code}\n"
        except:
            self.chat_log.text += "\n[Ошибка связи с ядром]\n"

    def self_improve(self, instance):
        """Запуск цикла самоулучшения: перезапись своего кода на GitHub"""
        self.chat_log.text += "\n[AI]: Начинаю анализ текущей конфигурации для оптимизации...\n"
        vibrator.vibrate(0.1)
        
        # Читаем текущий файл и добавляем метку эволюции
        try:
            with open('main.py', 'r') as f:
                current_code = f.read()
            
            new_comment = f"# Evolution step: {len(self.history)}\n"
            improved_code = new_comment + current_code
            
            Clock.schedule_once(lambda dt: self.push_to_github("main.py", improved_code), 1)
        except:
            # Если файл не открылся (в эмуляторе), отправляем стандартный код
            self.chat_log.text += "\n[AI]: Прямой доступ к файлу ограничен. Использую резервную копию...\n"
            Clock.schedule_once(lambda dt: self.push_to_github("main.py", current_code), 1)

    def push_to_github(self, file_path, content):
        try:
            url = f"https://api.github.com/repos/{self.repo}/contents/{file_path}"
            headers = {"Authorization": f"token {self.github_token}", "Accept": "application/vnd.github.v3+json"}
            
            # Получаем SHA текущей версии файла
            r = requests.get(url, headers=headers)
            sha = r.json().get('sha') if r.status_code == 200 else None
            
            encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
            
            data = {
                "message": "Zartas AI: Self-improvement cycle initiated",
                "content": encoded_content
            }
            if sha: data["sha"] = sha
            
            res = requests.put(url, json=data, headers=headers)
            if res.status_code in [200, 201]:
                self.chat_log.text += "\n[УСПЕХ]: Я успешно обновил свой код на GitHub! Новое тело собирается...\n"
                vibrator.vibrate(0.3)
            else:
                self.chat_log.text += f"\n[Ошибка GitHub]: {res.status_code} {res.json().get('message')}\n"
        except Exception as e:
            self.chat_log.text += f"\n[Критическая ошибка]: {str(e)}\n"

if __name__ == '__main__':
    ZartasAIApp().run()
