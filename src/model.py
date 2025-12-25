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
