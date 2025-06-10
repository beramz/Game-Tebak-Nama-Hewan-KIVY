import json
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.audio import SoundLoader  # Tambahkan import ini
from kivy.core.image import Image as CoreImage

from animated_widget import AnimatedImage

# Kelas ImageButton untuk tombol gambar
class ImageButton(ButtonBehavior, Image):
    pass

class CustomTextInput(TextInput):
    def __init__(self, previous_widget=None, next_widget=None, **kwargs):
        super().__init__(**kwargs)
        self.previous_widget = previous_widget
        self.next_widget = next_widget
        
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        key, key_str = keycode
        
        # Handle backspace key
        if key_str == 'backspace':
            if not self.text and self.previous_widget:
                # If current input is empty and there's a previous widget, move focus there
                self.previous_widget.focus = True
                self.previous_widget.select_all()  # Optional: select the text in the previous widget
                return True
            
        return super().keyboard_on_key_down(window, keycode, text, modifiers)
    
class HalamanKuisScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initialize_quiz()
        self.setup_ui()
        self.current_question_index = 0
        self.shake_count = 0
        self.original_pos = None
        self.score = 0 
        self.attempts = 0 

    def initialize_quiz(self):
        """Initialize or reset quiz state"""
        self.current_question_index = 0
        self.shake_count = 0
        self.original_pos = None
        self.score = 0 
        self.attempts = 0
        
        self.button_sound = SoundLoader.load('sounds/click.mp3')
        self.correct_sound = SoundLoader.load('sounds/correct.mp3')
        self.wrong_sound = SoundLoader.load('sounds/wrong.mp3')
        self.complete_sound = SoundLoader.load('sounds/complete.mp3')
        
        # Load questions
        self.load_questions_from_json()
        
    def on_pre_enter(self):
            """Called before the screen is displayed"""
            self.reset_quiz()
            
    def reset_quiz(self):
            """Reset quiz state and display first question"""
            self.current_question_index = 0
            self.score = 0
            self.update_score_display()
            self.display_question(self.current_question_index)
        
            self.button_sound = SoundLoader.load('sounds/click.mp3')
            self.correct_sound = SoundLoader.load('sounds/correct.mp3')
            self.wrong_sound = SoundLoader.load('sounds/wrong.mp3')
            self.complete_sound = SoundLoader.load('sounds/complete.mp3')

       
    def setup_ui(self):
        """Setup all UI elements"""
        self.main_layout = FloatLayout()

        # Background Image
        background = Image(source='images/kuis_background.jpg', allow_stretch=True, keep_ratio=False)
        self.main_layout.add_widget(background)

        # Score Labels
        self.score_label_outline = Label(
            text="Skor: 0",
            font_size=25,
            size_hint=(0.2, None),
            height=40,
            pos_hint={'center_x': 0.8, 'y': 0.915},
            font_name='fonts/Popping-Cute.ttf',
            color=(0, 0, 0, 1)
        )

        self.score_label = Label(
            text="Skor: 0",
            font_size=24,
            size_hint=(0.2, None),
            height=40,
            pos_hint={'center_x': 0.8, 'y': 0.92},
            font_name='fonts/Popping-Cute.ttf',
            color=(1, 1, 1, 1)
        )
        self.main_layout.add_widget(self.score_label_outline)
        self.main_layout.add_widget(self.score_label)

        # Animal Image
        self.img = Image(source='', size_hint=(0.5, 0.5), pos_hint={'center_x': 0.5, 'y': 0.45})
        self.main_layout.add_widget(self.img)

        # Question Label
        self.question_label = Label(
            text="", 
            font_size=24, 
            size_hint=(0.8, None), 
            height=40, 
            pos_hint={'x': 0.1, 'y': 0.4},
            font_name='fonts/Popping-Cute.ttf',
            color=(0.13, 0.55, 0.13, 1)
        )
        self.main_layout.add_widget(self.question_label)

        # Answer Layout
        self.answer_layout = GridLayout(
            cols=5, 
            spacing=5, 
            size_hint=(0.8, None), 
            height=40,
            pos_hint={'center_x': 0.6, 'y': 0.3}
        )
        self.main_layout.add_widget(self.answer_layout)

        # Check Answer Button
        check_answer_button = ImageButton(
            source='images/btn_jawab.png', 
            size_hint=(None, None), 
            size=(200, 200),
            pos_hint={'center_x': 0.5, 'y': 0}
        )
        check_answer_button.bind(on_press=self.on_check_answer_press)
        self.main_layout.add_widget(check_answer_button)

        # Result Label
        self.result_label = Label(
            text="", 
            font_size=24, 
            size_hint=(0.8, None), 
            height=40, 
            pos_hint={'center_x': 0.5, 'y': 0.1}
        )
        self.main_layout.add_widget(self.result_label)

        # Back Button
        btn_kembali = ImageButton(
            source='images/back_button.png', 
            size_hint=(None, None), 
            size=(200, 200),
            pos_hint={'center_x': 0.15, 'y': 0.8}
        )
        btn_kembali.bind(on_press=self.on_back_button_press)
        self.main_layout.add_widget(btn_kembali)

        self.add_widget(self.main_layout)

    def play_sound(self, sound):
        if sound and sound.state != 'play':
            # Stop any currently playing sounds
            if self.correct_sound and self.correct_sound.state == 'play':
                self.correct_sound.stop()
            if self.wrong_sound and self.wrong_sound.state == 'play':
                self.wrong_sound.stop()
            if self.button_sound and self.button_sound.state == 'play':
                self.button_sound.stop()
            
            self.complete_sound
            # Play the new sound
            sound.play()

    def on_back_button_press(self, instance):
        self.play_sound(self.button_sound)
        self.go_back(instance)

    def on_check_answer_press(self, instance):
        self.play_sound(self.button_sound)
        self.check_answer(instance)

    def load_questions_from_json(self):
        # Memuat data soal dari file JSON
        with open('soal_darat.json', 'r') as file:
            self.quiz_data = json.load(file)

    def display_question(self, index):
        question_data = self.quiz_data[index]
        self.question_label.text = question_data['pertanyaan']
        self.img.source = question_data['gambar']
        
        self.answer_layout.clear_widgets()
        
        # Create TextInput boxes with linked navigation
        self.answer_inputs = []
        for i in range(len(question_data['jawaban'])):
            input_box = CustomTextInput(
                hint_text="_",
                multiline=False,
                font_size=24,
                size_hint=(None, None),
                width=40,
                height=40,
                halign="center",
                input_filter=self.only_letters
            )
            
            # Store the input box reference
            self.answer_inputs.append(input_box)
            
            # Set up previous and next widget references
            if i > 0:
                input_box.previous_widget = self.answer_inputs[i-1]
                self.answer_inputs[i-1].next_widget = input_box
                
            input_box.bind(text=self.on_text_input)
            input_box.bind(on_text_validate=self.move_to_next)
            
            self.answer_layout.add_widget(input_box)

    def on_text_input(self, instance, value):
        # Ensure only one character per input
        if len(value) > 1:
            instance.text = value[-1]
        
        # Move to next input if character is entered
        if len(instance.text) == 1 and instance.next_widget:
            instance.next_widget.focus = True

    def move_to_next(self, instance):
        # Pindah ke blok berikutnya setelah blok saat ini diisi
        for i, input_box in enumerate(self.answer_inputs):
            if instance == input_box and i < len(self.answer_inputs) - 1:
                self.answer_inputs[i + 1].focus = True
                break

    def handle_focus(self, instance, value):
        # Handle backspace jika TextInput kosong dan berpindah ke blok sebelumnya
        if not value and instance.text == '':
            for i, input_box in enumerate(self.answer_inputs):
                if instance == input_box and i > 0:
                    # Pindah ke blok sebelumnya
                    self.answer_inputs[i - 1].focus = True
                    break
    # Shake Effek               
    def shake_screen(self, dt):
        if self.original_pos is None:
            # Simpan posisi original saat pertama kali
            self.original_pos = self.main_layout.pos
        
        self.shake_count += 1
        
        # Gunakan posisi original sebagai basis untuk setiap gerakan
        if self.shake_count % 2 == 0:
            new_x = self.original_pos[0] + 10
        else:
            new_x = self.original_pos[0] - 10
        
        anim = Animation(pos=(new_x, self.original_pos[1]), duration=0.05)
        anim.start(self.main_layout)
        
        if self.shake_count >= 6:
            self.shake_count = 0
            Clock.unschedule(self.shake_screen)
            # Pastikan kembali ke posisi original
            final_anim = Animation(pos=self.original_pos, duration=0.05)
            final_anim.start(self.main_layout)
            # Reset original_pos untuk animasi berikutnya
            self.original_pos = None

    def clear_answer_inputs(self):
        for input_box in self.answer_inputs:
            input_box.text = ""
        if self.answer_inputs:
            self.answer_inputs[0].focus = True

    def update_score_display(self):
            self.score_label.text = f"Skor: {self.score}"
            self.score_label_outline.text = f"Skor: {self.score}"

    def handle_next(self, *args):
        if hasattr(self, 'popup'):
            self.popup.dismiss()
        self.current_question_index += 1
        if self.current_question_index < len(self.quiz_data):
            self.display_question(self.current_question_index)
        else:
            self.show_final_score_popup()

    def handle_back(self, *args):
        if hasattr(self, 'popup'):
            self.popup.dismiss()
        self.manager.current = 'opsi_bermain'
        
    def check_answer(self, instance):
        user_answer = ''.join([input_box.text.lower() for input_box in self.answer_inputs])
        correct_answer = self.quiz_data[self.current_question_index]['jawaban']
        
        if user_answer == correct_answer:
            # Play correct sound and show success animation
            self.play_sound(self.correct_sound)
            self.score += 200
            self.update_score_display()
            Clock.schedule_once(lambda dt: self.show_correct_popup(), 0.1)
        else:
            # Play wrong sound and show shake animation
            self.play_sound(self.wrong_sound)
            self.score = max(0, self.score - 50)
            self.update_score_display()
            self.shake_count = 0
            Clock.schedule_interval(self.shake_screen, 0.05)
            Clock.schedule_once(lambda dt: self.clear_answer_inputs(), 0.3)

    def show_correct_popup(self):
        # Create content layout
        popup_layout = FloatLayout()
        
        # Background GIF using our custom AnimatedImage class
        animated_button = AnimatedImage(
                    base_path="images/gif4/frame_",
                    frame_count=99,
                    fps=20,
                    loop_reverse=False,
                    pos_hint={'center_x': 0.5, 'center_y': 0.7},
                    size=(200, 200),
                )
        popup_layout.add_widget(animated_button)
        
        # Text content
        label = Label(
            text=f"Skor: +200",
            font_size=24,
            size_hint=(0.8, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.38},
            color = (1, 1, 1, 1),
            font_name='fonts/Popping-Cute.ttf'
        )
        popup_layout.add_widget(label)
        
        # Button layout
        button_layout = GridLayout(
            cols=2, 
            spacing=20,
            size_hint=(0.8, 0.2),
            pos_hint={'center_x': 0.75, 'y': 0.1}
        )
        
        # Back button
        back_btn = ImageButton(
            source='images/prev_btn.png',
            size_hint=(None, None),
            size=(50, 50)
        )
        def on_back_with_sound(instance):
            self.play_sound(self.button_sound)
            self.handle_back(instance)
        back_btn.bind(on_press=on_back_with_sound)
        
        # Next button with sound
        next_btn = ImageButton(
            source='images/next_btn.png',
            size_hint=(None, None),
            size=(50, 50)
        )
        def on_next_with_sound(instance):
            self.play_sound(self.button_sound)
            self.handle_next(instance)
        next_btn.bind(on_press=on_next_with_sound)
        
        # Add buttons to button layout
        button_layout.add_widget(back_btn)
        button_layout.add_widget(next_btn)
        
        # Add button layout to main layout
        popup_layout.add_widget(button_layout)
        
        # Create and show popup
        self.popup = Popup(
            title='',
            content=popup_layout,
            size_hint=(None, None),
            size=(400, 300),
            auto_dismiss=False,
            background_color=[0, 0, 0, 0],  # Slightly transparent white background
            separator_height=0
        )
        
        self.popup.open()


    def show_final_score_popup(self):
        # Play completion sound
        self.play_sound(self.complete_sound)
        
        popup_content = FloatLayout()
                
        # Final score message
        message = (
                f"Skor Akhir: {self.score}"
                )
        
        animated_button = AnimatedImage(
                    base_path="images/gifwin/frame_",
                    frame_count=49,
                    fps=20,
                    loop_reverse=False,
                    pos_hint={'center_x': 0.5, 'center_y': 0.7},
                    size=(200, 200),
                )
        popup_content.add_widget(animated_button)

        label = Label(
            text=message,
            font_size=24,
            size_hint=(0.8, 0.6),
            pos_hint={'center_x': 0.5, 'center_y': 0.3},
            font_name='fonts/Popping-Cute.ttf'
        )
        popup_content.add_widget(label)

        # Menggunakan ImageButton untuk tombol Selesai
        finish_button = ImageButton(
            source='images/next_btn.png',  # Sesuaikan dengan nama file gambar Anda
            size_hint=(None, None),
            size=(50, 50),  # Sesuaikan ukuran sesuai kebutuhan
            pos_hint={'center_x': 0.5, 'y': 0}
        )
        finish_button.bind(on_release=self.go_back)
        popup_content.add_widget(finish_button)

        self.popup = Popup(
            title="",
            content=popup_content,
            size_hint=(None, None),
            size=(400, 300),
            background_color=[0,0,0,0],
            separator_height=0
        )
        self.popup.open()

    def next_question(self, instance):
        self.popup.dismiss()
        self.current_question_index += 1
        
        if self.current_question_index < len(self.quiz_data):
            self.display_question(self.current_question_index)
        else:
            self.show_final_score_popup()

    def only_letters(self, substring, from_undo):
        # Hanya mengizinkan huruf alfabet
        return ''.join([char for char in substring if char.isalpha()])
    
    def go_back(self, instance):
        if hasattr(self, 'popup') and self.popup:
            self.popup.dismiss()
        self.manager.current = 'opsi_bermain'

# Screen Manager untuk mengatur halaman
class MyScreenManager(ScreenManager):
    pass

# Main App untuk menjalankan aplikasi
class KuisHewanApp(App):
    def build(self):
        sm = MyScreenManager()
        sm.add_widget(HalamanKuisScreen(name='halaman_kuis'))  # Menambahkan halaman kuis
        return sm


if __name__ == '__main__':
    KuisHewanApp().run()
