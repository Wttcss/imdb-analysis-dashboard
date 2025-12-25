
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
