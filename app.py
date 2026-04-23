import streamlit as st
import pandas as pd
import plotly.express as px

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

df = load_data()

col1, col2 = st.columns([6,1])
with col2:
    if st.button("🔄 Refresh"):
        st.cache_data.clear()
        st.rerun()

if df.empty:
    st.warning("Could not load data. Check Sheet sharing settings.")
    st.stop()

# Find the row with numeric values after "TOTAL" section
# Your data has: TOTAL row, then header row, then numeric row
try:
    # Find row index where first column is numeric and > 10 (your total is 52)
    numeric_rows = df[pd.to_numeric(df.iloc[:, 0], errors='coerce').notna()]
    total_row = numeric_rows[numeric_rows.iloc[:, 0].astype(float) > 10].iloc[-1] # Get last row with total > 10
    
    total_apps = int(total_row[0])
    ulb_total = int(total_row[1])
    uda_total = int(total_row[2])
    dtcp_total = int(total_row[3])
    govt_total = int(total_row[4])
    ltp_total = int(total_row[5])
    
except Exception as e:
    st.error(f"Could not parse numbers from TOTAL row. Make sure the row with 52, 15, 23, 2, 3, 9 exists.")
    st.write("Debug - Last 5 rows of your sheet:")
    st.dataframe(df.tail(5))
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

# Show the raw data - first 15 rows is your Regular section
st.subheader("Detailed Authority-wise Data")
st.dataframe(df.head(15), use_container_width=True, hide_index=True)

st.caption("Dashboard reads from the numeric TOTAL row. Update numbers in your Sheet and click 🔄 Refresh.")
st.caption("Dashboard reads from TOTAL row. Update numbers in your Sheet and click 🔄 Refresh. Auto-refresh every 10 mins.")
