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
    page_icon="icon.jpg",
    layout="wide"
)

# ======================================================
# CUSTOM CSS
# ======================================================


st.markdown("""
<style>

/* BACKGROUND */
.stApp {
    background-color: #141414;
    color: white;
}

/* MAIN CONTENT */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* TITLE */
h1 {
    color: #E50914 !important;
    font-weight: 800;
    font-size: 52px;
}

/* SUBTITLE */
h2, h3 {
    color: white !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #000000;
    border-right: 2px solid #E50914;
}

/* SIDEBAR TEXT */
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* INPUT BOX */
.stTextInput input {
    background-color: #2b2b2b;
    color: white;
    border: 1px solid #E50914;
    border-radius: 10px;
}

/* SLIDER */
.stSlider {
    color: #E50914;
}

/* BUTTON */
.stButton > button {
    background-color: #E50914;
    color: white;

    font-weight: bold;

    border: none;
    border-radius: 10px;

    padding: 10px 20px;

    transition: 0.3s ease;
}

/* BUTTON HOVER */
.stButton > button:hover {
    background-color: #ff1f1f;
    transform: scale(1.03);
}

/* MOVIE CONTAINER */
[data-testid="stVerticalBlock"] {
    border-radius: 15px;
}

/* DIVIDER */
hr {
    border-color: rgba(255,255,255,0.1);
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

st.title("Sistem Rekomendasi Film")
st.subheader("Content-Based Filtering dengan TF-IDF + Cosine Similarity")

st.divider()

# ======================================================
# SIDEBAR
# ======================================================


selected_movie = st.sidebar.text_input(
    "Ketik nama film favoritmu:",
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

            st.markdown("""
            <div style="background: linear-gradient(90deg, rgba(229,9,20,0.15), rgba(229,9,20,0.08)); padding:18px; border-radius:12px; border:1px solid rgba(229,9,20,0.4); color:#ffb3b3; font-size:18px; font-weight:500;">
            Masukin nama film dulu yaa :)
            </div>
            """, unsafe_allow_html=True)

            st.stop()


    # ambil rekomendasi
    recommendations = get_recommendations(
        selected_movie,
        df,
        sim_matrix,
        top_n=num_recommendations
    )

    # tampilkan judul
    st.subheader(f"Film mirip dengan: {selected_movie}")

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
    st.markdown("""
        <div style="
    background-color: #1f1f1f;
    padding: 18px;
    border-radius: 12px;
    border-left: 5px solid #E50914;
    color: white;
    font-size: 18px;
     ">
       Ketik nama film favoritmu lalu klik tombol rekomendasi
       </div>
        """, unsafe_allow_html=True)
