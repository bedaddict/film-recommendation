import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

from recommender import (
    load_data,
    build_features,
    build_similarity_matrix,
    get_recommendations
)

# ======================================================
# CONFIG PAGE
# ======================================================

st.set_page_config(
    page_title="Sistem Rekomendasi Film",
    page_icon="🎬",
    layout="wide"
)

# ======================================================
# CUSTOM CSS
# ======================================================

components.html(f"""
<div style="
    background: rgba(255,255,255,0.08);
    padding: 25px;
    border-radius: 20px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.1);
">

<h2 style="
    color:#FACC15;
">
{rec['rank']}. {rec['title']}
</h2>

<p style="
    color:#CBD5E1;
">
🎭 Genre: {rec['genre']}
</p>

<p style="
    color:#FACC15;
    font-weight:bold;
">
🔥 Kemiripan: {rec['similarity']}%
</p>

<p style="
    color:white;
">
{rec['description']}
</p>

</div>
""", height=260)

# ======================================================
# LOAD MODEL
# ======================================================

@st.cache_data
def load_model():

    df = load_data("movies.csv")

    df = build_features(df)

    sim_matrix = build_similarity_matrix(df)

    return df, sim_matrix

# Load data
df, sim_matrix = load_model()

# ======================================================
# HEADER
# ======================================================

st.title("🎬 Sistem Rekomendasi Film")

st.subheader("Content-Based Filtering dengan TF-IDF + Cosine Similarity")

st.divider()

# ======================================================
# SIDEBAR
# ======================================================

st.sidebar.header("⚙️ Pengaturan")

selected_movie = st.sidebar.text_input(
    "🎬 Ketik nama film favoritmu:",
    placeholder="Contoh: Avatar, Interstellar, Batman..."
)

num_recommendations = st.sidebar.slider(
    "Jumlah rekomendasi:",
    min_value=1,
    max_value=10,
    value=5
)

recommend_button = st.sidebar.button("🎥 Cari Rekomendasi")

# ======================================================
# MAIN CONTENT
# ======================================================

if recommend_button:

    # cek input kosong
    if selected_movie.strip() == "":
        st.warning("⚠️ Masukin nama film dulu yaa 😭")
        st.stop()

    # ambil rekomendasi
    recommendations = get_recommendations(
        selected_movie,
        df,
        sim_matrix,
        top_n=num_recommendations
    )

    st.subheader(f"🍿 Film mirip dengan: {selected_movie}")

    # tampilkan hasil
    if recommendations:

        for rec in recommendations:

            st.markdown(f"""
            <div class="movie-card">

                <h3>{rec['rank']}. {rec['title']}</h3>

                <p class="genre">
                    🎭 Genre: {rec['genre']}
                </p>

                <p class="similarity">
                    🔥 Kemiripan: {rec['similarity']}%
                </p>

                <p>
                    {rec['description']}
                </p>

            </div>
            """, unsafe_allow_html=True)

else:

    st.info("👈 Ketik nama film favoritmu lalu klik tombol rekomendasi")
