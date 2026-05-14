# ============================================================
#  SISTEM REKOMENDASI FILM - Content-Based Filtering
#  Dibuat dengan Python + scikit-learn
# ============================================================
#
#  CARA KERJA (mudah dipahami):
#  1. Kita punya data film dengan genre & deskripsi
#  2. Kita ubah teks genre+deskripsi jadi angka (TF-IDF)
#  3. Kita hitung seberapa "mirip" setiap film satu sama lain
#  4. Ketika user pilih film, kita cari film yang paling mirip
#
# ============================================================

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import ast

# ── 1. LOAD DATA ──────────────────────────────────────────────
def load_data(filepath):
    """Membaca dataset film dari file CSV."""
    
    df = pd.read_csv(filepath)
    print(df.isnull().sum())

    # Isi data kosong dengan string kosong
    df = df.fillna('')

    # Bersihin genre JSON jadi text biasa
    def clean_genre(text):
        genres = ast.literal_eval(text)
        return ' '.join([g['name'] for g in genres])

    df['genre'] = df['genre'].apply(clean_genre)

    print(f"✅ Dataset berhasil dimuat: {len(df)} film ditemukan\n")
    
    return df


# ── 2. BUAT FITUR GABUNGAN ────────────────────────────────────
def build_features(df):
    """
    Menggabungkan kolom 'genre' dan 'description' jadi satu teks.
    Genre diberi bobot lebih dengan cara diulang 2x
    agar genre lebih berpengaruh saat menghitung kemiripan.
    """
    df = df.copy()
    df['features'] = df['genre'].str.replace(' ', '_') + ' ' + \
                     df['genre'].str.replace(' ', '_') + ' ' + \
                     df['description']
    return df


# ── 3. HITUNG KEMIRIPAN (TF-IDF + Cosine Similarity) ─────────
def build_similarity_matrix(df):
    """
    TF-IDF = cara mengubah teks jadi angka.
    - TF  (Term Frequency)  : seberapa sering kata muncul di film ini
    - IDF (Inverse Doc Freq): seberapa langka kata itu di semua film
    - Hasilnya: kata yang penting & jarang = nilai tinggi

    Cosine Similarity = cara mengukur kemiripan antara dua film.
    - Nilai 1.0 = identik
    - Nilai 0.0 = tidak mirip sama sekali
    """
    print("🔧 Membangun model TF-IDF...")

    tfidf = TfidfVectorizer(
        stop_words=None,   # kita tidak filter kata karena pakai Bahasa campuran
        ngram_range=(1, 2) # pakai kombinasi 1-2 kata agar lebih akurat
    )

    # Ubah teks jadi matrix angka
    tfidf_matrix = tfidf.fit_transform(df['features'])

    # Hitung kemiripan antar semua film
    similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)

    print(f"✅ Model selesai! Matrix kemiripan: {similarity.shape[0]}x{similarity.shape[1]} film\n")
    return similarity


# ── 4. FUNGSI REKOMENDASI ─────────────────────────────────────
def get_recommendations(movie_title, df, similarity_matrix, top_n=5):
    """
    Mencari film yang paling mirip dengan film pilihan user.

    Parameter:
    - movie_title      : judul film yang dipilih user
    - df               : dataframe berisi semua film
    - similarity_matrix: matrix kemiripan yang sudah dibuat
    - top_n            : berapa banyak rekomendasi yang mau ditampilkan
    """

    # Cari index film di dataset
    # str.lower() agar pencarian tidak case-sensitive
    titles_lower = df['title'].str.lower()
    query_lower  = movie_title.strip().lower()

    # Cek apakah film ada di dataset
    if query_lower not in titles_lower.values:
        print(f"❌ Film '{movie_title}' tidak ditemukan di database.")
        print("💡 Tip: Ketik nama film dengan benar (tidak harus huruf besar).\n")
        return None

    # Ambil index baris film tersebut
    idx = titles_lower[titles_lower == query_lower].index[0]

    # Ambil skor kemiripan film ini dengan semua film lain
    scores = list(enumerate(similarity_matrix[idx]))

    # Urutkan dari yang paling mirip (descending)
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    # Ambil top_n film, skip index 0 karena itu film itu sendiri (skor = 1.0)
    top_scores = scores[1 : top_n + 1]

    # Ambil judul & genre film yang direkomendasikan
    results = []
    for i, (film_idx, score) in enumerate(top_scores):
        results.append({
            'rank'       : i + 1,
            'title'      : df.iloc[film_idx]['title'],
            'genre'      : df.iloc[film_idx]['genre'],
            'similarity' : round(score * 100, 1),  # ubah ke persen
            'description': df.iloc[film_idx]['description']
        })

    return results


