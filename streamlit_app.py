import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import time
import json

# ============================================================================
# PAGE CONFIGURATION (must be first Streamlit command)
# ============================================================================
st.set_page_config(
    page_title="Company Profile – Deep Research",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if 'ticker' not in st.session_state:
    st.session_state.ticker = None
if 'loading' not in st.session_state:
    st.session_state.loading = False

# DEBUG: Print session state at the start
print("=" * 50)
print("DEBUG: Session state at start:")
print(f"  ticker: {st.session_state.ticker}")
print(f"  loading: {st.session_state.loading}")
print("=" * 50)

# Force flush to ensure logs appear
import sys
sys.stdout.flush()
sys.stderr.flush()

# ============================================================================
# LANDING PAGE - Company Input Form
# ============================================================================
if not st.session_state.ticker and not st.session_state.loading:
    print("DEBUG: Entering LANDING PAGE section")
    st.markdown("## Company Profile Deep Research")
    st.markdown("Enter a company name to generate a comprehensive profile")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        company_name = st.text_input(
            "Company Name",
            placeholder="e.g., DELL, Apple, Microsoft...",
            label_visibility="collapsed"
        )

        if st.button("Generate Profile", type="primary", use_container_width=True):
            import sys
            print(f"DEBUG: Button clicked with company_name: '{company_name}'", file=sys.stderr)
            print(f"DEBUG: Button clicked with company_name: '{company_name}'")
            sys.stderr.flush()
            if company_name.strip():
                print(f"DEBUG: Setting loading=True, company_name_input='{company_name.strip()}'", file=sys.stderr)
                print(f"DEBUG: Setting loading=True, company_name_input='{company_name.strip()}'")
                st.session_state.loading = True
                st.session_state.company_name_input = company_name.strip()
                print(f"DEBUG: Session state after setting - loading: {st.session_state.loading}, company_name_input: {st.session_state.company_name_input}", file=sys.stderr)
                print(f"DEBUG: Session state after setting - loading: {st.session_state.loading}, company_name_input: {st.session_state.company_name_input}")
                print("DEBUG: Calling st.rerun()", file=sys.stderr)
                print("DEBUG: Calling st.rerun()")
                sys.stderr.flush()
                st.rerun()
            else:
                print("DEBUG: Company name is empty, showing error")
                st.error("Please enter a company name.")

    print("DEBUG: Calling st.stop() to end LANDING PAGE section")
    st.stop()

# ============================================================================
# LOADING STATE - Data Fetching
# ============================================================================
print(f"DEBUG: Checking LOADING STATE condition - loading: {st.session_state.loading}")
if st.session_state.loading:
    print("DEBUG: Entering LOADING STATE section")
    print("DEBUG: About to import merge_sectors_data.pull_data_for_company")

    try:
        from merge_sectors_data import pull_data_for_company
        print("DEBUG: Successfully imported pull_data_for_company")
    except ImportError as ie:
        print(f"DEBUG: IMPORT ERROR: {str(ie)}")
        import traceback
        print(f"DEBUG: Import traceback: {traceback.format_exc()}")
        st.error(f"Failed to import required module: {str(ie)}")
        st.session_state.loading = False
        st.stop()
    except Exception as e:
        print(f"DEBUG: UNEXPECTED ERROR during import: {str(e)}")
        import traceback
        print(f"DEBUG: Import traceback: {traceback.format_exc()}")
        st.error(f"Unexpected error during import: {str(e)}")
        st.session_state.loading = False
        st.stop()

    # Check if company_name_input exists in session state
    if 'company_name_input' not in st.session_state:
        print("DEBUG: ERROR - company_name_input NOT in session state!")
        st.error("Error: Company name not found in session state")
        st.session_state.loading = False
        st.stop()

    print(f"DEBUG: About to display loading UI for company: {st.session_state.company_name_input}")
    st.markdown(f"### Generating profile for {st.session_state.company_name_input}...")
    st.markdown("Our AI agents are researching financial data, supply chain, customers, and regulatory information.")
    st.markdown("**This typically takes 5-10 minutes.**")

    progress_bar = st.progress(0)
    status_text = st.empty()

    stages = [
        ("Initializing research agents...", 0.05),
        ("Analyzing financial data...", 0.25),
        ("Mapping supply chain...", 0.45),
        ("Profiling customer segments...", 0.65),
        ("Reviewing regulatory footprint...", 0.85),
        ("Compiling final report...", 0.95),
    ]

    status_text.text(stages[0][0])
    progress_bar.progress(stages[0][1])

    try:
        print(f"DEBUG: About to call pull_data_for_company with: '{st.session_state.company_name_input}'")
        _, ticker = pull_data_for_company(st.session_state.company_name_input)
        print(f"DEBUG: pull_data_for_company returned ticker: {ticker}")

        if ticker:
            print(f"DEBUG: Ticker found: {ticker}, showing progress")
            for stage_text, stage_progress in stages[1:]:
                status_text.text(stage_text)
                progress_bar.progress(stage_progress)
                time.sleep(0.2)

            progress_bar.progress(1.0)
            status_text.text("Profile ready!")

            print(f"DEBUG: Setting ticker={ticker} and loading=False")
            st.session_state.ticker = ticker
            st.session_state.loading = False
            print(f"DEBUG: Session state after setting - ticker: {st.session_state.ticker}, loading: {st.session_state.loading}")
            time.sleep(0.5)
            print("DEBUG: Calling st.rerun() from success path")
            st.rerun()
        else:
            print("DEBUG: No ticker returned, showing error")
            st.error("Failed to retrieve data for the company. Please try again.")
            st.session_state.loading = False
            if st.button("Try Again"):
                st.rerun()
    except Exception as e:
        print(f"DEBUG: Exception occurred: {str(e)}")
        import traceback
        print(f"DEBUG: Traceback: {traceback.format_exc()}")
        st.error(f"An error occurred: {str(e)}")
        st.session_state.loading = False
        if st.button("Try Again"):
            st.rerun()

    print("DEBUG: Calling st.stop() to end LOADING STATE section")
    st.stop()

# ============================================================================
# LOAD DATA FROM JSON FILE
# ============================================================================
print("DEBUG: Reached MAIN REPORT section")
print(f"DEBUG: ticker from session state: {st.session_state.ticker}")
COMPANY_TICKER = st.session_state.ticker

# COMPANY_TICKER='DELL'

print(f"DEBUG: About to load JSON file: ./data/{COMPANY_TICKER}_profile.json")
try:
    with open(f"./data/{COMPANY_TICKER}_profile.json", 'r') as f:
        data = json.load(f)
    print(f"DEBUG: Successfully loaded JSON file")
except Exception as e:
    print(f"DEBUG: Failed to load JSON file: {str(e)}")
    st.error(f"Failed to load profile data: {str(e)}")
    st.stop()

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
def format_currency_billions(value_millions):
    """Format value in millions to billions string."""
    if value_millions is None:
        return "N/A"
    return f"${value_millions/1000:.1f}B"

def format_percentage(value, as_decimal=False):
    """Format percentage value."""
    if value is None:
        return "N/A"
    if as_decimal and value < 1:
        return f"{value*100:.1f}%"
    return f"{value:.1f}%"

def safe_int(value):
    """Safely convert to int."""
    if value is None:
        return "N/A"
    return f"{int(value):,}"

# ============================================================================
# EXTRACT DATA SECTIONS
# ============================================================================
data_meta = data['meta']
data_overview = data['company_overview']
data_financial = data['financial']
data_supply_chain = data['supply_chain']
data_customer_profile = data['customer_profile']
data_regulatory_footprint = data['regulatory_footprint']

# Custom CSS for BlackRock institutional aesthetic
st.markdown("""
<style>
    /* Main background and text */
    .stApp {
        background-color: #f8f9fa;
    }

    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 1.5rem 2rem;
        color: white;
        margin: -1rem -1rem 2rem -1rem;
        border-bottom: 3px solid #0ea5e9;
    }

    .main-header h1 {
        font-size: 1.75rem;
        font-weight: 600;
        margin: 0;
        color: white;
    }

    .main-header p {
        font-size: 0.875rem;
        margin: 0.25rem 0 0 0;
        color: #cbd5e1;
    }

    /* Metrics and cards */
    div[data-testid="stMetricValue"] {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e293b;
    }

    div[data-testid="stMetricLabel"] {
        font-size: 0.875rem;
        color: #64748b;
        font-weight: 500;
    }

    /* Dataframes */
    .dataframe {
        font-size: 0.875rem;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #f1f5f9;
        padding: 0.25rem;
        border-radius: 0.375rem;
    }

    .stTabs [data-baseweb="tab"] {
        height: 2.5rem;
        background-color: transparent;
        border-radius: 0.25rem;
        color: #64748b;
        font-weight: 500;
        font-size: 0.875rem;
        padding: 0 1.5rem;
    }

    .stTabs [aria-selected="true"] {
        background-color: white;
        color: #1e293b;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #e2e8f0;
    }

    /* Buttons */
    .stButton > button {
        background-color: #059669;
        color: white;
        border: 1px solid #047857;
        font-weight: 500;
        padding: 0.625rem 1.5rem;
        border-radius: 0.25rem;
        width: 100%;
    }

    .stButton > button:hover {
        background-color: #047857;
        border-color: #065f46;
    }

    /* Section headers */
    .section-header {
        font-size: 1.125rem;
        font-weight: 600;
        color: #1e293b;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }

    /* Risk badges */
    .risk-high {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }

    .risk-medium {
        background-color: #fef3c7;
        color: #92400e;
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }

    .risk-low {
        background-color: #d1fae5;
        color: #065f46;
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'company_history' not in st.session_state:
    st.session_state.company_history = [
        {
            "id": 1,
            "name": data_meta['company_name'],
            "status": "completed",
            "date_completed": data_meta['extraction_date'],
            "confidence": int(data_meta['confidence_overall'] * 100) if data_meta['confidence_overall'] <= 1 else int(data_meta['confidence_overall'])
        },
    ]

if 'show_modal' not in st.session_state:
    st.session_state.show_modal = False

# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.markdown(f"### 📊 {data_meta['company_name']}")
    st.markdown("*Current Report*")
    st.markdown("")

    # New Research Button
    if st.button("📊 New Research", use_container_width=True):
        st.session_state.show_modal = True

    st.markdown("---")

    # Research History
    st.markdown("#### Research History")
    st.markdown(f"""
        <div style="padding: 0.75rem; background: white; border: 1px solid #e2e8f0; border-radius: 0.375rem; margin-bottom: 0.75rem;">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="color: #059669; font-size: 1rem;">✓</span>
                <div style="flex: 1;">
                    <div style="font-weight: 600; font-size: 0.875rem; color: #1e293b;">{data_meta['company_name']}</div>
                    <div style="font-size: 0.75rem; color: #64748b; margin-top: 0.125rem;">{data_meta['extraction_date']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Current Report Navigation
    st.markdown("#### Current Report")
    sections = [
        "Overview",
        "Revenue Breakdown",
        "Business Segments",
        "Geographic Exposure",
        "Customer Profile",
        "Supply Chain",
        "Concentration Risk"
    ]

    for section in sections:
        st.markdown(f"- {section}")

# Modal for New Research (using expander as modal alternative)
if st.session_state.show_modal:
    with st.container():
        st.markdown("### 🔍 Start New Research")
        company_input = st.text_input("Enter company name or ticker symbol", placeholder="e.g., AAPL, Microsoft, Tesla")

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Start Research", use_container_width=True):
                if company_input:
                    new_company = {
                        "id": len(st.session_state.company_history) + 1,
                        "name": company_input,
                        "status": "in-progress",
                        "date_started": datetime.now().strftime("%b %d, %Y"),
                        "progress": 0
                    }
                    st.session_state.company_history.insert(0, new_company)
                    st.session_state.show_modal = False
                    st.rerun()

        with col2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.show_modal = False
                st.rerun()

        st.markdown("---")

# ============================================================================
# MAIN HEADER
# ============================================================================
confidence_pct = data_meta['confidence_overall'] * 100 if data_meta['confidence_overall'] <= 1 else data_meta['confidence_overall']
st.markdown(f"""
<div class="main-header">
    <h1>🏢 {data_meta['company_name']} – Company Profile & Deep Research</h1>
    <p>Generated on {data_meta['extraction_date']} • Confidence Score: {confidence_pct:.0f}% • Fiscal Year: FY{int(data_meta['baseline_fiscal_year'])}</p>
</div>
""", unsafe_allow_html=True)

# Action buttons
col1, col2, col3, col4 = st.columns([2, 2, 2, 6])
with col1:
    if st.button("📥 Export PDF"):
        st.toast("Export functionality coming soon")
with col2:
    if st.button("📊 Run Scenario Analysis"):
        st.toast("Scenario analysis coming soon")

st.markdown("---")

# ============================================================================
# Section 1: Company Overview
# ============================================================================
st.markdown(f'<div class="section-header">📋 Company Overview – {data_meta["company_name"]}</div>', unsafe_allow_html=True)

# Get HQ info
hq = data_overview.get('headquarters', {})
hq_display = f"{hq.get('city', 'N/A')}, {hq.get('country', '')}" if hq else "N/A"

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Ticker", data_meta['ticker'])
with col2:
    st.metric("Market Cap", format_currency_billions(data_financial['financial_baseline'].get('market_cap_usd_millions')))
with col3:
    st.metric("Employees", safe_int(data_overview.get('employees')))
with col4:
    st.metric("Founded", int(data_overview['founded']) if data_overview.get('founded') else "N/A")
with col5:
    st.metric("HQ", hq_display)

st.markdown(f"**Value Chain Position:** {data_overview.get('value_chain_position', 'N/A')}")
st.markdown(f"**Description:** {data_overview.get('business_description', 'N/A')}")

# ============================================================================
# Section 2: Revenue Breakdown
# ============================================================================
fin_baseline = data_financial['financial_baseline']
fiscal_year = int(data_meta['baseline_fiscal_year'])

st.markdown(f'<div class="section-header">💰 Revenue Breakdown (FY {fiscal_year})</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    st.metric("Total Revenue", format_currency_billions(fin_baseline.get('revenue_usd_millions')))
    st.metric("Gross Margin", format_percentage(fin_baseline.get('gross_margin'), as_decimal=True))
    st.metric("Operating Margin", format_percentage(fin_baseline.get('operating_margin'), as_decimal=True))
    st.metric("Net Margin", format_percentage(fin_baseline.get('net_margin'), as_decimal=True))

with col2:
    # Build revenue data from business segments
    segments = data_financial.get('business_segments', [])
    if segments:
        revenue_data = pd.DataFrame({
            'Segment': [seg['name'] for seg in segments],
            'Revenue': [seg.get('revenue_usd_millions', 0) / 1000 for seg in segments],  # Convert to billions
            'Percentage': [seg.get('revenue_percent', 0) for seg in segments]
        })

        fig = px.pie(revenue_data, values='Revenue', names='Segment',
                     title='Revenue by Segment ($B)',
                     color_discrete_sequence=['#1e40af', '#3b82f6', '#93c5fd', '#60a5fa'],
                     hole=0.4)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# Section 3: Business Segments
# ============================================================================
st.markdown('<div class="section-header">📊 Business Segments Analysis</div>', unsafe_allow_html=True)

segments = data_financial.get('business_segments', [])
if segments:
    segments_df = pd.DataFrame({
        'Segment': [seg['name'] for seg in segments],
        'Revenue ($B)': [seg.get('revenue_usd_millions', 0) / 1000 for seg in segments],
        'YoY Growth (%)': [seg.get('yoy_growth_percent', 0) for seg in segments],
        'Margin (%)': [seg.get('operating_margin_percent', 0) for seg in segments]
    })

    col1, col2 = st.columns([2, 1])

    with col1:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=segments_df['Segment'],
            y=segments_df['Revenue ($B)'],
            name='Revenue ($B)',
            marker_color='#1e40af'
        ))
        fig.update_layout(
            title='Revenue by Business Segment',
            xaxis_title='',
            yaxis_title='Revenue ($B)',
            height=350,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.dataframe(segments_df, use_container_width=True, hide_index=True)

    # Segment descriptions
    for seg in segments:
        with st.expander(f"📄 {seg['name']} Details"):
            st.markdown(seg.get('description', 'No description available.'))

# ============================================================================
# Section 4: Geographic Exposure
# ============================================================================
st.markdown('<div class="section-header">🌍 Geographic Exposure</div>', unsafe_allow_html=True)

geo_tabs = st.tabs(["Revenue Distribution", "Manufacturing Footprint", "Key Facilities"])

with geo_tabs[0]:
    st.markdown(f"**Revenue by Geography (FY {fiscal_year})**")

    regions = data_financial.get('revenue_by_region', [])
    has_region_data = regions and any(
        (r.get('revenue_usd_millions') or 0) > 0 or (r.get('percent_of_total') or 0) > 0
        for r in regions
    )

    if has_region_data:
        geo_revenue_df = pd.DataFrame([
            {
                'Region': r.get('region', 'N/A'),
                'Revenue ($B)': (r.get('revenue_usd_millions') or 0) / 1000,
                'Percentage': r.get('percent_of_total') or 0,
                'YoY Growth': r.get('yoy_growth_percent')
            }
            for r in regions
        ])
        geo_revenue_df = geo_revenue_df.sort_values('Percentage', ascending=False)

        col1, col2 = st.columns([3, 2])

        with col1:
            fig = px.pie(
                geo_revenue_df,
                values='Percentage',
                names='Region',
                title='Revenue Distribution by Region',
                color_discrete_sequence=px.colors.qualitative.Set2,
                hole=0.4
            )
            fig.update_traces(textposition='outside', textinfo='label+percent')
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("##### Regional Breakdown")
            for _, row in geo_revenue_df.iterrows():
                growth = row['YoY Growth']
                growth_str = f"↑ {growth:.0f}%" if growth and growth > 0 else (f"↓ {abs(growth):.0f}%" if growth and growth < 0 else "")
                growth_color = "green" if growth and growth > 0 else ("red" if growth and growth < 0 else "gray")

                st.markdown(f"""
                **{row['Region']}**
                💰 ${row['Revenue ($B)']:.1f}B ({row['Percentage']:.0f}%)
                <span style="color:{growth_color}">{growth_str}</span>
                """, unsafe_allow_html=True)
                st.progress(row['Percentage'] / 100)
    else:
        geo_notes = data_customer_profile.get('customer_characteristics', {}).get('geographic_notes', '')
        if geo_notes:
            st.info(f"📍 **Geographic Distribution:** {geo_notes}")

        if regions:
            region_names = [r.get('region', 'N/A') for r in regions]
            st.markdown(f"**Regions Covered:** {' • '.join(region_names)}")
        else:
            st.info("Detailed regional revenue breakdown not available in current data.")

with geo_tabs[1]:
    st.markdown("**Manufacturing & Assembly Locations**")

    facilities = data_supply_chain.get('company_owned_facilities', [])
    if facilities:
        manufacturing_df = pd.DataFrame({
            'Location': [f"{f['city']}, {f['country']}" for f in facilities],
            'Region Served': [f.get('region_served', 'N/A') for f in facilities],
            'Type': [', '.join(f.get('roles', [])).title() for f in facilities],
            'Primary Products': [f.get('products', 'N/A')[:60] + '...' if len(f.get('products', '')) > 60 else f.get('products', 'N/A') for f in facilities]
        })

        st.dataframe(manufacturing_df, use_container_width=True, hide_index=True)

        # Pie chart by country
        country_counts = pd.Series([f['country'] for f in facilities]).value_counts()
        fig = px.pie(values=country_counts.values, names=country_counts.index,
                     title='Facilities by Country',
                     color_discrete_sequence=px.colors.qualitative.Set2)
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

with geo_tabs[2]:
    st.markdown("**Contract Manufacturers & Partners**")

    cms = data_supply_chain.get('contract_manufacturers', [])
    if cms:
        facilities_df = pd.DataFrame({
            'Manufacturer': [cm['manufacturer_name'] for cm in cms],
            'HQ Country': [cm.get('headquarters_country', 'N/A') for cm in cms],
            'Type': [cm.get('relationship_type', 'N/A').upper() for cm in cms],
            'Production Locations': [', '.join(cm.get('production_countries', []))[:40] + '...' if len(', '.join(cm.get('production_countries', []))) > 40 else ', '.join(cm.get('production_countries', [])) for cm in cms],
            'Dependency': [cm.get('dependency_level', 'N/A').capitalize() for cm in cms]
        })

        st.dataframe(facilities_df, use_container_width=True, hide_index=True)

# ============================================================================
# Section 5: Customer Profile
# ============================================================================
st.markdown('<div class="section-header">👥 Customer Profile</div>', unsafe_allow_html=True)

cust_tabs = st.tabs(["Segment Mix", "Top Customers", "Industry Exposure", "Customer Characteristics"])

with cust_tabs[0]:
    st.markdown("**Customer Segment Mix**")

    segment_mix = data_customer_profile.get('segment_mix', {})
    if segment_mix:
        col1, col2 = st.columns([1, 1])

        with col1:
            mix_data = pd.DataFrame({
                'Segment': ['B2B (Business)', 'B2C (Consumer)', 'B2G (Government)'],
                'Percentage': [
                    segment_mix.get('b2b_percent', 0),
                    segment_mix.get('b2c_percent', 0),
                    segment_mix.get('b2g_percent', 0)
                ]
            })

            fig = px.pie(mix_data, values='Percentage', names='Segment',
                         title='Revenue by Customer Segment',
                         color_discrete_sequence=['#1e40af', '#3b82f6', '#93c5fd'],
                         hole=0.4)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.metric("B2B (Business)", f"{segment_mix.get('b2b_percent', 0):.1f}%")
            st.metric("B2C (Consumer)", f"{segment_mix.get('b2c_percent', 0):.1f}%")
            st.metric("B2G (Government)", f"{segment_mix.get('b2g_percent', 0):.1f}%")

            if segment_mix.get('notes'):
                with st.expander("📋 Methodology Notes"):
                    st.markdown(segment_mix['notes'])

with cust_tabs[1]:
    st.markdown("**Customer Concentration & Top Customers**")

    # Customer concentration metrics
    cust_conc = data_customer_profile.get('customer_concentration', {})
    if cust_conc:
        col1, col2, col3 = st.columns(3)
        with col1:
            conc_level = cust_conc.get('concentration_level', 'N/A')
            level_color = "#10b981" if conc_level.lower() == 'low' else "#f59e0b" if conc_level.lower() == 'medium' else "#ef4444"
            st.markdown(f"""
            <div style="padding: 1rem; background: white; border: 1px solid #e2e8f0; border-radius: 0.5rem; text-align: center;">
                <div style="font-size: 0.875rem; color: #64748b;">Concentration Level</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: {level_color};">{conc_level.upper()}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.metric("Top Customer %", f"{cust_conc.get('top_customer_percent') or 0:.1f}%")
        with col3:
            st.metric("Top 10 Customers %", f"{cust_conc.get('top_10_customers_percent') or 0:.1f}%")

        if not cust_conc.get('any_customer_over_10_percent'):
            st.success("✅ No single customer exceeds 10% of revenue - well-diversified customer base")
        else:
            st.warning("⚠️ One or more customers exceed 10% of revenue")

    # Top customers table
    st.markdown("**Top Customers**")
    top_customers = data_customer_profile.get('top_customers', [])
    if top_customers:
        cust_df = pd.DataFrame({
            'Customer': [c.get('name', 'N/A') for c in top_customers],
            'Industry': [c.get('industry') or 'N/A' for c in top_customers],
            'Type': [(c.get('type') or 'N/A').capitalize() for c in top_customers],
            'Revenue %': [f"{c.get('percent_of_revenue') or 0:.2f}%" for c in top_customers]
        })
        st.dataframe(cust_df, use_container_width=True, hide_index=True)

        # Customer details
        for cust in top_customers:
            if cust.get('notes'):
                with st.expander(f"📄 {cust['name']} Details"):
                    st.markdown(cust['notes'])

with cust_tabs[2]:
    st.markdown("**Industry Exposure**")

    industries = data_customer_profile.get('industry_exposure', [])
    if industries:
        col1, col2 = st.columns([1, 1])

        with col1:
            ind_df = pd.DataFrame({
                'Industry': [ind['industry'] for ind in industries],
                'Revenue %': [ind.get('percent_of_revenue', 0) for ind in industries],
                'Trend': [ind.get('trend', 'N/A').capitalize() for ind in industries]
            })

            # Color by trend
            colors = []
            for ind in industries:
                trend = ind.get('trend', '').lower()
                if trend == 'growing':
                    colors.append('#10b981')
                elif trend == 'declining':
                    colors.append('#ef4444')
                else:
                    colors.append('#3b82f6')

            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=ind_df['Industry'],
                y=ind_df['Revenue %'],
                marker_color=colors,
                text=ind_df['Trend'],
                textposition='outside'
            ))
            fig.update_layout(
                title='Revenue by Industry Vertical',
                xaxis_title='',
                yaxis_title='Revenue %',
                height=400,
                xaxis_tickangle=-45,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.dataframe(ind_df, use_container_width=True, hide_index=True)

            # Legend
            st.markdown("""
            **Trend Legend:**
            - 🟢 Growing
            - 🔵 Stable
            - 🔴 Declining
            """)

    # Industry notes
    for ind in industries:
        if ind.get('notes'):
            with st.expander(f"📄 {ind['industry']} Notes"):
                st.markdown(ind['notes'])

with cust_tabs[3]:
    st.markdown("**Customer Characteristics**")

    chars = data_customer_profile.get('customer_characteristics', {})
    if chars:
        col1, col2 = st.columns(2)

        with col1:
            if chars.get('typical_contract_length'):
                st.markdown("**📅 Typical Contract Length**")
                st.info(chars['typical_contract_length'])

            if chars.get('geographic_notes'):
                st.markdown("**🌍 Geographic Distribution**")
                st.info(chars['geographic_notes'])

        with col2:
            if chars.get('recurring_vs_transactional'):
                st.markdown("**💰 Revenue Model (Recurring vs Transactional)**")
                st.info(chars['recurring_vs_transactional'])

# ============================================================================
# Section 6: Supply Chain Dependencies
# ============================================================================
st.markdown('<div class="section-header">🔗 Supply Chain Dependencies</div>', unsafe_allow_html=True)

supply_tabs = st.tabs(["Critical Suppliers", "Contract Manufacturers", "Component Analysis"])

with supply_tabs[0]:
    st.markdown("**Top Critical Suppliers**")

    suppliers = data_supply_chain.get('critical_suppliers', [])
    if suppliers:
        suppliers_df = pd.DataFrame({
            'Supplier': [s['supplier_name'] for s in suppliers],
            'Component': [s.get('provides', s.get('component_category', 'N/A')) for s in suppliers],
            'HQ Country': [s.get('headquarters_country', 'N/A') for s in suppliers],
            'Dependency': [s.get('dependency_level', 'N/A').capitalize() for s in suppliers],
            'Manufacturing Locations': [', '.join(s.get('manufacturing_locations', []))[:30] + '...' if len(', '.join(s.get('manufacturing_locations', []))) > 30 else ', '.join(s.get('manufacturing_locations', [])) for s in suppliers]
        })

        st.dataframe(suppliers_df, use_container_width=True, hide_index=True)

        # Warning about high dependency suppliers
        high_dep = [s for s in suppliers if s.get('dependency_level') == 'high']
        if high_dep:
            supplier_names = ', '.join([s['supplier_name'] for s in high_dep[:3]])
            st.warning(f"⚠️ **Key Dependencies:** High dependency on {supplier_names}. Critical for supply chain resilience.")

with supply_tabs[1]:
    st.markdown("**Contract Manufacturers (ODM/OEM Partners)**")

    cms = data_supply_chain.get('contract_manufacturers', [])
    if cms:
        cm_df = pd.DataFrame({
            'Manufacturer': [cm['manufacturer_name'] for cm in cms],
            'Location': [f"{cm.get('headquarters_country', 'N/A')}" for cm in cms],
            'Products': [', '.join(cm.get('products_manufactured', []))[:40] + '...' if len(', '.join(cm.get('products_manufactured', []))) > 40 else ', '.join(cm.get('products_manufactured', [])) for cm in cms],
            'Relationship': [cm.get('relationship_type', 'N/A').upper() for cm in cms],
            'Dependency': [cm.get('dependency_level', 'N/A').capitalize() for cm in cms]
        })

        st.dataframe(cm_df, use_container_width=True, hide_index=True)

with supply_tabs[2]:
    st.markdown("**Component Sourcing Analysis**")

    # Group suppliers by component category
    suppliers = data_supply_chain.get('critical_suppliers', [])
    if suppliers:
        categories = {}
        for s in suppliers:
            cat = s.get('component_category', 'Other')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(s['supplier_name'])

        components_df = pd.DataFrame({
            'Component Category': list(categories.keys()),
            'Primary Suppliers': [', '.join(sups[:3]) for sups in categories.values()],
            'Supplier Count': [len(sups) for sups in categories.values()],
            'Concentration': ['High' if len(sups) <= 2 else 'Medium' if len(sups) <= 4 else 'Low' for sups in categories.values()]
        })

        st.dataframe(components_df, use_container_width=True, hide_index=True)

    # Supply chain concentration notes
    concentration = data_supply_chain.get('supplier_concentration', {})
    if concentration.get('concentration_notes'):
        st.info(f"📋 {concentration['concentration_notes']}")

# ============================================================================
# Section 6: Concentration & Risk Flags
# ============================================================================
st.markdown('<div class="section-header">⚠️ Concentration & Risk Analysis</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Supplier Concentration Risks**")

    # Generate risks from data
    suppliers = data_supply_chain.get('critical_suppliers', [])
    cms = data_supply_chain.get('contract_manufacturers', [])

    risk_data = []

    # CPU/GPU supplier risk
    cpu_gpu = [s for s in suppliers if s.get('component_category') in ['CPU', 'GPU'] and s.get('dependency_level') == 'high']
    if cpu_gpu:
        risk_data.append(("CPU/GPU Supplier Dependency", "High", f"High dependency on {', '.join([s['supplier_name'] for s in cpu_gpu[:2]])}"))

    # Memory supplier risk
    memory = [s for s in suppliers if s.get('component_category') == 'memory' and s.get('dependency_level') == 'high']
    if memory:
        risk_data.append(("Memory Supply Concentration", "Medium", f"Top {len(memory)} memory suppliers with high dependency"))

    # Taiwan exposure
    taiwan_cms = [cm for cm in cms if cm.get('headquarters_country') == 'Taiwan']
    if len(taiwan_cms) >= 3:
        risk_data.append(("Taiwan Geopolitical Risk", "High", f"Significant ODM/CM exposure in Taiwan ({len(taiwan_cms)} manufacturers)"))

    # Single source risks
    single_source = [s for s in suppliers if s.get('single_source') == True]
    if single_source:
        risk_data.append(("Single Source Components", "High", f"{len(single_source)} components with single-source suppliers"))

    for item, level, desc in risk_data:
        risk_class = "risk-high" if level == "High" else "risk-medium"
        st.markdown(f"""
        <div style="padding: 0.75rem; background: white; border: 1px solid #e2e8f0; border-radius: 0.375rem; margin-bottom: 0.75rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <strong style="font-size: 0.875rem; color: #1e293b;">{item}</strong>
                <span class="{risk_class}">{level}</span>
            </div>
            <div style="font-size: 0.8125rem; color: #64748b;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.markdown("**Geographic & Operational Risks**")

    geo_risks = []

    # China manufacturing exposure
    facilities = data_supply_chain.get('company_owned_facilities', [])
    china_facilities = [f for f in facilities if f.get('country') == 'China']
    if china_facilities:
        geo_risks.append(("China Manufacturing Exposure", "High" if len(china_facilities) >= 2 else "Medium", f"{len(china_facilities)} facilities in China; geopolitical tensions impact"))

    # Customer concentration
    cust_conc = data_customer_profile.get('customer_concentration', {})
    conc_level = cust_conc.get('concentration_level') or 'N/A'
    top_cust_pct = cust_conc.get('top_customer_percent') or 0
    if conc_level.lower() == 'low':
        geo_risks.append(("Revenue Concentration", "Low", f"Well-diversified: largest customer ~{top_cust_pct:.1f}% of revenue"))
    elif conc_level.lower() == 'high':
        geo_risks.append(("Revenue Concentration", "High", f"Top customer represents {top_cust_pct:.1f}% of revenue"))

    # Balance sheet risk
    bs_strength = fin_baseline.get('balance_sheet_strength') or 'N/A'
    debt_to_equity = fin_baseline.get('debt_to_equity') or 0
    if bs_strength.lower() == 'weak':
        geo_risks.append(("Balance Sheet Strength", "High", f"Weak balance sheet (D/E: {debt_to_equity:.1f})"))
    elif bs_strength.lower() == 'moderate':
        geo_risks.append(("Balance Sheet Strength", "Medium", f"Moderate balance sheet strength"))

    for item, level, desc in geo_risks:
        risk_class = "risk-high" if level == "High" else ("risk-medium" if level == "Medium" else "risk-low")
        st.markdown(f"""
        <div style="padding: 0.75rem; background: white; border: 1px solid #e2e8f0; border-radius: 0.375rem; margin-bottom: 0.75rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <strong style="font-size: 0.875rem; color: #1e293b;">{item}</strong>
                <span class="{risk_class}">{level}</span>
            </div>
            <div style="font-size: 0.8125rem; color: #64748b;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# Key Takeaways
# ============================================================================
st.markdown('<div class="section-header">💡 Key Takeaways & Strategic Considerations</div>', unsafe_allow_html=True)

# Generate takeaways from data
takeaways = []

# Segment growth
segments = data_financial.get('business_segments', [])
growing_segments = [s for s in segments if s.get('yoy_growth_percent', 0) > 10]
if growing_segments:
    top_growth = max(growing_segments, key=lambda x: x.get('yoy_growth_percent', 0))
    takeaways.append(f"**Strong Segment Growth:** {top_growth['name']} growing {top_growth.get('yoy_growth_percent', 0):.0f}% YoY")

# Supply chain initiatives
initiatives = data_supply_chain.get('supply_chain_initiatives', [])
if initiatives:
    takeaways.append(f"**Supply Chain Diversification:** {len(initiatives)} active initiatives including {initiatives[0].get('initiative', 'N/A')}")

# Customer diversification
cust_conc = data_customer_profile.get('customer_concentration', {})
if not cust_conc.get('any_customer_over_10_percent'):
    takeaways.append("**Customer Diversification:** No single customer exceeds 10% of revenue - well-diversified base")

# Geographic exposure
if china_facilities:
    takeaways.append(f"**Geographic Risk:** {len(china_facilities)} manufacturing facilities in China; consider China+1 strategy")

# Display takeaways
for i, takeaway in enumerate(takeaways, 1):
    st.markdown(f"{i}. {takeaway}")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #64748b; font-size: 0.75rem; padding: 1rem;">
    This report is generated using publicly available information and should not be considered financial advice.<br>
    Data sources: {data_meta.get('data_freshness_note', 'Company filings, industry reports')} • Confidence Score: {confidence_pct:.0f}%
</div>
""", unsafe_allow_html=True)
