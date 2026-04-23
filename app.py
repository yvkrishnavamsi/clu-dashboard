import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="CLU Dashboard - AP",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded"
)
col1, col2, col3 = st.columns([1,6,1])
with col2:
    st.image("https://upload.wikimedia.org/wikipedia/commons/1/13/Seal_of_Andhra_Pradesh.png", width=80)

# Custom CSS for better design
st.markdown("""
<style>
    /* Main container */
   .main.block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Metric cards styling */
    [data-testid="stMetricValue"] {
        font-size: 28px;
        font-weight: 600;
        color: #1f2937;
    }

    [data-testid="stMetricLabel"] {
        font-size: 14px;
        color: #6b7280;
        font-weight: 500;
    }

    /* Tabs styling */
   .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

   .stTabs [data-baseweb="tab"] {
        background-color: #f3f4f6;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 500;
    }

   .stTabs [aria-selected="true"] {
        background-color: #3b82f6;
        color: white;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f9fafb;
    }

    /* Headers */
    h1 {
        color: #111827;
        font-weight: 700;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #3b82f6;
    }

    h2, h3 {
        color: #374151;
        font-weight: 600;
    }

    /* Info box */
   .stAlert {
        background-color: #dbeafe;
        border-left: 4px solid #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

# Header with icon
st.markdown("# 📊 CLU Applications Dashboard")
st.markdown("### Government of Andhra Pradesh | Town & Country Planning Department")
st.markdown("---")

sheet_url = "https://docs.google.com/spreadsheets/d/1Q31RezteTX5reV7efFWKTFARF2bJcwRJgGZ5aatKxgg/export?format=csv&gid=0"

@st.cache_data(ttl=600)
def load_data():
    try:
        df = pd.read_csv(sheet_url)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

# Sidebar with better design
with st.sidebar:
    st.markdown("### 🎯 Filters")
    st.markdown("---")

    col1, col2 = st.columns([4,1])
    with col1:
        st.markdown("**Data Controls**")
    with col2:
        if st.button("🔄", help="Refresh data"):
            st.cache_data.clear()
            st.rerun()

    st.markdown("---")

    ulb_options = ['All'] + sorted([x for x in df['ULB Name'].dropna().unique() if str(x).strip()!= 'None'])
    uda_options = ['All'] + sorted([x for x in df['UDA Name'].dropna().unique() if str(x).strip()!= 'None'])

    selected_ulb = st.selectbox("🏛️ ULB Name", ulb_options)
    selected_uda = st.selectbox("🏢 UDA Name", uda_options)

    st.markdown("---")
    st.caption("Data refreshes every 10 minutes automatically")

if df.empty:
    st.stop()

if 'Designation' not in df.columns:
    st.error(f"'Designation' column not found. Available: {df.columns.tolist()}")
    st.stop()

df['Designation'] = df['Designation'].astype(str).str.upper().str.strip()

# Apply filters
filtered_df = df.copy()
if selected_ulb!= 'All':
    filtered_df = filtered_df[filtered_df['ULB Name'] == selected_ulb]
if selected_uda!= 'All':
    filtered_df = filtered_df[filtered_df['UDA Name'] == selected_uda]

# Show active filters
if selected_ulb!= 'All' or selected_uda!= 'All':
    st.info(f"**Active Filters:** ULB: `{selected_ulb}` | UDA: `{selected_uda}`")

# Counting logic
total_submitted = filtered_df['S.no'].count() if 'S.no' in filtered_df.columns else len(filtered_df)
pending_ulb = filtered_df[filtered_df['Designation'].str.contains('ULB') & ~filtered_df['Designation'].str.contains('UDA|APCRDA|DTCP')].shape[0]
pending_uda = filtered_df[filtered_df['Designation'].str.contains('UDA|APCRDA') & ~filtered_df['Designation'].str.contains('ULB|DTCP')].shape[0]
pending_ltp = filtered_df[filtered_df['Designation'].str.contains('SHORTFALL')].shape[0]
pending_dtcp = filtered_df[filtered_df['Designation'].str.contains('DTCP') & ~filtered_df['Designation'].str.contains('ULB|UDA|APCRDA')].shape[0]
pending_govt = filtered_df[filtered_df['Designation'].str.contains('GOVT') & ~filtered_df['Designation'].str.contains('ULB|UDA|APCRDA|DTCP')].shape[0]

# Metrics with better spacing
st.markdown("### 📈 Key Metrics")
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Total Submitted", f"{total_submitted:,}", help="Total applications received")
col2.metric("Pending with ULB", f"{pending_ulb:,}")
col3.metric("Pending with UDA", f"{pending_uda:,}", help="Includes APCRDA")
col4.metric("Shortfall", f"{pending_ltp:,}")
col5.metric("Pending with DT&CP", f"{pending_dtcp:,}")
col6.metric("Pending with GOVT", f"{pending_govt:,}")

st.markdown("---")

# Charts with custom colors
col1, col2 = st.columns([3, 2])
with col1:
    st.markdown("### 📊 Pendency by Authority")
    chart_data = pd.DataFrame({
        'Authority': ['Pending with ULB', 'Pending with UDA', 'Shortfall', 'Pending with DT&CP', 'Pending with GOVT'],
        'Count': [pending_ulb, pending_uda, pending_ltp, pending_dtcp, pending_govt]
    })
    fig = px.bar(
        chart_data,
        x='Authority',
        y='Count',
        text='Count',
        color='Authority',
        color_discrete_sequence=['#3b82f6', '#8b5cf6', '#f59e0b', '#10b981', '#ef4444']
    )
    fig.update_layout(
        showlegend=False,
        xaxis_title="",
        yaxis_title="Number of Applications",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12),
        height=400
    )
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 📉 Distribution")
    fig = px.pie(
        chart_data,
        values='Count',
        names='Authority',
        hole=0.5,
        color_discrete_sequence=['#3b82f6', '#8b5cf6', '#f59e0b', '#10b981', '#ef4444']
    )
    fig.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.3),
        height=400,
        font=dict(size=11)
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Detailed tables
st.markdown("### 📋 Detailed Application Data")
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📄 All Data",
    "🏛️ Pending with ULB",
    "🏢 Pending with UDA",
    "⚠️ Shortfall",
    "📐 Pending with DT&CP",
    "🏛️ Pending with GOVT"
])

with tab1:
    st.dataframe(filtered_df, use_container_width=True, hide_index=True, height=400)
with tab2:
    st.dataframe(filtered_df[filtered_df['Designation'].str.contains('ULB') & ~filtered_df['Designation'].str.contains('UDA|APCRDA|DTCP')], use_container_width=True, hide_index=True)
with tab3:
    st.dataframe(filtered_df[filtered_df['Designation'].str.contains('UDA|APCRDA') & ~filtered_df['Designation'].str.contains('ULB|DTCP')], use_container_width=True, hide_index=True)
with tab4:
    st.dataframe(filtered_df[filtered_df['Designation'].str.contains('SHORTFALL')], use_container_width=True, hide_index=True)
with tab5:
    st.dataframe(filtered_df[filtered_df['Designation'].str.contains('DTCP') & ~filtered_df['Designation'].str.contains('ULB|UDA|APCRDA')], use_container_width=True, hide_index=True)
with tab6:
    st.dataframe(filtered_df[filtered_df['Designation'].str.contains('GOVT') & ~filtered_df['Designation'].str.contains('ULB|UDA|APCRDA|DTCP')], use_container_width=True, hide_index=True)ed_df['Designation'].str.contains('GOVT') & ~filtered_df['Designation'].str.contains('ULB|UDA|APCRDA|DTCP')], use_container_width=True, hide_index=True)