# ── 5. TAMPILAN DI TERMINAL ───────────────────────────────────
def display_recommendations(movie_title, recommendations, df):
    """Menampilkan hasil rekomendasi dengan format yang rapi."""

    # Tampilkan info film yang dipilih
    chosen = df[df['title'].str.lower() == movie_title.strip().lower()].iloc[0]
    print("=" * 60)
    print(f"🎬  FILM YANG KAMU PILIH:")
    print(f"    {chosen['title']}")
    print(f"    Genre : {chosen['genre']}")
    print(f"    Sinopsis: {chosen['description'][:80]}...")
    print("=" * 60)
    print(f"\n🍿  REKOMENDASI FILM SERUPA:\n")

    for rec in recommendations:
        bar_len   = int(rec['similarity'] / 5)  # visual bar kemiripan
        bar       = "█" * bar_len + "░" * (20 - bar_len)
        print(f"  {rec['rank']}. {rec['title']}")
        print(f"     Genre      : {rec['genre']}")
        print(f"     Kemiripan  : [{bar}] {rec['similarity']}%")
        print(f"     Sinopsis   : {rec['description'][:80]}...")
        print()

    print("=" * 60)


# ── 6. TAMPILKAN SEMUA FILM ───────────────────────────────────
def show_all_movies(df):
    """Menampilkan daftar semua film beserta genrenya."""
    print("\n📋  DAFTAR SEMUA FILM YANG TERSEDIA:\n")
    for i, row in df.iterrows():
        print(f"  {i+1:2}. {row['title']:<30} | {row['genre']}")
    print()


# ── 7. PROGRAM UTAMA ──────────────────────────────────────────
def main():
    print("\n" + "=" * 60)
    print("   🎥  SISTEM REKOMENDASI FILM  🎥")
    print("   Content-Based Filtering dengan TF-IDF")
    print("=" * 60 + "\n")

    # Path ke dataset
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath   = os.path.join(script_dir, 'movies.csv')

    # Load data & bangun model
    df         = load_data(filepath)
    df         = build_features(df)
    sim_matrix = build_similarity_matrix(df)

    # Loop utama
    while True:
        print("\nApa yang ingin kamu lakukan?")
        print("  [1] Lihat semua film")
        print("  [2] Cari rekomendasi film")
        print("  [0] Keluar\n")

        choice = input("Pilih (0/1/2): ").strip()

        if choice == '0':
            print("\n👋 Sampai jumpa! Selamat menonton!\n")
            break

        elif choice == '1':
            show_all_movies(df)

        elif choice == '2':
            show_all_movies(df)
            user_input = input("Ketik nomor ATAU judul film yang kamu suka: ").strip()

            if not user_input:
                print("❗ Input tidak boleh kosong.")
                continue

            # Cek apakah user input angka (nomor urut)
            if user_input.isdigit():
                nomor = int(user_input)
                if 1 <= nomor <= len(df):
                    movie = df.iloc[nomor - 1]['title']
                    print(f"✅ Film dipilih: {movie}")
                else:
                    print(f"❗ Nomor harus antara 1 dan {len(df)}.")
                    continue
            else:
                movie = user_input

            try:
                n_input = input("Berapa rekomendasi yang kamu mau? (default 5): ").strip()
                n = int(n_input) if n_input else 5
            except ValueError:
                print("⚠️  Input tidak valid, pakai default 5.")
                n = 5

            recs = get_recommendations(movie, df, sim_matrix, top_n=n)

            if recs:
                display_recommendations(movie, recs, df)

        else:
            print("❗ Pilihan tidak valid. Ketik 0, 1, atau 2.")


# ── JALANKAN ──────────────────────────────────────────────────
if __name__ == "__main__":
    main()