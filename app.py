import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="CLU Applications Dashboard",
    layout="wide",
    page_icon="ap_logo.png",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    * { font-family: 'Inter', sans-serif; }
.main.block-container { padding: 0.5rem 1.5rem; max-width: 100%; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* KILL ALL STREAMLIT SPACING */
.block-container { padding-top: 0.5rem!important; }
    div[data-testid="stVerticalBlock"] { gap: 0!important; }
    div[data-testid="column"] { padding: 0 0.25rem!important; }
    div.element-container { margin: 0!important; padding: 0!important; }

.blue-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
    }

.blue-header-title {
        color: white;
        font-size: 24px;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
    }

.blue-header-subtitle {
        color: rgba(255, 255, 255, 0.9);
        font-size: 12px;
        margin-top: 0.25rem;
        font-weight: 500;
    }

.metric-card {
        background: white;
        border-radius: 10px;
        padding: 0.75rem 0.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        height: 140px!important;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        overflow: hidden;
        margin-bottom: 0.5rem;
    }

.metric-label {
        color: #6b7280;
        font-size: 9px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        line-height: 1.1;
        height: 22px;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 100%;
    }

.metric-value {
        color: #111827;
        font-size: 30px!important;
        font-weight: 700;
        line-height: 1;
        text-align: center;
    }

.metric-icon {
        font-size: 18px;
        text-align: center;
        height: 20px;
        line-height: 1;
    }

.chart-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        height: 420px;
        margin-bottom: 0.5rem;
    }

.table-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
    }

.section-title {
        font-size: 15px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 0.5rem;
    }

    [data-testid="stSidebar"] {
        background: #f9fafb;
        border-right: 1px solid #e5e7eb;
    }

.sidebar-title {
        font-size: 15px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 1rem;
    }

.stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #f3f4f6;
        padding: 4px;
        border-radius: 8px;
        margin-bottom: 0.5rem;
    }

.stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 6px;
        padding: 6px 10px;
        font-weight: 600;
        font-size: 11px;
        color: #6b7280;
        border: none;
    }

