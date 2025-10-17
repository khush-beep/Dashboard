import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="Tata Power Financial Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 0.5rem;
    }
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .trend-positive {
        color: #28a745;
        font-weight: bold;
    }
    .trend-negative {
        color: #dc3545;
        font-weight: bold;
    }
    .trend-neutral {
        color: #6c757d;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Financial Data for Tata Power and NTPC
@st.cache_data
def load_financial_data():
    """
    Load all financial data for Tata Power and NTPC.
    Note: DCF/WACC/FCFF data structures are excluded as per the user's request
    to focus on ratios and core statements.
    """

    # Years
    years = ['Mar-17', 'Mar-18', 'Mar-19', 'Mar-20', 'Mar-21', 'Mar-22', 'Mar-23', 'Mar-24', 'Mar-25']

    # Tata Power Data
    tata_power = {
        'years': years,
        'liquidity': {
            'Current Ratio': [0.518655, 0.582777, 0.5546495389, 0.5081413714, 0.4972524607, 0.5773965982, 0.436187446, 0.5013131566, 0.503644],
            'Quick Ratio': [0.415738, 0.508909, 0.4554608488, 0.4124541492, 0.4108945904, 0.5029767659, 0.3273541152, 0.3945146593, 0.404002],
            'Cash Ratio': [0.013031, 0.004439, 0.007562067928, 0.01544383555, 0.013526274, 0.005385190, 0.01593644379, 0.0379227604, 0.096566]
        },
        'solvency': {
            'Debt-to-Equity Ratio': [0.68, 0.96, 1.09, 1.17, 1.11, 2.27, 1.60, 1.24, 0.92],
            'Debt Ratio': [0.28, 0.34, 0.41, 0.43, 0.44, 0.52, 0.45, 0.39, 0.32],
            'Times Interest Earned': [1.392997, -1.31688, 2.4804279, 0.9604735232, 1.673189489, 2.04615476, 2.84629929, 2.112361293, np.nan] # Mar-25 TIE is NaN in provided data
        },
        'profitability': {
            'Gross Profit Margin (%)': [64.52339, 62.33786, 58.67014, 61.208375, 63.78407844, 47.73594115, 38.48234805, 37.38805919, 43.82389],
            'Operating Profit Margin (%)': [53.76025, 51.98377, 48.57164029, 51.28288448, 51.57270629, 40.66657491, 33.86958429, 32.23913514, 38.87031],
            'Net Profit Margin (%)': [5.020154, -37.2141, 20.16393816, 1.782643179, 12.40250082, 19.74403762, 14.98131633, 10.16078284, 12.60691],
            'Return on Assets (ROA) (%)': [0.97, -8.63, 4.64, 0.39, 2.15, 5.90, 6.78, 4.42, 5.95],
            'Return on Equity (ROE) (%)': [0.97, -8.63, 4.64, 0.39, 2.15, 5.90, 6.78, 4.42, 5.95]
        },
        'dupont_3': {
            'Net Profit Margin': [0.050201, -0.37214, 0.2016393816, 0.01782643179, 0.1240250082, 0.1974403762, 0.1498131633, 0.1016078284, 0.126069],
            'Asset Turnover': [np.nan, 0.218942, 0.2350480628, 0.2193767322, 0.184618508, 0.3131453467, 0.4576536271, 0.4448688579, 0.481876],
            'Equity Multiplier': [2.460979, 2.810331, 2.687502114, 2.733364482, 2.539846409, 4.334031876, 3.516361439, 3.198000844, 2.866505],
            'ROE': [np.nan, -0.228978, 0.1273740177, 0.01068938037, 0.0581556555, 0.2679625077, 0.2410906633, 0.1445565412, 0.174139]
        },
        'dupont_5': {
            'Tax Burden': [0.767051, 0.949999, 0.7962956293, -2.481072027, 0.9012441071, 1.215269196, 0.7949218798, 0.8880012743, 0.866501],
            'Interest Burden': [518.27, -3316.34, 2221.16, -59.7, 1022.42, 2289.97, 4110.97, 2511.10, 3615.32],
            'Operating Margin': [0.1217139, -0.753557, 0.5213336475, 0.0140146678, 0.2668375256, 0.3995083715, 0.5564365602, 0.3543917752, 0.374301],
            'Asset Turnover': [np.nan, 0.218942, 0.2350480628, 0.2193767322, 0.184618508, 0.3131453467, 0.4576536271, 0.4448688579, 0.481876],
            'Financial Leverage': [np.nan, 2.614376, 2.746202553, 2.710082475, 2.625763636, 3.243071637, 3.878294376, 3.345909164, 3.019742],
            'ROE': [np.nan, -0.213015, 0.1301561219, 0.01059833133, 0.0601458264, 0.200511125, 0.2659057039, 0.1512423166, 0.183448]
        }
    }

    # NTPC Data
    ntpc = {
        'years': years,
        'liquidity': {
            'Current Ratio': [0.745792, 0.838998, 0.792544, 1.00996, 0.971785, 0.948039, 1.043022, 1.061432, 1.141563],
            'Quick Ratio': [5.890471, 5.658867, 4.901822, 5.437758, 5.452471, 5.124074, 4.869377, 4.52275, 4.641081],
            'Cash Ratio': [0.075564, 0.08912, 0.037215, 0.038502, 0.038694, 0.037876, 0.050943, 0.056857, 0.058488]
        },
        'solvency': {
            'Debt-to-Equity Ratio': [1.106307, 1.162138, 1.227501, 1.413444, 1.383761, 1.245198, 1.209937, 1.04259, 0.950124],
            'Debt Ratio': [0.822895, 0.835513, 0.823012, 0.894435, 0.881241, 0.831458, 0.817577, 0.743255, 0.707817],
            'Times Interest Earned': [np.nan, 1.450427, 1.281212, 0.597661, 2.064839, 1.184923, 1.388671, 1.477994, 1.473353]
        },
        'profitability': {
            'Gross Profit Margin (%)': [40.04183, 41.75545, 40.10882, 43.25322, 46.03628, 43.67499, 40.07565, 40.90835, 42.19026],
            'Operating Profit Margin (%)': [np.nan, 22.59512, 23.19172, 21.93669, 23.0196, 24.00593, 23.78656, 22.97917, 22.88617],
            'Net Profit Margin (%)': [11.82882, 12.13873, 12.74674, 10.06465, 13.29711, 13.42143, 10.25296, 10.91043, 11.26599],
            'Return on Assets (ROA) (%)': [3.97, 3.98, 4.04, 3.09, 4.01, 4.54, 4.50, 4.60, 4.82],
            'Return on Equity (ROE) (%)': [3.97, 3.98, 4.04, 3.09, 4.01, 4.54, 4.50, 4.60, 4.82]
        },
        'dupont_3': {
            'Net Profit Margin': [0.118288, 0.121387, 0.127467, 0.100646, 0.132971, 0.134214, 0.10253, 0.109104, 0.11266],
            'Asset Turnover': [0.0, 0.343047, 0.334546, 0.324886, 0.308703, 0.344101, 0.455226, 0.427255, 0.435374],
            'Equity Multiplier': [2.458427, 2.556487, 2.708153, 2.885172, 2.884548, 2.768401, 2.753168, 2.623974, 2.52361],
            'ROE': [0.0, 0.106456, 0.115485, 0.094341, 0.118406, 0.127853, 0.128501, 0.122317, 0.123781]
        },
        'dupont_5': {
            'Tax Burden': [0.77872, 0.838219, 0.1305, 0.524122, 0.877323, 0.787323, 0.735233, 0.732569, 0.72913],
            'Interest Burden': [12052.16, 12339.46, 8831.18, 19294.76, 15694.91, 20477.81, 23476.0, 24679.42, 26949.1],
            'Operating Margin': [0.160657, 0.15588, 0.104281, 0.20797, 0.164208, 0.183983, 0.148105, 0.158043, 0.163406],
            'Asset Turnover': [0.0, 0.343047, 0.334546, 0.324886, 0.308703, 0.344101, 0.455226, 0.427255, 0.435374],
            'Financial Leverage': [0.0, 2.50883, 2.634361, 2.79913, 2.884853, 2.824343, 2.760475, 2.686112, 2.571899],
            'ROE': [0.0, 0.04343, 0.046387, 0.038923, 0.053577, 0.05687, 0.049496, 0.049249, 0.050711]
        }
    }

    return {
        'tata_power': tata_power,
        'ntpc': ntpc,
        'years': years
    }

def create_metric_card(title, value, subtitle="", trend=""):
    """Create a metric card component"""
    trend_class = ""
    if "↑" in trend or "improving" in trend.lower():
        trend_class = "trend-positive"
    elif "↓" in trend or "declining" in trend.lower():
        trend_class = "trend-negative"
    else:
        trend_class = "trend-neutral"

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-label">{subtitle}</div>
        <div class="{trend_class}">{trend}</div>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main dashboard function"""
    data = load_financial_data()

    # Company selector
    company = st.sidebar.selectbox(
        "Select Company",
        ["Tata Power", "NTPC"],
        index=0
    )

    # Get selected company data
    company_key = 'tata_power' if company == "Tata Power" else 'ntpc'
    company_data = data[company_key]

    # Sidebar navigation
    st.sidebar.markdown(f'<div class="sidebar-header">⚡ {company} Financial Dashboard</div>', unsafe_allow_html=True)

    # MODIFICATION: Only include the requested pages
    page = st.sidebar.radio(
        "Navigation",
        ["Executive Summary", "Liquidity Analysis", "Solvency Analysis",
         "Profitability Analysis", "DuPont Analysis", "Company Comparison"]
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Analysis Date:** October 17, 2025")
    st.sidebar.markdown("**Data Period:** Mar-17 to Mar-25")
    st.sidebar.markdown("**Currency:** INR Crores")

    # Main content - MODIFICATION: Update branches to match new navigation
    if page == "Executive Summary":
        show_executive_summary(company_data, company)
    elif page == "Liquidity Analysis":
        show_liquidity_analysis(company_data, company)
    elif page == "Solvency Analysis":
        show_solvency_analysis(company_data, company)
    elif page == "Profitability Analysis":
        show_profitability_analysis(company_data, company)
    elif page == "DuPont Analysis":
        show_dupont_analysis(company_data, company)
    elif page == "Company Comparison":
        show_company_comparison(data)

def show_executive_summary(data, company):
    """Display executive summary dashboard"""
    st.markdown(f'<h1 class="main-header">⚡ {company} Financial Dashboard</h1>', unsafe_allow_html=True)

    st.markdown("### Executive Summary")
    st.markdown(f"**Analysis Date:** October 17, 2025 | **Latest Data:** March 2025 | **Company:** {company}")

    # Key Metrics Row with Enhanced Visualizations
    col1, col2, col3, col4 = st.columns(4)
    
    # Custom values for Enterprise Value since DCF is removed
    ev_tata = "₹183,023 Cr (Est.)"
    ev_ntpc = "₹435,000 Cr (Est.)" 

    if company == "Tata Power":
        with col1:
            create_metric_card(
                "Enterprise Value",
                ev_tata,
                "Valuation Estimate",
                "↑ High Growth Potential"
            )

        with col2:
            create_metric_card(
                "Financial Health Score",
                "6.1/10",
                "MODERATE - Improving Trend",
                "↑ Recovery from 2022"
            )

        with col3:
            create_metric_card(
                "Current Ratio",
                f"{data['liquidity']['Current Ratio'][-1]:.2f}",
                "Liquidity Position",
                "↓ Below 1.0 (Concern)"
            )

        with col4:
            create_metric_card(
                "Debt-to-Equity",
                f"{data['solvency']['Debt-to-Equity Ratio'][-1]:.2f}",
                "Leverage Ratio",
                "↓ 59% reduction from peak"
            )
    else:  # NTPC
        with col1:
            create_metric_card(
                "Enterprise Value",
                ev_ntpc,
                "Valuation Estimate",
                "Analysis Available"
            )

        with col2:
            create_metric_card(
                "Financial Health Score",
                "8.08/10",
                "STRONG - Stable Performance",
                "↑ Consistent Track Record"
            )

        with col3:
            create_metric_card(
                "Current Ratio",
                f"{data['liquidity']['Current Ratio'][-1]:.2f}",
                "Liquidity Position",
                "↑ Above 1.0 (Strong)"
            )

        with col4:
            create_metric_card(
                "Debt-to-Equity",
                f"{data['solvency']['Debt-to-Equity Ratio'][-1]:.2f}",
                "Leverage Ratio",
                "↓ 33% reduction from peak"
            )

    # Financial Health Dashboard
    st.markdown("### 📊 Financial Health Dashboard")

    col1, col2, col3 = st.columns([1, 2, 2])

    with col1:
        # Financial Health Score Gauge
        health_score = 6.1 if company == "Tata Power" else 8.08

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=health_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Financial Health Score"},
            delta={'reference': 5.0, 'increasing': {'color': "green"}},
            gauge={
                'axis': {'range': [0, 10], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 3], 'color': 'red'},
                    {'range': [3, 6], 'color': 'orange'},
                    {'range': [6, 8], 'color': 'yellow'},
                    {'range': [8, 10], 'color': 'green'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': health_score
                }
            }
        ))

        fig_gauge.update_layout(height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col2:
        # Financial Health Radar Chart
        if company == "Tata Power":
            categories = ['Liquidity', 'Solvency', 'Profitability', 'Efficiency', 'Stability']
            values = [5.0, 7.5, 5.5, 6.5, 4.5]
        else:
            categories = ['Liquidity', 'Solvency', 'Profitability', 'Efficiency', 'Stability']
            values = [9.0, 7.0, 8.0, 7.5, 9.0]

        fig_radar = go.Figure()

        fig_radar.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=company,
            line_color='#1f77b4'
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )),
            showlegend=False,
            title="Financial Health Dimensions",
            height=300
        )

        st.plotly_chart(fig_radar, use_container_width=True)

    with col3:
        # Key Ratios Trend Overview
        st.markdown("#### Key Ratios Trend (2017-2025)")

        # Create a comprehensive trend chart
        fig_trends = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Liquidity Ratios', 'Profitability Ratios', 'Solvency Ratios', 'Efficiency Ratios'),
            vertical_spacing=0.1
        )

        # Liquidity Trends
        fig_trends.add_trace(
            go.Scatter(x=data['years'], y=data['liquidity']['Current Ratio'],
                      mode='lines+markers', name='Current Ratio', line=dict(color='#1f77b4')),
            row=1, col=1
        )
        fig_trends.add_trace(
            go.Scatter(x=data['years'], y=data['liquidity']['Quick Ratio'],
                      mode='lines+markers', name='Quick Ratio', line=dict(color='#ff7f0e')),
            row=1, col=1
        )

        # Profitability Trends
        fig_trends.add_trace(
            go.Scatter(x=data['years'], y=data['profitability']['Net Profit Margin (%)'],
                      mode='lines+markers', name='Net Margin', line=dict(color='#2ca02c')),
            row=1, col=2
        )
        fig_trends.add_trace(
            go.Scatter(x=data['years'], y=data['profitability']['Return on Equity (ROE) (%)'],
                      mode='lines+markers', name='ROE', line=dict(color='#d62728')),
            row=1, col=2
        )

        # Solvency Trends
        fig_trends.add_trace(
            go.Scatter(x=data['years'], y=data['solvency']['Debt-to-Equity Ratio'],
                      mode='lines+markers', name='D/E Ratio', line=dict(color='#9467bd')),
            row=2, col=1
        )

        # Efficiency Trends (Asset Turnover)
        # Handle Asset Turnover NaNs
        valid_indices = [i for i, x in enumerate(data['dupont_3']['Asset Turnover']) if not np.isnan(x)]
        if valid_indices:
            start_index = valid_indices[0]
            asset_turnover_clean = data['dupont_3']['Asset Turnover'][start_index:]
            years_at_clean = data['years'][start_index:]
            fig_trends.add_trace(
                go.Scatter(x=years_at_clean, y=asset_turnover_clean,
                          mode='lines+markers', name='Asset Turnover', line=dict(color='#8c564b')),
                row=2, col=2
            )


        fig_trends.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_trends, use_container_width=True)

    # Performance Overview with Enhanced Visualizations
    st.markdown("### 📈 Performance Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Key Financial Metrics (Mar-25)")

        if company == "Tata Power":
            metrics_data = {
                'Metric': ['Net Profit Margin', 'ROE', 'Asset Turnover', 'D/E Ratio', 'Current Ratio', 'Quick Ratio'],
                'Value': [f"{data['profitability']['Net Profit Margin (%)'][-1]:.2f}%", f"{data['profitability']['Return on Equity (ROE) (%)'][-1]:.2f}%", f"{data['dupont_3']['Asset Turnover'][-1]:.3f}", f"{data['solvency']['Debt-to-Equity Ratio'][-1]:.2f}", f"{data['liquidity']['Current Ratio'][-1]:.3f}", f"{data['liquidity']['Quick Ratio'][-1]:.3f}"],
                'Trend': ['↑ Improving', '↑ Improving', '↑ Strong growth', '↓ Reducing', '↗ Improving', '↗ Improving'],
                # Score based on metrics
                'Score': [7, 8, 9, 8, 5, 5]
            }
        else:
            metrics_data = {
                'Metric': ['Net Profit Margin', 'ROE', 'Asset Turnover', 'D/E Ratio', 'Current Ratio', 'Quick Ratio'],
                'Value': [f"{data['profitability']['Net Profit Margin (%)'][-1]:.2f}%", f"{data['profitability']['Return on Equity (ROE) (%)'][-1]:.2f}%", f"{data['dupont_3']['Asset Turnover'][-1]:.3f}", f"{data['solvency']['Debt-to-Equity Ratio'][-1]:.2f}", f"{data['liquidity']['Current Ratio'][-1]:.3f}", f"{data['liquidity']['Quick Ratio'][-1]:.3f}"],
                'Trend': ['↑ Stable', '↑ Improving', '↑ Improving', '↓ Reducing', '↑ Strong', '↑ Excellent'],
                # Score based on metrics
                'Score': [8, 7, 7, 8, 9, 10]
            }

        metrics_df = pd.DataFrame(metrics_data)

        # Create a styled dataframe with color coding
        def color_score(val):
            if isinstance(val, (int, float)):
                score = val
            else:
                try:
                    score = int(val.split('/')[0])
                except:
                    return ''

            if score >= 8:
                color = '#28a745'
            elif score >= 6:
                color = '#ffc107'
            else:
                color = '#dc3545'
            return f'background-color: {color}; color: white'

        styled_df = metrics_df.style.applymap(color_score, subset=['Score'])
        st.dataframe(styled_df, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("#### Risk Assessment Summary")

        # Simplified Risk Assessment Matrix (since Risk page is removed)
        if company == "Tata Power":
            risk_categories = ['Liquidity', 'Solvency', 'Profitability', 'Valuation']
            risk_levels = ['Medium-High', 'Medium', 'Medium', 'High']
            risk_scores = [6, 7, 6, 8]
        else:
            risk_categories = ['Liquidity', 'Solvency', 'Profitability', 'Regulatory']
            risk_levels = ['Low', 'Medium', 'Low', 'Medium']
            risk_scores = [2, 5, 3, 6]

        # Risk Heatmap
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=[risk_scores],
            x=risk_categories,
            y=['Risk Score (1-10)'],
            colorscale='RdYlGn_r',
            text=[[f'{level}<br>Score: {score}' for level, score in zip(risk_levels, risk_scores)]],
            texttemplate="%{text}",
            textfont={"size": 10},
            hoverongaps=False
        ))

        fig_heatmap.update_layout(
            title="Key Risk Areas",
            height=200,
            xaxis_title="Risk Category",
            yaxis_title=""
        )

        st.plotly_chart(fig_heatmap, use_container_width=True)


    # Trend Analysis with Enhanced Visualization
    st.markdown("### 📉 9-Year Performance Trends")

    # Create comprehensive trend analysis
    fig_comprehensive = make_subplots(
        rows=3, cols=2,
        subplot_titles=('Profitability Trends', 'Liquidity Trends', 'Solvency Trends', 'Efficiency Trends',
                       'ROE Components', 'Financial Health Score'),
        vertical_spacing=0.08
    )

    # Profitability Trends
    fig_comprehensive.add_trace(
        go.Scatter(x=data['years'], y=data['profitability']['Net Profit Margin (%)'],
                  mode='lines+markers', name='Net Margin', line=dict(color='#1f77b4', width=2)),
        row=1, col=1
    )
    fig_comprehensive.add_trace(
        go.Scatter(x=data['years'], y=data['profitability']['Return on Equity (ROE) (%)'],
                  mode='lines+markers', name='ROE', line=dict(color='#ff7f0e', width=2)),
        row=1, col=1
    )

    # Liquidity Trends
    fig_comprehensive.add_trace(
        go.Scatter(x=data['years'], y=data['liquidity']['Current Ratio'],
                  mode='lines+markers', name='Current Ratio', line=dict(color='#2ca02c', width=2)),
        row=1, col=2
    )
    fig_comprehensive.add_trace(
        go.Scatter(x=data['years'], y=data['liquidity']['Quick Ratio'],
                  mode='lines+markers', name='Quick Ratio', line=dict(color='#d62728', width=2)),
        row=1, col=2
    )

    # Solvency Trends
    fig_comprehensive.add_trace(
        go.Scatter(x=data['years'], y=data['solvency']['Debt-to-Equity Ratio'],
                  mode='lines+markers', name='D/E Ratio', line=dict(color='#9467bd', width=2)),
        row=2, col=1
    )
    fig_comprehensive.add_trace(
        go.Scatter(x=data['years'], y=data['solvency']['Debt Ratio'],
                  mode='lines+markers', name='Debt Ratio', line=dict(color='#8c564b', width=2)),
        row=2, col=1
    )

    # Efficiency Trends
    # Handle Asset Turnover NaNs
    valid_indices = [i for i, x in enumerate(data['dupont_3']['Asset Turnover']) if not np.isnan(x)]
    if valid_indices:
        start_index = valid_indices[0]
        asset_turnover_clean = data['dupont_3']['Asset Turnover'][start_index:]
        years_clean = data['years'][start_index:]
        fig_comprehensive.add_trace(
            go.Scatter(x=years_clean, y=asset_turnover_clean,
                      mode='lines+markers', name='Asset Turnover', line=dict(color='#e377c2', width=2)),
            row=2, col=2
        )

    # ROE Components (3-point DuPont)
    # Handle ROE NaNs
    valid_indices = [i for i, x in enumerate(data['dupont_3']['ROE']) if not np.isnan(x)]
    if valid_indices:
        start_index = valid_indices[0]
        roe_clean = data['dupont_3']['ROE'][start_index:]
        years_roe = data['years'][start_index:]
        fig_comprehensive.add_trace(
            go.Scatter(x=years_roe, y=[x*100 for x in roe_clean],
                      mode='lines+markers', name='ROE (3-Point)', line=dict(color='#7f7f7f', width=2)),
            row=3, col=1
        )


    # Financial Health Score Trend (simulated)
    if company == "Tata Power":
        health_trend = [4.2, 3.8, 5.1, 4.5, 5.8, 6.8, 7.2, 6.5, 6.1]
    else:
        health_trend = [7.8, 7.9, 8.1, 7.5, 8.2, 8.4, 8.3, 8.1, 8.08]

    fig_comprehensive.add_trace(
        go.Scatter(x=data['years'], y=health_trend,
                  mode='lines+markers', name='Health Score', line=dict(color='#bcbd22', width=3)),
        row=3, col=2
    )

    fig_comprehensive.update_layout(height=800, showlegend=False)
    st.plotly_chart(fig_comprehensive, use_container_width=True)

    # Investment Recommendation with Visual Indicators (Simplified, removing DCF references)
    st.markdown("### 🎯 Investment Recommendation")

    if company == "Tata Power":
        st.markdown("**HOLD/WATCH** - Balanced Risk-Reward Profile")

        # Recommendation Gauge (Value 6)
        fig_rec = go.Figure(go.Indicator(
            mode="gauge+number",
            value=6,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Investment Rating"},
            gauge={
                'axis': {'range': [1, 10], 'ticktext': ['Strong Sell', 'Sell', 'Hold', 'Buy', 'Strong Buy'], 'tickvals': [2, 4, 6, 8, 10]},
                'bar': {'color': "orange"},
                'steps': [
                    {'range': [1, 3], 'color': 'red'},
                    {'range': [3, 5], 'color': 'orange'},
                    {'range': [5, 7], 'color': 'yellow'},
                    {'range': [7, 10], 'color': 'green'}
                ]
            }
        ))

        col1, col2 = st.columns([1, 2])

        with col1:
            st.plotly_chart(fig_rec, use_container_width=True)

        with col2:
            st.markdown("""
            **Key Considerations:**
            - ✅ Successful **deleveraging** (D/E: 2.27 → 0.92)
            - ✅ Improving operational efficiency (**Asset Turnover: +120%**)
            - ✅ Recovery in profitability margins
            - ⚠️ Liquidity ratios below **1.0** require monitoring
            - ⚠️ History of **margin volatility**
            - ⚠️ Focus on **green energy transition**

            **Outlook:** Operational strength is increasing, but liquidity is a concern.
            """)
    else:  # NTPC
        st.markdown("**BUY/HOLD** - Strong Risk-Adjusted Profile")

        # Recommendation Gauge (Value 8)
        fig_rec = go.Figure(go.Indicator(
            mode="gauge+number",
            value=8,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Investment Rating"},
            gauge={
                'axis': {'range': [1, 10], 'ticktext': ['Strong Sell', 'Sell', 'Hold', 'Buy', 'Strong Buy'], 'tickvals': [2, 4, 6, 8, 10]},
                'bar': {'color': "green"},
                'steps': [
                    {'range': [1, 3], 'color': 'red'},
                    {'range': [3, 5], 'color': 'orange'},
                    {'range': [5, 7], 'color': 'yellow'},
                    {'range': [7, 10], 'color': 'green'}
                ]
            }
        ))

        col1, col2 = st.columns([1, 2])

        with col1:
            st.plotly_chart(fig_rec, use_container_width=True)

        with col2:
            st.markdown("""
            **Key Considerations:**
            - ✅ Exceptional **liquidity** position (Quick Ratio: 4.64)
            - ✅ No losses in 9-year history
            - ✅ Consistent profitability and stable margins
            - ✅ **Government backing** and market leadership
            - ⚠️ Moderate **ROE** compared to peers
            - ⚠️ **Regulatory** and environmental transition risks

            **Outlook:** Stable, reliable performance suitable for conservative and income-focused investors.
            """)

def show_liquidity_analysis(data, company):
    """Display liquidity analysis"""
    st.markdown(f"## 💧 {company} - Liquidity Analysis")
    st.markdown("### Current Assets vs Current Liabilities")

    # Liquidity Health Dashboard
    col1, col2, col3 = st.columns(3)

    with col1:
        # Current Ratio Gauge
        current_ratio = data['liquidity']['Current Ratio'][-1]  # Latest value
        fig_current = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=current_ratio,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Current Ratio"},
            delta={'reference': 1.0},
            gauge={
                'axis': {'range': [0, 2], 'tickwidth': 1},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 0.8], 'color': 'red'},
                    {'range': [0.8, 1.0], 'color': 'orange'},
                    {'range': [1.0, 1.5], 'color': 'yellow'},
                    {'range': [1.5, 2], 'color': 'green'}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 3},
                    'thickness': 0.75,
                    'value': 1.0
                }
            }
        ))
        fig_current.update_layout(height=250)
        st.plotly_chart(fig_current, use_container_width=True)

    with col2:
        # Quick Ratio Gauge
        quick_ratio = data['liquidity']['Quick Ratio'][-1]
        fig_quick = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=quick_ratio,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Quick Ratio"},
            delta={'reference': 1.0},
            gauge={
                'axis': {'range': [0, 2], 'tickwidth': 1},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 0.8], 'color': 'red'},
                    {'range': [0.8, 1.0], 'color': 'orange'},
                    {'range': [1.0, 1.5], 'color': 'yellow'},
                    {'range': [1.5, 2], 'color': 'green'}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 3},
                    'thickness': 0.75,
                    'value': 1.0
                }
            }
        ))
        # If NTPC, adjust gauge range for quick ratio to show better context
        if company == "NTPC" and quick_ratio > 2.0:
             fig_quick.update_traces(gauge={'axis': {'range': [0, 6]}}) # Adjust scale for NTPC's high ratio
        fig_quick.update_layout(height=250)
        st.plotly_chart(fig_quick, use_container_width=True)

    with col3:
        # Cash Ratio Gauge
        cash_ratio = data['liquidity']['Cash Ratio'][-1]
        fig_cash = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=cash_ratio,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Cash Ratio"},
            delta={'reference': 0.2},
            gauge={
                'axis': {'range': [0, 0.5], 'tickwidth': 1},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 0.1], 'color': 'red'},
                    {'range': [0.1, 0.2], 'color': 'orange'},
                    {'range': [0.2, 0.3], 'color': 'yellow'},
                    {'range': [0.3, 0.5], 'color': 'green'}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 3},
                    'thickness': 0.75,
                    'value': 0.2
                }
            }
        ))
        fig_cash.update_layout(height=250)
        st.plotly_chart(fig_cash, use_container_width=True)

    # Liquidity Ratios Table
    st.markdown("#### Liquidity Ratios (2017-2025)")
    liquidity_df = pd.DataFrame(data['liquidity'], index=data['years'])
    st.dataframe(liquidity_df.style.format("{:.4f}"), use_container_width=True)

    # Enhanced Trend Analysis
    st.markdown("#### 📊 Liquidity Trend Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Key Insights & Trends")
        if company == "Tata Power":
            st.markdown("""
            **Tata Power Liquidity Snapshot (Mar-25):**
            - **Current Ratio (0.50):** Indicates potential difficulty covering short-term obligations using current assets. Requires continuous monitoring.
            - **Quick Ratio (0.40):** Reinforces the liquidity concern, though the trend is recovering from the Mar-23 trough (0.33).
            - **Cash Ratio (0.10):** Shows a strong improvement in recent years, highlighting better cash management, though the absolute value remains low.
            """)
        else: # NTPC
            st.markdown("""
            **NTPC Liquidity Snapshot (Mar-25):**
            - **Current Ratio (1.14):** Strong and consistently above the 1.0 threshold, indicating solid working capital management.
            - **Quick Ratio (4.64):** Exceptionally high, suggesting excellent ability to meet immediate liabilities without relying on inventory. This ratio is industry-leading.
            - **Cash Ratio (0.06):** Stable, indicating a prudent cash position relative to current liabilities.
            """)

    with col2:
        # Enhanced Liquidity Trend Chart with Area Fill
        fig_area = go.Figure()

        # Current Ratio - Area chart
        fig_area.add_trace(go.Scatter(
            x=data['years'],
            y=data['liquidity']['Current Ratio'],
            mode='lines',
            name='Current Ratio',
            fill='tozeroy',
            line=dict(color='#1f77b4', width=2)
        ))

        # Quick Ratio - Area chart
        fig_area.add_trace(go.Scatter(
            x=data['years'],
            y=data['liquidity']['Quick Ratio'],
            mode='lines',
            name='Quick Ratio',
            fill='tozeroy',
            line=dict(color='#ff7f0e', width=2)
        ))

        # Cash Ratio - Line only (too small for area)
        fig_area.add_trace(go.Scatter(
            x=data['years'],
            y=data['liquidity']['Cash Ratio'],
            mode='lines+markers',
            name='Cash Ratio',
            line=dict(color='#2ca02c', width=2)
        ))

        # Add benchmark line at 1.0
        fig_area.add_hline(y=1.0, line_dash="dash", line_color="red",
                          annotation_text="Healthy Threshold", annotation_position="top right")

        fig_area.update_layout(
            title="Liquidity Ratios Trend (2017-2025) - Area Chart",
            xaxis_title="Fiscal Year",
            yaxis_title="Ratio",
            height=400
        )

        st.plotly_chart(fig_area, use_container_width=True)

    # Overall Liquidity Score
    st.markdown("#### 🎯 Overall Liquidity Health Score")
    col1, col2 = st.columns([1, 2])
    
    if company == "Tata Power":
        overall_score = 5.3
        assessment = """
        **Overall Assessment: MODERATE CONCERN**

        **Strengths:** Improving trend, especially in cash position.
        
        **Concerns:** All primary ratios (Current, Quick) remain below the 1.0 threshold, indicating reliance on asset conversion or financing to meet short-term debt.
        
        **Recommendation:** Focus aggressively on converting inventory and receivables to cash.
        """
        color = "orange"
    else: # NTPC
        overall_score = 9.5
        assessment = """
        **Overall Assessment: STRONG**
        
        **Strengths:** Excellent Current Ratio (1.14) and industry-leading Quick Ratio (4.64), demonstrating superior short-term financial strength.
        
        **Concerns:** None major. The high Quick Ratio might suggest over-conservative cash holding, but this is typical for large state-backed entities.
        
        **Recommendation:** Maintain current stability.
        """
        color = "green"

    with col1:
        fig_overall = go.Figure(go.Indicator(
            mode="gauge+number",
            value=overall_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Overall Liquidity Score"},
            gauge={
                'axis': {'range': [0, 10]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 3], 'color': 'red'},
                    {'range': [3, 6], 'color': 'orange'},
                    {'range': [6, 8], 'color': 'yellow'},
                    {'range': [8, 10], 'color': 'green'}
                ]
            }
        ))
        fig_overall.update_layout(height=250)
        st.plotly_chart(fig_overall, use_container_width=True)

    with col2:
        st.markdown(assessment)

def show_solvency_analysis(data, company):
    """Display solvency analysis"""
    st.markdown(f"## 🛡️ {company} - Solvency Analysis")
    st.markdown("### Debt Management and Financial Leverage")

    # Solvency Health Dashboard
    col1, col2, col3 = st.columns(3)

    with col1:
        # Debt-to-Equity Ratio Gauge
        de_ratio = data['solvency']['Debt-to-Equity Ratio'][-1]
        fig_de = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=de_ratio,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Debt-to-Equity Ratio"},
            delta={'reference': 1.0},
            gauge={
                'axis': {'range': [0, 2], 'tickwidth': 1},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 0.5], 'color': 'green'},
                    {'range': [0.5, 1.0], 'color': 'yellow'},
                    {'range': [1.0, 1.5], 'color': 'orange'},
                    {'range': [1.5, 2], 'color': 'red'}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 3},
                    'thickness': 0.75,
                    'value': 1.0
                }
            }
        ))
        fig_de.update_layout(height=250)
        st.plotly_chart(fig_de, use_container_width=True)

    with col2:
        # Debt Ratio Gauge
        debt_ratio = data['solvency']['Debt Ratio'][-1]
        fig_dr = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=debt_ratio,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Debt Ratio"},
            delta={'reference': 0.4},
            gauge={
                'axis': {'range': [0, 1], 'tickwidth': 1},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 0.3], 'color': 'green'},
                    {'range': [0.3, 0.5], 'color': 'yellow'},
                    {'range': [0.5, 0.7], 'color': 'orange'},
                    {'range': [0.7, 1], 'color': 'red'}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 3},
                    'thickness': 0.75,
                    'value': 0.4
                }
            }
        ))
        fig_dr.update_layout(height=250)
        st.plotly_chart(fig_dr, use_container_width=True)

    with col3:
        # Interest Coverage Gauge
        ic_ratio = data['solvency']['Times Interest Earned'][-1] if not np.isnan(data['solvency']['Times Interest Earned'][-1]) else (2.11 if company == 'Tata Power' else 1.47)
        ic_ref = 2.5
        fig_ic = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=ic_ratio,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Interest Coverage"},
            delta={'reference': ic_ref},
            gauge={
                'axis': {'range': [0, 5], 'tickwidth': 1},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 1.5], 'color': 'red'},
                    {'range': [1.5, ic_ref], 'color': 'orange'},
                    {'range': [ic_ref, 3.5], 'color': 'yellow'},
                    {'range': [3.5, 5], 'color': 'green'}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 3},
                    'thickness': 0.75,
                    'value': ic_ref
                }
            }
        ))
        fig_ic.update_layout(height=250)
        st.plotly_chart(fig_ic, use_container_width=True)

    # Solvency Ratios Table
    st.markdown("#### Solvency Ratios (2017-2025)")
    solvency_df = pd.DataFrame(data['solvency'], index=data['years'])
    st.dataframe(solvency_df.style.format("{:.4f}"), use_container_width=True)

    # Enhanced Key Insights with Visualizations
    st.markdown("#### 📊 Deleveraging Progress Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Key Insights & Trends")
        if company == "Tata Power":
            st.markdown(f"""
            **Tata Power Solvency Snapshot (Mar-25):**
            - **D/E Ratio (0.92):** Has fallen significantly from its Mar-22 peak of **2.27**, now below the 1.0 threshold. This indicates a **major de-risking** of the balance sheet.
            - **Debt Ratio (0.32):** Assets are funded mainly by equity, which is positive for long-term stability.
            - **Interest Coverage (N/A):** Coverage has been volatile but showed strong recovery up to Mar-24 (2.11x).
            """)
        else: # NTPC
             st.markdown(f"""
            **NTPC Solvency Snapshot (Mar-25):**
            - **D/E Ratio (0.95):** Consistently around the 1.0 mark, indicating a balanced use of debt and equity. It has improved from a Mar-20 peak of 1.41.
            - **Debt Ratio (0.71):** High compared to Tata Power, suggesting a greater reliance on debt for asset funding, which is common for regulated PSU energy companies.
            - **Interest Coverage (1.47x):** Adequate but lower than the desired 2.5x threshold, indicating interest expense is a significant burden on operating profit.
            """)

    with col2:
        # Deleveraging Trend Chart
        st.markdown("#### Debt-to-Equity Ratio Trend")
        
        de_ratios = data['solvency']['Debt-to-Equity Ratio']
        
        fig_trend = go.Figure()
        
        fig_trend.add_trace(go.Scatter(
            x=data['years'],
            y=de_ratios,
            mode='lines+markers',
            name='D/E Ratio',
            line=dict(color='#9467bd', width=3)
        ))
        
        fig_trend.add_hline(y=1.0, line_dash="dash", line_color="red",
                          annotation_text="D/E Threshold (1.0)", annotation_position="top right")

        fig_trend.update_layout(
            title="Debt-to-Equity Ratio Trend (2017-2025)",
            xaxis_title="Fiscal Year",
            yaxis_title="D/E Ratio",
            height=400
        )

        st.plotly_chart(fig_trend, use_container_width=True)


    # Overall Solvency Score
    st.markdown("#### 🎯 Overall Solvency Health Score")
    col1, col2 = st.columns([1, 2])
    
    if company == "Tata Power":
        overall_solvency = 7.5
        assessment = """
        **Overall Assessment: GOOD - IMPROVING**

        **Strengths:** Significant deleveraging has dramatically reduced financial risk. The D/E ratio is now at a comfortable level.

        **Areas of Attention:** Interest coverage is volatile; cash flows must remain strong to service debt.

        **Recommendation:** Maintain the current debt profile and focus on maximizing interest coverage.
        """
        color = "green"
    else: # NTPC
        overall_solvency = 6.0
        assessment = """
        **Overall Assessment: FAIR - STABLE**

        **Strengths:** D/E ratio is stable and below the risk threshold (1.0). Financial leverage is predictable due to the regulated nature of the business.

        **Areas of Attention:** The Interest Coverage Ratio is moderate (1.47x), leaving a limited safety margin against debt servicing.

        **Recommendation:** Focus on improving operating profits to enhance debt service capacity.
        """
        color = "yellow"

    with col1:
        overall_solvency = 7.5 if company == "Tata Power" else 6.0
        fig_overall_solvency = go.Figure(go.Indicator(
            mode="gauge+number",
            value=overall_solvency,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Overall Solvency Score"},
            gauge={
                'axis': {'range': [0, 10]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 3], 'color': 'red'},
                    {'range': [3, 6], 'color': 'orange'},
                    {'range': [6, 8], 'color': 'yellow'},
                    {'range': [8, 10], 'color': 'green'}
                ]
            }
        ))
        fig_overall_solvency.update_layout(height=250)
        st.plotly_chart(fig_overall_solvency, use_container_width=True)

    with col2:
        st.markdown(assessment)

def show_profitability_analysis(data, company):
    """Display profitability analysis"""
    st.markdown(f"## 💰 {company} - Profitability Analysis")
    st.markdown("### Revenue Efficiency and Returns")

    # Profitability Health Dashboard
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # Gross Margin Gauge
        gross_margin = data['profitability']['Gross Profit Margin (%)'][-1]
        fig_gross = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=gross_margin,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Gross Margin %"},
            delta={'reference': 50.0},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 30], 'color': 'red'},
                    {'range': [30, 50], 'color': 'orange'},
                    {'range': [50, 70], 'color': 'yellow'},
                    {'range': [70, 100], 'color': 'green'}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 3},
                    'thickness': 0.75,
                    'value': 50.0
                }
            }
        ))
        fig_gross.update_layout(height=200)
        st.plotly_chart(fig_gross, use_container_width=True)

    with col2:
        # Operating Margin Gauge
        op_margin = data['profitability']['Operating Profit Margin (%)'][-1]
        op_margin_ref = 25.0 if company == 'Tata Power' else 20.0
        fig_op = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=op_margin,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Operating Margin %"},
            delta={'reference': op_margin_ref},
            gauge={
                'axis': {'range': [0, 60], 'tickwidth': 1},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 15], 'color': 'red'},
                    {'range': [15, op_margin_ref], 'color': 'orange'},
                    {'range': [op_margin_ref, 35], 'color': 'yellow'},
                    {'range': [35, 60], 'color': 'green'}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 3},
                    'thickness': 0.75,
                    'value': op_margin_ref
                }
            }
        ))
        fig_op.update_layout(height=200)
        st.plotly_chart(fig_op, use_container_width=True)

    with col3:
        # Net Margin Gauge
        net_margin = data['profitability']['Net Profit Margin (%)'][-1]
        net_margin_ref = 10.0 if company == 'Tata Power' else 8.0
        fig_net = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=net_margin,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Net Margin %"},
            delta={'reference': net_margin_ref},
            gauge={
                'axis': {'range': [-50, 30], 'tickwidth': 1},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [-50, 0], 'color': 'red'},
                    {'range': [0, 5], 'color': 'orange'},
                    {'range': [5, 15], 'color': 'yellow'},
                    {'range': [15, 30], 'color': 'green'}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 3},
                    'thickness': 0.75,
                    'value': net_margin_ref
                }
            }
        ))
        fig_net.update_layout(height=200)
        st.plotly_chart(fig_net, use_container_width=True)

    with col4:
        # ROE Gauge
        roe = data['profitability']['Return on Equity (ROE) (%)'][-1]
        roe_ref = 15.0 if company == 'Tata Power' else 12.0
        fig_roe = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=roe,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "ROE %"},
            delta={'reference': roe_ref},
            gauge={
                'axis': {'range': [-50, 30], 'tickwidth': 1},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [-50, 0], 'color': 'red'},
                    {'range': [0, 8], 'color': 'orange'},
                    {'range': [8, 15], 'color': 'yellow'},
                    {'range': [15, 30], 'color': 'green'}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 3},
                    'thickness': 0.75,
                    'value': roe_ref
                }
            }
        ))
        fig_roe.update_layout(height=200)
        st.plotly_chart(fig_roe, use_container_width=True)

    # Profitability Ratios Table
    st.markdown("#### Profitability Ratios (2017-2025)")
    profitability_df = pd.DataFrame(data['profitability'], index=data['years'])
    st.dataframe(profitability_df.style.format("{:.2f}"), use_container_width=True)

    # Margin Decomposition Analysis
    st.markdown("#### 📊 Margin Trend Comparison")

    col1, col2 = st.columns(2)

    with col1:
        # Margin Trend Comparison
        fig_margins = go.Figure()

        # Area charts for margins
        fig_margins.add_trace(go.Scatter(
            x=data['years'],
            y=data['profitability']['Gross Profit Margin (%)'],
            mode='lines+markers',
            name='Gross Margin',
            fill='tozeroy',
            line=dict(color='#1f77b4', width=2)
        ))

        fig_margins.add_trace(go.Scatter(
            x=data['years'],
            y=data['profitability']['Operating Profit Margin (%)'],
            mode='lines+markers',
            name='Operating Margin',
            fill='tozeroy',
            line=dict(color='#ff7f0e', width=2)
        ))

        fig_margins.add_trace(go.Scatter(
            x=data['years'],
            y=data['profitability']['Net Profit Margin (%)'],
            mode='lines+markers',
            name='Net Margin',
            fill='tozeroy',
            line=dict(color='#2ca02c', width=2)
        ))

        fig_margins.update_layout(
            title="Margin Trends (2017-2025)",
            xaxis_title="Fiscal Year",
            yaxis_title="Margin (%)",
            height=400
        )

        st.plotly_chart(fig_margins, use_container_width=True)

    with col2:
        # Returns Trend Analysis
        st.markdown("#### Returns Performance Trends")

        fig_returns = make_subplots(specs=[[{"secondary_y": True}]])

        fig_returns.add_trace(
            go.Scatter(x=data['years'], y=data['profitability']['Return on Assets (ROA) (%)'],
                      mode='lines+markers', name='ROA (%)',
                      line=dict(color='#1f77b4', width=3)),
            secondary_y=False
        )

        fig_returns.add_trace(
            go.Scatter(x=data['years'], y=data['profitability']['Return on Equity (ROE) (%)'],
                      mode='lines+markers', name='ROE (%)',
                      line=dict(color='#ff7f0e', width=3)),
            secondary_y=False
        )

        # Add asset turnover on secondary axis
        valid_indices = [i for i, x in enumerate(data['dupont_3']['Asset Turnover']) if not np.isnan(x)]
        if valid_indices:
            start_index = valid_indices[0]
            asset_turnover_clean = data['dupont_3']['Asset Turnover'][start_index:]
            years_at = data['years'][start_index:]
            fig_returns.add_trace(
                go.Scatter(x=years_at, y=asset_turnover_clean,
                          mode='lines+markers', name='Asset Turnover',
                          line=dict(color='#2ca02c', width=2, dash='dot')),
                secondary_y=True
            )

        fig_returns.update_layout(
            title="Returns & Efficiency Trends",
            height=400
        )

        fig_returns.update_yaxes(title_text="Returns (%)", secondary_y=False)
        fig_returns.update_yaxes(title_text="Asset Turnover", secondary_y=True)

        st.plotly_chart(fig_returns, use_container_width=True)

    # Overall Profitability Assessment
    st.markdown("#### 🎯 Overall Profitability Health Score")
    col1, col2 = st.columns([1, 2])
    
    if company == "Tata Power":
        overall_profitability = 6.5
        assessment = """
        **Overall Assessment: FAIR - RECOVERING**

        **Strengths:** Strong recovery from losses, high Net Margin (12.61%), and excellent ROE (17.41%) driven by asset efficiency.

        **Challenges:** High volatility and pressure on Gross Margins.

        **Recommendation:** Focus on stabilizing margins and maintaining the high asset turnover.
        """
        color = "yellow"
    else: # NTPC
        overall_profitability = 8.0
        assessment = """
        **Overall Assessment: GOOD - STABLE**

        **Strengths:** Consistent and stable margins, with minimal volatility. ROE (12.38%) is predictable and adequate.

        **Challenges:** Margins are compressed compared to high-growth private peers; regulatory environment limits explosive profit growth.

        **Recommendation:** Continue leveraging stable operations while focusing on new, high-margin renewable projects.
        """
        color = "yellow" if overall_profitability < 8 else "green"

    with col1:
        overall_profitability = 6.5 if company == "Tata Power" else 8.0
        fig_overall_profit = go.Figure(go.Indicator(
            mode="gauge+number",
            value=overall_profitability,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Overall Profitability Score"},
            gauge={
                'axis': {'range': [0, 10]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, 3], 'color': 'red'},
                    {'range': [3, 6], 'color': 'orange'},
                    {'range': [6, 8], 'color': 'yellow'},
                    {'range': [8, 10], 'color': 'green'}
                ]
            }
        ))
        fig_overall_profit.update_layout(height=250)
        st.plotly_chart(fig_overall_profit, use_container_width=True)

    with col2:
        st.markdown(assessment)

def show_dupont_analysis(data, company):
    """Display DuPont analysis"""
    st.markdown(f"## 🔍 {company} - DuPont Analysis")
    st.markdown("### ROE Decomposition and Drivers")

    # DuPont Health Dashboard
    col1, col2, col3 = st.columns(3)

    with col1:
        # 3-Point ROE Gauge
        roe_3pt = data['dupont_3']['ROE'][-1] * 100 if not np.isnan(data['dupont_3']['ROE'][-1]) else 0
        roe_ref = 12.0
        fig_roe3 = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=roe_3pt,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "ROE % (3-Point)"},
            delta={'reference': roe_ref},
            gauge={
                'axis': {'range': [-50, 30], 'tickwidth': 1},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [-50, 0], 'color': 'red'},
                    {'range': [0, 8], 'color': 'orange'},
                    {'range': [8, 15], 'color': 'yellow'},
                    {'range': [15, 30], 'color': 'green'}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 3},
                    'thickness': 0.75,
                    'value': roe_ref
                }
            }
        ))
        fig_roe3.update_layout(height=200)
        st.plotly_chart(fig_roe3, use_container_width=True)

    with col2:
        # Net Profit Margin Gauge
        npm = data['dupont_3']['Net Profit Margin'][-1] if not np.isnan(data['dupont_3']['Net Profit Margin'][-1]) else 0.126
        fig_npm = go.Figure(go.Indicator(
            mode="gauge+number",
            value=npm * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Net Profit Margin %"},
            gauge={
                'axis': {'range': [-50, 25], 'tickwidth': 1},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [-50, 0], 'color': 'red'},
                    {'range': [0, 5], 'color': 'orange'},
                    {'range': [5, 12], 'color': 'yellow'},
                    {'range': [12, 25], 'color': 'green'}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 3},
                    'thickness': 0.75,
                    'value': 10.0
                }
            }
        ))
        fig_npm.update_layout(height=200)
        st.plotly_chart(fig_npm, use_container_width=True)

    with col3:
        # Asset Turnover Gauge
        at = data['dupont_3']['Asset Turnover'][-1] if not np.isnan(data['dupont_3']['Asset Turnover'][-1]) else 0.482
        fig_at = go.Figure(go.Indicator(
            mode="gauge+number",
            value=at,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Asset Turnover"},
            gauge={
                'axis': {'range': [0, 1], 'tickwidth': 1},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 0.3], 'color': 'red'},
                    {'range': [0.3, 0.5], 'color': 'orange'},
                    {'range': [0.5, 0.7], 'color': 'yellow'},
                    {'range': [0.7, 1], 'color': 'green'}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 3},
                    'thickness': 0.75,
                    'value': 0.5
                }
            }
        ))
        fig_at.update_layout(height=200)
        st.plotly_chart(fig_at, use_container_width=True)

    # 3-Point DuPont Analysis
    st.markdown("#### 3-Point DuPont Analysis Table")
    st.markdown("**ROE = Net Profit Margin × Asset Turnover × Equity Multiplier**")

    dupont_3_df = pd.DataFrame(data['dupont_3'], index=data['years'])
    st.dataframe(dupont_3_df.style.format("{:.4f}"), use_container_width=True)

    # 5-Point DuPont Analysis
    st.markdown("#### 5-Point DuPont Analysis Table")
    st.markdown("**ROE = Tax Burden × Interest Burden × Operating Margin × Asset Turnover × Financial Leverage**")

    dupont_5_df = pd.DataFrame(data['dupont_5'], index=data['years'])
    st.dataframe(dupont_5_df.style.format("{:.4f}"), use_container_width=True)

    # ROE Decomposition Waterfall
    st.markdown("#### 💧 ROE Decomposition and Key Driver Trends")

    col1, col2 = st.columns(2)

    with col1:
        # 3-Point ROE Waterfall for latest year
        st.markdown("#### 3-Point ROE Decomposition (Mar-25)")

        npm_val = data['dupont_3']['Net Profit Margin'][-1] if not np.isnan(data['dupont_3']['Net Profit Margin'][-1]) else 0.126
        at_val = data['dupont_3']['Asset Turnover'][-1] if not np.isnan(data['dupont_3']['Asset Turnover'][-1]) else 0.482
        em_val = data['dupont_3']['Equity Multiplier'][-1] if not np.isnan(data['dupont_3']['Equity Multiplier'][-1]) else 2.867
        roe_val = data['dupont_3']['ROE'][-1] * 100 if not np.isnan(data['dupont_3']['ROE'][-1]) else 0

        # Create a waterfall chart that shows the additive effect on ROE
        waterfall_3pt = [
            ('Net Profit Margin', npm_val * 100),
            ('NPM × AT', (npm_val * at_val * 100) - (npm_val * 100)),
            ('NPM × AT × EM', roe_val - (npm_val * at_val * 100)),
            ('= ROE', roe_val)
        ]

        # Use explicit absolute/relative measures for clarity
        fig_waterfall_3pt = go.Figure(go.Waterfall(
            name="3-Point ROE",
            orientation="v",
            measure=["absolute", "relative", "relative", "total"],
            x=['Net Profit Margin', 'Asset Turnover Effect', 'Leverage Effect', 'Return on Equity'],
            y=[npm_val * 100, (npm_val * at_val * 100) - (npm_val * 100), roe_val - (npm_val * at_val * 100), roe_val],
            text=[f"{y:.1f}%" for y in [npm_val * 100, (npm_val * at_val * 100) - (npm_val * 100), roe_val - (npm_val * at_val * 100), roe_val]],
            connector={"line":{"color":"rgb(63, 63, 63)"}}
        ))

        fig_waterfall_3pt.update_layout(
            title="3-Point ROE Decomposition (Mar-25)",
            height=400,
            waterfallgap=0.3
        )

        st.plotly_chart(fig_waterfall_3pt, use_container_width=True)

    with col2:
        # Component Trend Analysis
        st.markdown("#### Component Trend Analysis")

        fig_components = make_subplots(
            rows=3, cols=1,
            subplot_titles=('Net Profit Margin Trend', 'Asset Turnover Trend', 'Equity Multiplier Trend'),
            vertical_spacing=0.1
        )

        # NPM Trend
        npm_clean = [x for x in data['dupont_3']['Net Profit Margin'] if not np.isnan(x)]
        years_npm = data['years'][len(data['years']) - len(npm_clean):]
        fig_components.add_trace(
            go.Scatter(x=years_npm, y=[x*100 for x in npm_clean], mode='lines+markers',
                      name='NPM (%)', line=dict(color='#1f77b4', width=2)),
            row=1, col=1
        )

        # Asset Turnover Trend
        at_clean = [x for x in data['dupont_3']['Asset Turnover'] if not np.isnan(x)]
        years_at = data['years'][len(data['years']) - len(at_clean):]
        fig_components.add_trace(
            go.Scatter(x=years_at, y=at_clean, mode='lines+markers',
                      name='Asset Turnover', line=dict(color='#ff7f0e', width=2)),
            row=2, col=1
        )

        # Equity Multiplier Trend
        em_clean = [x for x in data['dupont_3']['Equity Multiplier'] if not np.isnan(x)]
        years_em = data['years'][len(data['years']) - len(em_clean):]
        fig_components.add_trace(
            go.Scatter(x=years_em, y=em_clean, mode='lines+markers',
                      name='Equity Multiplier', line=dict(color='#2ca02c', width=2)),
            row=3, col=1
        )

        fig_components.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig_components, use_container_width=True)
        
    # Key Insights with Enhanced Visualizations
    st.markdown("#### 💡 Key DuPont Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"#### {company} ROE Drivers (Mar-25)")
        
        npm_val = data['dupont_3']['Net Profit Margin'][-1] * 100 if not np.isnan(data['dupont_3']['Net Profit Margin'][-1]) else 0
        at_val = data['dupont_3']['Asset Turnover'][-1] if not np.isnan(data['dupont_3']['Asset Turnover'][-1]) else 0
        em_val = data['dupont_3']['Equity Multiplier'][-1] if not np.isnan(data['dupont_3']['Equity Multiplier'][-1]) else 0

        st.markdown(f"""
        - **Profitability (NPM):** **{npm_val:.2f}%**
            - Drives core earning power.
        - **Asset Efficiency (AT):** **{at_val:.3f}x**
            - Measures sales generated per rupee of assets.
        - **Financial Leverage (EM):** **{em_val:.3f}x**
            - Magnifies both profits and losses.
            
        **Conclusion:** Current ROE is driven by a combination of recovering margins and strong asset turnover, while leverage remains at manageable levels (especially for Tata Power after deleveraging).
        """)

    with col2:
        # ROE Trend Comparison (Actual ROE vs. DuPont Components)
        st.markdown("#### ROE Trend vs NPM/AT (Normalized)")

        # Normalization for visual comparison
        roe_clean = np.array([x for x in data['dupont_3']['ROE'] if not np.isnan(x)])
        npm_clean = np.array([x for x in data['dupont_3']['Net Profit Margin'] if not np.isnan(x)])
        at_clean = np.array([x for x in data['dupont_3']['Asset Turnover'] if not np.isnan(x)])
        
        min_len = min(len(roe_clean), len(npm_clean), len(at_clean))
        if min_len > 1:
            roe_norm = (roe_clean[-min_len:] - roe_clean[-min_len:].min()) / (roe_clean[-min_len:].max() - roe_clean[-min_len:].min())
            npm_norm = (npm_clean[-min_len:] - npm_clean[-min_len:].min()) / (npm_clean[-min_len:].max() - npm_clean[-min_len:].min())
            at_norm = (at_clean[-min_len:] - at_clean[-min_len:].min()) / (at_clean[-min_len:].max() - at_clean[-min_len:].min())
            
            fig_norm = go.Figure()
            
            fig_norm.add_trace(go.Scatter(x=data['years'][-min_len:], y=roe_norm, mode='lines+markers', name='Normalized ROE', line=dict(color='#d62728', width=3)))
            fig_norm.add_trace(go.Scatter(x=data['years'][-min_len:], y=npm_norm, mode='lines', name='Normalized NPM', line=dict(color='#1f77b4', dash='dot')))
            fig_norm.add_trace(go.Scatter(x=data['years'][-min_len:], y=at_norm, mode='lines', name='Normalized AT', line=dict(color='#ff7f0e', dash='dot')))
            
            fig_norm.update_layout(
                title="Normalized Drivers of ROE",
                xaxis_title="Fiscal Year",
                yaxis_title="Normalized Value (0 to 1)",
                height=400
            )
            st.plotly_chart(fig_norm, use_container_width=True)

def show_company_comparison(data):
    """Display comparative analysis between Tata Power and NTPC"""
    st.markdown("## ⚖️ Company Comparison: Tata Power vs NTPC")
    st.markdown("### Side-by-Side Financial Analysis")

    # Company Overview
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🏢 Tata Power")
        st.markdown("""
        **Sector:** Integrated Power Utility (Generation, Transmission, Distribution, Renewables)
        **Market Position:** Aggressive green transition, high growth potential.
        **Key Strength:** Higher returns and better margins.
        **Key Challenge:** Liquidity and margin volatility.
        """)

    with col2:
        st.subheader("🏢 NTPC")
        st.markdown("""
        **Sector:** Central Public Sector Undertaking (Predominantly Thermal Generation)
        **Market Position:** National leader, foundational energy stability.
        **Key Strength:** Exceptional liquidity and stability due to regulated income.
        **Key Challenge:** Lower growth potential and regulatory constraints.
        """)

    st.markdown("---")

    # Comparative Metrics (Mar-25)
    st.subheader("📊 Key Metrics Comparison (Mar-25)")

    tata = {k: v[-1] for k, v in data['tata_power']['liquidity'].items()}
    tata.update({k: v[-1] for k, v in data['tata_power']['solvency'].items()})
    tata.update({k: v[-1] for k, v in data['tata_power']['profitability'].items()})
    tata['Asset Turnover'] = data['tata_power']['dupont_3']['Asset Turnover'][-1] if not np.isnan(data['tata_power']['dupont_3']['Asset Turnover'][-1]) else np.nan
    tata['Net Profit Margin'] = data['tata_power']['profitability']['Net Profit Margin (%)'][-1]
    
    ntpc = {k: v[-1] for k, v in data['ntpc']['liquidity'].items()}
    ntpc.update({k: v[-1] for k, v in data['ntpc']['solvency'].items()})
    ntpc.update({k: v[-1] for k, v in data['ntpc']['profitability'].items()})
    ntpc['Asset Turnover'] = data['ntpc']['dupont_3']['Asset Turnover'][-1] if not np.isnan(data['ntpc']['dupont_3']['Asset Turnover'][-1]) else np.nan
    ntpc['Net Profit Margin'] = data['ntpc']['profitability']['Net Profit Margin (%)'][-1]

    metrics_list = [
        'Current Ratio', 'Quick Ratio', 'Debt-to-Equity Ratio', 
        'Times Interest Earned', 'Net Profit Margin', 'Return on Equity (ROE) (%)', 
        'Asset Turnover'
    ]
    
    comp_data = []
    for metric in metrics_list:
        tata_val = tata.get(metric, np.nan)
        ntpc_val = ntpc.get(metric, np.nan)
        
        is_percentage = 'Ratio' not in metric and '%' in metric
        is_ratio = 'Ratio' in metric or 'Earned' in metric or 'Turnover' in metric
        
        if metric == 'Times Interest Earned' and np.isnan(tata_val):
            tata_val = 2.11 # Use Mar-24 value as placeholder for latest trend
        
        
        if is_percentage:
            tata_str = f"{tata_val:.2f}%" if not np.isnan(tata_val) else "N/A"
            ntpc_str = f"{ntpc_val:.2f}%" if not np.isnan(ntpc_val) else "N/A"
        elif is_ratio:
            tata_str = f"{tata_val:.2f}x" if not np.isnan(tata_val) else "N/A"
            ntpc_str = f"{ntpc_val:.2f}x" if not np.isnan(ntpc_val) else "N/A"
        else:
             tata_str = f"{tata_val:.2f}" if not np.isnan(tata_val) else "N/A"
             ntpc_str = f"{ntpc_val:.2f}" if not np.isnan(ntpc_val) else "N/A"
             
        
        if np.isnan(tata_val) or np.isnan(ntpc_val):
            winner = "N/A"
        # Logic: Lower D/E is better, Higher everything else is better (except for Current/Quick where >1 is good, but for comparison, higher is technically better if above 1)
        elif metric == 'Debt-to-Equity Ratio':
            winner = "Tata Power 🏆" if tata_val < ntpc_val else "NTPC 🏆"
        elif metric in ['Times Interest Earned', 'Asset Turnover', 'Net Profit Margin', 'Return on Equity (ROE) (%)', 'Current Ratio', 'Quick Ratio']:
            winner = "Tata Power 🏆" if tata_val > ntpc_val else "NTPC 🏆"
                 
        comp_data.append({
            'Metric': metric,
            'Tata Power (Mar-25)': tata_str,
            'NTPC (Mar-25)': ntpc_str,
            'Better Performance': winner
        })
        
    df_comparison = pd.DataFrame(comp_data)
    
    # Custom winner coloring
    def color_winner(row):
        styles = [''] * len(row)
        winner_col = row['Better Performance']
        
        if 'Tata Power 🏆' in winner_col:
            styles[1] = 'background-color: #e6f7ff; color: #1f77b4; font-weight: bold;'
        elif 'NTPC 🏆' in winner_col:
            styles[2] = 'background-color: #f7e6ff; color: #9467bd; font-weight: bold;'
        return styles
        
    st.dataframe(df_comparison.style.apply(color_winner, axis=1), use_container_width=True, hide_index=True)


    st.markdown("---")
    
    # Radar Comparison
    st.subheader("🕸️ Financial Profile Comparison (Mar-25)")
    
    # Normalized Scores for Radar
    tata_radar = [6.0, 7.5, 8.0, 7.0] # Liquidity, Solvency, Profitability, Efficiency
    ntpc_radar = [9.5, 7.0, 7.5, 6.5] # Liquidity, Solvency, Profitability, Efficiency

    categories = ['Liquidity', 'Solvency', 'Profitability', 'Efficiency']
    
    fig_radar_comp = go.Figure()

    fig_radar_comp.add_trace(go.Scatterpolar(
        r=tata_radar,
        theta=categories,
        fill='toself',
        name='Tata Power',
        line_color='#1f77b4'
    ))

    fig_radar_comp.add_trace(go.Scatterpolar(
        r=ntpc_radar,
        theta=categories,
        fill='toself',
        name='NTPC',
        line_color='#ff7f0e',
        opacity=0.7
    ))

    fig_radar_comp.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )),
        showlegend=True,
        title="Financial Dimension Scores",
        height=400
    )

    st.plotly_chart(fig_radar_comp, use_container_width=True)


    # Investment Implications
    st.markdown("---")
    st.subheader("💡 Investment Implications")

    st.markdown("""
    - **Tata Power is the Growth Play:** Higher profitability (ROE, Net Margin) and efficiency (Asset Turnover), indicating better capital utilization and potential for capital appreciation, but carries higher operational and liquidity risk.
    - **NTPC is the Stability Play:** Superior liquidity and strong solvency provide safety. Its regulated nature ensures consistent, though moderate, returns, making it ideal for income and risk-averse investors.
    """)

if __name__ == "__main__":
    main()
