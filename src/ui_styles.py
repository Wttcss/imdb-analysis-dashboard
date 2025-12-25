# =============================================================================
# 2. ONYX CSS SYSTEM (Pro Aesthetics)
# =============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;900&display=swap');

    /* GLOBAL */
    .stApp { background-color: #050505; color: #E5E5E5; font-family: 'Inter', sans-serif; }
    [data-testid="stSidebar"] { display: none; }
    #MainMenu, footer, header { visibility: hidden; }

    /* HERO */
    .hero {
        position: relative;
        height: 550px;
        width: 100%;
        background-size: cover;
        background-position: center 20%;
        border-radius: 0 0 24px 24px;
        margin-bottom: 40px;
        box-shadow: 0 20px 80px rgba(0,0,0,0.9);
        border-bottom: 1px solid #333;
    }
    .hero-overlay {
        position: absolute; top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(0deg, #050505 0%, rgba(5,5,5,0.85) 40%, rgba(5,5,5,0.1) 100%);
        border-radius: 0 0 24px 24px;
    }
    .hero-content { position: absolute; bottom: 60px; left: 60px; z-index: 10; max-width: 900px; }
    .hero-title {
        font-size: 5.5rem; font-weight: 900; line-height: 1; margin-bottom: 15px;
        text-shadow: 0 10px 40px rgba(0,0,0,1); color: white;
    }
    .hero-meta {
        font-size: 1.3rem; color: #ccc; font-weight: 500; display: flex; gap: 20px; align-items: center;
    }

    /* CARDS */
    .card-container {
        background: #111; border: 1px solid #222; border-radius: 12px;
        overflow: hidden; transition: transform 0.3s ease; height: 100%;
    }
    .card-container:hover {
        transform: translateY(-8px); border-color: #F5C518;
        box-shadow: 0 20px 50px rgba(245, 197, 24, 0.2);
    }
    .card-img {
        width: 100%; height: 400px; object-fit: cover; border-bottom: 1px solid #222;
    }
    .card-body { padding: 15px; text-align: center; }

    .card-title {
        font-weight: 700; font-size: 1.1rem; white-space: nowrap; overflow: hidden;
        text-overflow: ellipsis; color: white; margin: 0;
    }

    /* STATS ROW */
    .stats-container {
        display: flex; justify-content: space-between; align-items: center;
        border-top: 1px solid #222; padding-top: 10px; margin-top: 10px;
    }
    .stat-box { text-align: center; width: 48%; }
    .stat-label { font-size: 0.65rem; color: #666; font-weight: 700; letter-spacing: 1px; margin-bottom: 2px; }
    .stat-val { font-size: 0.95rem; font-weight: 700; color: #fff; }
    .stat-gold { color: #F5C518; }

    /* RANK BADGE */
    .rank-circle {
        position: absolute; top: 10px; left: 10px;
        width: 40px; height: 40px; border-radius: 50%;
        background: #F5C518; color: black; font-weight: 900;
        display: flex; align-items: center; justify-content: center;
        font-size: 1.2rem; box-shadow: 0 5px 15px rgba(0,0,0,0.5); z-index: 5;
    }

    /* METRICS & CHARTS */
    div[data-testid="stMetric"] {
        background: #0F0F0F; border: 1px solid #222; border-radius: 12px; padding: 20px; border-left: 4px solid #F5C518;
    }
    div[data-testid="stMetricValue"] { color: white; font-weight: 800; }

    /* TABS */
    .stTabs [data-baseweb="tab-list"] { gap: 24px; border-bottom: 1px solid #222; }
    .stTabs [data-baseweb="tab"] { color: #888; font-weight: 600; font-size: 1rem; border: none; background: transparent; }
    .stTabs [aria-selected="true"] { color: #F5C518; border-bottom: 2px solid #F5C518; }

    /* BUTTONS */
    .stButton > button {
        background: #F5C518; color: black; font-weight: 800; border-radius: 8px; border: none; width: 100%;
    }
    .stButton > button:hover { background: white; }
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #111 !important; color: white !important; border-radius: 8px !important; border: 1px solid #333 !important;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 5. UI LAYOUT
# =============================================================================
if 'data_loaded' not in st.session_state:
    st.markdown("""
    <div style="text-align:center; padding:80px 20px; background:radial-gradient(circle, #1A1A1A 0%, #050505 100%); border-radius:24px; border:1px solid #222;">
        <h1 style="color:#F5C518; font-size:3.5rem; margin-bottom:10px;">IMDb ONYX</h1>
        <p style="color:#ccc; font-size:1.2rem; margin-bottom:30px;">Strategic Box Office Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload 'dash.csv' to Unlock", type="csv")
    if uploaded_file:
        st.session_state['data_loaded'] = True
        st.session_state['file'] = uploaded_file
        st.rerun()
    st.stop()

df = load_data(st.session_state['file'])
if df.empty:
    st.error("Data Unreadable.")
    st.stop()

# HERO
top_movie = df.sort_values('revenue', ascending=False).iloc[0]
hero_img = get_smart_poster(top_movie['original_title'])

st.markdown(f"""
<div class="hero" style="background-image: url('{hero_img}');">
    <div class="hero-overlay"></div>
    <div class="hero-content">
        <span class="hero-tag">#1 All-Time</span>
        <h1 class="hero-title">{top_movie['original_title']}</h1>
        <div class="hero-meta">
            <span style="color:#F5C518; font-weight:800;">★ {top_movie['vote_average']}</span>
            <span>{int(top_movie['Year'])}</span>
            <span>{top_movie['main_genre']}</span>
            <span>${top_movie['revenue'] / 1e9:.2f} Billion</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# TABS
tab1, tab2, tab3 = st.tabs(["🏆 Top 10 Leaders", "📊 Strategic Analytics", "🧠 AI Simulator"])

