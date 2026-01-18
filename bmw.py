import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page configuration
st.set_page_config(
    page_title='BMW Data Dashboard',
    page_icon='🚗',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Custom CSS with dark background and enhanced styling
st.markdown("""
    <style>
        * {
            margin: 0;
            padding: 0;
        }
        body {
            background: linear-gradient(135deg, #0d1b2a 0%, #1a3a52 50%, #0d1b2a 100%);
            color: #ecf0f1;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .stApp {
            background: linear-gradient(135deg, #0d1b2a 0%, #1a3a52 50%, #0d1b2a 100%);
        }
        .main-header {
            font-size: 3rem;
            font-weight: 900;
            background: linear-gradient(135deg, #00d4ff 0%, #00ff88 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
            margin-bottom: 2.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            letter-spacing: 2px;
        }
        h2 {
            background: linear-gradient(90deg, #00d4ff 0%, #00ff88 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 1.8rem;
            margin: 1.5rem 0;
        }
        h3 {
            color: #00d4ff;
            font-size: 1.2rem;
            margin: 1rem 0;
        }
        .stMetric {
            background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(0, 255, 136, 0.1) 100%);
            padding: 1.5rem !important;
            border-radius: 15px !important;
            border: 2px solid rgba(0, 212, 255, 0.3);
            box-shadow: 0 8px 32px rgba(0, 212, 255, 0.1);
            backdrop-filter: blur(10px);
        }
        [data-testid="stMetricValue"] {
            color: #00ff88 !important;
            font-size: 2rem !important;
            font-weight: bold;
        }
        [data-testid="stMetricLabel"] {
            color: #00d4ff !important;
            font-size: 1rem !important;
        }
        [data-testid="stDataFrame"] {
            background-color: rgba(26, 47, 74, 0.8) !important;
            border-radius: 15px !important;
            border: 2px solid rgba(0, 212, 255, 0.2) !important;
        }
        hr {
            border: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, #00d4ff, transparent);
            margin: 2rem 0;
        }
        .stSelectbox, .stSlider, .stTextInput {
            border-radius: 10px !important;
        }
        [data-baseweb="input"] {
            border-color: rgba(0, 212, 255, 0.3) !important;
            background-color: rgba(26, 47, 74, 0.5) !important;
        }
        [data-baseweb="select"] {
            border-color: rgba(0, 212, 255, 0.3) !important;
            background-color: rgba(26, 47, 74, 0.5) !important;
        }
        .stButton > button {
            background: linear-gradient(135deg, #00d4ff 0%, #00ff88 100%);
            color: #0d1b2a !important;
            border: none;
            border-radius: 10px;
            font-weight: bold;
            padding: 10px 20px;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            box-shadow: 0 8px 25px rgba(0, 212, 255, 0.4);
            transform: translateY(-2px);
        }
        .separator {
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.5), transparent);
            margin: 2rem 0;
        }
    </style>
""", unsafe_allow_html=True)

# Load Data
df = pd.read_csv('bmw.csv')

# Display header with decorative elements
st.markdown("<div style='text-align: center; margin: 2rem 0;'>", unsafe_allow_html=True)
st.markdown("<h1 class='main-header'>🚗 BMW Data Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00ff88; font-size: 1.1rem; letter-spacing: 1px;'>Advanced Analytics & Insights</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Display metrics in columns with enhanced styling
st.markdown("<div class='separator'></div>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

metric_data = [
    ("📊 Total Records", f"{len(df):,}"),
    ("📈 Total Columns", str(len(df.columns))),
    ("💾 Data Size", f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB"),
    ("⚠️ Missing Values", str(df.isnull().sum().sum()))
]

for idx, (label, value) in enumerate(metric_data):
    with [col1, col2, col3, col4][idx]:
        st.metric(label=label, value=value)

# Dataset section
st.markdown("<div class='separator'></div>", unsafe_allow_html=True)
st.markdown("<h2>📊 Dataset Overview</h2>", unsafe_allow_html=True)
st.dataframe(df, use_container_width=True, height=400)

# Dataset Information section
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("<h3 style='color: #00d4ff;'>📋 Column Information</h3>", unsafe_allow_html=True)
    column_info = pd.DataFrame({
        'Column': df.columns,
        'Data Type': df.dtypes.values,
        'Non-Null Count': df.count().values,
        'Missing': df.isnull().sum().values
    })
    st.dataframe(column_info, use_container_width=True)

with col2:
    st.markdown("<h3 style='color: #00ff88;'>📈 Basic Statistics</h3>", unsafe_allow_html=True)
    st.dataframe(df.describe(), use_container_width=True)

# Visualization Section
st.markdown("<div class='separator'></div>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>📈 Interactive Data Visualizations</h2>", unsafe_allow_html=True)

# Get numeric columns for plotting
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

if len(numeric_cols) > 0:
    # Row 1: Distribution and Box Plot
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<h3 style='color: #00d4ff;'>📊 Distribution Analysis</h3>", unsafe_allow_html=True)
        selected_col1 = st.selectbox("Select column for histogram:", numeric_cols, key="hist")
        fig1 = px.histogram(df, x=selected_col1, nbins=30, 
                           title=f"Distribution of {selected_col1}",
                           color_discrete_sequence=['#00d4ff'])
        fig1.update_layout(
            plot_bgcolor='rgba(26, 47, 74, 0.3)',
            paper_bgcolor='rgba(13, 27, 42, 0.8)',
            font=dict(color='#ecf0f1', size=11),
            hovermode='x unified',
            showlegend=False,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("<h3 style='color: #00ff88;'>📦 Box Plot Analysis</h3>", unsafe_allow_html=True)
        selected_col2 = st.selectbox("Select column for box plot:", numeric_cols, key="box")
        fig2 = px.box(df, y=selected_col2, 
                     title=f"Box Plot of {selected_col2}",
                     color_discrete_sequence=['#ff6b9d'])
        fig2.update_layout(
            plot_bgcolor='rgba(26, 47, 74, 0.3)',
            paper_bgcolor='rgba(13, 27, 42, 0.8)',
            font=dict(color='#ecf0f1', size=11),
            showlegend=False,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Row 2: Correlation and Scatter
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("<h3 style='color: #ffd700;'>🔗 Correlation Heatmap</h3>", unsafe_allow_html=True)
        correlation_matrix = df[numeric_cols].corr()
        fig3 = px.imshow(correlation_matrix, 
                        color_continuous_scale='Turbo',
                        title="Feature Correlation Matrix",
                        labels=dict(color="Correlation"),
                        color_continuous_midpoint=0)
        fig3.update_layout(
            plot_bgcolor='rgba(26, 47, 74, 0.3)',
            paper_bgcolor='rgba(13, 27, 42, 0.8)',
            font=dict(color='#ecf0f1', size=11),
            margin=dict(l=50, r=50, t=50, b=50)
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    with col4:
        st.markdown("<h3 style='color: #ff6b6b;'>🎯 Scatter Plot</h3>", unsafe_allow_html=True)
        if len(numeric_cols) >= 2:
            col_x = st.selectbox("X-axis:", numeric_cols, key="scatter_x")
            col_y = st.selectbox("Y-axis:", numeric_cols, key="scatter_y", index=min(1, len(numeric_cols)-1))
            fig4 = px.scatter(df, x=col_x, y=col_y, 
                            title=f"{col_x} vs {col_y}",
                            color_discrete_sequence=['#00ff88'],
                            opacity=0.7)
            fig4.update_traces(marker=dict(size=8, opacity=0.6))
            fig4.update_layout(
                plot_bgcolor='rgba(26, 47, 74, 0.3)',
                paper_bgcolor='rgba(13, 27, 42, 0.8)',
                font=dict(color='#ecf0f1', size=11),
                hovermode='closest',
                margin=dict(l=50, r=50, t=50, b=50)
            )
            st.plotly_chart(fig4, use_container_width=True)
    
    # Row 3: Top Values Bar Charts
    st.markdown("<div class='separator'></div>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #ffd700;'>🏆 Top Values Analysis</h3>", unsafe_allow_html=True)
    col5, col6 = st.columns(2)
    
    with col5:
        st.markdown("<h3 style='color: #00d4ff;'>📊 Top 10 Values</h3>", unsafe_allow_html=True)
        selected_col3 = st.selectbox("Select column for top values:", numeric_cols, key="top")
        top_values = df[selected_col3].nlargest(10)
        fig5 = px.bar(x=top_values.values, y=range(len(top_values)), 
                     orientation='h',
                     title=f"Top 10 {selected_col3}",
                     color=top_values.values,
                     color_continuous_scale='Viridis')
        fig5.update_layout(
            plot_bgcolor='rgba(26, 47, 74, 0.3)',
            paper_bgcolor='rgba(13, 27, 42, 0.8)',
            font=dict(color='#ecf0f1', size=11),
            showlegend=False,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        st.plotly_chart(fig5, use_container_width=True)
    
    with col6:
        st.markdown("<h3 style='color: #00ff88;'>📉 Line Plot Trend</h3>", unsafe_allow_html=True)
        selected_col4 = st.selectbox("Select column for line plot:", numeric_cols, key="line")
        fig6 = px.line(df, y=selected_col4, title=f"Trend of {selected_col4}",
                      color_discrete_sequence=['#ff6b9d'],
                      markers=True)
        fig6.update_traces(marker=dict(size=4, opacity=0.6))
        fig6.update_layout(
            plot_bgcolor='rgba(26, 47, 74, 0.3)',
            paper_bgcolor='rgba(13, 27, 42, 0.8)',
            font=dict(color='#ecf0f1', size=11),
            hovermode='x unified',
            margin=dict(l=50, r=50, t=50, b=50)
        )
        st.plotly_chart(fig6, use_container_width=True)

# Footer
st.markdown("<div class='separator'></div>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center; color: #00d4ff; font-size: 0.9rem; letter-spacing: 1px;'>"
    "🚗 BMW Data Dashboard | "
    f"Last updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}</p>",
    unsafe_allow_html=True
)