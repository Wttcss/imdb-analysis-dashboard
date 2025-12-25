# 🎬 IMDb Analysis & Interactive Dashboard

## Project Overview
This project performs an end-to-end analysis of movie metadata and delivers
an interactive dashboard for exploring box office performance, profitability,
and efficiency. The goal is to transform raw movie data into structured
insights and provide an analytical interface for decision support.

The final output is a Streamlit-based dashboard that enables dynamic
exploration of trends, comparisons, and simulated outcomes.

---

## Objectives
- Analyze key drivers of movie revenue and profitability  
- Evaluate return on investment (ROI) across different budget ranges  
- Identify high-performing genres and market patterns  
- Provide interactive, visual analytics through a dashboard  
- Simulate revenue outcomes using a machine learning model  

---

## Dataset
- **Source:** Public movie metadata (IMDb / TMDB-style data)
- **Level:** Movie-level records
- **Size:** Several thousand movies
- **Main Features:**
  - Budget
  - Revenue
  - Popularity
  - Runtime
  - Vote Average
  - Genre
  - Release Date

### Data Preparation
- Merged multiple CSV files into a single dataset  
- Parsed release dates and extracted release year  
- Cleaned missing and inconsistent values  
- Removed invalid records (zero or unrealistic budget/revenue)  
- Standardized categorical variables such as genre  

---

## Analysis Workflow
1. Data ingestion and validation  
2. Data cleaning and preprocessing  
3. Feature engineering (Profit, ROI, Budget tiers)  
4. Exploratory data analysis (EDA)  
5. Dashboard development using Streamlit  
6. Predictive modeling for revenue simulation  

---

## Dashboard Description
The Streamlit dashboard provides the following components:

### Executive Metrics
- Total box office revenue  
- Total profit  
- Average ROI  
- Average production budget  

### Leaderboards
- Top-grossing movies ranked by revenue  
- Visual presentation using posters and ratings  

### Strategic Analytics
- Budget vs revenue vs rating (3D visualization)  
- Genre-level profitability analysis  
- Budget efficiency and ROI trends  

### Interactive Exploration
- Dynamic filtering and hover-based insights  
- High-performance interactive visualizations  

---

## Machine Learning Component
A machine learning model is integrated to support scenario-based analysis.

- **Model:** Gradient Boosting Regressor  
- **Target Variable:** Revenue  
- **Input Features:**
  - Budget
  - Popularity
  - Runtime
  - Vote Average
  - Main Genre  

The model is used to simulate potential revenue and profit outcomes based
on hypothetical inputs.

> Note: The forecasting model is intended for analytical and educational
purposes only and should not be interpreted as financial advice.

---

