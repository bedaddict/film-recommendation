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

/* BACKGROUND UTAMA */
.stApp {
    background: linear-gradient(
        135deg,
        #0F172A 0%,
        #1E293B 50%,
        #111827 100%
    );
    color: white;
}

/* TITLE */
h1 {
    color: #FACC15 !important;
    font-weight: 800;
    text-align: center;
    font-size: 52px;
}

/* SUBTITLE */
h2, h3 {
    color: white !important;
}

/* TEXT */
p, label, div {
    color: white;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 2px solid #FACC15;
}

/* SIDEBAR TITLE */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #FACC15 !important;
}

/* CARD FILM */
.movie-card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);

    padding: 25px;
    border-radius: 20px;

    border: 1px solid rgba(255,255,255,0.15);

    margin-bottom: 20px;

    transition: 0.3s ease;
}

/* HOVER CARD */
.movie-card:hover {
    transform: translateY(-5px);
    border: 1px solid #FACC15;
    box-shadow: 0 10px 30px rgba(250,204,21,0.25);
}

/* JUDUL FILM */
.movie-card h3 {
    color: #FACC15 !important;
    margin-bottom: 10px;
}

/* GENRE */
.genre {
    color: #CBD5E1;
    font-size: 14px;
    margin-bottom: 8px;
}

/* SIMILARITY */
.similarity {
    color: #FACC15;
    font-weight: bold;
    font-size: 16px;
    margin-bottom: 10px;
}

/* BUTTON */
.stButton > button {
    background: linear-gradient(
        90deg,
        #FACC15,
        #EAB308
    );

    color: black;
    font-weight: bold;

    border: none;
    border-radius: 12px;

    padding: 10px 20px;

    transition: 0.3s ease;
}

/* BUTTON HOVER */
.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0 5px 20px rgba(250,204,21,0.4);
}

/* SELECTBOX */
div[data-baseweb="select"] > div {
    background-color: #1E293B;
    color: white;
    border-radius: 10px;
}

/* SLIDER */
.stSlider {
    color: #FACC15;
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
