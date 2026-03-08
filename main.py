import requests, json, socket, ssl, time
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
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Поле для ключа
        self.api_input = TextInput(hint_text="Вставь API Key", size_hint=(1, 0.07), password=True, multiline=False)
        
        # Окно вывода
        self.scroll = ScrollView(size_hint=(1, 0.75))
        self.chat_log = Label(
            text="[color=00FF00][Zartas AI]:[/color] Запуск системы полной диагностики v17.5...\n", 
            size_hint_y=None, markup=True, halign='left', valign='top'
        )
        self.chat_log.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        self.chat_log.bind(texture_size=self.chat_log.setter('size'))
        self.scroll.add_widget(self.chat_log)
        
        # Кнопка "Черный ящик"
        self.copy_btn = Button(text="СКОПИРОВАТЬ ПОЛНЫЙ ОТЧЕТ", size_hint=(1, 0.08), background_color=(1, 0.2, 0.2, 1))
        self.copy_btn.bind(on_press=self.copy_to_clipboard)
        
        # Поле ввода
        self.input = TextInput(hint_text="Введите текст для теста...", size_hint=(1, 0.1), multiline=False)
        self.input.bind(on_text_validate=self.send_message)
        
        self.layout.add_widget(self.api_input)
        self.layout.add_widget(self.scroll)
        self.layout.add_widget(self.copy_btn)
        self.layout.add_widget(self.input)
        return self.layout

    def log(self, text):
        self.chat_log.text += f"\n{text}"

    def copy_to_clipboard(self, instance):
        clean_text = self.chat_log.text.replace("[color=00FF00]", "").replace("[/color]", "").replace("[b]", "").replace("[/b]", "")
        Clipboard.copy(clean_text)
        self.copy_btn.text = "ОТЧЕТ В БУФЕРЕ ОБМЕНА!"
        Clock.schedule_once(lambda dt: setattr(self.copy_btn, 'text', "СКОПИРОВАТЬ ПОЛНЫЙ ОТЧЕТ"), 2)

    def send_message(self, instance):
        user_text = self.input.text.strip()
        key = self.api_input.text.strip()
        if not user_text or not key: return
        self.log(f"[b]Вы:[/b] {user_text}")
        self.input.text = ""
        Clock.schedule_once(lambda dt: self.full_scan(user_text, key), 0.1)

    def full_scan(self, text, key):
        self.log("-" * 30)
        self.log("[START] ГЛУБОКОЕ СКАНИРОВАНИЕ...")
        
        # 1. Проверка IP и Геолокации (через сторонний API)
        try:
            geo = requests.get('https://ipapi.co/json/', timeout=5).json()
            self.log(f"[NET] IP: {geo.get('ip')} | Страна: {geo.get('country_name')} | Провайдер: {geo.get('org')}")
        except:
            self.log("[NET] Ошибка определения геопозиции.")

        # 2. Проверка порта 443 (SSL) до Google
        host = "generativelanguage.googleapis.com"
        try:
            start_t = time.time()
            sock = socket.create_connection((host, 443), timeout=5)
            context = ssl.create_default_context()
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                self.log(f"[SSL] Соединение с {host} защищено (TLS {ssock.version()})")
            self.log(f"[PING] Задержка до Google: {int((time.time() - start_t)*1000)}ms")
        except Exception as e:
            self.log(f"[!!] ОШИБКА SSL/ПОРТА: {str(e)}")

        # 3. Атака по моделям (gemini-1.5 и gemini-2.0)
        models = ["gemini-1.5-flash-002", "gemini-1.5-flash", "gemini-2.0-flash-exp", "gemini-1.5-pro"]
        headers = {'Content-Type': 'application/json', 'User-Agent': 'Zartas-AI-Mobile/1.0'}
        payload = {"contents": [{"parts": [{"text": text}]}]}
        
        for m in models:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={key}"
            try:
                self.log(f"[TRY] Модель: {m}")
                r = requests.post(url, headers=headers, json=payload, timeout=12)
                self.log(f"  -> Код: {r.status_code}")
                
                if r.status_code == 200:
                    ans = r.json()['candidates'][0]['content']['parts'][0]['text']
                    self.log(f"[SUCCESS] {m} в сети!")
                    self.log(f"[color=00FF00][b]Zartas AI:[/b][/color] {ans}")
                    return
                else:
                    self.log(f"  -> Ответ сервера: {r.text[:120]}...")
            except Exception as e:
                self.log(f"  -> Ошибка запроса: {str(e)[:60]}")

        self.log("[FINISH] Сканирование завершено. Жду отчет.")

if __name__ == '__main__':
    try:
        ZartasAIApp().run()
    except Exception as e:
        # Если приложение крашнется, мы не увидим это в логе, но Buildozer сохранит в logcat
        print(f"CRITICAL CRASH: {e}")
