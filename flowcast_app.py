#!/usr/bin/env python3
"""
FlowCast Report Generator by Books & Balances
Financial health check in 60 seconds - Upload Xero data, instantly see where you are,
where you're heading, and what to notice.

To run:
    pip install -r requirements.txt
    streamlit run flowcast_app.py
"""

import streamlit as st
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Import FlowCast modules
from parser import FlowCastParser
from charts import ChartGenerator, fig_to_bytes, COLORS
from metrics import MetricsCalculator
from forecaster import Forecaster
from insights import InsightGenerator
from exporters.excel import create_excel_report, create_zip_download

# Page configuration
st.set_page_config(
    page_title="FlowCast by Books & Balances",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern Blue/Slate Brand Colors (Linear/Vercel inspired)
BRAND = {
    'primary': '#3B82F6',       # Modern blue
    'primary_light': '#60A5FA', # Lighter blue
    'primary_dark': '#2563EB',  # Darker blue for hover
    'secondary': '#10B981',     # Green accent
    'accent': '#8B5CF6',        # Purple accent
    'positive': '#10B981',      # Success green (emerald)
    'negative': '#EF4444',      # Alert red
    'text': '#1E293B',          # Slate 800 - very dark, readable
    'text_secondary': '#64748B', # Slate 500 - secondary
    'text_muted': '#94A3B8',    # Slate 400 - muted
    'background': '#F8FAFC',    # Slate 50
    'surface_1': '#FFFFFF',     # White surface
    'surface_2': '#F1F5F9',     # Slate 100
    'card': '#FFFFFF',          # Card background
    'border': '#E2E8F0',        # Slate 200
    'border_subtle': '#F1F5F9', # Very light border
    'border_default': '#E2E8F0', # Default border
}

# Custom CSS - Modern SaaS Design (Linear/Notion/Vercel inspired)
st.markdown(f"""
<style>
    /* ============================================
       NUCLEAR RESET - Override ALL Streamlit defaults
       ============================================ */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    .stApp * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }}

    /* Remove Streamlit's random padding/margins */
    .block-container {{
        padding: 2rem 3rem !important;
        max-width: 1200px !important;
    }}

    /* Force ALL text to be visible */
    .stApp p, .stApp span, .stApp div, .stApp label {{
        color: {BRAND['text']} !important;
    }}

    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    /* App background */
    .stApp {{
        background: {BRAND['background']} !important;
    }}

    /* ============================================
       CSS VARIABLES
       ============================================ */
    :root {{
        --space-1: 0.25rem;
        --space-2: 0.5rem;
        --space-3: 0.75rem;
        --space-4: 1rem;
        --space-5: 1.5rem;
        --space-6: 2rem;
        --space-7: 3rem;
        --radius-sm: 6px;
        --radius-md: 8px;
        --radius-lg: 12px;
        --radius-xl: 16px;
        --radius-full: 9999px;
        --shadow-sm: 0 1px 2px rgba(0,0,0,0.04), 0 1px 3px rgba(0,0,0,0.03);
        --shadow-md: 0 4px 6px rgba(0,0,0,0.04), 0 2px 4px rgba(0,0,0,0.03);
        --shadow-lg: 0 10px 25px rgba(0,0,0,0.06), 0 5px 10px rgba(0,0,0,0.04);
        --transition: 0.2s ease;
    }}

    /* ============================================
       TYPOGRAPHY
       ============================================ */
    .main-header {{
        background: linear-gradient(135deg, {BRAND['primary']} 0%, {BRAND['primary_dark']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.25rem;
        letter-spacing: -0.02em;
    }}

    .sub-header {{
        font-size: 1.125rem;
        color: {BRAND['text_secondary']} !important;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }}

    .brand-tag {{
        display: inline-block;
        background: {BRAND['primary']};
        color: white !important;
        padding: 0.375rem 0.875rem;
        border-radius: var(--radius-full);
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        margin-bottom: 1rem;
        text-transform: uppercase;
    }}

    /* ============================================
       SECTION HEADERS - Clean underline
       ============================================ */
    .section-header {{
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        color: {BRAND['text']} !important;
        margin: 2.5rem 0 1.25rem 0 !important;
        padding-bottom: 0.75rem !important;
        border-bottom: 2px solid {BRAND['border']} !important;
        display: block !important;
    }}

    /* ============================================
       FEATURE GRID - Forces equal height cards
       ============================================ */
    .feature-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
        align-items: stretch;
        margin: 1.5rem 0;
    }}

    .feature-grid-4 {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        align-items: stretch;
        margin: 1.5rem 0;
    }}

    @media (max-width: 768px) {{
        .feature-grid, .feature-grid-4 {{
            grid-template-columns: 1fr;
        }}
    }}

    /* ============================================
       FEATURE CARDS - Equal height, clean style
       ============================================ */
    .feature-card {{
        background: {BRAND['card']};
        border: 1px solid {BRAND['border']};
        border-radius: var(--radius-lg);
        padding: 1.75rem;
        display: flex;
        flex-direction: column;
        min-height: 180px;
        text-align: center;
        transition: all var(--transition);
    }}

    .feature-card:hover {{
        border-color: #CBD5E1;
        box-shadow: var(--shadow-lg);
        transform: translateY(-2px);
    }}

    .feature-icon {{
        font-size: 2.25rem;
        margin-bottom: 1rem;
        line-height: 1;
    }}

    .feature-title {{
        color: {BRAND['text']} !important;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }}

    .feature-desc {{
        color: {BRAND['text_secondary']} !important;
        font-size: 0.875rem;
        line-height: 1.5;
        flex-grow: 1;
    }}

    /* ============================================
       METRIC CARDS
       ============================================ */
    .metric-card {{
        background: {BRAND['card']};
        border: 1px solid {BRAND['border']};
        border-radius: var(--radius-lg);
        padding: 1.25rem;
        transition: all var(--transition);
    }}

    .metric-card:hover {{
        border-color: #CBD5E1;
        box-shadow: var(--shadow-md);
    }}

    .metric-label {{
        font-size: 0.75rem;
        color: {BRAND['text_secondary']} !important;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }}

    .metric-value {{
        font-size: 1.5rem;
        font-weight: 700;
        color: {BRAND['text']} !important;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}

    /* ============================================
       STATUS INDICATORS
       ============================================ */
    .status-dot {{
        width: 10px;
        height: 10px;
        border-radius: var(--radius-full);
        display: inline-block;
        margin-right: 0.5rem;
    }}

    .status-green {{ background: {BRAND['positive']}; }}
    .status-yellow {{ background: #F59E0B; }}
    .status-red {{ background: {BRAND['negative']}; }}
    .status-neutral {{ background: {BRAND['text_muted']}; }}

    /* ============================================
       HEALTH BADGE
       ============================================ */
    .health-badge {{
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1.25rem;
        border-radius: var(--radius-full);
        font-weight: 600;
        font-size: 0.875rem;
    }}

    .health-green {{
        background: {BRAND['positive']};
        color: white !important;
    }}

    .health-yellow {{
        background: #F59E0B;
        color: white !important;
    }}

    .health-red {{
        background: {BRAND['negative']};
        color: white !important;
    }}

    /* ============================================
       INSIGHT BOXES
       ============================================ */
    .insight-box {{
        border-radius: var(--radius-lg);
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        border: 1px solid {BRAND['border']};
        transition: all var(--transition);
    }}

    .insight-box:hover {{
        box-shadow: var(--shadow-sm);
    }}

    .insight-positive {{
        background: #ECFDF5;
        border-left: 3px solid {BRAND['positive']};
    }}

    .insight-negative {{
        background: #FEF2F2;
        border-left: 3px solid {BRAND['negative']};
    }}

    .insight-neutral {{
        background: #EFF6FF;
        border-left: 3px solid {BRAND['primary']};
    }}

    .insight-icon {{
        font-size: 1.125rem;
        flex-shrink: 0;
    }}

    .insight-text {{
        color: {BRAND['text']} !important;
        font-size: 0.875rem;
        line-height: 1.5;
    }}

    /* ============================================
       STREAMLIT METRIC - Override defaults
       ============================================ */
    [data-testid="stMetric"] {{
        background: {BRAND['card']} !important;
        border: 1px solid {BRAND['border']} !important;
        border-radius: var(--radius-lg) !important;
        padding: 1.25rem !important;
    }}

    [data-testid="stMetricValue"], [data-testid="stMetricValue"] > div {{
        color: {BRAND['text']} !important;
        font-weight: 700 !important;
    }}

    [data-testid="stMetricLabel"], [data-testid="stMetricLabel"] > div {{
        color: {BRAND['text_secondary']} !important;
    }}

    [data-testid="stMetricDelta"] {{
        color: {BRAND['text_secondary']} !important;
    }}

    [data-testid="stMetricDelta"] svg {{
        display: none;
    }}

    /* ============================================
       BUTTONS - Modern gradient style
       ============================================ */
    .stDownloadButton > button,
    [data-testid="stDownloadButton"] > button,
    .stButton > button {{
        background: linear-gradient(135deg, {BRAND['primary']} 0%, {BRAND['primary_dark']} 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        padding: 0.625rem 1.25rem !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3) !important;
        transition: all var(--transition) !important;
    }}

    .stDownloadButton > button:hover,
    [data-testid="stDownloadButton"] > button:hover,
    .stButton > button:hover {{
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.4) !important;
    }}

    .stDownloadButton > button:active,
    .stButton > button:active {{
        transform: translateY(0) !important;
    }}

    /* ============================================
       FILE UPLOADER - Complete redesign
       ============================================ */
    [data-testid="stFileUploader"] {{
        background: transparent !important;
    }}

    [data-testid="stFileUploader"] > div {{
        background: transparent !important;
    }}

    /* Hide the label area if it's causing issues */
    [data-testid="stFileUploader"] > div:first-child > div:first-child {{
        color: {BRAND['text']} !important;
    }}

    [data-testid="stFileUploader"] section {{
        background: {BRAND['card']} !important;
        border: 2px dashed {BRAND['border']} !important;
        border-radius: var(--radius-xl) !important;
        padding: 2.5rem 2rem !important;
        transition: all var(--transition) !important;
    }}

    [data-testid="stFileUploader"] section:hover {{
        border-color: {BRAND['primary']} !important;
        background: #F8FAFC !important;
    }}

    [data-testid="stFileUploader"] section > div {{
        background: transparent !important;
    }}

    [data-testid="stFileUploader"] button {{
        background: linear-gradient(135deg, {BRAND['primary']} 0%, {BRAND['primary_dark']} 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4) !important;
        transition: all var(--transition) !important;
    }}

    [data-testid="stFileUploader"] button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5) !important;
    }}

    [data-testid="stFileUploader"] small {{
        color: {BRAND['text_secondary']} !important;
    }}

    [data-testid="stFileUploader"] [data-testid="stMarkdownContainer"] p {{
        color: {BRAND['text']} !important;
        font-weight: 500 !important;
    }}

    /* ============================================
       SELECTBOX - Modern styling
       ============================================ */
    [data-testid="stSelectbox"] > div > div {{
        background: {BRAND['card']} !important;
        border: 1px solid {BRAND['border']} !important;
        border-radius: var(--radius-md) !important;
        transition: all var(--transition) !important;
    }}

    [data-testid="stSelectbox"] > div > div:hover {{
        border-color: {BRAND['primary_light']} !important;
    }}

    [data-testid="stSelectbox"] > div > div:focus-within {{
        border-color: {BRAND['primary']} !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }}

    /* ============================================
       CHART CONTAINER
       ============================================ */
    .chart-container {{
        background: {BRAND['card']};
        border-radius: var(--radius-lg);
        padding: 1rem;
        box-shadow: var(--shadow-sm);
        border: 1px solid {BRAND['border']};
        margin-bottom: 1rem;
        transition: all var(--transition);
    }}

    .chart-container:hover {{
        box-shadow: var(--shadow-md);
    }}

    /* ============================================
       PRO TIP BOX
       ============================================ */
    .pro-tip-box {{
        background: #EFF6FF;
        padding: 1.5rem;
        border-radius: var(--radius-lg);
        text-align: center;
        border: 1px solid #DBEAFE;
    }}

    .pro-tip-box .tip-icon {{
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }}

    .pro-tip-box .tip-title {{
        color: {BRAND['primary']} !important;
        font-weight: 600;
        font-size: 1rem;
    }}

    .pro-tip-box .tip-text {{
        color: {BRAND['text_secondary']} !important;
        font-size: 0.875rem;
        margin-top: 0.5rem;
        line-height: 1.5;
    }}

    /* ============================================
       MESSAGES
       ============================================ */
    .stSuccess {{
        background: #ECFDF5 !important;
        border-left: 3px solid {BRAND['positive']} !important;
        border-radius: var(--radius-md) !important;
    }}

    .stInfo {{
        background: #EFF6FF !important;
        border-left: 3px solid {BRAND['primary']} !important;
        border-radius: var(--radius-md) !important;
    }}

    /* ============================================
       CAPTION TEXT
       ============================================ */
    .stCaption, [data-testid="stCaption"] {{
        color: {BRAND['text_secondary']} !important;
    }}

    /* ============================================
       LABELS
       ============================================ */
    label[data-testid="stWidgetLabel"] {{
        color: {BRAND['text']} !important;
        font-weight: 500 !important;
    }}

    /* ============================================
       FOOTER
       ============================================ */
    .footer {{
        text-align: center;
        color: {BRAND['text_secondary']} !important;
        font-size: 0.875rem;
        padding: 1.5rem 0;
    }}

    .footer a {{
        color: {BRAND['primary']} !important;
        text-decoration: none;
        font-weight: 500;
    }}

    .footer a:hover {{
        text-decoration: underline;
    }}

    .footer .tagline {{
        font-size: 0.75rem;
        color: {BRAND['text_muted']} !important;
        margin-top: 0.25rem;
    }}

    /* ============================================
       ANIMATIONS
       ============================================ */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(8px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    .animate-in {{
        animation: fadeIn 0.3s ease-out forwards;
    }}

    /* ============================================
       DIVIDER OVERRIDE
       ============================================ */
    hr {{
        border: none !important;
        border-top: 1px solid {BRAND['border']} !important;
        margin: 1.5rem 0 !important;
    }}
</style>
""", unsafe_allow_html=True)


def get_status_indicator(status: str) -> str:
    """Return HTML for status indicator dot."""
    return f'<span class="status-dot status-{status}"></span>'


def get_status_icon(status: str) -> str:
    """Return emoji for insight type."""
    icons = {
        'positive': '✨',
        'negative': '⚠️',
        'neutral': '💡'
    }
    return icons.get(status, '💡')


def render_metric_card(label: str, value: str, status: str):
    """Render a beautiful metric card with status indicator."""
    indicator = get_status_indicator(status)
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{indicator}{value}</div>
    </div>
    """, unsafe_allow_html=True)


def render_insights(insights: list):
    """Render the insights panel with beautiful styling."""
    for insight in insights:
        icon = get_status_icon(insight['type'])
        insight_class = f"insight-{insight['type']}"
        st.markdown(f'''
        <div class="insight-box {insight_class}">
            <span class="insight-icon">{icon}</span>
            <span class="insight-text">{insight["text"]}</span>
        </div>
        ''', unsafe_allow_html=True)


def get_feature_card_html(icon: str, title: str, description: str) -> str:
    """Return HTML for a feature card (used in grid layouts)."""
    return f'''
    <div class="feature-card">
        <div class="feature-icon">{icon}</div>
        <div class="feature-title">{title}</div>
        <div class="feature-desc">{description}</div>
    </div>
    '''


def render_feature_grid(cards: list, columns: int = 3):
    """Render feature cards in a CSS Grid for equal heights."""
    grid_class = "feature-grid" if columns == 3 else "feature-grid-4"
    cards_html = "".join([get_feature_card_html(c['icon'], c['title'], c['desc']) for c in cards])
    st.markdown(f'''
    <div class="{grid_class}">
        {cards_html}
    </div>
    ''', unsafe_allow_html=True)


# =============================================================================
# MAIN APP
# =============================================================================

def main():
    # Header with branding
    st.markdown('<div style="text-align: center;"><span class="brand-tag">BOOKS & BALANCES</span></div>', unsafe_allow_html=True)
    st.markdown('<p class="main-header">FlowCast</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Financial health check in 60 seconds</p>', unsafe_allow_html=True)

    # File upload section
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        uploaded_file = st.file_uploader(
            "📁 Upload your Xero P&L Export",
            type=['xlsx', 'xls'],
            help="Export your Profit & Loss report from Xero as 'Current financial Year Month by Month'"
        )

        # Currency selector
        currency = st.selectbox(
            "💱 Currency",
            options=['£ GBP', '$ USD', '€ EUR', 'A$ AUD', 'C$ CAD'],
            index=0,
            help="Select your currency for the report"
        )
        currency_symbol = currency.split(' ')[0]

    if uploaded_file is not None:
        try:
            # Parse the file
            with st.spinner('✨ Analysing your financial data...'):
                parser = FlowCastParser(uploaded_file)
                data = parser.parse()

                # Calculate metrics
                metrics_calc = MetricsCalculator(data)
                metrics = metrics_calc.calculate_all()
                health_summary = metrics_calc.get_health_summary()

                # Generate forecast
                forecaster = Forecaster(data, horizon=6)
                forecast_data = forecaster.generate_forecast()

                # Generate insights
                insight_gen = InsightGenerator(data, metrics, forecast_data)
                insights = insight_gen.generate_insights()

            # Show success message
            st.success(f"✅ Successfully loaded data for **{data.get('company', 'your company')}**")

            # =================================================================
            # SUMMARY CARD - Key Metrics with Traffic Lights
            # =================================================================
            st.markdown('<div class="section-header">📊 Financial Health Summary</div>', unsafe_allow_html=True)

            # Overall health badge
            health_status = health_summary['overall_status']
            health_text = health_summary['overall']
            health_icons = {'green': '🌟', 'yellow': '⚡', 'red': '🔔'}
            health_icon = health_icons.get(health_status, '📊')

            st.markdown(f'<span class="health-badge health-{health_status}">{health_icon} {health_text}</span>',
                       unsafe_allow_html=True)

            st.markdown("")

            # Key metrics in columns
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                gm = metrics['gross_margin']
                render_metric_card("Gross Margin", gm['formatted'], gm['status'])

            with col2:
                om = metrics['operating_margin']
                render_metric_card("Operating Margin", om['formatted'], om['status'])

            with col3:
                rt = metrics['revenue_trend']
                render_metric_card("Revenue Trend", rt['formatted'], rt['status'])

            with col4:
                cc = metrics['cost_control']
                render_metric_card("Cost Control", cc['formatted'], cc['status'])

            # Additional metrics row
            st.markdown("")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                tr = metrics['total_revenue']
                st.metric("💰 Total Revenue", f"{currency_symbol}{tr['value']:,.0f}")

            with col2:
                tp = metrics['total_profit']
                delta_color = "normal" if tp['value'] >= 0 else "inverse"
                st.metric("📈 Operating Profit", f"{currency_symbol}{tp['value']:,.0f}",
                         delta=f"{metrics['operating_margin']['formatted']} margin",
                         delta_color=delta_color)

            with col3:
                br = metrics['monthly_burn_rate']
                st.metric("🔥 Monthly Burn Rate", f"{currency_symbol}{br['value']:,.0f}")

            with col4:
                le = metrics['largest_expense']
                st.metric("📋 Largest Expense", le['category'],
                         delta=f"{le['percentage']:.0f}% of costs")

            st.markdown("---")

            # =================================================================
            # INSIGHTS PANEL
            # =================================================================
            st.markdown('<div class="section-header">💡 Key Insights</div>', unsafe_allow_html=True)

            if insights:
                render_insights(insights)
            else:
                st.info("Upload more data to generate insights.")

            st.markdown("---")

            # =================================================================
            # CHARTS with Forecast Overlay
            # =================================================================
            st.markdown('<div class="section-header">📈 Charts & Forecasts</div>', unsafe_allow_html=True)

            # Generate charts with forecast data and currency
            with st.spinner('🎨 Creating beautiful charts...'):
                generator = ChartGenerator(data, forecast_data, currency=currency_symbol)
                charts = {
                    'operating_profit': generator.create_operating_profit_chart(),
                    'admin_costs_pie': generator.create_admin_costs_pie(),
                    'revenue_profit_trend': generator.create_revenue_profit_trend(),
                    'profit_expenses_trend': generator.create_profit_expenses_trend(),
                }

            # Display charts in a grid
            col1, col2 = st.columns(2)

            with col1:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.pyplot(charts['revenue_profit_trend'])
                st.caption("📊 Dashed lines show 6-month forecast with confidence bands")
                st.download_button(
                    "⬇️ Download Trend Chart",
                    fig_to_bytes(charts['revenue_profit_trend']),
                    "revenue_profit_trend.png",
                    "image/png"
                )
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.pyplot(charts['operating_profit'])
                st.download_button(
                    "⬇️ Download Profit Chart",
                    fig_to_bytes(charts['operating_profit']),
                    "operating_profit.png",
                    "image/png"
                )
                st.markdown('</div>', unsafe_allow_html=True)

            col3, col4 = st.columns(2)

            with col3:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.pyplot(charts['profit_expenses_trend'])
                st.download_button(
                    "⬇️ Download Cumulative Chart",
                    fig_to_bytes(charts['profit_expenses_trend']),
                    "profit_expenses_trend.png",
                    "image/png"
                )
                st.markdown('</div>', unsafe_allow_html=True)

            with col4:
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.pyplot(charts['admin_costs_pie'])
                st.download_button(
                    "⬇️ Download Costs Chart",
                    fig_to_bytes(charts['admin_costs_pie']),
                    "admin_costs_pie.png",
                    "image/png"
                )
                st.markdown('</div>', unsafe_allow_html=True)

            # =================================================================
            # DOWNLOAD SECTION
            # =================================================================
            st.markdown("---")
            st.markdown('<div class="section-header">📦 Download Reports</div>', unsafe_allow_html=True)

            # Try to import PDF and PPTX exporters
            pdf_data = None
            pptx_data = None

            try:
                from exporters.pdf import create_pdf_report
                pdf_data = create_pdf_report(data, metrics, insights, forecast_data, currency_symbol)
            except ImportError:
                pass
            except Exception:
                pass

            try:
                from exporters.pptx import create_pptx_report
                pptx_data = create_pptx_report(data, metrics, insights, charts, forecast_data, currency_symbol)
            except ImportError as e:
                st.warning(f"PowerPoint export unavailable: Missing module - {e}")
            except Exception as e:
                st.warning(f"PowerPoint export error: {e}")

            # Create columns for download buttons
            if pdf_data and pptx_data:
                col1, col2, col3, col4 = st.columns(4)
            elif pdf_data or pptx_data:
                col1, col2, col3 = st.columns(3)
            else:
                col1, col2 = st.columns(2)

            with col1:
                excel_data = create_excel_report(data, charts, metrics, forecast_data)
                st.download_button(
                    "📊 Excel Report",
                    excel_data,
                    "FlowCast_Report.xlsx",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

            with col2:
                zip_data = create_zip_download(charts, excel_data, pdf_data, pptx_data)
                st.download_button(
                    "📁 Everything (ZIP)",
                    zip_data,
                    "FlowCast_Complete.zip",
                    "application/zip",
                    use_container_width=True
                )

            if pdf_data:
                with col3:
                    st.download_button(
                        "📄 PDF Report",
                        pdf_data,
                        "FlowCast_Report.pdf",
                        "application/pdf",
                        use_container_width=True
                    )

            if pptx_data:
                col_idx = col4 if pdf_data else col3
                with col_idx:
                    st.download_button(
                        "📽️ PowerPoint",
                        pptx_data,
                        "FlowCast_Report.pptx",
                        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        use_container_width=True
                    )

            # Footer
            st.markdown("---")
            st.markdown("""
            <div class="footer">
                <strong>FlowCast</strong> by <a href="https://www.booksandbalances.co.uk" target="_blank">Books & Balances</a>
                <div class="tagline">Financial clarity, delivered beautifully.</div>
            </div>
            """, unsafe_allow_html=True)

            # Close all figures to free memory
            for fig in charts.values():
                plt.close(fig)

        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            st.info("Please make sure you've uploaded a valid Xero Profit & Loss export in the 'Month by Month' format.")
            import traceback
            with st.expander("Show technical details"):
                st.code(traceback.format_exc())

    else:
        # Show beautiful landing page when no file uploaded
        st.markdown("---")

        # How it works section - CSS Grid for equal heights
        st.markdown('<div class="section-header">How It Works</div>', unsafe_allow_html=True)

        render_feature_grid([
            {'icon': '📤', 'title': '1. Export from Xero', 'desc': 'Go to Reporting → Profit and Loss → Month by Month → Export to Excel'},
            {'icon': '⬆️', 'title': '2. Upload Here', 'desc': 'Drag and drop your Excel file above. We\'ll analyse it instantly.'},
            {'icon': '📊', 'title': '3. Get Insights', 'desc': 'See your financial health, forecasts, and download beautiful reports.'},
        ], columns=3)

        st.markdown("---")

        # What you get section - CSS Grid for equal heights (4 columns)
        st.markdown('<div class="section-header">What You Get</div>', unsafe_allow_html=True)

        render_feature_grid([
            {'icon': '🎯', 'title': 'Health Metrics', 'desc': 'Gross margin, operating margin, revenue trends, and cost control indicators with traffic light status.'},
            {'icon': '🔮', 'title': '6-Month Forecast', 'desc': 'AI-powered projections with confidence bands. See where your business is heading.'},
            {'icon': '💡', 'title': 'Smart Insights', 'desc': 'Automated analysis that surfaces what matters. No more guessing, just clarity.'},
            {'icon': '📦', 'title': 'Export Anywhere', 'desc': 'Download as PNG charts, Excel workbook, PDF report, or PowerPoint deck.'},
        ], columns=4)

        st.markdown("---")

        # Pro tip
        st.markdown("""
        <div class="pro-tip-box">
            <div class="tip-icon">💡</div>
            <div class="tip-title">Pro Tip</div>
            <div class="tip-text">
                The more months of data you provide, the more accurate your forecast will be.<br>
                We recommend at least 6 months of historical data for best results.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Footer
        st.markdown("---")
        st.markdown("""
        <div class="footer">
            <strong>FlowCast</strong> by <a href="https://www.booksandbalances.co.uk" target="_blank">Books & Balances</a>
            <div class="tagline">Financial clarity, delivered beautifully.</div>
        </div>
        """, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
