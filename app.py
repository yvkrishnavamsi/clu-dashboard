import streamlit as st
import pandas as pd
import plotly.express as px
import re

st.set_page_config(page_title="CLU Applications Dashboard", layout="wide")
st.title("CLU Applications Dashboard - Andhra Pradesh")

sheet_url = "https://docs.google.com/spreadsheets/d/1_BwfciEui4JuSs7fdRV9BPJupBcVFUs2A61YRASmzb8/export?format=csv"

@st.cache_data(ttl=600)
def load_data():
    df = pd.read_csv(sheet_url)
    return df

raw_df = load_data()

# Parse totals from headers
def extract_count(col_name):
    match = re.search(r'-\s*(\d+)', str(col_name))
    return int(match.group(1)) if match else 0

ulb_total = extract_count(raw_df.columns[1]) if len(raw_df.columns) > 1 else 0
uda_total = extract_count(raw_df.columns[2]) if len(raw_df.columns) > 2 else 0
ltp_total = extract_count(raw_df.columns[3]) if len(raw_df.columns) > 3 else 0
dtcp_total = extract_count(raw_df.columns[4]) if len(raw_df.columns) > 4 else 0
govt_total = extract_count(raw_df.columns[5]) if len(raw_df.columns) > 5 else 0

total = ulb_total + uda_total + ltp_total + dtcp_total + govt_total

col1, col2 = st.columns([6,1])
with col2:
    if st.button("🔄 Refresh"):
        st.cache_data.clear()
        st.rerun()

# Metrics from header totals
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Pending", total)
col2.metric("Pending with ULB", ulb_total)
col3.metric("Pending with UDA", uda_total)
col4.metric("LTP Shortfall", ltp_total)
col5.metric("DT&CP + GOVT", dtcp_total + govt_total)

st.markdown("---")

# Chart from totals
chart_data = pd.DataFrame({
    'Status': ['ULB', 'UDA', 'LTP Shortfall', 'DT&CP', 'GOVT'],
    'Count': [ulb_total, uda_total, ltp_total, dtcp_total, govt_total]
})
fig = px.bar(chart_data, x='Status', y='Count', text='Count', title="Applications by Pending Authority")
st.plotly_chart(fig, use_container_width=True)

# Show raw table
st.subheader("Authority-wise Details")
st.dataframe(raw_df, use_container_width=True, hide_index=True)
