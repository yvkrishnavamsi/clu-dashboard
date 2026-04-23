import streamlit as st
import pandas as pd
import plotly.express as px
import re

st.set_page_config(page_title="CLU Applications Dashboard", layout="wide")
st.title("CLU Applications Dashboard - Andhra Pradesh")

sheet_url = "https://docs.google.com/spreadsheets/d/1_BwfciEui4JuSs7fdRV9BPJupBcVFUs2A61YRASmzb8/export?format=csv"

@st.cache_data(ttl=600)
def load_data():
    try:
        df = pd.read_csv(sheet_url)
        return df
    except Exception as e:
        st.error(f"Error loading Google Sheet: {e}")
        return pd.DataFrame()

raw_df = load_data()

col1, col2 = st.columns([6,1])
with col2:
    if st.button("🔄 Refresh"):
        st.cache_data.clear()
        st.rerun()

if raw_df.empty:
    st.warning("Could not load data. Check Sheet sharing settings.")
    st.stop()

# Extract totals from column headers like "Pending with ULB - 15"
def extract_count(col_name):
    match = re.search(r'-\s*(\d+)', str(col_name))
    return int(match.group(1)) if match else 0

# Get counts from headers - adjust index if your columns shift
cols = raw_df.columns.tolist()
ulb_total = extract_count(cols[1]) if len(cols) > 1 else 0
uda_total = extract_count(cols[2]) if len(cols) > 2 else 0
ltp_total = extract_count(cols[3]) if len(cols) > 3 else 0
dtcp_total = extract_count(cols[4]) if len(cols) > 4 else 0
govt_total = extract_count(cols[5]) if len(cols) > 5 else 0

total_pending = ulb_total + uda_total + ltp_total + dtcp_total + govt_total

# Top metrics
st.subheader("Status Summary")
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Total Pending", total_pending)
col2.metric("ULB", ulb_total)
col3.metric("UDA", uda_total)
col4.metric("LTP Shortfall", ltp_total)
col5.metric("DT&CP", dtcp_total)
col6.metric("GOVT", govt_total)

st.markdown("---")

# Bar chart
col1, col2 = st.columns(2)
with col1:
    st.subheader("Pendency by Authority")
    chart_data = pd.DataFrame({
        'Authority': ['ULB', 'UDA', 'LTP', 'DT&CP', 'GOVT'],
        'Count': [ulb_total, uda_total, ltp_total, dtcp_total, govt_total]
    })
    fig = px.bar(chart_data, x='Authority', y='Count', text='Count', color='Authority')
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Distribution")
    fig = px.pie(chart_data, values='Count', names='Authority', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

# Raw data table
st.subheader("Authority-wise Details")
st.dataframe(raw_df, use_container_width=True, hide_index=True)
st.caption("Data auto-refreshes every 10 minutes. Click 🔄 Refresh for instant update.")
# Detailed table
st.subheader("Detailed Status Report")
st.dataframe(df, use_container_width=True, hide_index=True)

