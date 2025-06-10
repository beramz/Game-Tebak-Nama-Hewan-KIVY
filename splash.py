from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.video import Video 
from kivy.clock import Clock
from kivy.core.audio import SoundLoader 
from animated_widget import AnimatedImage

class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super(SplashScreen, self).__init__(**kwargs)
        layout = FloatLayout()

        # Tambahkan video sebagai background splash

        splash_video = AnimatedImage (
                    base_path="images/gifsplash/frame_",
                    frame_count=49,
                    fps=20,
                    loop_reverse=False,
                    pos_hint={'center_x': 0.5, 'center_y': 0.5},
                    size=(200, 200),)
        layout.add_widget(splash_video)

        self.add_widget(layout)

        # Memuat dan memutar audio (optional, jika tidak ada audio di video)
        self.splash_audio = SoundLoader.load('sounds/splashost.mp3') 
        if self.splash_audio:
            self.splash_audio.play() 

        # Timer untuk pindah ke screen berikutnya (misalnya 10 detik)
        Clock.schedule_once(self.switch_to_main, 8) 

    def switch_to_main(self, dt):
        # Hentikan video dan audio ketika splash screen berakhir
        if self.splash_audio:
            self.splash_audio.stop()

        # Pindah ke layar utama setelah splash screen selesai
        self.manager.current = 'selamat_datang'
