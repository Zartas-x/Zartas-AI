import requests, json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard

class ZartasAIApp(App):
    def build(self):
        # Основной контейнер
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 1. Поле для ввода API Ключа
        self.api_input = TextInput(
            hint_text="Вставь API Key сюда", 
            size_hint=(1, 0.1), 
            password=True,
            multiline=False
        )
        
        # 2. Окно чата (скроллбар + текст)
        self.scroll = ScrollView(size_hint=(1, 0.7))
        self.chat_log = Label(
            text="[color=00FF00][Zartas AI]:[/color] Версия 15.0. Путь к модели исправлен. Жду твой ключ и первое сообщение!\n", 
            size_hint_y=None, 
            markup=True, 
            halign='left', 
            valign='top'
        )
        # Магия для переноса текста по словам
        self.chat_log.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        self.chat_log.bind(texture_size=self.chat_log.setter('size'))
        self.scroll.add_widget(self.chat_log)
        
        # 3. Кнопка копирования логов (для отладки)
        self.copy_btn = Button(
            text="СКОПИРОВАТЬ ВСЕ ЛОГИ", 
            size_hint=(1, 0.08), 
            background_color=(0.2, 0.6, 1, 1)
        )
        self.copy_btn.bind(on_press=self.copy_to_clipboard)
        
        # 4. Поле ввода сообщения
        self.input = TextInput(
            hint_text="Напиши 'Привет'...", 
            size_hint=(1, 0.1), 
            multiline=False
        )
        self.input.bind(on_text_validate=self.send_message)
        
        # Добавляем всё на экран
        self.layout.add_widget(self.api_input)
        self.layout.add_widget(self.scroll)
        self.layout.add_widget(self.copy_btn)
        self.layout.add_widget(self.input)
        
        return self.layout

    def copy_to_clipboard(self, instance):
        try:
            # Очищаем текст от тегов оформления перед копированием
            clean_text = self.chat_log.text.replace("[color=00FF00]", "").replace("[/color]", "").replace("[b]", "").replace("[/b]", "")
            Clipboard.copy(clean_text)
            self.copy_btn.text = "ТЕКСТ СКОПИРОВАН!"
        except Exception as e:
            self.copy_btn.text = f"ОШИБКА: {str(e)}"
        
        # Возвращаем название кнопки через 2 секунды
        Clock.schedule_once(lambda dt: setattr(self.copy_btn, 'text', "СКОПИРОВАТЬ ВСЕ ЛОГИ"), 2)

    def send_message(self, instance):
        user_text = self.input.text.strip()
        key = self.api_input.text.replace(" ", "").strip()
        
        if not user_text:
            return
        if not key:
            self.chat_log.text += "\n[СИСТЕМА]: Сначала вставь API ключ выше!"
            return

        self.chat_log.text += f"\n[b]Вы:[/b] {user_text}"
        self.input.text = ""
        
        # Запускаем запрос в отдельном потоке (через Clock), чтобы интерфейс не завис
        Clock.schedule_once(lambda dt: self.fetch_ai_response(user_text, key), 0.1)

    def fetch_ai_response(self, text, key):
        # Самый надежный формат URL для Gemini 1.5 Flash
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
        
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [
                {
                    "parts": [{"text": text}]
                }
            ]
        }
        
        try:
            self.chat_log.text += f"\n[LOG]: Соединение с Google v1beta..."
            
            # Прямой POST запрос
            r = requests.post(url, headers=headers, json=payload, timeout=20)
            
            self.chat_log.text += f"\n[LOG]: Статус {r.status_code}"
            
            if r.status_code == 200:
                data = r.json()
                if 'candidates' in data and len(data['candidates']) > 0:
                    ai_answer = data['candidates'][0]['content']['parts'][0]['text']
                    self.chat_log.text += f"\n[color=00FF00][b]Zartas AI:[/b][/color] {ai_answer}\n"
                else:
                    self.chat_log.text += f"\n[ОШИБКА]: Google прислал пустой ответ.\n"
            else:
                # Выводим текст ошибки от Google, если он прислал не 200
                self.chat_log.text += f"\n[КРИТИЧЕСКАЯ ОШИБКА]:\n{r.text}\n"
        except Exception as e:
            self.chat_log.text += f"\n[ОШИБКА СЕТИ]: Проверь VPN! {str(e)}\n"

if __name__ == '__main__':
    ZartasAIApp().run()
