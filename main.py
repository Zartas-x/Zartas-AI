import requests, json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from urllib3.exceptions import InsecureRequestWarning

# Отключаем ворнинги SSL
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class ZartasAIApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.api_input = TextInput(hint_text="API Key (Gemini)", size_hint=(1, 0.1), password=True, multiline=False)
        
        self.scroll = ScrollView(size_hint=(1, 0.7))
        self.chat_log = Label(
            text="[color=00FF00][Zartas AI]:[/color] Система 19.0 (Март 2026). Модели: 2.5/3.0. Жду ключ!\n", 
            size_hint_y=None, markup=True, halign='left', valign='top'
        )
        self.chat_log.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        self.chat_log.bind(texture_size=self.chat_log.setter('size'))
        self.scroll.add_widget(self.chat_log)
        
        self.copy_btn = Button(text="КОПИРОВАТЬ ЛОГИ", size_hint=(1, 0.08), background_color=(0.2, 0.6, 1, 1))
        self.copy_btn.bind(on_press=self.copy_to_clipboard)
        
        self.input = TextInput(hint_text="Напиши что-нибудь...", size_hint=(1, 0.1), multiline=False)
        self.input.bind(on_text_validate=self.send_message)
        
        self.layout.add_widget(self.api_input)
        self.layout.add_widget(self.scroll)
        self.layout.add_widget(self.copy_btn)
        self.layout.add_widget(self.input)
        return self.layout

    def copy_to_clipboard(self, instance):
        clean_text = self.chat_log.text.replace("[color=00FF00]", "").replace("[/color]", "").replace("[b]", "").replace("[/b]", "")
        Clipboard.copy(clean_text)
        self.copy_btn.text = "СКОПИРОВАНО!"
        Clock.schedule_once(lambda dt: setattr(self.copy_btn, 'text', "КОПИРОВАТЬ ЛОГИ"), 2)

    def send_message(self, instance):
        user_text = self.input.text.strip()
        key = self.api_input.text.strip()
        if not user_text or not key: return
        self.chat_log.text += f"\n[b]Вы:[/b] {user_text}"
        self.input.text = ""
        Clock.schedule_once(lambda dt: self.fetch_ai_response(user_text, key), 0.1)

    def fetch_ai_response(self, text, key):
        # Список самых актуальных моделей на сегодня (по совету Грока и моим данным)
        target_models = ["gemini-2.5-flash", "gemini-3-flash", "gemini-1.5-flash"]
        headers = {'Content-Type': 'application/json'}
        payload = {"contents": [{"parts": [{"text": text}]}]}
        
        for model in target_models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
            try:
                self.chat_log.text += f"\n[LOG]: Штурм {model} (no-verify)..."
                # Выключаем verify, чтобы пробить ошибку сертификата
                r = requests.post(url, headers=headers, json=payload, timeout=15, verify=False)
                
                if r.status_code == 200:
                    data = r.json()
                    ans = data['candidates'][0]['content']['parts'][0]['text']
                    self.chat_log.text += f"\n[color=00FF00][b]Zartas AI:[/b][/color] {ans}\n"
                    return # Успех, выходим из цикла
                else:
                    self.chat_log.text += f"\n[LOG]: {model} -> {r.status_code}"
            except Exception as e:
                self.chat_log.text += f"\n[ERR]: {model} сбой: {str(e)[:40]}"

        self.chat_log.text += f"\n[ФИНАЛ]: Ни одна модель не ответила. Проверь VPN или Ключ."

if __name__ == '__main__':
    ZartasAIApp().run()
