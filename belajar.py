from kivy.app import App  # Mengimpor App dari Kivy
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.audio import SoundLoader 

# Tombol gambar menggunakan ButtonBehavior dan Image
class ImageButton(ButtonBehavior, Image):
    pass

# Halaman Belajar
class Belajar(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.button_sound = SoundLoader.load('sounds/click.mp3')

        # Gunakan FloatLayout agar elemen bisa diatur posisi absolut di atas background
        layout = FloatLayout()

        # Gambar latar belakang untuk halaman Belajar
        background = Image(source='images/mainmenu.jpg', allow_stretch=True, size_hint=(1, 1))
        layout.add_widget(background)

        label_air = Label(
            text='Hai kamu ingin mengenal\nhewan apa?',
            font_size='22sp',
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            font_name='fonts/Popping-Cute.ttf',
            color=(0.13, 0.55, 0.13, 1),
            halign='center', 
            valign='middle', 
        )
        layout.add_widget(label_air)

        # Tombol Hewan Darat
        btn_darat = ImageButton(source='images/tombol_darat1.png', size_hint=(0.3, 0.3),  
                                pos_hint={'center_x': 0.3, 'center_y': 0.5}, 
                                on_release=self.on_hewan_darat_press)
        layout.add_widget(btn_darat)

        # Tombol Hewan Air
        btn_air = ImageButton(source='images/tombol_air1.png', size_hint=(0.3, 0.3),  
                              pos_hint={'center_x': 0.7, 'center_y': 0.5},  
                              on_release=self.on_hewan_air_press)
        layout.add_widget(btn_air)

        # Tombol Kembali
        btn_kembali = ImageButton(source='images/back_button.png', 
                                  size_hint=(None, None), size=(200, 200),  
                                  pos_hint={'center_x': 0.15, 'y': 0.8})  
        btn_kembali.bind(on_press=self.on_back_press) 
        layout.add_widget(btn_kembali)

        # Tambahkan layout ke screen
        self.add_widget(layout)

    def play_button_sound(self):
        if self.button_sound:
            self.button_sound.play()

    def on_hewan_darat_press(self, instance):
        self.play_button_sound()
        self.go_to_hewan_darat(instance)
        
    def on_hewan_air_press(self, instance):
        self.play_button_sound()
        self.go_to_hewan_air(instance)

    def on_back_press(self, instance):
        self.play_button_sound()
        self.go_back(instance)

    def go_to_hewan_darat(self, instance):
        print("Tombol Hewan Darat Ditekan")
        self.manager.current = 'hewan_darat' 

    def go_to_hewan_air(self, instance):
        print("Tombol Hewan Air Ditekan")
        self.manager.current = 'hewan_air'

    def go_back(self, instance):
        self.manager.current = 'selamat_datang'

class HewanAirScreen(Screen):
    def __init__(self, **kwargs):
        super(HewanAirScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # Gambar latar belakang untuk halaman Hewan Air
        background = Image(source='images/air_background.jpg', allow_stretch=True, size_hint=(1, 1))
        layout.add_widget(background)

        # Tambahkan deskripsi atau gambar hewan air di sini
        label = Label(text="Halaman Hewan Air masih dalam pengembangan.")
        layout.add_widget(label)

        self.add_widget(layout)

# Screen Manager untuk mengelola pergantian halaman
class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Belajar(name='belajar'))
        self.add_widget(HewanAirScreen(name='hewan_air'))


# Main App
class KuisHewanApp(App):
    def build(self):
        return MyScreenManager()


if __name__ == '__main__':
    KuisHewanApp().run()
