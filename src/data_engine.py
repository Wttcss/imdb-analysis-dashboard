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
