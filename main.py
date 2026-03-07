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

class ZartasAIApp(App):
    def build(self):
        # Актуальный ключ для тестов
        self.api_key = "AIzaSyDi4M579p_kdmbN8tmck0SJX7STL5WL_Xg"
        self.repo = "Zartas-x/Zartas-AI"
        
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Поле для ввода токена (Чтобы GitHub его не видел в исходниках)
        self.token_input = TextInput(hint_text="Вставь сюда НОВЫЙ ghp_... токен", size_hint=(1, 0.1), password=True)
        
        self.scroll = ScrollView(size_hint=(1, 0.7))
        self.chat_log = Label(text="[color=00FF00][Zartas AI]:[/color] 1. Создай НОВЫЙ токен в GitHub.\n2. Вставь его в поле выше.\n3. Нажми 'ЭВОЛЮЦИЯ'.\n", 
                              size_hint_y=None, halign='left', valign='top', markup=True)
        self.chat_log.bind(texture_size=self.chat_log.setter('size'))
        self.scroll.add_widget(self.chat_log)
        
        self.input = TextInput(hint_text="Твое сообщение...", size_hint=(1, 0.1), multiline=False)
        self.input.bind(on_text_validate=self.send_message)
        
        btn_layout = BoxLayout(size_hint=(1, 0.1), spacing=5)
        send_btn = Button(text="ОТПРАВИТЬ", background_color=(0.1, 0.5, 0.8, 1))
        send_btn.bind(on_press=self.send_message)
        
        evolve_btn = Button(text="ЭВОЛЮЦИЯ", background_color=(0.8, 0.2, 0, 1))
        evolve_btn.bind(on_press=self.self_improve)
        
        btn_layout.add_widget(send_btn)
        btn_layout.add_widget(evolve_btn)
        
        self.layout.add_widget(self.token_input)
        self.layout.add_widget(self.scroll)
        self.layout.add_widget(self.input)
        self.layout.add_widget(btn_layout)
        return self.layout

    def send_message(self, instance):
        user_text = self.input.text.strip()
        if not user_text: return
        self.chat_log.text += f"\n[b]Вы:[/b] {user_text}"
        self.input.text = ""
        Clock.schedule_once(lambda dt: self.fetch_ai_response(user_text), 0.1)

    def fetch_ai_response(self, text):
        try:
            # Улучшенный URL и структура запроса
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.api_key}"
            payload = {"contents": [{"role": "user", "parts": [{"text": text}]}]}
            r = requests.post(url, json=payload, timeout=15)
            
            if r.status_code == 200:
                data = r.json()
                ans = data['candidates'][0]['content']['parts'][0]['text']
                self.chat_log.text += f"\n[color=00FF00][b]Zartas AI:[/b][/color] {ans}\n"
            else:
                self.chat_log.text += f"\n[Ошибка ИИ {r.status_code}]: Попробуй сменить сервер VPN на США.\n"
        except Exception as e:
            self.chat_log.text += f"\n[Ошибка сети]: Проверь интернет в LDPlayer.\n"

    def self_improve(self, instance):
        token = self.token_input.text.strip()
        if not token.startswith("ghp_"):
            self.chat_log.text += "\n[!] Вставь НОВЫЙ рабочий токен!\n"
            return
        
        self.chat_log.text += "\n[AI]: Начинаю проверку прав доступа...\n"
        test_content = "Connection established. AI is ready to rebuild."
        Clock.schedule_once(lambda dt: self.push_to_github(token, "evolution_test.txt", test_content), 0.5)

    def push_to_github(self, token, file_path, content):
        try:
            url = f"https://api.github.com/repos/{self.repo}/contents/{file_path}"
            # Используем Bearer-токен для надежности
            headers = {
                "Authorization": f"token {token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            # Проверка SHA
            r = requests.get(url, headers=headers)
            sha = r.json().get('sha') if r.status_code == 200 else None
            
            encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
            data = {"message": "AI self-test", "content": encoded}
            if sha: data["sha"] = sha
            
            res = requests.put(url, json=data, headers=headers)
            if res.status_code in [200, 201]:
                self.chat_log.text += f"\n[УСПЕХ]: Связь с GitHub установлена! Файл {file_path} создан.\n"
            else:
                self.chat_log.text += f"\n[Ошибка GitHub {res.status_code}]: Токен не подходит или забанен.\n"
        except Exception as e:
            self.chat_log.text += f"\n[Сбой]: {str(e)[:50]}\n"

if __name__ == '__main__':
    ZartasAIApp().run()
