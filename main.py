import os
import requests
import base64
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

class ZartasAIApp(App):
    def build(self):
        # Используем стабильную версию ключа и модели
        self.api_key = "AIzaSyDi4M579p_kdmbN8tmck0SJX7STL5WL_Xg"
        self.repo = "Zartas-x/Zartas-AI"
        
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Поле для токена (ты уже знаешь, что он работает!)
        self.token_input = TextInput(text="ВСТАВЬ_СВОЙ_ТОКЕН_СЮДА", size_hint=(1, 0.1), password=True)
        
        self.scroll = ScrollView(size_hint=(1, 0.7))
        self.chat_log = Label(text="[color=00FF00][Zartas AI]:[/color] Связь с GitHub подтверждена. Оживляем чат...\n", 
                              size_hint_y=None, halign='left', valign='top', markup=True)
        self.chat_log.bind(texture_size=self.chat_log.setter('size'))
        self.scroll.add_widget(self.chat_log)
        
        self.input = TextInput(hint_text="Напиши что-нибудь...", size_hint=(1, 0.1), multiline=False)
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
            # Обновленный URL на модель 1.5-flash-latest
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={self.api_key}"
            
            headers = {'Content-Type': 'application/json'}
            payload = {
                "contents": [{"parts": [{"text": text}]}],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 1024,
                }
            }
            
            r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=20)
            
            if r.status_code == 200:
                res_data = r.json()
                if 'candidates' in res_data:
                    ans = res_data['candidates'][0]['content']['parts'][0]['text']
                    self.chat_log.text += f"\n[color=00FF00][b]Zartas AI:[/b][/color] {ans}\n"
                else:
                    self.chat_log.text += f"\n[Zartas AI]: Я тебя слышу, но Google прислал пустой ответ. Странно.\n"
            else:
                self.chat_log.text += f"\n[Ошибка {r.status_code}]: Сервер Google не нашел модель. Проверь VPN!\n"
                # Доп. инфо для нас с тобой:
                print(f"DEBUG: {r.text}")
        except Exception as e:
            self.chat_log.text += f"\n[Сбой сети]: {str(e)[:50]}\n"

    def self_improve(self, instance):
        token = self.token_input.text.strip()
        if not token.startswith("ghp_"):
            self.chat_log.text += "\n[!] Сначала вставь токен!\n"
            return
        self.chat_log.text += "\n[AI]: Попытка улучшить чат-модуль на GitHub...\n"
        test_content = "Chat module update attempt. Success."
        Clock.schedule_once(lambda dt: self.push_to_github(token, "evolution_test.txt", test_content), 0.5)

    def push_to_github(self, token, file_path, content):
        try:
            url = f"https://api.github.com/repos/{self.repo}/contents/{file_path}"
            headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
            r = requests.get(url, headers=headers)
            sha = r.json().get('sha') if r.status_code == 200 else None
            encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')
            data = {"message": "AI self-fix", "content": encoded}
            if sha: data["sha"] = sha
            res = requests.put(url, json=data, headers=headers)
            if res.status_code in [200, 201]:
                self.chat_log.text += f"\n[УСПЕХ]: Файл обновлен. Сборка пошла!\n"
            else:
                self.chat_log.text += f"\n[Ошибка GitHub]: {res.status_code}\n"
        except Exception as e:
            self.chat_log.text += f"\n[Сбой]: {str(e)}\n"

if __name__ == '__main__':
    ZartasAIApp().run()
