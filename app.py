import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CLU Applications Dashboard", layout="wide")
st.title("CLU Applications Dashboard - Andhra Pradesh")

# REPLACE THIS URL with your new Sheet + gid
sheet_url = "https://docs.google.com/spreadsheets/d/1Q31RezteTX5reV7efFWKTFARF2bJcwRJgGZ5aatKxgg/export?format=csv&gid=0"

@st.cache_data(ttl=600)
def load_data():
    try:
        df = pd.read_csv(sheet_url)
        return df
    except Exception as e:
        st.error(f"Error loading Google Sheet: {e}")
        st.error("Check 1: Sheet is set to 'Anyone with the link - Viewer'")
        st.error("Check 2: The gid in the URL matches your data tab")
        return pd.DataFrame()

df = load_data()

col1, col2 = st.columns([6,1])
with col2:
    if st.button("🔄 Refresh"):
        st.cache_data.clear()
        st.rerun()

if df.empty:
    st.stop()

# Auto-find the TOTAL row by looking for the row with the highest first column value
try:
    numeric_col = pd.to_numeric(df.iloc[:, 0], errors='coerce')
    total_row_index = numeric_col.idxmax() # Row with largest number in col 1, should be your total
    total_row = df.iloc[total_row_index]
    
    total_apps = int(total_row[0])
    ulb_total = int(total_row[1])
    uda_total = int(total_row[2])
    dtcp_total = int(total_row[3])
    govt_total = int(total_row[4])
    ltp_total = int(total_row[5])
    
except Exception as e:
    st.error("Could not auto-detect TOTAL row. Showing your Sheet data below:")
    st.dataframe(df)
    st.info("Make sure your TOTAL row with numbers is in the sheet. Update the gid if needed.")
    st.stop()

# Top metrics
st.subheader("Overall Status Summary")
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
col1.metric("Total Received", total_apps)
col2.metric("Pending ULB", ulb_total)
col3.metric("Pending UDA", uda_total)
col4.metric("LTP Shortfall", ltp_total)
col5.metric("Pending DT&CP", dtcp_total)
col6.metric("Pending GOVT", govt_total)
col7.metric("Total Pending", ulb_total + uda_total + ltp_total + dtcp_total + govt_total)

st.markdown("---")

# Charts
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
    st.subheader("Pending Distribution")
    fig = px.pie(chart_data, values='Count', names='Authority', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

# Show raw data
st.subheader("Detailed Authority-wise Data")
st.dataframe(df.head(15), use_container_width=True, hide_index=True)

st.caption(f"Reading from Sheet. Update data and click 🔄 Refresh. Auto-refresh: 10 mins.")
