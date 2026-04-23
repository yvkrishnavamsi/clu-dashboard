import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CLU Applications Dashboard", layout="wide")
st.title("CLU Applications Dashboard - Andhra Pradesh")

sheet_url = "https://docs.google.com/spreadsheets/d/1_BwfciEui4JuSs7fdRV9BPJupBcVFUs2A61YRASmzb8/export?format=csv"

@st.cache_data(ttl=600)
def load_data():
    try:
        df = pd.read_csv(sheet_url, header=None) # Read without header to handle multiple sections
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

# Find the TOTAL row - it's the last section in your sheet
# Look for row where first column contains "TOTAL"
total_row_index = raw_df[raw_df[0].astype(str).str.contains('TOTAL', case=False, na=False)].index
if len(total_row_index) == 0:
    st.error("Could not find TOTAL row in Sheet. Make sure last section has 'TOTAL' in column A.")
    st.stop()

total_row = raw_df.iloc[total_row_index[-1]] # Get the last TOTAL row

# Extract values: Assuming order is Total, ULB, UDA, DT&CP, GOVT, LTP
try:
    total_apps = int(pd.to_numeric(total_row[0], errors='coerce'))
    ulb_total = int(pd.to_numeric(total_row[1], errors='coerce'))
    uda_total = int(pd.to_numeric(total_row[2], errors='coerce'))
    dtcp_total = int(pd.to_numeric(total_row[3], errors='coerce'))
    govt_total = int(pd.to_numeric(total_row[4], errors='coerce'))
    ltp_total = int(pd.to_numeric(total_row[5], errors='coerce'))
except:
    st.error("Could not parse numbers from TOTAL row. Check that row contains only numbers.")
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

# Show the raw data - find where Regular section starts
st.subheader("Detailed Authority-wise Data")
# Display first 15 rows which is your main Regular data
st.dataframe(pd.read_csv(sheet_url).head(15), use_container_width=True, hide_index=True)

st.caption("Dashboard reads from TOTAL row. Update numbers in your Sheet and click 🔄 Refresh. Auto-refresh every 10 mins.")
