import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import PyPizza
import matplotlib.font_manager as fm
import requests
from highlight_text import fig_text, ax_text
from PIL import Image
from io import BytesIO
import streamlit as st
from matplotlib.patches import Circle
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import numpy as np
from highlight_text import fig_text, ax_text
import matplotlib.patheffects as path_effects
import os
from io import StringIO

# Set page config
st.set_page_config(
    page_title="Wallet Score",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply dark theme styling
def apply_dark_theme():
    # Custom CSS for dark mode
    st.markdown("""
    <style>
        .main {
            background-color: #121212;
            color: #FFFFFF;
        }
        .stApp {
            background-color: #121212;
        }
        .css-1d391kg, .css-1wrcr25, div[data-baseweb="select"] > div {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        .stSelectbox label, .stSlider label, .stRadio label {
            color: #FFFFFF;
        }
        .stMarkdown {
            color: #FFFFFF;
        }
        header {
            background-color: #1E1E1E !important;
        }
        .stTabs [data-baseweb="tab-list"] {
            background-color: #1E1E1E;
        }
        .stTabs [data-baseweb="tab"] {
            color: #FFFFFF;
        }
        button {
            background-color: #440981 !important;
        }
        .stDataFrame {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        input, textarea {
            background-color: #2C2C2C !important;
            color: #FFFFFF !important;
        }
        h1, h2, h3 {
            color: #FFFFFF !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Apply dark theme
apply_dark_theme()

# Kanit Fonts - We'll check if the font files exist first
font_light = "Kanit-Light.ttf"
font_regular = "Kanit-Regular.ttf"
font_bold = "Kanit-Bold.ttf"

# Setup for font files - with fallback handling
try:
    font_l = fm.FontProperties(fname=font_light)
    font_r = fm.FontProperties(fname=font_regular)
    font_b = fm.FontProperties(fname=font_bold)
except:
    # Use default fonts if Kanit is not available
    st.warning("Kanit font files not found. Using system defaults.")
    font_l = fm.FontProperties(family="sans-serif", weight="light")
    font_r = fm.FontProperties(family="sans-serif", weight="normal")
    font_b = fm.FontProperties(family="sans-serif", weight="bold")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Data Input", "Chart Customization", "About"])

# Main function
def run():
    if page == "Data Input":
        st.title("Wallet Score")
        
        # Tab options for data input
        input_tab = st.radio("Choose data input method:", 
                               ["Search Wallet", "Upload CSV", "Demo Data"], 
                               horizontal=True)
        
        if input_tab == "Search Wallet":
            # Original wallet search functionality
            try:
                # Try to load the data file
                df = pd.read_csv('crypto_data.csv')
                
                # Input
                search_input = st.text_input("Enter Wallet Address").strip()
                
                # Filtering
                if search_input:
                    filtered_wallets = df[df['wallet_address'].str.contains(search_input, case=False, na=False)]
                    wallet_list = filtered_wallets['wallet_address'].tolist()
                else:
                    wallet_list = []
                
                # Dropdown
                if wallet_list:
                    selected_wallet = st.selectbox("Select Wallet", wallet_list)
                    select_metrics(df, selected_wallet)
                else:
                    if search_input:
                        st.warning("No matching wallets found.")
                    else:
                        st.info("Enter a wallet address to search.")
            except FileNotFoundError:
                st.error("crypto_data.csv file not found. Please upload a CSV file or use the Demo Data option.")
        
        elif input_tab == "Upload CSV":
            st.subheader("Upload Your Data")
            
            # Sample template
            st.info("Your CSV should include wallet_address and score columns (gambling_score, lending_score, etc.)")
            
            # Create a sample template for download
            sample_data = {
                "wallet_address": ["wallet123", "wallet456"],
                "overall_score": [85, 72],
                "gambling_score": [90, 65],
                "lending_score": [85, 70],
                "perpetuals_score": [75, 80],
                "nft_score": [95, 60],
                "dex_score": [80, 75],
                "staking_score": [70, 85]
            }
            sample_df = pd.DataFrame(sample_data)
            
            # Create download button for template
            csv = sample_df.to_csv(index=False)
            st.download_button(
                label="Download CSV Template",
                data=csv,
                file_name="wallet_score_template.csv",
                mime="text/csv"
            )
            
            # File uploader
            uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
            
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    st.success("File uploaded successfully!")
                    
                    # Display data preview
                    st.subheader("Data Preview")
                    st.dataframe(df.head())
                    
                    # Check if required columns exist
                    required_cols = ["wallet_address", "overall_score"]
                    score_cols = [col for col in df.columns if col.endswith('_score')]
                    
                    if "wallet_address" not in df.columns:
                        st.error("CSV must contain a 'wallet_address' column")
                    elif len(score_cols) < 2:
                        st.error("CSV must contain at least two score columns (ending with '_score')")
                    else:
                        # Select wallet from uploaded file
                        selected_wallet = st.selectbox("Select Wallet", df['wallet_address'].tolist())
                        select_metrics(df, selected_wallet)
                
                except Exception as e:
                    st.error(f"Error reading CSV: {e}")
        
        elif input_tab == "Demo Data":
            st.subheader("Demo Data")
            
            # Create demo data
            demo_data = {
                "wallet_address": ["0xDemo1", "0xDemo2", "0xDemo3"],
                "overall_score": [85, 72, 91],
                "gambling_score": [90, 65, 88],
                "lending_score": [85, 70, 92],
                "perpetuals_score": [75, 80, 85],
                "nft_score": [95, 60, 78],
                "dex_score": [80, 75, 95],
                "staking_score": [70, 85, 90]
            }
            demo_df = pd.DataFrame(demo_data)
            
            # Display demo data
            st.dataframe(demo_df)
            
            # Select wallet from demo data
            selected_wallet = st.selectbox("Select Demo Wallet", demo_df['wallet_address'].tolist())
            select_metrics(demo_df, selected_wallet)
    
    elif page == "Chart Customization":
        st.title("Chart Customization")
        
        # Chart customization options
        customize_chart()
    
    elif page == "About":
        st.title("About Wallet Score")
        st.markdown("""
        ### What is Wallet Score?
        
        Wallet Score is a tool for visualizing cryptocurrency wallet metrics using radar/pizza charts. 
        This tool helps you understand different aspects of wallet activity across various dimensions.
        
        ### How to Use
        
        1. **Data Input**: Search for a wallet, upload your own CSV, or use demo data
        2. **Select Metrics**: Choose which metrics to display on your chart
        3. **Customize**: Adjust colors, styles, and layout of your visualization
        4. **Generate & Download**: Create your chart and download it in various formats
        
        ### Metrics Explained
        
        * **Gambling Score**: Activity related to crypto gambling platforms
        * **Lending Score**: Participation in lending protocols
        * **Perpetuals Score**: Trading activity in perpetual contracts
        * **NFT Score**: Involvement in NFT markets
        * **DEX Score**: Activity on decentralized exchanges
        * **Staking Score**: Participation in staking protocols
        
        ### About the Overall Score
        
        The overall score is a weighted calculation of all individual metrics, giving a comprehensive 
        view of the wallet's activity and engagement across the crypto ecosystem.
        """)

# Function to select metrics and generate chart
def select_metrics(df, selected_wallet):
    if selected_wallet:
        wallet_data = df[df['wallet_address'] == selected_wallet].iloc[0]
        
        # Metrics
        available_metrics = {}
        
        # Dynamically get all score columns except overall_score
        for col in wallet_data.index:
            if col.endswith('_score') and col != 'overall_score':
                metric_name = col.replace('_score', '').title()
                available_metrics[col] = metric_name
        
        # Extraction
        metric_values = {metric: round(wallet_data[metric]) for metric in available_metrics.keys()}
        overall_score = round(wallet_data["overall_score"]) if "overall_score" in wallet_data else 0
        
        # Multiselect with default selection of all metrics
        default_selection = list(available_metrics.values())
        selected_metrics = st.multiselect("Select Metrics to Display", 
                                         [available_metrics[m] for m in available_metrics],
                                         default=default_selection)
        
        # Columns
        selected_columns = [m for m in available_metrics if available_metrics[m] in selected_metrics]
        
        if len(selected_columns) < 2:
            st.warning("Select at least 2 metrics")
        else:
            # Values & labels
            values = [metric_values[m] for m in selected_columns]
            params = [available_metrics[m] for m in selected_columns]
            
            # Get chart settings from session state or set defaults
            if 'chart_settings' not in st.session_state:
                st.session_state.chart_settings = {
                    'title': "Wallet Analysis",
                    'subtitle': f"Address: {selected_wallet[:10]}...",
                    'highlight_color': "#440981",
                    'background_color': "#121212" if st.session_state.get('dark_mode', True) else "#e9eae3",
                    'text_color': "#FFFFFF" if st.session_state.get('dark_mode', True) else "#000000",
                    'slice_bg_color': "#2E2E2A",
                    'straight_line': False,
                    'show_overall_score': True
                }
            
            # Quick customization in the Data Input page
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.chart_settings['title'] = st.text_input(
                    "Chart Title", 
                    value=st.session_state.chart_settings['title']
                )
            with col2:
                st.session_state.chart_settings['subtitle'] = st.text_input(
                    "Chart Subtitle", 
                    value=st.session_state.chart_settings['subtitle']
                )
            
            st.session_state.chart_settings['highlight_color'] = st.color_picker(
                "Highlight Color", 
                value=st.session_state.chart_settings['highlight_color']
            )
            
            # CMAP
            norm = mcolors.Normalize(vmin=0, vmax=100)
            start_color = st.session_state.chart_settings['slice_bg_color']
            end_color = st.session_state.chart_settings['highlight_color']
            custom_colormap = mcolors.LinearSegmentedColormap.from_list(
                "custom_gradient", 
                [start_color, end_color], 
                N=100
            )
            slice_colors = [custom_colormap(norm(value)) for value in values]
            
            # Generate Chart
            if st.button("Generate Chart"):
                generate_chart(
                    params, 
                    values, 
                    slice_colors, 
                    st.session_state.chart_settings,
                    overall_score
                )

# Function to customize chart settings
def customize_chart():
    st.info("Customize the appearance of your chart. These settings will apply to the next chart you generate.")
    
    # Initialize settings if not present
    if 'chart_settings' not in st.session_state:
        st.session_state.chart_settings = {
            'title': "Wallet Analysis",
            'subtitle': "Address: 0x...",
            'highlight_color': "#440981",
            'background_color': "#121212",
            'text_color': "#FFFFFF",
            'slice_bg_color': "#2E2E2A",
            'straight_line': False,
            'show_overall_score': True,
            'dark_mode': True
        }
    
    # Theme options
    theme_col1, theme_col2 = st.columns(2)
    with theme_col1:
        dark_mode = st.checkbox("Dark Mode", value=st.session_state.chart_settings.get('dark_mode', True))
        st.session_state.chart_settings['dark_mode'] = dark_mode
        
        if dark_mode:
            st.session_state.chart_settings['background_color'] = "#121212"
            st.session_state.chart_settings['text_color'] = "#FFFFFF"
        else:
            st.session_state.chart_settings['background_color'] = "#e9eae3"
            st.session_state.chart_settings['text_color'] = "#000000"
    
    with theme_col2:
        st.session_state.chart_settings['straight_line'] = st.checkbox(
            "Use Straight Lines", 
            value=st.session_state.chart_settings.get('straight_line', False)
        )
        st.session_state.chart_settings['show_overall_score'] = st.checkbox(
            "Show Overall Score", 
            value=st.session_state.chart_settings.get('show_overall_score', True)
        )
    
    # Color settings
    st.subheader("Colors")
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.chart_settings['highlight_color'] = st.color_picker(
            "Highlight Color", 
            value=st.session_state.chart_settings['highlight_color']
        )
        
        st.session_state.chart_settings['slice_bg_color'] = st.color_picker(
            "Slice Background Color", 
            value=st.session_state.chart_settings['slice_bg_color']
        )
    
    with col2:
        # Allow overriding the theme-based colors
        st.session_state.chart_settings['background_color'] = st.color_picker(
            "Background Color", 
            value=st.session_state.chart_settings['background_color']
        )
        
        st.session_state.chart_settings['text_color'] = st.color_picker(
            "Text Color", 
            value=st.session_state.chart_settings['text_color']
        )
    
    # Text settings
    st.subheader("Text")
    text_col1, text_col2 = st.columns(2)
    
    with text_col1:
        st.session_state.chart_settings['title'] = st.text_input(
            "Chart Title", 
            value=st.session_state.chart_settings['title']
        )
    
    with text_col2:
        st.session_state.chart_settings['subtitle'] = st.text_input(
            "Chart Subtitle", 
            value=st.session_state.chart_settings['subtitle']
        )
    
    # Preview note
    st.info("These settings will be applied the next time you generate a chart in the Data Input tab.")

# Function to generate the chart
def generate_chart(params, values, slice_colors, settings, overall_score):
    # Background and colors based on mode
    background_color = settings['background_color']
    text_color = settings['text_color']
    highlight_color = settings['highlight_color']
    
    # Create the pizza chart
    baker = PyPizza(
        params=params,
        background_color=background_color,
        straight_line=settings['straight_line'],
        straight_line_color=text_color,
        last_circle_color=text_color,
        last_circle_lw=1,
        other_circle_lw=0,
        inner_circle_size=15
    )
    
    fig, ax = baker.make_pizza(
        values,
        figsize=(9.5, 11),
        blank_alpha=0.1,
        param_location=111,
        kwargs_slices=dict(
            edgecolor=text_color, 
            zorder=2, 
            linewidth=1, 
            color=slice_colors
        ),
        kwargs_params=dict(
            color=text_color, 
            fontsize=15, 
            fontproperties=font_r, 
            zorder=2, 
            va="center"
        ),
        kwargs_values=dict(
            color=text_color, 
            fontsize=13, 
            fontproperties=font_b, 
            zorder=3,
            bbox=dict(
                edgecolor=text_color, 
                facecolor=background_color, 
                boxstyle="round,pad=0.2", 
                lw=1.5
            )
        )
    )
    
    # Set chart background
    ax.set_facecolor(background_color)
    fig.set_facecolor(background_color)
    
    # Titles
    fig.text(
        0.04, 0.960, settings['title'], size=30,
        ha="left", fontproperties=font_b, color=text_color
    )

    fig.text(
        0.04, 0.935,
        settings['subtitle'],
        size=15,
        ha="left", fontproperties=font_r, color=text_color, alpha=0.8
    )
    
    # Text effect for overall score
    text_effect = [
        path_effects.Stroke(linewidth=2.5, foreground=highlight_color), 
        path_effects.Normal()
    ]
    
    # Overall_score
    if settings['show_overall_score']:
        ax.text(
            0, -15, f"{overall_score}", 
            fontsize=32, 
            alpha=1, 
            fontproperties=font_b,
            ha="center", 
            va="center", 
            color=text_color, 
            bbox=dict(
                facecolor="none", 
                edgecolor="none", 
                boxstyle="circle,pad=0", 
                zorder=-10
            ),
            path_effects=text_effect
        )
    
    # Accent line
    fig.add_artist(
        plt.Line2D(
            (0.0425, 0.9575), 
            (0.900, 0.900), 
            color=highlight_color, 
            linewidth=8, 
            alpha=1, 
            transform=fig.transFigure
        )
    )
    
    # Display chart
    st.pyplot(fig)
    
    # Download options
    st.subheader("Download Options")
    download_col1, download_col2, download_col3 = st.columns(3)
    
    with download_col1:
        # PNG Download
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=300, facecolor=background_color)
        buf.seek(0)
        st.download_button(
            label="Download PNG",
            data=buf,
            file_name="wallet_score.png",
            mime="image/png"
        )
    
    with download_col2:
        # PDF Download
        buf = BytesIO()
        fig.savefig(buf, format='pdf', dpi=300, facecolor=background_color)
        buf.seek(0)
        st.download_button(
            label="Download PDF",
            data=buf,
            file_name="wallet_score.pdf",
            mime="application/pdf"
        )
    
    with download_col3:
        # SVG Download
        buf = BytesIO()
        fig.savefig(buf, format='svg', facecolor=background_color)
        buf.seek(0)
        st.download_button(
            label="Download SVG",
            data=buf,
            file_name="wallet_score.svg",
            mime="image/svg+xml"
        )

# Run
if __name__ == "__main__":
    run()
