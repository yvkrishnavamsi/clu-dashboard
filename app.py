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

.block-container { padding-top: 0.5rem!important; }
    div[data-testid="stVerticalBlock"] { gap: 0.5rem!important; }
    div[data-testid="column"] { padding: 0 0.25rem!important; }
    div.element-container { margin: 0!important; padding: 0!important; }

.blue-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 0.5rem;
        text-align: center;
    }

.blue-header h1 {
        color: white;
        font-size: 24px;
        font-weight: 700;
        margin: 0;
        padding: 0;
    }

.blue-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 12px;
        margin: 0.25rem 0 0 0;
        padding: 0;
        font-weight: 500;
    }

.filter-container {
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
    }

.metric-box {
        background: white;
        border-radius: 10px;
        padding: 0.75rem 0.5rem;
        border: 1px solid #e5e7eb;
        height: 135px;
        text-align: center;
    }

.metric-label {
        color: #6b7280;
        font-size: 9px;
        font-weight: 700;
        text-transform: uppercase;
        line-height: 1.1;
        height: 22px;
        margin-bottom: 0.25rem;
    }

.metric-value {
        font-size: 28px;
        font-weight: 700;
        line-height: 1;
        margin: 0.25rem 0;
    }

.metric-icon {
        font-size: 18px;
        height: 20px;
        line-height: 1;
    }

    [data-testid="stSidebar"] {
        background: #f9fafb;
        border-right: 1px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

# BLUE HEADER WITH TITLE
st.markdown('''
<div class="blue-header">
    <h1>CLU Applications Dashboard</h1>
    <p>Government of Andhra Pradesh | Directorate of Town & Country Planning Department</p>
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

if df.empty:
    st.stop()

if 'Designation' not in df.columns:
    st.error(f"'Designation' column not found. Available: {df.columns.tolist()}")
    st.stop()

df['Designation'] = df['Designation'].astype(str).str.upper().str.strip()

# FILTERS IN MAIN AREA - NOW VISIBLE
st.markdown('<div class="filter-container">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
with col1:
    ulb_options = ['All'] + sorted([x for x in df['ULB Name'].dropna().unique() if str(x).strip()!= 'None'])
    selected_ulb = st.selectbox("🏛️ ULB Name", ulb_options, key="main_ulb")
with col2:
    uda_options = ['All'] + sorted([x for x in df['UDA Name'].dropna().unique() if str(x).strip()!= 'None'])
    selected_uda = st.selectbox("🏢 UDA Name", uda_options, key="main_uda")
with col3:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Data", use_container_width=True, type="primary"):
        st.cache_data.clear()
        st.rerun()
with col4:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    st.caption("⏱️ 10 min")
st.markdown('</div>', unsafe_allow_html=True)

# Sidebar filters too
with st.sidebar:
    st.markdown("### 🎯 Data Filters")
    st.selectbox("🏛️ ULB Name", ulb_options, key="side_ulb", index=ulb_options.index(selected_ulb))
    st.selectbox("🏢 UDA Name", uda_options, key="side_uda", index=uda_options.index(selected_uda))
    st.divider()
    st.caption("⏱️ Auto-refresh: 10 min")

# Apply filters - sync both
selected_ulb = st.session_state.get('main_ulb', selected_ulb)
selected_uda = st.session_state.get('main_uda', selected_uda)

filtered_df = df.copy()
if selected_ulb!= 'All':
    filtered_df = filtered_df[filtered_df['ULB Name'] == selected_ulb]
if selected_uda!= 'All':
    filtered_df = filtered_df[filtered_df['UDA Name'] == selected_uda]

if selected_ulb!= 'All' or selected_uda!= 'All':
    st.info(f"🔍 **Active Filters:** ULB: {selected_ulb} | UDA: {selected_uda}")

# Metrics
total_submitted = filtered_df['S.no'].count() if 'S.no' in filtered_df.columns else len(filtered_df)
pending_ulb = filtered_df[filtered_df['Designation'].str.contains('ULB') & ~filtered_df['Designation'].str.contains('UDA|APCRDA|DTCP')].shape[0]
pending_uda = filtered_df[filtered_df['Designation'].str.contains('UDA|APCRDA') & ~filtered_df['Designation'].str.contains('ULB|DTCP')].shape[0]
pending_ltp = filtered_df[filtered_df['Designation'].str.contains('SHORTFALL')].shape[0]
pending_dtcp = filtered_df[filtered_df['Designation'].str.contains('DTCP') & ~filtered_df['Designation'].str.contains('ULB|UDA|APCRDA')].shape[0]
pending_govt = filtered_df[filtered_df['Designation'].str.contains('GOVT') & ~filtered_df['Designation'].str.contains('ULB|UDA|APCRDA|DTCP')].shape[0]

# Metric Cards
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
        <div class="metric-box">
            <div class="metric-icon">{icon}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-value" style="color: {color};">{value:,}</div>
        </div>
        ''', unsafe_allow_html=True)

# Charts
col1, col2 = st.columns([3, 2], gap="small")

with col1:
    with st.container(border=True):
        st.markdown("##### 📊 Pendency by Authority")
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
            height=340,
            margin=dict(t=10, b=80, l=0, r=0),
            bargap=0.4
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col2:
    with st.container(border=True):
        st.markdown("##### 📈 Distribution Overview")
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
            height=340,
            margin=dict(t=10, b=60, l=0, r=0),
            annotations=[dict(text=f'{total_submitted:,}<br>Total', x=0.5, y=0.5, font_size=16, showarrow=False, font_family='Inter')]
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# Data Tables
with st.container(border=True):
    st.markdown("##### 📋 Detailed Application Records")
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "All Data",
        "Pending with ULB",
        "Pending with UDA",
        "Shortfall",
        "Pending with DT&CP",
        "Pending with GOVT"
    ])

    with tab1:
        st.dataframe(filtered_df, use_container_width=True, hide_index=True, height=380)
    with tab2:
        st.dataframe(filtered_df[filtered_df['Designation'].str.contains('ULB') & ~filtered_df['Designation'].str.contains('UDA|APCRDA|DTCP')], use_container_width=True, hide_index=True, height=380)
    with tab3:
        st.dataframe(filtered_df[filtered_df['Designation'].str.contains('UDA|APCRDA') & ~filtered_df['Designation'].str.contains('ULB|DTCP')], use_container_width=True, hide_index=True, height=380)
    with tab4:
        st.dataframe(filtered_df[filtered_df['Designation'].str.contains('SHORTFALL')], use_container_width=True, hide_index=True, height=380)
    with tab5:
        st.dataframe(filtered_df[filtered_df['Designation'].str.contains('DTCP') & ~filtered_df['Designation'].str.contains('ULB|UDA|APCRDA')], use_container_width=True, hide_index=True, height=380)
    with tab6:
        st.dataframe(filtered_df[filtered_df['Designation'].str.contains('GOVT') & ~filtered_df['Designation'].str.contains('ULB|UDA|APCRDA|DTCP')], use_container_width=True, hide_index=True, height=380)
