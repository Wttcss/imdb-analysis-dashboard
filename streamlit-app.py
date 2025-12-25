import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
import urllib.parse
import numpy as np

# =============================================================================
# 1. APP CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="IMDb Analysis Dashboard",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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
# 3. 4K POSTER DATABASE
# =============================================================================
POSTER_DB = {
    "avatar": "https://image.tmdb.org/t/p/original/kyeqWdyUXW608qlYkRqosgbbJyK.jpg",
    "titanic": "https://image.tmdb.org/t/p/original/9xjZS2rlVxm8SFx8kPC3aIGCOYQ.jpg",
    "the avengers": "https://image.tmdb.org/t/p/original/RYMX2wcKCBAr24UyPD7xwmjaTn.jpg",
    "jurassic world": "https://image.tmdb.org/t/p/original/uXZYawqUsChGSj54wcuBtEdUJbh.jpg",
    "furious 7": "https://upload.wikimedia.org/wikipedia/en/b/b8/Furious_7_poster.jpg",
    "avengers: age of ultron": "https://image.tmdb.org/t/p/original/4ssDuvEDkSArWEdyBl2X5EHvYKU.jpg",
    "frozen": "https://upload.wikimedia.org/wikipedia/en/0/05/Frozen_%282013_film%29_poster.jpg",
    "iron man 3": "http://3.bp.blogspot.com/-E-p3JrvqpEA/UX65iuaX6EI/AAAAAAAAFNQ/mGz7Y_-Ctv0/s1600/Iron_Man_3_New_Poster_Final_Latino_V2_Cine_1.jpg",
    "minions": "https://resizing.flixster.com/8KeqKZfuOFJT6OVZLnCgmwthTI4=/206x305/v2/https://resizing.flixster.com/-XZAfHZM39UwaGJIFWKAE8fS0ak=/v3/t/assets/p11376954_p_v13_bc.jpg",
    "captain america: civil war": "https://image.tmdb.org/t/p/original/rAGiXaUfPzY7CDEyNKUofk3Kw2e.jpg",
    "transformers: dark of the moon": "https://image.tmdb.org/t/p/original/kvXLZqY0Ngl1XSw7EaMQO0C1CCj.jpg",
    "the lord of the rings: the return of the king": "https://image.tmdb.org/t/p/original/rCzpDGLbOoPwLjy3OAm5NUPOznC.jpg",
    "skyfall": "https://image.tmdb.org/t/p/original/u29Zgu6B47C56X5X5fM1rQ5q.jpg",
    "transformers: age of extinction": "https://image.tmdb.org/t/p/original/ykFh9raB1K6Zf9Wl5sZg1w9eX.jpg",
    "the dark knight rises": "https://image.tmdb.org/t/p/original/85cWkCVftiVs0BV86x0nl1phPTv.jpg",
    "toy story 3": "https://image.tmdb.org/t/p/original/AbbXspMOwdvwWZgVX0dadPrM9Ff.jpg",
    "pirates of the caribbean: dead man's chest": "https://image.tmdb.org/t/p/original/uXEqmloGyP7UXAwd_x7H9C.jpg",
    "pirates of the caribbean: on stranger tides": "https://image.tmdb.org/t/p/original/w2PMyoyLU22YvrGKzsmVM0fKd.jpg",
    "alice in wonderland": "https://image.tmdb.org/t/p/original/1HtWyQsp5O6l9K8sV56hR3aVlZl.jpg",
    "the hobbit: an unexpected journey": "https://image.tmdb.org/t/p/original/yHA9Fc37VmpUA5UncTxxo3rTGVA.jpg",
    "the dark knight": "https://image.tmdb.org/t/p/original/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
    "star wars: the force awakens": "https://image.tmdb.org/t/p/original/wqnLdwVXoBjKibfR5TRBck12nJ1.jpg",
    "harry potter and the philosopher's stone": "https://image.tmdb.org/t/p/original/wuMc08IPKEatf9rnMNXvIDxqP4W.jpg",
}