.stTabs [aria-selected="true"] {
        background: white;
        color: #3b82f6;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }

.info-banner {
        background: linear-gradient(135deg, #dbeafe 0%, #eff6ff 100%);
        border-left: 4px solid #3b82f6;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        font-size: 12px;
        color: #1e40af;
        font-weight: 500;
    }

.divider {
        height: 1px;
        background: #e5e7eb;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# BLUE HEADER WITH TITLE INSIDE
st.markdown('''
<div class="blue-header">
    <div class="blue-header-title">CLU Applications Dashboard</div>
    <div class="blue-header-subtitle">Government of Andhra Pradesh | Directorate of Town & Country Planning Department</div>
</div>
''', unsafe_allow_html=True)

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

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-title">🎯 Data Filters</div>', unsafe_allow_html=True)
    if st.button("🔄 Refresh Data", use_container_width=True, type="primary"):
        st.cache_data.clear()
        st.rerun()
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    ulb_options = ['All'] + sorted([x for x in df['ULB Name'].dropna().unique() if str(x).strip()!= 'None'])
    uda_options = ['All'] + sorted([x for x in df['UDA Name'].dropna().unique() if str(x).strip()!= 'None'])
    selected_ulb = st.selectbox("🏛️ ULB Name", ulb_options)
    selected_uda = st.selectbox("🏢 UDA Name", uda_options)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.caption("⏱️ Auto-refresh: 10 min")

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

if selected_ulb!= 'All' or selected_uda!= 'All':
    st.markdown(f'<div class="info-banner">🔍 <strong>Active Filters:</strong> ULB: {selected_ulb} | UDA: {selected_uda}</div>', unsafe_allow_html=True)

# Metrics
total_submitted = filtered_df['S.no'].count() if 'S.no' in filtered_df.columns else len(filtered_df)
pending_ulb = filtered_df[filtered_df['Designation'].str.contains('ULB') & ~filtered_df['Designation'].str.contains('UDA|APCRDA|DTCP')].shape[0]
pending_uda = filtered_df[filtered_df['Designation'].str.contains('UDA|APCRDA') & ~filtered_df['Designation'].str.contains('ULB|DTCP')].shape[0]
pending_ltp = filtered_df[filtered_df['Designation'].str.contains('SHORTFALL')].shape[0]
pending_dtcp = filtered_df[filtered_df['Designation'].str.contains('DTCP') & ~filtered_df['Designation'].str.contains('ULB|UDA|APCRDA')].shape[0]
pending_govt = filtered_df[filtered_df['Designation'].str.contains('GOVT') & ~filtered_df['Designation'].str.contains('ULB|UDA|APCRDA|DTCP')].shape[0]

# Metric Cards Row
col1, col2, col3, col4, col5, col6 = st.columns(6, gap="small")

metrics = [
    ("📥", "Total<br>Submitted", total_submitted, "#3b82f6"),
    ("🏘️", "Pending with<br>ULB", pending_ulb, "#8b5cf6"),
    ("🏗️", "Pending with<br>UDA", pending_uda, "#06b6d4"),
    ("⚠️", "Shortfall", pending_ltp, "#f59e0b"),
    ("📋", "Pending with<br>DT&CP", pending_dtcp, "#10b981"),
    ("🏛️", "Pending with<br>GOVT", pending_govt, "#ef4444")
]

for col, (icon, label, value, color) in zip([col1, col2, col3, col4, col5, col6], metrics):
    with col:
        st.markdown(f'''
        <div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-value" style="color: {color};">{value:,}</div>
        </div>
        ''', unsafe_allow_html=True)

# Charts Row - FILLS THE WHITE BLANK SPACES
col1, col2 = st.columns([3, 2], gap="small")

with col1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📊 Pendency by Authority</div>', unsafe_allow_html=True)
    chart_data = pd.DataFrame({
        'Authority': ['Pending with ULB', 'Pending with UDA', 'Shortfall', 'Pending with DT&CP', 'Pending with GOVT'],
        'Count': [pending_ulb, pending_uda, pending_ltp, pending_dtcp, pending_govt]
    })
    fig = go.Figure()
    colors = ['#8b5cf6', '#06b6d4', '#f59e0b', '#10b981', '#ef4444']
    fig.add_trace(go.Bar(
        x=chart_data['Authority'],
        y=chart_data['Count'],
        marker=dict(color=colors, line=dict(color='white', width=2)),
        text=chart_data['Count'],
        textposition='outside',
        textfont=dict(size=11, family='Inter', color='#374151', weight=600),
        hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
    ))
    fig.update_layout(
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=9)),
        yaxis=dict(showgrid=True, gridcolor='#f3f4f6', zeroline=False, tickfont=dict(size=9)),
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Inter', size=10, color='#6b7280'),
        height=360,
        margin=dict(t=10, b=80, l=0, r=0),
        bargap=0.4
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📈 Distribution Overview</div>', unsafe_allow_html=True)
    fig = go.Figure(data=[go.Pie(
        labels=chart_data['Authority'],
        values=chart_data['Count'],
        hole=0.65,
        marker=dict(colors=colors, line=dict(color='white', width=3)),
        textinfo='label+percent',
        textfont=dict(size=9, family='Inter'),
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percent: %{percent}<extra></extra>'
    )])
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Inter', size=9),
        height=360,
        margin=dict(t=10, b=60, l=0, r=0),
        annotations=[dict(text=f'{total_submitted:,}<br>Total', x=0.5, y=0.5, font_size=16, showarrow=False, font_family='Inter')]
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

# Data Tables - FILLS REMAINING BLANK SPACE
st.markdown('<div class="table-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📋 Detailed Application Records</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "All Data",
    "Pending with ULB",
    "Pending with UDA",
    "Shortfall",
    "Pending with DT&CP",
    "Pending with GOVT"
])

with tab1:
    st.dataframe(filtered_df, use_container_width=True, hide_index=True, height=400)
with tab2:
    st.dataframe(filtered_df[filtered_df['Designation'].str.contains('ULB') & ~filtered_df['Designation'].str.contains('UDA|APCRDA|DTCP')], use_container_width=True, hide_index=True, height=400)
with tab3:
    st.dataframe(filtered_df[filtered_df['Designation'].str.contains('UDA|APCRDA') & ~filtered_df['Designation'].str.contains('ULB|DTCP')], use_container_width=True, hide_index=True, height=400)
with tab4:
    st.dataframe(filtered_df[filtered_df['Designation'].str.contains('SHORTFALL')], use_container_width=True, hide_index=True, height=400)
with tab5:
    st.dataframe(filtered_df[filtered_df['Designation'].str.contains('DTCP') & ~filtered_df['Designation'].str.contains('ULB|UDA|APCRDA')], use_container_width=True, hide_index=True, height=400)
with tab6:
    st.dataframe(filtered_df[filtered_df['Designation'].str.contains('GOVT') & ~filtered_df['Designation'].str.contains('ULB|UDA|APCRDA|DTCP')], use_container_width=True, hide_index=True, height=400)

st.markdown('</div>', unsafe_allow_html=True)
