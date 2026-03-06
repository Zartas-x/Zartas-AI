from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

# Это основной класс твоего приложения
class ZartasAIApp(App):
    def build(self):
        # Создаем главный контейнер
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Заголовок
        self.label = Label(
            text="Zartas AI: Система готова", 
            font_size='20sp',
            size_hint_y=None,
            height=100
        )
        
        # Кнопка запуска (пока просто для теста интерфейса)
        self.btn = Button(
            text="ЗАПУСТИТЬ ИИ",
            background_color=(0, 1, 0, 1), # Зеленая кнопка
            size_hint=(None, None),
            size=(200, 100),
            pos_hint={'center_x': 0.5}
        )
        self.btn.bind(on_press=self.on_click)

        # Добавляем элементы в макет
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.btn)
        
        return self.layout

    def on_click(self, instance):
        self.label.text = "ИИ Zartas анализирует систему..."
        print("Кнопка нажата! ИИ запущен.")

if __name__ == "__main__":
    ZartasAIApp().run()
