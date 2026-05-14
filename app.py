# ======================================================
# HEADER
# ======================================================

st.title("🎬 Sistem Rekomendasi Film")
st.write("Content-Based Filtering dengan TF-IDF + Cosine Similarity")

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
