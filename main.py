from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex

class ZartasAIApp(App):
    def build(self):
        # Главный контейнер (вертикальный)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Заголовок
        layout.add_widget(Label(
            text="Zartas AI Console", 
            font_size='20sp', 
            size_hint_y=None, 
            height=50
        ))
        
        # Поле вывода (Логи) - только для чтения
        self.log_area = TextInput(
            readonly=True, 
            background_color=(0, 0, 0, 1), 
            foreground_color=(0, 1, 0, 1),
            font_name='Roboto' # Стандартный шрифт Android
        )
        layout.add_widget(self.log_area)
        
        # Кнопка действия
        btn = Button(
            text="ЭВОЛЮЦИЯ", 
            size_hint_y=None, 
            height=60,
            background_color=get_color_from_hex('#28a745'),
            background_normal=''
        )
        btn.bind(on_press=self.evolve)
        layout.add_widget(btn)
        
        return layout

    def log(self, message):
        self.log_area.text += f"> {message}\n"

    def evolve(self, instance):
        self.log("Запуск процесса эволюции...")
        self.log("Проверка системы...")
        self.log("Версия 19.1 (Kivy) активна.")

if __name__ == "__main__":
    ZartasAIApp().run()
