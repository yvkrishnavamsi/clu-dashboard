import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="DT&CP Applications Dashboard", layout="wide")
st.title("CLU Applications Dashboard - Andhra Pradesh")

# Summary data
summary = {
    'Status': ['Pending with ULB', 'Pending with UDA', 'Pending with DT&CP', 'Pending with GOVT', 'Pending with LTP(shortfall)'],
    'Count': [15, 23, 2, 3, 9]
}
df_summary = pd.DataFrame(summary)

# Detailed breakdown - I parsed your text
detail_data = [
    ["Regular", "ULB", "Anantapur Municipal Corporation", "WPRS", 1],
    ["Regular", "ULB", "Anantapur Municipal Corporation", "TPS", 1],
    ["Regular", "ULB", "Bethamcherla Nagar Panchayat", "TPO", 1],
    ["Regular", "ULB", "Bhimavaram Municipality", "WPRS", 1],
    ["Regular", "ULB", "Chittoor Municipal Corporation", "WPRS", 1],
    ["Regular", "ULB", "Greater Visakhapatnam Municipal Corporation", "COM", 1],
    ["Regular", "ULB", "Guntakal Municipality", "WPRS", 1],
    ["Regular", "ULB", "Kadapa Municipal Corporation", "WPRS", 1],
    ["Regular", "ULB", "Kadapa Municipal Corporation", "TPBO", 1],
    ["Regular", "ULB", "Kadapa Municipal Corporation", "ACP", 1],
    ["Regular", "ULB", "Kurnool Municipal Corporation", "TPS", 1],
    ["Regular", "ULB", "Narsaraopeta Municipality", "WPRS", 1],
    ["Regular", "ULB", "Nellore Municipal Corporation", "TPO", 1],
    ["Regular", "ULB", "Tadepalligudem Municipality", "TPS", 1],
    ["Regular", "ULB", "Vijayanagaram Municipal Corporation", "WPRS", 1],
    ["Regular", "UDA", "APCRDA", "TPA", 2],
    ["Regular", "UDA", "Anantapuramu Hindupur UDA", "JPO", 4],
    ["Regular", "UDA", "Chittoor UDA", "JPO", 1],
    ["Regular", "UDA", "Eluru UDA", "JPO", 2],
    ["Regular", "UDA", "Kurnool UDA", "SDM", 2],
    ["Regular", "UDA", "Kurnool UDA", "VC", 3],
    ["Regular", "UDA", "Machilipatnam UDA", "JPO", 1],
    ["Regular", "UDA", "Nellore UDA", "WPRS", 1],
    ["Regular", "UDA", "Tirupati UDA", "WPRS", 2],
    ["Regular", "UDA", "Palamaner-Kuppam-Madanapalle UDA", "VC", 1],
    ["Regular", "UDA", "VMRDA", "WPRS", 1],
    ["Regular", "UDA", "VMRDA", "ADM", 2],
    ["Regular", "UDA", "VMRDA", "MC", 1],
    ["Regular", "DT&CP", "DT&CP", "TPA", 1],
    ["Regular", "DT&CP", "DT&CP", "DIR", 1],
    ["Regular", "GOVT", "GOVT", "OSD", 1],
    ["CLU SUO MOTU", "GOVT", "GOVT", "GOVT_SO", 2],
]
df_detail = pd.DataFrame(detail_data, columns=['Type', 'Pending_With', 'Authority', 'Officer', 'Count'])

# KPI Row
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Total Applications", "52")
col2.metric("Pending with ULB", "15")
col3.metric("Pending with UDA", "23") 
col4.metric("Pending with DT&CP", "2")
col5.metric("Pending with GOVT", "3")
col6.metric("LTP Shortfall", "9")

st.divider()

# Charts
col1, col2 = st.columns(2)
with col1:
    fig_bar = px.bar(df_summary, x='Status', y='Count', title='Applications by Pending Status', 
                     color='Status', text='Count')
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    fig_pie = px.pie(df_detail.groupby('Type')['Count'].sum().reset_index(), 
                     names='Type', values='Count', title='Regular vs CLU SUO MOTU')
    st.plotly_chart(fig_pie, use_container_width=True)

# Filters + Table
st.subheader("Detailed Authority-wise Breakdown")
filter_col1, filter_col2 = st.columns(2)
with filter_col1:
    type_filter = st.multiselect("Application Type", options=df_detail['Type'].unique(), default=df_detail['Type'].unique())
with filter_col2:
    pending_filter = st.multiselect("Pending With", options=df_detail['Pending_With'].unique(), default=df_detail['Pending_With'].unique())

filtered_df = df_detail[df_detail['Type'].isin(type_filter) & df_detail['Pending_With'].isin(pending_filter)]
st.dataframe(filtered_df, use_container_width=True, hide_index=True)

# Download button
st.download_button("Download Filtered Data as CSV", filtered_df.to_csv(index=False), "applications.csv")