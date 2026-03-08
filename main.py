import requests
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivy.core.window import Window
from urllib3.exceptions import InsecureRequestWarning

# Отключаем SSL предупреждения
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

class ZartasAIApp(App):
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.1, 1)  # Тёмная тема

        self.layout = BoxLayout(orientation='vertical', padding=15, spacing=10)

        # Заголовок
        title = Label(
            text="[color=00FF88][b]Zartas AI v19.1[/b] — Март 2026[/color]",
            size_hint=(1, 0.08),
            markup=True,
            font_size='18sp'
        )

        self.api_input = TextInput(
            hint_text="Вставь Gemini API Key (AIzaSy...)",
            size_hint=(1, 0.09),
            password=True,
            multiline=False,
            font_size='16sp'
        )

        self.scroll = ScrollView(size_hint=(1, 0.68))
        self.chat_log = Label(
            text="[color=00FF88][Zartas AI]:[/color] Система запущена v19.1 (08.03.2026)\n"
                 "Актуальные модели: gemini-3.1-flash-lite-preview и 2.5-flash\n"
                 "Вставь ключ и пиши...\n",
            size_hint_y=None,
            markup=True,
            halign='left',
            valign='top',
            padding=(10, 10)
        )
        self.chat_log.bind(width=lambda i, v: setattr(i, 'text_size', (v - 20, None)))
        self.chat_log.bind(texture_size=self.chat_log.setter('size'))
        self.scroll.add_widget(self.chat_log)

        self.copy_btn = Button(
            text="📋 КОПИРОВАТЬ ВЕСЬ ЧАТ",
            size_hint=(1, 0.08),
            background_color=(0.1, 0.6, 1, 1)
        )
        self.copy_btn.bind(on_press=self.copy_to_clipboard)

        self.input = TextInput(
            hint_text="Напиши сообщение...",
            size_hint=(1, 0.1),
            multiline=False,
            font_size='17sp'
        )
        self.input.bind(on_text_validate=self.send_message)

        self.layout.add_widget(title)
        self.layout.add_widget(self.api_input)
        self.layout.add_widget(self.scroll)
        self.layout.add_widget(self.copy_btn)
        self.layout.add_widget(self.input)

        return self.layout

    def copy_to_clipboard(self, instance):
        clean = self.chat_log.text.replace("[color=00FF88]", "").replace("[/color]", "").replace("[b]", "").replace("[/b]", "")
        Clipboard.copy(clean)
        self.copy_btn.text = "✅ СКОПИРОВАНО!"
        Clock.schedule_once(lambda dt: setattr(self.copy_btn, 'text', "📋 КОПИРОВАТЬ ВЕСЬ ЧАТ"), 1.8)

    def send_message(self, instance):
        user_text = self.input.text.strip()
        key = self.api_input.text.strip()

        if not user_text or not key:
            self.add_log("[color=FF4444]Ошибка: введи ключ и сообщение[/color]")
            return

        self.add_log(f"[b]Вы:[/b] {user_text}")
        self.input.text = ""

        Clock.schedule_once(lambda dt: self.fetch_ai_response(user_text, key), 0.1)

    def add_log(self, text):
        self.chat_log.text += "\n" + text
        # Автопрокрутка вниз
        Clock.schedule_once(lambda dt: setattr(self.scroll, 'scroll_y', 0), 0.1)

    def fetch_ai_response(self, text, key):
        # Самые рабочие модели на 08.03.2026
        models = [
            "gemini-3.1-flash-lite-preview",   # самый быстрый и стабильный
            "gemini-2.5-flash",
            "gemini-3-flash-preview",
            "gemini-2.5-flash-lite"
        ]

        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{"parts": [{"text": text}]}],
            "generationConfig": {"temperature": 0.7, "maxOutputTokens": 2048}
        }

        for model in models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
            
            try:
                self.add_log(f"[color=8888FF]→ Пробую {model}...[/color]")
                r = requests.post(url, headers=headers, json=payload, timeout=20, verify=False)

                if r.status_code == 200:
                    data = r.json()
                    answer = data['candidates'][0]['content']['parts'][0]['text']
                    self.add_log(f"[color=00FF88][b]Zartas AI:[/b][/color] {answer}")
                    return  # Успех — выходим

                else:
                    error_msg = r.json().get('error', {}).get('message', r.text[:100])
                    self.add_log(f"[color=FFAA00]{model} → {r.status_code} | {error_msg[:80]}[/color]")

            except Exception as e:
                self.add_log(f"[color=FF4444]Ошибка {model}: {str(e)[:70]}[/color]")

        self.add_log("[color=FF0000][b]❌ Все модели не ответили. Проверь ключ или интернет.[/b][/color]")


if __name__ == '__main__':
    ZartasAIApp().run()
