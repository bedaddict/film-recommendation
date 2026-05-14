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
# CUSTOM CSS (TEMA KUNING)
# ======================================================

st.markdown(
    """
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
    """,
    unsafe_allow_html=True
)

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
    st.info("👈 Pilih film di sidebar lalu klik tombol rekomendasi")