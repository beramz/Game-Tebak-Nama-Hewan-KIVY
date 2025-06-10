from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.audio import SoundLoader
from halaman_kuis_air import HalamanKuisAirScreen
from selamat_datang import SelamatDatangScreen
from halaman_kuis import HalamanKuisScreen
from hewan_darat import HewanDaratScreen  
from hewan_air import HewanAirScreen     
from belajar import Belajar
from opsi_bermain import OpsiBermain
from splash import SplashScreen
from kivy.core.window import Window

class MyScreenManager(ScreenManager):
    pass

class KuisHewanApp(App):
    def build(self):
        Window.size = (360, 640)
        
        # Memuat dan memutar backsound
        # self.backsound = SoundLoader.load('sounds/backsound.mp3')
        # if self.backsound:
        #     self.backsound.loop = True
        #     self.backsound.play()
            

        # Membuat ScreenManager dan menambahkan halaman
        sm = MyScreenManager()
        sm.add_widget(SplashScreen(name='splash_screen'))
        sm.add_widget(SelamatDatangScreen(name='selamat_datang'))
        sm.add_widget(HalamanKuisScreen(name='halaman_kuis'))
        sm.add_widget(HalamanKuisAirScreen(name='halaman_kuis_air'))
        sm.add_widget(Belajar(name='belajar'))
        sm.add_widget(HewanDaratScreen(name='hewan_darat'))  # Tambahkan hewan darat screen
        sm.add_widget(HewanAirScreen(name='hewan_air'))      # Tambahkan hewan air screen
        sm.add_widget(OpsiBermain(name='opsi_bermain'))
        # Set screen awal
        sm.current = 'splash_screen'
        return sm

    # def on_stop(self):
    #     # Hentikan musik ketika aplikasi ditutup
    #     if self.backsound:
    #         self.backsound.stop()

if __name__ == '__main__':
    KuisHewanApp().run()
