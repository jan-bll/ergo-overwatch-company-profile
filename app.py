"""
Company Profile Viewer - Streamlit POC
Displays company data extracted by the Company Intelligence Agent (Deep Research)
"""

import streamlit as st
import json
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Overwatch - Company Profile",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling (forced bright mode)
st.markdown("""
<style>
    /* Force light mode globally */
    .stApp {
        background-color: #FFFFFF !important;
        color: #1A202C !important;
    }
    
    /* Force light mode for header */
    header[data-testid="stHeader"] {
        background-color: #FFFFFF !important;
    }
    
    /* Force light mode for all text elements */
    .stApp, .stApp p, .stApp span, .stApp div, .stApp label, 
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: #1A202C !important;
    }
    
    /* Sidebar styling - matches Ergo logo background */
    [data-testid="stSidebar"] {
        background-color: #EDF2F7 !important;
        padding-top: 1rem !important;
    }
    
    [data-testid="stSidebar"] * {
        color: #1A202C !important;
    }
    
    [data-testid="stSidebarNav"] {
        background-color: #EDF2F7 !important;
    }
    
    /* Remove white backgrounds from sidebar elements */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        background-color: transparent !important;
    }
    
    [data-testid="stSidebar"] .element-container {
        background-color: transparent !important;
    }
    
    /* Sidebar content spacing */
    [data-testid="stSidebar"] .block-container {
        padding-top: 1rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    /* Logo styling */
    [data-testid="stSidebar"] img {
        margin-bottom: 1rem !important;
    }
    
    /* Sidebar labels */
    [data-testid="stSidebar"] label {
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        margin-bottom: 0.5rem !important;
        color: #2D3748 !important;
    }
    
    /* Sidebar text */
    [data-testid="stSidebar"] .stMarkdown {
        background-color: transparent !important;
    }
    
    [data-testid="stSidebar"] p {
        background-color: transparent !important;
    }
    
    /* Selectbox/Dropdown styling */
    [data-testid="stSidebar"] [data-baseweb="select"] {
        background-color: transparent !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: #E2E8F0 !important;
        border: 1px solid #CBD5E0 !important;
        border-radius: 8px !important;
    }
    
    [data-baseweb="select"] * {
        color: #1A202C !important;
    }
    
    /* Main content selectbox */
    .main [data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border-color: #CBD5E0 !important;
    }
    
    /* Multiselect styling - Blue theme to match Ergo */
    [data-baseweb="tag"] {
        background-color: #3182CE !important;
        color: #FFFFFF !important;
        border-radius: 6px !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        padding: 0.25rem 0.5rem !important;
    }
    
    [data-baseweb="tag"] span[role="button"] {
        color: #FFFFFF !important;
    }
    
    /* Dropdown menu */
    [role="listbox"] {
        background-color: #FFFFFF !important;
    }
    
    [role="option"] {
        background-color: #FFFFFF !important;
        color: #1A202C !important;
    }
    
    [role="option"]:hover {
        background-color: #F7FAFC !important;
    }
    
    /* Input fields - transparent in sidebar */
    [data-testid="stSidebar"] input, 
    [data-testid="stSidebar"] textarea, 
    [data-testid="stSidebar"] select {
        background-color: #E2E8F0 !important;
        color: #1A202C !important;
        border: 1px solid #CBD5E0 !important;
    }
    
    /* Input fields in main content */
    .main input, .main textarea, .main select {
        background-color: #FFFFFF !important;
        color: #1A202C !important;
        border-color: #E2E8F0 !important;
    }
    
    /* Sidebar multiselect container */
    [data-testid="stSidebar"] [data-baseweb="select"] {
        background-color: transparent !important;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #FFFFFF !important;
        color: #1A202C !important;
        border: 2px solid #E2E8F0 !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        border-color: #3182CE !important;
        color: #3182CE !important;
    }
    
    .stButton > button[kind="primary"] {
        background-color: #3182CE !important;
        color: #FFFFFF !important;
        border: 2px solid #3182CE !important;
        box-shadow: 0 2px 4px rgba(49, 130, 206, 0.2) !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background-color: #2C5282 !important;
        border-color: #2C5282 !important;
    }
    
    /* Cards and containers */
    [data-testid="stVerticalBlock"] > div {
        background-color: #FFFFFF !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #1A202C !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #4A5568 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #FFFFFF !important;
        gap: 0.5rem !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #F7FAFC !important;
        color: #4A5568 !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 500 !important;
        border: none !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF !important;
        color: #3182CE !important;
        border-bottom: 3px solid #3182CE !important;
        font-weight: 600 !important;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        background-color: #FFFFFF !important;
        padding: 1.5rem 0 !important;
    }
    
    /* Expanders */
    [data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        margin-bottom: 0.75rem !important;
    }
    
    [data-testid="stExpander"] details {
        background-color: #FFFFFF !important;
    }
    
    [data-testid="stExpander"] summary {
        background-color: #F7FAFC !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stExpander"][open] summary {
        border-bottom: 1px solid #E2E8F0 !important;
        border-radius: 8px 8px 0 0 !important;
    }
    
    /* Info/warning boxes */
    .stAlert {
        background-color: #EBF8FF !important;
        color: #1A202C !important;
        border-left: 4px solid #3182CE !important;
        border-radius: 8px !important;
        padding: 1rem !important;
    }
    
    /* Markdown */
    .stMarkdown {
        color: #1A202C !important;
    }
    
    /* Sidebar markdown */
    [data-testid="stSidebar"] .stMarkdown {
        font-size: 0.95rem !important;
        background-color: transparent !important;
    }
    
    /* Sidebar info boxes */
    [data-testid="stSidebar"] .stMarkdown p {
        margin-bottom: 0.5rem !important;
        line-height: 1.6 !important;
        background-color: transparent !important;
    }
    
    /* Remove borders from sidebar hr */
    [data-testid="stSidebar"] hr {
        margin: 1.5rem 0 !important;
        border-top: 1px solid #CBD5E0 !important;
        opacity: 0.5 !important;
    }
    
    /* Sidebar headings */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #2D3748 !important;
        background-color: transparent !important;
    }
    
    /* Main content area padding */
    .main .block-container {
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
        max-width: 1400px !important;
    }
    
    /* Metrics styling */
    [data-testid="stMetric"] {
        background-color: #F7FAFC !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        border-left: 4px solid #3182CE !important;
    }
    
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2D3748 !important;
        margin-bottom: 0.5rem !important;
    }
    .section-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #2D3748 !important;
        border-bottom: 3px solid #3182CE;
        padding-bottom: 0.75rem;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #FFFFFF;
        border-radius: 8px;
        padding: 1rem;
        border-left: 4px solid #3182CE;
    }
    .flag-high {
        background-color: #FED7D7;
        border-left: 4px solid #C53030;
        padding: 0.75rem;
        border-radius: 4px;
        margin-bottom: 0.5rem;
        color: #742A2A !important;
    }
    .flag-medium {
        background-color: #FEEBC8;
        border-left: 4px solid #C05621;
        padding: 0.75rem;
        border-radius: 4px;
        margin-bottom: 0.5rem;
        color: #7C2D12 !important;
    }
    .flag-low {
        background-color: #C6F6D5;
        border-left: 4px solid #276749;
        padding: 0.75rem;
        border-radius: 4px;
        margin-bottom: 0.5rem;
        color: #22543D !important;
    }
    .source-badge {
        display: inline-block;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .tier-1 { background-color: #C6F6D5; color: #276749; }
    .tier-2 { background-color: #BEE3F8; color: #2B6CB0; }
    .tier-3 { background-color: #FEEBC8; color: #C05621; }
    .tier-4 { background-color: #FED7D7; color: #C53030; }
    
    /* Horizontal dividers */
    hr {
        margin: 2rem 0 !important;
        border: none !important;
        border-top: 2px solid #E2E8F0 !important;
    }
    
    /* Code/badge styling */
    code {
        background-color: #EDF2F7 !important;
        color: #2D3748 !important;
        padding: 0.2rem 0.5rem !important;
        border-radius: 4px !important;
        font-size: 0.9em !important;
        font-weight: 500 !important;
    }
    
    /* Improve spacing for markdown lists */
    .stMarkdown ul, .stMarkdown ol {
        padding-left: 1.5rem !important;
    }
    
    .stMarkdown li {
        margin-bottom: 0.5rem !important;
        line-height: 1.6 !important;
    }
    
    /* Footer styling */
    footer {
        visibility: hidden !important;
    }
</style>
""", unsafe_allow_html=True)


