from kivy.app import App  
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.clock import Clock
from belajar import Belajar 
from opsi_bermain import OpsiBermain 


# Tombol gambar menggunakan ButtonBehavior dan Image
class ImageButton(ButtonBehavior, Image):
    pass

# Halaman Selamat Datang
class SelamatDatangScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Inisialisasi sound effect dan backsound
        self.button_sound = SoundLoader.load('sounds/click.mp3')
        self.backsound = SoundLoader.load('sounds/backsound.mp3')
        self.is_backsound_playing = True 

        # Gunakan FloatLayout agar elemen bisa diatur posisi absolut di atas background video
        layout = FloatLayout()

        # Background Gambar
        self.background = Image(source='images/mainmenu.jpg')
        self.background.size_hint = (1, 1)
        self.background.allow_stretch = True
        layout.add_widget(self.background)

        title_image = Image(source='images/judul.png', size_hint=(3, 1),
                            pos_hint={'center_x': 0.5, 'center_y': 0.7})
        layout.add_widget(title_image)
        
        # Tombol Bermain
        btn_bermain = ImageButton(source='images/bermain.png', size_hint=(0.4, 0.4),
                                  pos_hint={'center_x': 0.7, 'center_y': 0.4},
                                  on_release=self.on_bermain_press)
        layout.add_widget(btn_bermain)
        self.animate_widget(btn_bermain, 0.4, 0.4)

        # Tombol Belajar
        btn_belajar = ImageButton(source='images/belajar.png', size_hint=(0.3, 0.3),
                                  pos_hint={'center_x': 0.3, 'center_y': 0.4},
                                  on_release=self.on_belajar_press)
        layout.add_widget(btn_belajar)
        self.animate_widget(btn_belajar, 0.3, 0.3)
        
        # Tombol Sound (posisi di pojok kanan atas)
        self.btn_sound = ImageButton(
            source='images/sound_on.png', 
            size_hint=(0.1, 0.1),
            pos_hint={'right': 0.95, 'top': 0.95},
            on_release=self.toggle_backsound
        )
        layout.add_widget(self.btn_sound)
        
        # Tambahkan layout ke screen
        self.add_widget(layout)

        # Jadwalkan pemutaran backsound setelah inisialisasi
        Clock.schedule_once(self.start_backsound, 0.1)

    def start_backsound(self, dt):
        # Mulai backsound
        if self.backsound and self.is_backsound_playing:
            self.backsound.loop = True
            self.backsound.play()

    def animate_widget(self, widget, initial_size_hint_x, initial_size_hint_y):
        anim_increase = Animation(size_hint=(initial_size_hint_x * 1.1, initial_size_hint_y * 1.1), duration=0.5)
        anim_decrease = Animation(size_hint=(initial_size_hint_x, initial_size_hint_y), duration=0.5)
        anim_increase += anim_decrease
        anim_increase.repeat = True
        anim_increase.start(widget)

    def toggle_backsound(self, instance):
        if self.button_sound:
            self.button_sound.play() 
            
        if not self.is_backsound_playing:
            # Jika backsound sedang off, nyalakan
            if self.backsound:
                self.backsound.loop = True
                self.backsound.play()
                self.is_backsound_playing = True
                self.btn_sound.source = 'images/sound_on.png'
        else:
            # Jika backsound sedang on, matikan
            if self.backsound:
                self.backsound.stop()
                self.is_backsound_playing = False
                self.btn_sound.source = 'images/sound_off.png'

    def play_button_sound(self):
        if self.button_sound:
            self.button_sound.play()
        
    def on_bermain_press(self, instance):
        self.play_button_sound()
        self.go_to_kuis(instance)
        
    def on_belajar_press(self, instance):
        self.play_button_sound()
        self.go_to_belajar(instance)
        
    def go_to_kuis(self, instance):
        print("Tombol Bermain Ditekan")
        self.manager.current = 'opsi_bermain'

    def go_to_belajar(self, instance):
        print("Tombol Belajar Ditekan")
        self.manager.current = 'belajar'

    def on_leave(self):
        # Simpan status backsound saat meninggalkan screen
        if hasattr(App.get_running_app(), 'backsound_playing'):
            App.get_running_app().backsound_playing = self.is_backsound_playing

    def on_enter(self):
        # Periksa status backsound saat memasuki screen
        if hasattr(App.get_running_app(), 'backsound_playing'):
            if App.get_running_app().backsound_playing != self.is_backsound_playing:
                self.toggle_backsound(None)


class KuisScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = FloatLayout()
        background = Image(source='images/kuis_background.png', allow_stretch=True, keep_ratio=False)
        layout.add_widget(background)
        self.add_widget(layout)


class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(SelamatDatangScreen(name='selamat_datang'))
        self.add_widget(OpsiBermain(name='opsi_bermain'))
        self.add_widget(Belajar(name='belajar'))


class KuisHewanApp(App):
    def build(self):
        self.backsound_playing = True 
        return MyScreenManager()


if __name__ == '__main__':
    KuisHewanApp().run()