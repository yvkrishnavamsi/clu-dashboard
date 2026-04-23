import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CLU Applications Dashboard", layout="wide")
st.title("CLU Applications Dashboard - Andhra Pradesh")

# Your Google Sheet CSV link
sheet_url = "https://docs.google.com/spreadsheets/d/1_BwfciEui4JuSs7fdRV9BPJupBcVFUs2A61YRASmzb8/export?format=csv"

@st.cache_data(ttl=600)  # Auto-refresh every 10 minutes
def load_data():
    try:
        df = pd.read_csv(sheet_url)
        return df
    except Exception as e:
        st.error(f"Error loading data from Google Sheet: {e}")
        return pd.DataFrame()

df = load_data()

# Add refresh button for instant updates
col1, col2 = st.columns([6,1])
with col2:
    if st.button("🔄 Refresh"):
        st.cache_data.clear()
        st.rerun()

if df.empty:
    st.warning("No data found. Check your Google Sheet link and column names.")
    st.stop()

# --- Your dashboard code starts here ---
# Make sure your Google Sheet has columns: Type, Pending_With, Authority, Officer, Count

# Top metrics
total = df['Count'].sum()
ulb_pending = df[df['Pending_With'] == 'Pending with ULB']['Count'].sum()
ltp_shortfall = df[df['Pending_With'] == 'LTP Shortfall']['Count'].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Applications", total)
col2.metric("Pending with ULB", ulb_pending)
col3.metric("LTP Shortfall", ltp_shortfall)
col4.metric("Other Pending", total - ulb_pending - ltp_shortfall)

st.markdown("---")

# Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Regular vs CLU SUO MOTU")
    pie_data = df.groupby('Type')['Count'].sum().reset_index()
    fig = px.pie(pie_data, values='Count', names='Type', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Pending Status Breakdown")
    bar_data = df.groupby('Pending_With')['Count'].sum().reset_index()
    fig = px.bar(bar_data, x='Pending_With', y='Count', text='Count')
    fig.update_layout(xaxis_title="", yaxis_title="Count")
    st.plotly_chart(fig, use_container_width=True)

# Detailed table
st.subheader("Detailed Status Report")
st.dataframe(df, use_container_width=True, hide_index=True)
