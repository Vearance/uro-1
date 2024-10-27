# Robots Duel

Program ini adalah sebuah permainan turn-based sederhana antar dua buah robot.
Repository ini terdiri dari dua buah file:
1. main.py: berfungsi sebagai program utama
2. robots.csv: berfungsi untuk menyimpan data dari robot

Setiap robot memiliki dua buah jenis serangan, yaitu basic attack dan ultimate.
Setiap robot dilengkapi stats seperti hitpoints, damage, defense, critical chance, speed, dan waktu charge ultimate.

## Fitur

- Memuat data robot dari file CSV.
- Membuat dan menyimpan robot baru ke file CSV.
- Memilih robot untuk bertarung.
- Mensimulasikan pertarungan turn-based berdasarkan speed.
- Mengetahui sisa hitpoints serta melacak jumlah serangan dan penggunaan ultimate dari masing-masing robot.

## Penjelasan Code

Class Robot -> atribut dari robot
- Hitpoints: Total darah.
- Damage: Kekuatan serangan.
- Defense: Mengurangi damage yang diterima.
- Critical Hit Chance: Peluang serangan lebih kuat 1,5x dari damage normal.
- Speed: Menentukan robot mana yang menyerang lebih dulu dan peluang serangan tambahan.
- Ultimate Charge: Jumlah ronde untuk charge ultimate.
- Ultimate Power: Multiplier damage ultimate.

Class Battle -> mengatur sistem pertarungan
- Menentukan robot yang menyerang lebih dulu berdasarkan speed. -> Hanya ada 2 robot yang masuk ke battle.
- Menjalankan serangan dan menghitung damage, termasuk critical hit dan pengurangan damage oleh defense.
- Otomatis menggunakan ultimate jika sudah tercharge penuh.
- Perhitungan extra attack. -> Jika residu dari speed (robot1-robot2, stacked) melebihi speed lawan, maka akan ada extra attack.
- Memberikan hasil pertarungan, termasuk sisa hitpoints serta jumlah basic attack dan ultimate.

Class Game -> mengelola alur permainan
- Load robot dari file CSV.
- Pilihan membuat robot baru dan menyimpannya ke dalam file CSV.
- Menampilkan robot yang dapat untuk dipilih.
- Memulai pertarungan antara dua robot yang dipilih.

## Format File CSV

File 'robots.csv' harus mengikuti format ini:

| name    | hitpoints | damage | defense | crit | speed | ultimate_charge | ultimate_power |
|---------|-----------|--------|---------|------|-------|-----------------|----------------|
| RoboOne | 50        | 30     | 10      | 0.1  | 25    | 5               | 3              |
| RoboTwo | 50        | 25     | 12      | 0.05 | 20    | 4               | 3              |

## Cara Bermain

1. Run 'main.py' untuk memulai permainan, pastikan ada file 'robots.csv' dalam repository.
2. Ada opsi membuat robot baru.
3. Pilih dua robot yang akan digunakan dalam pertarungan.
4. Robot akan bertarung secara bergiliran. Status pemenang didapatkan ketika berhasil mengurangi hitpoints lawan hingga 0.
5. Setelah pertarungan selesai, sisa hitpoints pemenang serta statistik pertarungan (jumlah serangan dan ultimate) akan ditampilkan.
