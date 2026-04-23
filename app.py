import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CLU Applications Dashboard", layout="wide")
st.title("CLU Applications Dashboard - Andhra Pradesh")

sheet_url = "https://docs.google.com/spreadsheets/d/1Q31RezteTX5reV7efFWKTFARF2bJcwRJgGZ5aatKxgg/export?format=csv&gid=0"

@st.cache_data(ttl=600)
def load_data():
    try:
        df = pd.read_csv(sheet_url)
        df.columns = df.columns.str.strip()
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
    st.stop()

if 'Designation' not in df.columns:
    st.error(f"'Designation' column not found. Available: {df.columns.tolist()}")
    st.stop()

df['Designation'] = df['Designation'].astype(str).str.upper().str.strip()

# Counting logic - Added APCRDA to UDA filter
total_submitted = df['S.no'].count() if 'S.no' in df.columns else len(df)
pending_ulb = df[df['Designation'].str.contains('ULB') & ~df['Designation'].str.contains('UDA|APCRDA|DTCP')].shape[0]
pending_uda = df[df['Designation'].str.contains('UDA|APCRDA') & ~df['Designation'].str.contains('ULB|DTCP')].shape[0]
pending_ltp = df[df['Designation'].str.contains('SHORTFALL')].shape[0]
pending_dtcp = df[df['Designation'].str.contains('DTCP') & ~df['Designation'].str.contains('ULB|UDA|APCRDA')].shape[0]
pending_govt = df[df['Designation'].str.contains('GOVT') & ~df['Designation'].str.contains('ULB|UDA|APCRDA|DTCP')].shape[0]

# Metrics
st.subheader("Application Status Summary")
c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric("Total Submitted", total_submitted)
c2.metric("Pending with ULB", pending_ulb)
c3.metric("Pending with UDA", pending_uda)
c4.metric("Shortfall", pending_ltp)
c5.metric("Pending with DT&CP", pending_dtcp)
c6.metric("Pending with GOVT", pending_govt)

st.markdown("---")

# Charts
col1, col2 = st.columns(2)
with col1:
    st.subheader("Pendency by Authority")
    chart_data = pd.DataFrame({
        'Authority': ['Pending with ULB', 'Pending with UDA', 'Shortfall', 'Pending with DT&CP', 'Pending with GOVT'],
        'Count': [pending_ulb, pending_uda, pending_ltp, pending_dtcp, pending_govt]
    })
    fig = px.bar(chart_data, x='Authority', y='Count', text='Count', color='Authority')
    fig.update_layout(showlegend=False, xaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Pending Distribution")
    fig = px.pie(chart_data, values='Count', names='Authority', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

# Detailed tables - APCRDA included in UDA tab
st.subheader("Detailed Data")
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["All Data", "Pending with ULB", "Pending with UDA", "Shortfall", "Pending with DT&CP", "Pending with GOVT"])

with tab1:
    st.dataframe(df, use_container_width=True, hide_index=True)
with tab2:
    st.dataframe(df[df['Designation'].str.contains('ULB') & ~df['Designation'].str.contains('UDA|APCRDA|DTCP')], use_container_width=True, hide_index=True)
with tab3:
    st.dataframe(df[df['Designation'].str.contains('UDA|APCRDA') & ~df['Designation'].str.contains('ULB|DTCP')], use_container_width=True, hide_index=True)
with tab4:
    st.dataframe(df[df['Designation'].str.contains('SHORTFALL')], use_container_width=True, hide_index=True)
with tab5:
    st.dataframe(df[df['Designation'].str.contains('DTCP') & ~df['Designation'].str.contains('ULB|UDA|APCRDA')], use_container_width=True, hide_index=True)
with tab6:
    st.dataframe(df[df['Designation'].str.contains('GOVT') & ~df['Designation'].str.contains('ULB|UDA|APCRDA|DTCP')], use_container_width=True, hide_index=True)

st.caption("Live from Google Sheets. Add/edit rows → Click 🔄 Refresh. Auto-refresh every 10 mins.")