def load_company_data(file_path: str) -> dict:
    """Load company profile JSON from file"""
    with open(file_path, 'r') as f:
        return json.load(f)


def get_available_profiles() -> list:
    """Get list of available company profile files"""
    data_dir = Path(__file__).parent / "data"
    if not data_dir.exists():
        return []
    return list(data_dir.glob("*_profile.json"))


def render_confidence_badge(confidence: float) -> str:
    """Render confidence score as colored badge"""
    if confidence >= 0.8:
        color = "green"
    elif confidence >= 0.6:
        color = "orange"
    else:
        color = "red"
    return f":{color}[{confidence:.0%} confidence]"


def render_tier_badge(tier: int) -> str:
    """Render source tier badge"""
    tier_colors = {1: "green", 2: "blue", 3: "orange", 4: "red"}
    tier_labels = {1: "Tier 1 - SEC Filing", 2: "Tier 2 - Official", 3: "Tier 3 - Analyst", 4: "Tier 4 - Reference"}
    return f":{tier_colors.get(tier, 'gray')}[{tier_labels.get(tier, 'Unknown')}]"


def render_overview(data: dict):
    """Render company overview section"""
    overview = data.get("company_overview", {})
    meta = data.get("meta", {})

    st.markdown('<p class="section-header">Company Overview</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.markdown(f"**{overview.get('business_description', 'N/A')}**")

        hq = overview.get("headquarters", {})
        st.markdown(f"📍 **Headquarters:** {hq.get('city', 'N/A')}, {hq.get('country', 'N/A')}")
        st.markdown(f"📅 **Founded:** {overview.get('founded', 'N/A')}")
        st.markdown(f"👥 **Employees:** {overview.get('employees', 0):,}")

    with col2:
        st.markdown(f"**Business Model:** `{overview.get('business_model', 'N/A').upper()}`")
        st.markdown(f"**Value Chain:** `{overview.get('value_chain_position', 'N/A').upper()}`")

    with col3:
        st.markdown(f"**Data Quality:** {render_confidence_badge(meta.get('confidence_overall', 0))}")
        st.markdown(f"**Fiscal Year:** FY{meta.get('baseline_fiscal_year', 'N/A')}")
        st.markdown(f"**Updated:** {meta.get('extraction_date', 'N/A')}")

    # Business segments
    st.markdown("---")
    st.markdown("**Business Segments**")
    segments = overview.get("primary_segments", [])
    if segments:
        seg_df = pd.DataFrame(segments)
        fig = px.pie(seg_df, values='revenue_percent', names='name',
                     title="Revenue by Segment",
                     color_discrete_sequence=px.colors.qualitative.Set2,
                     template="plotly_white")
        fig.update_layout(
            height=300, 
            margin=dict(t=30, b=0, l=0, r=0),
            paper_bgcolor='white',
            plot_bgcolor='white',
            font=dict(color='#1A202C')
        )
        st.plotly_chart(fig, use_container_width=True)


def render_geographic_exposure(data: dict):
    """Render geographic exposure section"""
    geo = data.get("geographic_exposure", {})

    st.markdown('<p class="section-header">Geographic Exposure</p>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📊 Revenue", "🏭 Manufacturing", "🏢 Key Facilities"])

    with tab1:
        revenue_data = geo.get("revenue_by_region", [])
        if revenue_data:
            df = pd.DataFrame(revenue_data)

            col1, col2 = st.columns([1, 1])
            with col1:
                fig = px.pie(df, values='percent_of_total', names='region',
                            title="Revenue Distribution",
                            color_discrete_sequence=px.colors.qualitative.Pastel,
                            template="plotly_white")
                fig.update_layout(
                    height=350,
                    paper_bgcolor='white',
                    plot_bgcolor='white',
                    font=dict(color='#1A202C')
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = px.bar(df, x='region', y='yoy_growth',
                            title="YoY Growth by Region (%)",
                            color='yoy_growth',
                            color_continuous_scale=['red', 'yellow', 'green'],
                            template="plotly_white")
                fig.update_layout(
                    height=350, 
                    showlegend=False,
                    paper_bgcolor='white',
                    plot_bgcolor='white',
                    font=dict(color='#1A202C')
                )
                st.plotly_chart(fig, use_container_width=True)

    with tab2:
        mfg_data = geo.get("manufacturing_footprint", [])
        if mfg_data:
            df = pd.DataFrame(mfg_data)
            df['percent_of_production'] = df['percent_of_production'].fillna(0)

            fig = px.bar(df, x='country', y='percent_of_production',
                        title="Manufacturing by Country (%)",
                        color='percent_of_production',
                        color_continuous_scale='Blues',
                        template="plotly_white")
            fig.update_layout(
                height=400,
                paper_bgcolor='white',
                plot_bgcolor='white',
                font=dict(color='#1A202C')
            )
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("**Manufacturing Notes:**")
            for item in mfg_data:
                st.markdown(f"- **{item['country']}**: {item.get('notes', 'N/A')}")

    with tab3:
        facilities = geo.get("key_facilities", [])
        for facility in facilities:
            loc = facility.get("location", {})
            with st.expander(f"📍 {facility.get('name', 'Unknown')} - {loc.get('city', '')}, {loc.get('country', '')}"):
                st.markdown(f"**Type:** `{facility.get('type', 'N/A').upper()}`")
                st.markdown(f"**Function:** {facility.get('function', 'N/A')}")
                st.markdown(f"**Significance:** {facility.get('significance', 'N/A')}")
                st.markdown(render_tier_badge(facility.get('source_tier', 4)))


def render_supply_chain(data: dict):
    """Render supply chain dependencies section"""
    supply = data.get("supply_chain", {})

    st.markdown('<p class="section-header">Supply Chain Dependencies</p>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔗 Critical Suppliers", "🏭 Contract Manufacturers", "🌍 Geographic Concentration"])

    with tab1:
        suppliers = supply.get("critical_suppliers", [])

        # Group by dependency level
        critical = [s for s in suppliers if s.get("dependency_level") == "critical"]
        high = [s for s in suppliers if s.get("dependency_level") == "high"]

        if critical:
            st.markdown("**🔴 CRITICAL Dependencies**")
            for s in critical:
                single_source_badge = "⚠️ SINGLE SOURCE" if s.get("single_source") else ""
                st.markdown(f"""
                <div class="flag-high">
                <strong>{s.get('name', 'Unknown')}</strong> ({s.get('headquarters_country', 'N/A')}) {single_source_badge}<br/>
                <em>Provides:</em> {s.get('provides', 'N/A')}<br/>
                <small>{s.get('notes', '')}</small>
                </div>
                """, unsafe_allow_html=True)

        if high:
            st.markdown("**🟠 HIGH Dependencies**")
            for s in high:
                single_source_badge = "⚠️ SINGLE SOURCE" if s.get("single_source") else ""
                st.markdown(f"""
                <div class="flag-medium">
                <strong>{s.get('name', 'Unknown')}</strong> ({s.get('headquarters_country', 'N/A')}) {single_source_badge}<br/>
                <em>Provides:</em> {s.get('provides', 'N/A')}<br/>
                <small>{s.get('notes', '')}</small>
                </div>
                """, unsafe_allow_html=True)

    with tab2:
        cms = supply.get("contract_manufacturers", [])
        if cms:
            for cm in cms:
                countries = ", ".join(cm.get("production_countries", []))
                st.markdown(f"""
                **{cm.get('name', 'Unknown')}** ({cm.get('headquarters_country', 'N/A')})
                - Production: {countries}
                - Products: {cm.get('products_manufactured', 'N/A')}
                """)
                st.markdown("---")

    with tab3:
        concentration = supply.get("supplier_geography_concentration", {})
        if concentration:
            col1, col2 = st.columns([1, 2])
            with col1:
                st.metric("Top Country", concentration.get("top_country", "N/A"))
                st.metric("Concentration", f"{concentration.get('top_country_percent', 0)}%")
            with col2:
                st.markdown("**Top 3 Countries:**")
                for country in concentration.get("top_3_countries", []):
                    st.markdown(f"- {country}")
                st.info(concentration.get("concentration_note", ""))


def render_customer_profile(data: dict):
    """Render customer profile section"""
    customer = data.get("customer_profile", {})

    st.markdown('<p class="section-header">Customer Profile</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("**Segment Mix**")
        segment_mix = customer.get("segment_mix", {})
        seg_data = {
            "Segment": ["B2B (Enterprise)", "B2C (Consumer)", "B2G (Government)"],
            "Percent": [
                segment_mix.get("b2b_percent", 0),
                segment_mix.get("b2c_percent", 0),
                segment_mix.get("b2g_percent", 0)
            ]
        }
        fig = px.pie(pd.DataFrame(seg_data), values='Percent', names='Segment',
                    color_discrete_sequence=px.colors.qualitative.Set3,
                    template="plotly_white")
        fig.update_layout(
            height=300, 
            margin=dict(t=20, b=0, l=0, r=0),
            paper_bgcolor='white',
            plot_bgcolor='white',
            font=dict(color='#1A202C')
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Industry Exposure**")
        industries = customer.get("industry_exposure", [])
        if industries:
            ind_df = pd.DataFrame(industries)
            fig = px.bar(ind_df, x='percent_of_revenue', y='industry', orientation='h',
                        color='percent_of_revenue', color_continuous_scale='Viridis',
                        template="plotly_white")
            fig.update_layout(
                height=300, 
                showlegend=False, 
                margin=dict(t=20, b=0, l=0, r=0),
                paper_bgcolor='white',
                plot_bgcolor='white',
                font=dict(color='#1A202C')
            )
            st.plotly_chart(fig, use_container_width=True)

    # Concentration
    concentration = customer.get("customer_concentration", {})
    st.markdown("**Customer Concentration**")
    st.info(f"**Level:** {concentration.get('concentration_level', 'N/A').upper()} | {concentration.get('note', 'N/A')}")


def render_regulatory_footprint(data: dict):
    """Render regulatory exposure section"""
    reg = data.get("regulatory_footprint", {})

    st.markdown('<p class="section-header">Regulatory Footprint</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("**Primary Jurisdictions**")
        for jurisdiction in reg.get("primary_jurisdictions", []):
            exposure = jurisdiction.get("exposure_level", "low")
            css_class = f"flag-{exposure}"
            bodies = ", ".join(jurisdiction.get("regulatory_bodies", []))
            st.markdown(f"""
            <div class="{css_class}">
            <strong>{jurisdiction.get('jurisdiction', 'Unknown')}</strong><br/>
            <em>Bodies:</em> {bodies}<br/>
            <em>Key Requirements:</em> {', '.join(jurisdiction.get('key_requirements', [])[:3])}
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("**Trade Exposure**")
        trade = reg.get("trade_exposure", {})

        tariff = trade.get("tariff_exposure", {})
        export = trade.get("export_controls", {})
        sanctions = trade.get("sanctions_exposure", {})

        trade_data = {
            "Category": ["Tariffs", "Export Controls", "Sanctions"],
            "Level": [
                tariff.get("level", "low"),
                export.get("level", "low"),
                sanctions.get("level", "low")
            ]
        }

        for cat, level in zip(trade_data["Category"], trade_data["Level"]):
            color = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(level, "⚪")
            st.markdown(f"{color} **{cat}:** {level.upper()}")

        if tariff.get("key_tariffs"):
            with st.expander("Tariff Details"):
                for t in tariff.get("key_tariffs", []):
                    st.markdown(f"- {t}")


def render_financial_baseline(data: dict):
    """Render financial baseline section"""
    fin = data.get("financial_baseline", {})

    st.markdown('<p class="section-header">Financial Baseline</p>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        revenue = fin.get("revenue_usd_millions", 0)
        st.metric("Revenue", f"${revenue/1000:.1f}B")
        st.metric("Market Cap", f"${fin.get('market_cap_usd_millions', 0)/1000:.1f}B")

    with col2:
        st.metric("Gross Margin", f"{fin.get('gross_margin', 0):.1%}")
        st.metric("Operating Margin", f"{fin.get('operating_margin', 0):.1%}")

    with col3:
        st.metric("Cash Position", f"${fin.get('cash_position_usd_millions', 0)/1000:.1f}B")
        st.metric("Total Debt", f"${fin.get('total_debt_usd_millions', 0)/1000:.1f}B")

    with col4:
        st.metric("Debt/Equity", f"{fin.get('debt_to_equity', 0):.1f}x")
        strength = fin.get("balance_sheet_strength", "N/A")
        strength_color = {"strong": "🟢", "adequate": "🟡", "weak": "🔴"}.get(strength, "⚪")
        st.metric("Balance Sheet", f"{strength_color} {strength.upper()}")


def render_concentration_flags(data: dict):
    """Render concentration flags/warnings"""
    flags = data.get("concentration_flags", [])

    if not flags:
        return

    st.markdown('<p class="section-header">⚠️ Concentration Flags</p>', unsafe_allow_html=True)

    for flag in flags:
        severity = flag.get("severity", "low")
        css_class = f"flag-{severity}"
        st.markdown(f"""
        <div class="{css_class}">
        <strong>[{flag.get('flag_type', 'unknown').upper()}]</strong> {flag.get('description', 'N/A')}<br/>
        <small>{flag.get('details', '')}</small>
        </div>
        """, unsafe_allow_html=True)


def render_strategic_initiatives(data: dict):
    """Render strategic initiatives section"""
    initiatives = data.get("strategic_initiatives", [])

    if not initiatives:
        return

    st.markdown('<p class="section-header">Strategic Initiatives</p>', unsafe_allow_html=True)

    for init in initiatives:
        status_icons = {"announced": "📢", "in_progress": "🔄", "completed": "✅"}
        icon = status_icons.get(init.get("status", ""), "❓")

        with st.expander(f"{icon} {init.get('name', 'Unknown')} - {init.get('type', 'N/A').upper()}"):
            st.markdown(f"**Description:** {init.get('description', 'N/A')}")
            st.markdown(f"**Status:** {init.get('status', 'N/A').upper()}")
            st.markdown(f"**Geographic Relevance:** {init.get('geographic_relevance', 'N/A')}")


def render_data_quality(data: dict):
    """Render data quality section"""
    quality = data.get("data_quality", {})
    meta = data.get("meta", {})

    st.markdown('<p class="section-header">Data Quality</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("**Source Summary**")
        source_summary = quality.get("source_summary", {})
        source_data = {
            "Tier": ["Tier 1 (SEC)", "Tier 2 (Official)", "Tier 3 (Analyst)", "Tier 4 (Reference)"],
            "Count": [
                source_summary.get("tier_1_count", 0),
                source_summary.get("tier_2_count", 0),
                source_summary.get("tier_3_count", 0),
                source_summary.get("tier_4_count", 0)
            ]
        }
        fig = px.bar(pd.DataFrame(source_data), x='Tier', y='Count',
                    color='Count', color_continuous_scale='Greens',
                    template="plotly_white")
        fig.update_layout(
            height=250, 
            showlegend=False,
            paper_bgcolor='white',
            plot_bgcolor='white',
            font=dict(color='#1A202C')
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Data Gaps**")
        for gap in quality.get("data_gaps", []):
            st.markdown(f"- ⚠️ {gap}")

        st.markdown("**Stale Data Warnings**")
        for warning in quality.get("stale_data_warnings", []):
            st.markdown(f"- 📅 {warning}")

    st.markdown("**Primary Sources**")
    for source in meta.get("primary_sources", []):
        st.markdown(f"- 📄 {source}")


def main():
    """Main application entry point"""

    # Sidebar - Company Selection
    logo_path = Path(__file__).parent / "ergo_png.png"
    if logo_path.exists():
        st.sidebar.image(str(logo_path), use_container_width=True)
    st.sidebar.markdown("---")

    # Get available profiles
    profiles = get_available_profiles()

    if not profiles:
        st.sidebar.warning("No company profiles found in data/ directory")
        st.error("No company profiles available. Please run the Company Intelligence Agent first.")
        return

    # Automatically load the first profile (no selection needed)
    selected_profile = profiles[0].stem.replace("_profile", "")
    profile_path = profiles[0]

    try:
        data = load_company_data(profile_path)
    except Exception as e:
        st.error(f"Error loading profile: {e}")
        return

    # Sidebar info - Display company ticker
    meta = data.get("meta", {})
    st.sidebar.markdown(f"### {meta.get('ticker', 'N/A')}")
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Data Date:** {meta.get('extraction_date', 'N/A')}")
    st.sidebar.markdown(f"**Confidence:** {meta.get('confidence_overall', 0):.0%}")

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Navigation**")
    sections = st.sidebar.multiselect(
        "Show Sections",
        ["Overview", "Geographic", "Supply Chain", "Customers", "Regulatory", "Financial", "Initiatives", "Flags", "Data Quality"],
        default=["Overview", "Geographic", "Supply Chain", "Flags"]
    )

    # Main content
    st.markdown(f'<p class="main-header">{meta.get("company_name", "Company Profile")}</p>', unsafe_allow_html=True)
    st.markdown(f"*{meta.get('data_freshness_note', '')}*")
    st.markdown("---")

    # Render selected sections
    if "Overview" in sections:
        render_overview(data)
        st.markdown("---")

    if "Geographic" in sections:
        render_geographic_exposure(data)
        st.markdown("---")

    if "Supply Chain" in sections:
        render_supply_chain(data)
        st.markdown("---")

    if "Customers" in sections:
        render_customer_profile(data)
        st.markdown("---")

    if "Regulatory" in sections:
        render_regulatory_footprint(data)
        st.markdown("---")

    if "Financial" in sections:
        render_financial_baseline(data)
        st.markdown("---")

    if "Initiatives" in sections:
        render_strategic_initiatives(data)
        st.markdown("---")

    if "Flags" in sections:
        render_concentration_flags(data)
        st.markdown("---")

    if "Data Quality" in sections:
        render_data_quality(data)

    # Footer
    st.markdown("---")
    st.markdown("*Ergo Overwatch POC - Company Profile Viewer*")

    # Action button for scenario analysis
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎯 Run Scenario Analysis →", type="primary", use_container_width=True):
            st.info("Scenario analysis not yet implemented. This would trigger FLOS analysts with selected scenarios.")


if __name__ == "__main__":
    main()
