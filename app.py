```python
import streamlit as st
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

st.markdown("""
<style>

.stApp {
    background-color: #FFF8E7;
}

h1, h2, h3 {
    color: #F4B400;
    font-weight: bold;
}

.movie-card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    border: 2px solid #FFD54F;
    margin-bottom: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
}

.similarity {
    color: #E65100;
    font-weight: bold;
}

.genre {
    color: #795548;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

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

selected_movie = st.sidebar.selectbox(
    "Pilih film favoritmu:",
    sorted(df['title'].tolist())
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

    recommendations = get_recommendations(
        selected_movie,
        df,
        sim_matrix,
        top_n=num_recommendations
    )

    st.subheader(f"🍿 Film mirip dengan: {selected_movie}")

    if recommendations:

        for rec in recommendations:

            st.markdown(
                f"""
                <div class="movie-card">
                    <h3>{rec['rank']}. {rec['title']}</h3>
                    <p class="genre">🎭 Genre: {rec['genre']}</p>
                    <p class="similarity">🔥 Kemiripan: {rec['similarity']}%</p>
                    <p>{rec['description']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

else:

    st.info("👈 Pilih film di sidebar lalu klik tombol rekomendasi")
```
