# Animal Guessing Game

## Deskripsi

Game Tebak Gambar Hewan adalah aplikasi edukatif interaktif yang dikembangkan menggunakan framework Kivy. Game ini menantang pemain untuk mengidentifikasi berbagai hewan melalui petunjuk visual, dirancang untuk menghibur sekaligus mendidik pemain dari segala usia dalam menguji pengetahuan mereka tentang dunia hewan.

## Fitur Utama

### 🎮 Menu dan Navigasi
- **Menu Utama**: Interface yang intuitif dengan opsi "Mulai Game"
- **Mode Permainan**: Pilihan antara "Hewan Darat" dan "Hewan Air"

### 🎯 Gameplay
- **Identifikasi Visual**: Pemain disajikan gambar hewan untuk ditebak
- **Sistem Poin**: Setiap jawaban benar dihargai dengan poin
- **Pelacakan Skor**: Sistem skor kompetitif yang melacak performa pemain

### 🔊 Audio & Multimedia
- **Efek Suara**: 
  - Suara perayaan untuk jawaban benar
  - Suara berbeda untuk jawaban salah
- **Musik Latar**: Background music yang dimainkan sepanjang permainan

### 📊 Sistem Penilaian
- **Ringkasan Skor**: Total poin yang diperoleh di akhir permainan
- **Motivasi Replay**: Mendorong pemain untuk meningkatkan performa

## Teknologi yang Digunakan

- **Framework**: Kivy (Python)
- **Platform**: Cross-platform (Android, iOS, Desktop)
- **Bahasa Pemrograman**: Python

## Struktur Proyek

```
animal-guessing-game/
├── main.py
├── assets/
│   ├── images/
│   │   ├── land_animals/
│   │   └── water_animals/
│   ├── sounds/
│   │   ├── correct.wav
│   │   ├── wrong.wav
│   │   └── background_music.mp3
│   └── fonts/
├── screens/
│   ├── menu_screen.py
│   ├── game_screen.py
│   └── score_screen.py
└── README.md
```

## Instalasi

### Prasyarat
```bash
pip install kivy
pip install kivy[base]
```

### Menjalankan Game
```bash
python main.py
```

## Cara Bermain

1. **Mulai Game**: Tekan tombol "Mulai Game" di menu utama
2. **Pilih Mode**: Pilih antara "Hewan Darat" atau "Hewan Air"
3. **Tebak Hewan**: Lihat gambar yang ditampilkan dan pilih jawaban yang benar
4. **Dapatkan Poin**: Setiap jawaban benar akan menambah skor Anda
5. **Lihat Hasil**: Cek total skor di akhir permainan

## Fitur Teknis

### Manajemen State Game
- Pelacakan skor real-time
- Transisi antar layar yang smooth
- Pengelolaan data permainan yang efisien

### Integrasi Multimedia
- Dukungan format audio multiple
- Optimasi performa untuk mobile
- UI responsif untuk berbagai ukuran layar

### Cross-Platform Compatibility
- Kompatibel dengan Android, iOS, dan Desktop
- Adaptive UI untuk berbagai resolusi
- Performa yang dioptimalkan untuk perangkat mobile

## Kontribusi

Jika Anda ingin berkontribusi pada proyek ini:

1. Fork repository
2. Buat branch fitur baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## Pengembangan Selanjutnya

- [ ] Penambahan lebih banyak kategori hewan
- [ ] Mode multiplayer
- [ ] Sistem achievement dan badge
- [ ] Leaderboard global
- [ ] Animasi yang lebih interaktif
- [ ] Dukungan multiple bahasa

## Lisensi

Proyek ini dilisensikan di bawah MIT License - lihat file [LICENSE](LICENSE) untuk detail.

## Kontak

Untuk pertanyaan atau saran, silakan hubungi:
- Email: [your-email@example.com]
- GitHub: [your-username]

---

*Dibuat dengan ❤️ menggunakan Kivy Framework*