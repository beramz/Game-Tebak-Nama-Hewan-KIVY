from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty
from kivy.graphics import PushMatrix, PopMatrix, Rotate, Scale
from kivy.core.audio import SoundLoader

# ImageButton class dengan properti tambahan untuk animasi
class AnimatedImageButton(ButtonBehavior, Image):
    angle = NumericProperty(0)  # Untuk rotasi
    scale = NumericProperty(1)  # Untuk zoom
    animation_type = StringProperty(None)  # Untuk menyimpan tipe animasi

    def __init__(self, **kwargs):
        # Ambil animation_type dari kwargs jika ada
        self.animation_type = kwargs.pop('animation_type', None)

        super(AnimatedImageButton, self).__init__(**kwargs)

        # Menambahkan instruksi grafis untuk zoom
        if self.animation_type == 'zoom':
            with self.canvas.before:
                PushMatrix()
                self.scaling = Scale(1, 1, 1)
            with self.canvas.after:
                PopMatrix()
            self.bind(scale=self._update_scale)

    def _update_rot_pos(self, *args):
        self.rot.origin = self.center
        self.rot.angle = self.angle

    def _update_scale(self, *args):
        self.scaling.x = self.scaling.y = self.scale

# Halaman Hewan Darat
class HewanDaratScreen(Screen):
    def __init__(self, **kwargs):
        super(HewanDaratScreen, self).__init__(**kwargs)
        self.button_sound = SoundLoader.load('sounds/click.mp3')
        
        layout = FloatLayout()

        # Background
        background = Image(source='images/darat_background.png', allow_stretch=True, keep_ratio=False,
                         size_hint=(1, 1), pos_hint={'x': 0, 'y': 0})
        layout.add_widget(background)

        # Back button
        btn_kembali = AnimatedImageButton(source='images/back_button.png',
                                        size_hint=(None, None), size=(200, 200),
                                        pos_hint={'center_x': 0.15, 'y': 0.8})
        btn_kembali.bind(on_press=self.on_back_button_press)
        layout.add_widget(btn_kembali)

        # Add animal buttons with animation
        self.giraffe = self.add_hewan_button(layout, 'images/giraffe.png', 'images/popup_giraffe.png', 
                                           {'x': 0, 'y': 0.2}, (160, 220), 'horizontal')
        self.bear = self.add_hewan_button(layout, 'images/bear.png', 'images/popup_bear.png', 
                                        {'x': 0.4, 'y': 0.2}, (120, 180), 'horizontal')
        self.tiger = self.add_hewan_button(layout, 'images/tiger.png', 'images/popup_tiger.png', 
                                         {'x': 0.5, 'y': 0}, (120, 180), 'zoom')
        self.monkey = self.add_hewan_button(layout, 'images/monkey.png', 'images/popup_monkey.png', 
                                          {'x': 0.7, 'y': 0.4}, (90, 150), 'zoom')

        self.add_widget(layout)
        
        Clock.schedule_once(self.start_animations, 0.5)

    def play_sound(self):
        if self.button_sound and self.button_sound.state != 'play':
            self.button_sound.play()

    def add_hewan_button(self, layout, image_source, popup_image_source, pos_hint, size, anim_type):
        btn = AnimatedImageButton(source=image_source, 
                                size_hint=(None, None), 
                                width=size[0], 
                                height=size[1], 
                                animation_type=anim_type)
        # Bind dengan fungsi yang memutar suara dan menampilkan materi
        btn.bind(on_press=lambda x: self.on_hewan_press(popup_image_source))
        btn.pos_hint = pos_hint
        layout.add_widget(btn)
        return btn
    
    def on_hewan_press(self, popup_image_source):
        # Play sound first
        self.play_sound()
        # Then show materi
        self.show_materi(popup_image_source)

    def on_back_button_press(self, instance):
        # Play sound first
        self.play_sound()
        # Then go back
        self.go_back(instance)

    def start_animations(self, dt):
        # Animasi horizontal untuk giraffe
        if self.giraffe.animation_type == 'horizontal':
            self.animate_horizontal(self.giraffe, 0.05)
        
        # Animasi horizontal untuk bear
        if self.bear.animation_type == 'horizontal':
            self.animate_horizontal(self.bear, 0.1)
        
        # Animasi rotasi untuk monkey
        if self.monkey.animation_type == 'zoom':
            self.animate_zoom(self.monkey)
        
        # Animasi zoom untuk tiger
        if self.tiger.animation_type == 'zoom':
            self.animate_zoom(self.tiger)

    def animate_horizontal(self, widget, offset):
        original_x = widget.pos_hint['x']
        anim1 = Animation(pos_hint={'x': original_x + offset}, duration=2)
        anim2 = Animation(pos_hint={'x': original_x}, duration=2)
        anim = anim1 + anim2
        anim.repeat = True
        anim.start(widget)

    def animate_zoom(self, widget):
        anim1 = Animation(scale=1.1, duration=1)
        anim2 = Animation(scale=1, duration=1)
        anim = anim1 + anim2
        anim.repeat = True
        anim.start(widget)

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
        sm.add_widget(HewanDaratScreen(name='hewan_darat'))
        return sm

if __name__ == '__main__':
    KuisHewanApp().run()