def get_smart_poster(title):
    clean_title = str(title).strip().lower()
    if clean_title in POSTER_DB: return POSTER_DB[clean_title]
    for key in POSTER_DB:
        if key in clean_title or clean_title in key: return POSTER_DB[key]
    safe_title = urllib.parse.quote(str(title))
    return f"https://placehold.co/400x600/111/F5C518/png?text={safe_title}&font=roboto"


# =============================================================================
# 4. DATA ENGINE
# =============================================================================
@st.cache_data
def load_data(file):
    try:
        df = pd.read_csv(file)
        if 'release_date' in df.columns:
            df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
            df['Year'] = df['release_date'].dt.year
        else:
            df['Year'] = 0
        for c in ['budget', 'revenue', 'popularity', 'runtime', 'vote_average']:
            if c in df.columns: df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
        df = df[(df['budget'] > 1000) & (df['revenue'] > 0)]
        df['ROI'] = (df['revenue'] - df['budget']) / df['budget']
        df['profit'] = df['revenue'] - df['budget']
        df = df[df['main_genre'].notna() & (df['main_genre'] != '')]
        return df
    except:
        return pd.DataFrame()


@st.cache_resource
def train_model(df):
    try:
        # Features used for the app
        features = ['budget', 'popularity', 'runtime', 'vote_average', 'main_genre']
        X = df[features]
        # Target: Revenue (So we can calculate profit)
        y = df['revenue']

        pre = ColumnTransformer([
            ('num', SimpleImputer(strategy='median'), ['budget', 'popularity', 'runtime', 'vote_average']),
            ('cat', OneHotEncoder(handle_unknown='ignore'), ['main_genre'])
        ])

        # --- YOUR CUSTOM MODEL CONFIGURATION ---
        model = Pipeline([
            ('pre', pre),
            ('clf', GradientBoostingRegressor(
                n_estimators=300,
                learning_rate=0.05,
                max_depth=4,
                min_samples_leaf=10,
                random_state=42
            ))
        ])

        model.fit(X, y)
        return model
    except:
        return None


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

# --- TAB 1: TOP 10 LEADERBOARD (Annotated) ---
with tab1:
    st.markdown("### 🔥 The Billion Dollar Club")
    top_10 = df.sort_values('revenue', ascending=False).head(10).reset_index(drop=True)

    cols = st.columns(5)
    for idx, (i, row) in enumerate(top_10.iloc[:5].iterrows()):
        with cols[idx]:
            poster = get_smart_poster(row['original_title'])
            st.markdown(f"""
            <div class="card-container">
                <div class="rank-circle">{idx + 1}</div>
                <img src="{poster}" class="card-img">
                <div class="card-body">
                    <div class="card-title">{row['original_title']}</div>
                    <div class="stats-container">
                        <div class="stat-box">
                            <div class="stat-label">RATING</div>
                            <div class="stat-val">★ {row['vote_average']}</div>
                        </div>
                        <div style="border-left:1px solid #333; height:20px;"></div>
                        <div class="stat-box">
                            <div class="stat-label">REVENUE</div>
                            <div class="stat-val stat-gold">${row['revenue'] / 1e9:.2f}B</div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    cols2 = st.columns(5)
    for idx, (i, row) in enumerate(top_10.iloc[5:10].iterrows()):
        with cols2[idx]:
            poster = get_smart_poster(row['original_title'])
            st.markdown(f"""
            <div class="card-container">
                <div class="rank-circle">{idx + 6}</div>
                <img src="{poster}" class="card-img">
                <div class="card-body">
                    <div class="card-title">{row['original_title']}</div>
                    <div class="stats-container">
                        <div class="stat-box">
                            <div class="stat-label">RATING</div>
                            <div class="stat-val">★ {row['vote_average']}</div>
                        </div>
                        <div style="border-left:1px solid #333; height:20px;"></div>
                        <div class="stat-box">
                            <div class="stat-label">REVENUE</div>
                            <div class="stat-val stat-gold">${row['revenue'] / 1e9:.2f}B</div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# --- TAB 2: STRATEGIC ANALYTICS ---
with tab2:
    st.markdown("### 📊 Executive Decision Support")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Box Office", f"${df['revenue'].sum() / 1e9:.2f}B")
    c2.metric("Total Profit", f"${df['profit'].sum() / 1e9:.2f}B")
    c3.metric("Avg ROI", f"{df['ROI'].mean() * 100:.0f}%")
    c4.metric("Avg Budget", f"${df['budget'].mean() / 1e6:.0f}M")

    st.markdown("---")

    # 3D CUBE
    st.markdown("**🌌 Market Sweet Spot (3D Analysis)**")
    fig_3d = px.scatter_3d(df, x='budget', y='revenue', z='vote_average',
                           color='ROI', size='popularity', hover_name='original_title',
                           template='plotly_dark', color_continuous_scale='Turbo', height=600)
    fig_3d.update_layout(paper_bgcolor="rgba(0,0,0,0)", scene=dict(bgcolor="rgba(0,0,0,0)"))
    st.plotly_chart(fig_3d, use_container_width=True)

    col_a, col_b = st.columns(2)

    # PROFIT LEADERBOARD
    with col_a:
        st.markdown("**💰 Most Profitable Genres**")
        profit_by_genre = df.groupby('main_genre')['profit'].mean().sort_values(ascending=False).head(8).reset_index()
        fig_bar = px.bar(profit_by_genre, x='profit', y='main_genre', orientation='h',
                         template='plotly_dark', color='profit', color_continuous_scale='Greens')
        fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_bar, use_container_width=True)

    # BUDGET EFFICIENCY
    with col_b:
        st.markdown("**📉 Budget vs ROI Efficiency**")
        df['Budget_Bin'] = pd.cut(df['budget'], bins=10, labels=False)
        roi_trend = df.groupby('Budget_Bin')['ROI'].median().reset_index()
        fig_line = px.line(roi_trend, x='Budget_Bin', y='ROI', markers=True, template="plotly_dark")
        fig_line.update_traces(line_color='#F5C518', line_width=4)
        fig_line.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                               xaxis_title="Budget Tier (Low to High)", yaxis_title="Median ROI")
        st.plotly_chart(fig_line, use_container_width=True)

