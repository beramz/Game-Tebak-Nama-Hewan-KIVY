from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from belajar import Belajar

# ImageButton class dengan tambahan fungsi animasi dan suara
class AnimatedImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(AnimatedImageButton, self).__init__(**kwargs)
        self.original_x = None
        self.anim = None
        # Load sound effect
        self.click_sound = SoundLoader.load('sounds/click.mp3')

    def on_press(self):
        # Play sound when button is pressed
        if self.click_sound:
            self.click_sound.play()

# Halaman Hewan Air
class HewanAirScreen(Screen):
    def __init__(self, **kwargs):
        super(HewanAirScreen, self).__init__(**kwargs)
        layout = FloatLayout()

        # Menambahkan gambar latar belakang
        background = Image(source='images/background_air.png', allow_stretch=True, keep_ratio=False,
                         size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        layout.add_widget(background)

        # Membuat tombol "Kembali" di kiri atas
        btn_kembali = AnimatedImageButton(source='images/back_button.png',
                                      size_hint=(None, None), size=(200, 200),
                                      pos_hint={'center_x': 0.15, 'y': 0.8})
        btn_kembali.bind(on_release=self.go_back)
        layout.add_widget(btn_kembali)

        # Menambahkan gambar hewan dan deskripsinya
        self.dolphin = self.add_hewan_button(layout, 'images/dolphin.png', 'images/popup_lumba.png', {'x': 0, 'y': 0.4}, (160, 220))
        self.shark = self.add_hewan_button(layout, 'images/shark.png', 'images/popup_hiu.png', {'x': 0.4, 'y': 0.2}, (120, 180))
        self.turtle = self.add_hewan_button(layout, 'images/turtle.png', 'images/popup_penyu.png', {'x': 0.5, 'y': 0}, (120, 180))
        self.octopus = self.add_hewan_button(layout, 'images/octopus.png', 'images/popup_squid.png', {'x': 0.5, 'y': 0.4}, (90, 150))

        self.add_widget(layout)
        
        # Memulai animasi setelah layout selesai
        Clock.schedule_once(self.start_animations, 0.5)

    def add_hewan_button(self, layout, image_source, popup_image_source, pos_hint, size):
        btn = AnimatedImageButton(source=image_source, size_hint=(None, None), width=size[0], height=size[1])
        btn.bind(on_release=lambda x: self.show_materi(popup_image_source))
        btn.pos_hint = pos_hint
        btn.original_x = pos_hint['x']  # Simpan posisi x awal
        layout.add_widget(btn)
        return btn

    def start_animations(self, dt):
        # Animasi untuk semua hewan
        self.animate_horizontal(self.dolphin, 0.13)  # Dolphin bergerak lebih jauh
        self.animate_horizontal(self.shark, 0.1)    # Shark bergerak sedang
        self.animate_horizontal(self.turtle, 0.15)   # Turtle bergerak lebih lambat
        self.animate_horizontal(self.octopus, 0.17)  # Octopus bergerak normal

    def animate_horizontal(self, widget, offset):
        # Hentikan animasi yang sedang berjalan (jika ada)
        if widget.anim:
            widget.anim.cancel()

        # Buat animasi baru
        original_x = widget.original_x
        anim1 = Animation(pos_hint={'x': original_x + offset}, duration=2)
        anim2 = Animation(pos_hint={'x': original_x}, duration=2)
        widget.anim = anim1 + anim2
        widget.anim.repeat = True
        widget.anim.start(widget)

    def show_materi(self, popup_image_source):
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        img = Image(source=popup_image_source, size_hint=(1, 1), allow_stretch=True)
        popup_layout.add_widget(img)

        popup = Popup(content=popup_layout,
                     size_hint=(None, None), size=(400, 400),
                     title=' ',
                     background='',
                     background_color=[0, 0, 0, 0],
                     separator_height=0)
        popup.open()

    def go_back(self, instance):
        self.manager.current = 'belajar'

class MyScreenManager(ScreenManager):
    pass

class KuisHewanApp(App):
    def build(self):
        sm = MyScreenManager()
        sm.add_widget(HewanAirScreen(name='hewan_air'))
        sm.add_widget(Belajar(name='belajar'))
        return sm

if __name__ == '__main__':
    KuisHewanApp().run()