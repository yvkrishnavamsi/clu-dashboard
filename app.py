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

# BLUE HEADER
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

# BETTER CLEANING - Remove extra spaces, handle variations
df['Designation'] = df['Designation'].astype(str).str.upper().str.strip().str.replace(r'\s+', ' ', regex=True)
df['Designation'] = df['Designation'].replace(['NAN', 'NONE', 'NULL', ''], 'UNASSIGNED')

# FILTERS
st.markdown('<div class="filter-container">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
with col1:
    ulb_options = ['All'] + sorted([x for x in df['ULB Name'].dropna().unique() if str(x).strip()!= 'None'])
    selected_ulb = st.selectbox("🏛️ ULB Name", ulb_options)
with col2:
    uda_options = ['All'] + sorted([x for x in df['UDA Name'].dropna().unique() if str(x).strip()!= 'None'])
    selected_uda = st.selectbox("🏢 UDA Name", uda_options)
with col3:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Data", use_container_width=True, type="primary"):
        st.cache_data.clear()
        st.rerun()
with col4:
    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    st.caption("⏱️ 10 min")
st.markdown('</div>', unsafe_allow_html=True)

# Sidebar filters
with st.sidebar:
    st.markdown("### 🎯 Data Filters")
    st.selectbox("🏛️ ULB Name", ulb_options, key="side_ulb", index=ulb_options.index(selected_ulb))
    st.selectbox("🏢 UDA Name", uda_options, key="side_uda", index=uda_options.index(selected_uda))
    st.divider()
    st.caption("⏱️ Auto-refresh: 10 min")

# Apply filters
filtered_df = df.copy()
if selected_ulb!= 'All':
    filtered_df = filtered_df[filtered_df['ULB Name'] == selected_ulb]
if selected_uda!= 'All':
    filtered_df = filtered_df[filtered_df['UDA Name'] == selected_uda]

if selected_ulb!= 'All' or selected_uda!= 'All':
    st.info(f"🔍 **Active Filters:** ULB: {selected_ulb} | UDA: {selected_uda}")

# DEBUG - Show ALL Designations with counts
with st.expander("🔍 All Designations", expanded=False):
    debug_counts = filtered_df['Designation'].value_counts().reset_index()
    debug_counts.columns = ['Designation', 'Count']
    st.dataframe(debug_counts, use_container_width=True, hide_index=True)
    st.caption(f"Total unique designations: {len(debug_counts)}")

# AUTHORITY CATEGORIZATION - Broader matching
def categorize_designation(desig):
    desig = str(desig).upper()
    if any(x in desig for x in ['ULB', 'MUNICIPAL', 'CORPORATION', 'NAGARA', 'MUNICIPALITY']):
        return 'ULB'
    elif any(x in desig for x in ['UDA', 'APCRDA', 'DEVELOPMENT AUTHORITY']):
        return 'UDA'
    elif any(x in desig for x in ['SHORTFALL', 'LTP', 'DEFICIENCY', 'PENDING DOC']):
        return 'SHORTFALL'
    elif any(x in desig for x in ['DTCP', 'DIRECTOR', 'TOWN PLANNING', 'TPBO', 'WPRS', 'TPG', 'TP']):
        return 'DTCP'
    elif any(x in desig for x in ['GOVT', 'GOVERNMENT', 'SECRETARIAT', 'ADM', 'ADMIN', 'SECRETARY', 'APO', 'AD', 'COMMISSIONER']):
        return 'GOVT'
    else:
        return 'OTHER'

filtered_df['Authority_Category'] = filtered_df['Designation'].apply(categorize_designation)

# AUTHORITY COUNTS
total_submitted = filtered_df['S.no'].count() if 'S.no' in filtered_df.columns else len(filtered_df)
pending_ulb = filtered_df[filtered_df['Authority_Category'] == 'ULB'].shape[0]
pending_uda = filtered_df[filtered_df['Authority_Category'] == 'UDA'].shape[0]
pending_ltp = filtered_df[filtered_df['Authority_Category'] == 'SHORTFALL'].shape[0]
pending_dtcp = filtered_df[filtered_df['Authority_Category'] == 'DTCP'].shape[0]
pending_govt = filtered_df[filtered_df['Authority_Category'] == 'GOVT'].shape[0]

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

# CHARTS
col1, col2 = st.columns([3, 2], gap="small")

with col1:
    with st.container(border=True):
        st.markdown("##### 📊 Pendency by Authority")
        chart_data = pd.DataFrame({
            'Authority': ['Pending with ULB', 'Pending with UDA', 'Shortfall', 'Pending with DT&CP', 'Pending with GOVT'],
            'Count': [pending_ulb, pending_uda, pending_ltp, pending_dtcp, pending_govt]
        })
        fig = go.Figure()
        colors_bar = ['#8b5cf6', '#06b6d4', '#f59e0b', '#10b981', '#ef4444']
        fig.add_trace(go.Bar(
            x=chart_data['Authority'],
            y=chart_data['Count'],
            marker=dict(color=colors_bar, line=dict(color='white', width=2)),
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
        st.markdown("##### 📈 Distribution by Designation")
        # SHOW ALL DESIGNATIONS - Combine small ones into "Others" if >15 items
        designation_counts = filtered_df['Designation'].value_counts().reset_index()
        designation_counts.columns = ['Designation', 'Count']
        designation_counts = designation_counts[designation_counts['Designation']!= 'UNASSIGNED']
        designation_counts = designation_counts.sort_values('Count', ascending=False)

        # If more than 15 designations, group small ones
        if len(designation_counts) > 15:
            top_14 = designation_counts.head(14)
            others_count = designation_counts.iloc[14:]['Count'].sum()
            others_row = pd.DataFrame({'Designation': ['OTHERS'], 'Count': [others_count]})
            designation_counts = pd.concat([top_14, others_row], ignore_index=True)

        if not designation_counts.empty:
            colors_pie = ['#3b82f6', '#8b5cf6', '#06b6d4', '#f59e0b', '#10b981', '#ef4444', '#ec4899', '#14b8a6', '#f97316', '#6366f1', '#84cc16', '#06b6d4', '#a855f7', '#f43f5e', '#6b7280']
            fig = go.Figure(data=[go.Pie(
                labels=designation_counts['Designation'],
                values=designation_counts['Count'],
                hole=0.55,
                marker=dict(colors=colors_pie[:len(designation_counts)], line=dict(color='white', width=2)),
                textinfo='label+percent',
                textfont=dict(size=7, family='Inter'),
                textposition='auto',
                hovertemplate='<b>%{label}</b><br>Files: %{value}<br>Percent: %{percent}<extra></extra>'
            )])
            fig.update_layout(
                showlegend=False,
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family='Inter', size=8),
                height=340,
                margin=dict(t=10, b=60, l=0, r=0),
                annotations=[dict(text=f'{total_submitted:,}<br>Total', x=0.5, y=0.5, font_size=16, showarrow=False, font_family='Inter')]
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.warning("No designation data available")

# TABLE TABS - AUTHORITY WISE
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
        st.dataframe(filtered_df[filtered_df['Authority_Category'] == 'ULB'], use_container_width=True, hide_index=True, height=380)
    with tab3:
        st.dataframe(filtered_df[filtered_df['Authority_Category'] == 'UDA'], use_container_width=True, hide_index=True, height=380)
    with tab4:
        st.dataframe(filtered_df[filtered_df['Authority_Category'] == 'SHORTFALL'], use_container_width=True, hide_index=True, height=380)
    with tab5:
        st.dataframe(filtered_df[filtered_df['Authority_Category'] == 'DTCP'], use_container_width=True, hide_index=True, height=380)
    with tab6:
        st.dataframe(filtered_df[filtered_df['Authority_Category'] == 'GOVT'], use_container_width=True, hide_index=True, height=380)
