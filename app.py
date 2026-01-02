import streamlit as st
import pandas as pd
import os

# 1. THIS MUST BE THE FIRST LINE AND ONLY APPEAR ONCE
st.set_page_config(page_title="Euprime Lead Dashboard", layout="wide")

# --- 2. DATA LOADING ---
@st.cache_data
def load_scored_data():
    file_path = "leads_scored.csv"
    if not os.path.exists(file_path):
        return None
    try:
        data = pd.read_csv(file_path)
        # Ensure Probability is numeric for the slider to work
        data['Probability'] = pd.to_numeric(data['Probability'], errors='coerce').fillna(0)
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# --- 3. DASHBOARD UI ---
st.title("🧬 Business Developer AI Agent")
st.markdown("### 3D In-Vitro Model: Qualified Lead Generation")

df = load_scored_data()

if df is not None and not df.empty:
    # --- SIDEBAR FILTERS ---
    st.sidebar.header("Filter Leads")
    
    # 1. Probability Slider
    min_score = st.sidebar.slider("Minimum Match Probability %", 0, 100, 0)
    
    # 2. Location Filter
    loc_col = 'Location (Person)'
    if loc_col in df.columns:
        locations = sorted(df[loc_col].dropna().unique().tolist())
        selected_locs = st.sidebar.multiselect("Filter by Location", options=locations)
    else:
        selected_locs = []

    # 3. Search Box
    search_query = st.sidebar.text_input("Search Company or Title")

    # --- APPLY FILTERS ---
    filtered_df = df[df['Probability'] >= min_score]
    
    if selected_locs:
        filtered_df = filtered_df[filtered_df[loc_col].isin(selected_locs)]
        
    if search_query:
        filtered_df = filtered_df[
            filtered_df['Company'].str.contains(search_query, case=False, na=False) |
            filtered_df['Title'].str.contains(search_query, case=False, na=False)
        ]

    # --- METRICS ---
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Leads", len(filtered_df))
    m2.metric("High Match (80%+)", len(filtered_df[filtered_df['Probability'] >= 80]))
    m3.metric("Avg Probability", f"{filtered_df['Probability'].mean():.1f}%" if not filtered_df.empty else "0%")

    # --- TABLE DISPLAY ---
    st.subheader("Qualified Leads List")
    st.dataframe(
        filtered_df,
        column_config={
            "Probability": st.column_config.ProgressColumn(
                "Match Score", format="%d%%", min_value=0, max_value=100
            ),
            "LinkedIn": st.column_config.LinkColumn("LinkedIn Profile"),
        },
        use_container_width=True,
        hide_index=True
    )
    
    # Download Button
    st.download_button(
        "📥 Download Current View (CSV)",
        data=filtered_df.to_csv(index=False),
        file_name="qualified_leads_filtered.csv",
        mime="text/csv"
    )

else:
    st.warning("📡 No data found. Please ensure 'leads_scored.csv' is in your folder.")
    if st.button("Retry Load"):
        st.rerun()