# --- TAB 3: AI STUDIO (Custom Model) ---
with tab3:
    st.markdown("### 🧠 Forecasting Studio")
    st.caption("Powered by Gradient Boosting Regressor (Custom Tuned)")

    model = train_model(df)

    if model:
        with st.container():
            c1, c2 = st.columns(2)
            with c1:
                b = st.number_input("Budget ($)", 1000000, 500000000, 100000000, step=1000000)
                g = st.selectbox("Genre", df['main_genre'].unique())
            with c2:
                p = st.slider("Hype Score", 0, 100, 50)
                v = st.slider("Target Rating", 1.0, 10.0, 7.0)

            if st.button("Run Forecast"):
                input_data = pd.DataFrame(
                    {'budget': [b], 'popularity': [p], 'runtime': [120], 'vote_average': [v], 'main_genre': [g]})
                pred = model.predict(input_data)[0]
                profit = pred - b
                m1, m2 = st.columns(2)
                m1.metric("Forecasted Revenue", f"${pred:,.0f}")
                m2.metric("Forecasted Profit", f"${profit:,.0f}", delta=f"{(profit / b) * 100:.0f}% ROI")
                if profit > 0: st.balloons()
#-----------------------------------------------------
# =============================================================================
# FOOTER
# =============================================================================
st.markdown("---")  # This adds a thin divider line

# We use 3 columns to center the content in the middle
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div style="text-align: center; font-family: 'Inter', sans-serif;">
        <p style="color: #888888; font-size: 14px; margin-bottom: 5px;">
            Designed & Built by <strong style="color: #E5E5E5;">[Faisal Abdulaziz]</strong>
        </p>
        <p style="font-size: 14px;">
            <a href="https://www.linkedin.com/in/faisal-abdulaziz-44145b323/" target="_blank" style="text-decoration: none; color: #F5C518; font-weight: 600; margin-right: 15px;">
                LinkedIn ↗
            </a>
            <a href="https://github.com/Wttcss" target="_blank" style="text-decoration: none; color: #F5C518; font-weight: 600;">
                GitHub ↗
            </a>
        </p>
    </div>
    """, unsafe_allow_html=True)


    # sometimes it gaves "data unreadable" at the Ai Simulator section [just refresh and it will run ]
