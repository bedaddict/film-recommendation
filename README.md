# 🎥 Sistem Rekomendasi Film
### Content-Based Filtering dengan Python & scikit-learn

---

## 📁 Struktur File

```
movie_recommender/
│
├── recommender.py    ← Program utama (jalankan ini!)
├── movies.csv        ← Database film (bisa kamu tambah sendiri)
├── requirements.txt  ← Daftar library yang dibutuhkan
└── README.md         ← Panduan ini
```

---

## 🚀 Cara Menjalankan

### Langkah 1 — Install library yang dibutuhkan
Buka terminal / command prompt, lalu ketik:
```bash
pip install -r requirements.txt
```

### Langkah 2 — Jalankan programnya
```bash
python recommender.py
```

### Langkah 3 — Ikuti menu di layar
```
Apa yang ingin kamu lakukan?
  [1] Lihat semua film
  [2] Cari rekomendasi film
  [0] Keluar
```

---

## 🧠 Cara Kerja (Penjelasan Mudah)

### 1. TF-IDF (Term Frequency - Inverse Document Frequency)
Cara mengubah teks (genre & deskripsi film) menjadi angka agar komputer bisa membandingkannya.

- **TF**: Seberapa sering sebuah kata muncul di film ini?
- **IDF**: Seberapa langka kata itu di semua film?
- Kata yang sering muncul DAN langka = nilai tinggi = penting!

**Contoh:**
- Kata "Action" muncul di banyak film → IDF rendah
- Kata "Gotham" hanya di film Batman → IDF tinggi → lebih berpengaruh

### 2. Cosine Similarity
Cara mengukur seberapa mirip dua film berdasarkan nilai TF-IDF mereka.

- Nilai **1.0** = Film identik
- Nilai **0.5** = Agak mirip
- Nilai **0.0** = Tidak mirip sama sekali

**Analogi:** Bayangkan setiap film adalah panah (vektor) di ruang besar. Cosine similarity mengukur sudut antara dua panah. Semakin kecil sudutnya → semakin mirip filmnya.

### 3. Alur Lengkap
```
Data Film (teks)
      ↓
Gabungkan genre + deskripsi
      ↓
TF-IDF → ubah teks jadi angka
      ↓
Cosine Similarity → hitung kemiripan semua film
      ↓
User pilih film → cari yang paling mirip
      ↓
Tampilkan rekomendasi! 🎬
```

---

## ➕ Cara Menambah Film Baru

Buka file `movies.csv` dengan Excel atau teks editor, lalu tambah baris baru dengan format:

```
Judul Film,Genre1 Genre2 Genre3,Deskripsi singkat film
```

**Contoh:**
```
Avatar,Action Adventure Sci-Fi,Seorang mantan marinir dikirim ke planet Pandora dan jatuh cinta dengan penduduk aslinya
```

**Tips genre yang bisa kamu pakai:**
`Action, Adventure, Animation, Biography, Comedy, Crime, Documentary, Drama, Family, Fantasy, History, Horror, Music, Mystery, Romance, Sci-Fi, Thriller`

---

## 🔧 Kustomisasi

Kamu bisa ubah beberapa hal di `recommender.py`:

| Baris | Yang bisa diubah | Contoh |
|-------|-----------------|--------|
| `ngram_range=(1, 2)` | Kombinasi kata (1=satu kata, 2=dua kata) | `(1, 3)` untuk tiga kata |
| `top_n=5` | Jumlah rekomendasi default | `top_n=10` |
| Genre diulang 2x | Bobot genre vs deskripsi | Ubah jadi 3x untuk lebih fokus ke genre |

---

## 📚 Library yang Digunakan

| Library | Kegunaan |
|---------|----------|
| `pandas` | Membaca dan mengolah data CSV |
| `scikit-learn` | TF-IDF dan Cosine Similarity |
| `numpy` | Operasi matematika (dipakai scikit-learn di balik layar) |

---

## 🌱 Langkah Selanjutnya (jika mau berkembang)

1. **Tambah data lebih banyak** → Download dataset dari [Kaggle TMDB](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)
2. **Coba Collaborative Filtering** → Rekomendasi berdasarkan rating user lain
3. **Buat Web App** → Pakai Flask atau Streamlit agar ada tampilannya
4. **Tambah fitur rating** → User bisa kasih nilai, sistem makin pintar

---

*Selamat belajar Machine Learning! 🚀*
