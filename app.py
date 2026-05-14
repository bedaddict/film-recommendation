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

/* BACKGROUND */
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

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 2px solid #FACC15;
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
}

/* BUTTON HOVER */
.stButton > button:hover {
    transform: scale(1.03);
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


selected_movie = st.sidebar.text_input(
    "🎬 Ketik nama film favoritmu:",
    placeholder="Contoh: Interstellar, Avatar, Batman..."
)

num_recommendations = st.sidebar.slider(
    "Jumlah rekomendasi:",
    min_value=1,
    max_value=10,
    value=5
)

recommend_button = st.sidebar.button("Cari Rekomendasi")

# ======================================================
# MAIN CONTENT
# ======================================================

if recommend_button:

    # validasi input kosong
    if selected_movie.strip() == "":
        st.warning("Masukin nama film dulu yaa")
        st.stop()

    # ambil rekomendasi
    recommendations = get_recommendations(
        selected_movie,
        df,
        sim_matrix,
        top_n=num_recommendations
    )

    # tampilkan judul
    st.subheader(f"🍿 Film mirip dengan: {selected_movie}")

    # kalau ada hasil
    if recommendations:

        for rec in recommendations:

            with st.container():

                st.markdown(f"""
                ### {rec['rank']}. {rec['title']}
                """)

                st.write(f"Genre: {rec['genre']}")

                st.write(f"Kemiripan: {rec['similarity']}%")

                st.write(rec['description'])

                st.divider()

else:

    st.info("Ketik nama film favoritmu lalu klik tombol rekomendasi")
