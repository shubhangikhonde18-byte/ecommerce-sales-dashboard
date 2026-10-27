import streamlit as st
import pandas as pd
import plotly.express as px

# Page Setup
st.set_page_config(
    page_title="E-Commerce Retail Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# Dark Theme Custom Styling
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    section[data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    header[data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    
    .kpi-card {
        background-color: #161b22;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #30363d;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        transition: all 0.3s ease-in-out;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: #1f77b4;
        box-shadow: 0 8px 20px rgba(31, 119, 180, 0.4);
    }
    .kpi-icon { font-size: 26px; margin-bottom: 8px; }
    .kpi-title { font-size: 13px; color: #8b949e; font-weight: 600; text-transform: uppercase; }
    .kpi-value { font-size: 24px; color: #ffffff; font-weight: bold; margin-top: 5px; }

    .stPlotlyChart {
        background-color: #161b22;
        border-radius: 10px;
        border: 1px solid #30363d;
        padding: 10px;
        transition: all 0.3s ease-in-out;
    }
    .stPlotlyChart:hover {
        transform: translateY(-5px);
        border-color: #1f77b4;
        box-shadow: 0 8px 20px rgba(31, 119, 180, 0.4);
    }

    div.stDownloadButton > button {
        background-color: #21262d;
        color: #ffffff !important;
        border: 1px solid #30363d;
        width: 100%;
        border-radius: 6px;
    }
    div.stDownloadButton > button:hover {
        background-color: #30363d;
        border-color: #1f77b4;
        color: #ffffff !important;
    }
    div.stDownloadButton > button p {
        color: #ffffff !important;
    }
    
    h1, h2, h3 { color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

# Load Cleaned Data
@st.cache_data
def load_data():
    df = pd.read_csv('cleaned_ecommerce_data.csv')
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    return df

df = load_data()

# Clean Sidebar
with st.sidebar:
    st.markdown("## 🛍️ **E-Commerce Analytics**")
    st.markdown("---")
    st.markdown("### 📊 **Dashboard View**")
    st.markdown("<span style='color: #8b949e; font-size: 14px;'>Online Retail Dataset</span>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🌍 **Filters**")
    all_countries = ["All Countries"] + list(df['Country'].unique())
    selected_country = st.selectbox("Select Country", all_countries)

    # Date Range Filter
    st.markdown("---")
    st.markdown("### 📅 **Date Filter**")
    
    min_date = df['InvoiceDate'].min().date()
    max_date = df['InvoiceDate'].max().date()
    
    start_date = st.date_input("Start Date", min_date, min_value=min_date, max_value=max_date, key="start")
    end_date = st.date_input("End Date", max_date, min_value=min_date, max_value=max_date, key="end")

# Filter Data based on Country & Date Range
if selected_country != "All Countries":
    filtered_df = df[
        (df['Country'] == selected_country) & 
        (df['InvoiceDate'].dt.date >= start_date) & 
        (df['InvoiceDate'].dt.date <= end_date)
    ]
else:
    filtered_df = df[
        (df['InvoiceDate'].dt.date >= start_date) & 
        (df['InvoiceDate'].dt.date <= end_date)
    ]

# Download Button in Sidebar
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📥 **Export Data**")
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Filtered CSV",
        data=csv_data,
        file_name='filtered_ecommerce_sales.csv',
        mime='text/csv',
    )

# Header
st.markdown("# E-Commerce Retail Sales Dashboard")
st.caption("Interactive Portfolio Project based on Cleaned Online Retail Data")
st.markdown("---")

# KPI Metrics with Hover Effect Cards
total_sales = filtered_df['TotalSales'].sum()
total_orders = filtered_df['InvoiceNo'].nunique()
total_customers = filtered_df['CustomerID'].nunique()
avg_val = total_sales / total_orders if total_orders > 0 else 0

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-icon">💰</div>
            <div class="kpi-title">Total Revenue</div>
            <div class="kpi-value">£{total_sales:,.2f}</div>
        </div>
    ''', unsafe_allow_html=True)

with k2:
    st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-icon">📦</div>
            <div class="kpi-title">Total Orders</div>
            <div class="kpi-value">{total_orders:,}</div>
        </div>
    ''', unsafe_allow_html=True)

with k3:
    st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-icon">👥</div>
            <div class="kpi-title">Unique Customers</div>
            <div class="kpi-value">{total_customers:,}</div>
        </div>
    ''', unsafe_allow_html=True)

with k4:
    st.markdown(f'''
        <div class="kpi-card">
            <div class="kpi-icon">📈</div>
            <div class="kpi-title">Avg Order Value</div>
            <div class="kpi-value">£{avg_val:,.2f}</div>
        </div>
    ''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Charts Row 1: Monthly Trend & Top Products
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Monthly Sales Trend")
    monthly_trend = filtered_df.groupby('Month')['TotalSales'].sum().reset_index()
    fig_trend = px.line(
        monthly_trend, x='Month', y='TotalSales',
        markers=True, line_shape='spline',
        color_discrete_sequence=['#1f77b4']
    )
    fig_trend.update_layout(template="plotly_dark", paper_bgcolor="#161b22", plot_bgcolor="#161b22", height=280, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_trend, use_container_width=True)

with col_right:
    st.subheader("Top 5 Revenue Products")
    top_prod = filtered_df.groupby('Description')['TotalSales'].sum().reset_index().sort_values(by='TotalSales', ascending=False).head(5)
    fig_bar = px.bar(top_prod, x='TotalSales', y='Description', orientation='h', color='TotalSales', color_continuous_scale='Blues')
    fig_bar.update_layout(template="plotly_dark", paper_bgcolor="#161b22", plot_bgcolor="#161b22", yaxis=dict(autorange="reversed"), height=280, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_bar, use_container_width=True)

# Charts Row 2: Top Countries & Quantity vs Unit Price Scatter
c1, c2 = st.columns(2)

with c1:
    st.subheader("Top Countries by Revenue")
    top_c = filtered_df.groupby('Country')['TotalSales'].sum().reset_index().sort_values(by='TotalSales', ascending=False).head(5)
    fig_country = px.bar(
        top_c, x='Country', y='TotalSales',
        color='TotalSales', color_continuous_scale='Viridis'
    )
    fig_country.update_layout(template="plotly_dark", paper_bgcolor="#161b22", plot_bgcolor="#161b22", height=280, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_country, use_container_width=True)

with c2:
    st.subheader("Quantity vs Unit Price Analysis")
    sample_df = filtered_df.sample(min(1000, len(filtered_df))) if len(filtered_df) > 0 else filtered_df
    fig_scatter = px.scatter(
        sample_df, x='Quantity', y='UnitPrice',
        color='TotalSales', color_continuous_scale='Plasma',
        opacity=0.7
    )
    fig_scatter.update_layout(template="plotly_dark", paper_bgcolor="#161b22", plot_bgcolor="#161b22", height=280, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Raw Data View Expander at the bottom
st.markdown("---")
with st.expander("🔍 View Filtered Data Table (Raw Data Preview)"):
    st.markdown("<span style='color: #8b949e;'>Here is the filtered dataset based on your selected country and date range:</span>", unsafe_allow_html=True)
    st.dataframe(filtered_df, use_container_width=True)