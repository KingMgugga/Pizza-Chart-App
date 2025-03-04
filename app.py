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
import requests
from PIL import Image
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import numpy as np
from highlight_text import fig_text, ax_text
import matplotlib.patheffects as path_effects

# Fonts
font_light = "Panton Light.otf"
font_regular = "Panton Regular.otf"
font_bold = "Panton Bold.otf"

font_l = fm.FontProperties(fname=font_light)
font_r = fm.FontProperties(fname=font_regular)
font_b = fm.FontProperties(fname=font_bold)

# Data
df = pd.read_csv('crypto_data.csv')

def run():
    st.markdown("<h1 style='font-size: 24px;'>Wallet Score</h1>", unsafe_allow_html=True)

    # Input
    search_input = st.text_input("Enter Wallet Address").strip()
    username_input = st.text_input("Enter Username").strip()
    
    # Filtering
    if search_input:
        filtered_wallets = df[df['wallet_address'].str.contains(search_input, case=False, na=False)]
        wallet_list = filtered_wallets['wallet_address'].tolist()
    else:
        wallet_list = []

    # Dropdown
    if wallet_list:
        selected_wallet = st.selectbox("Select Wallet", wallet_list)
    else:
        selected_wallet = None

    if selected_wallet:
        wallet_data = filtered_wallets[filtered_wallets['wallet_address'] == selected_wallet].iloc[0]

        # Metrics
        available_metrics = {
            "gambling_score": "Gambling",
            "perpetuals_score": "Perpetuals",
            "lending_score": "Lending",
            "nft_score": "NFTs",
            "dex_score": "DEX",
            "staking_score": "Staking"
        }

        # Extraction
        metric_values = {metric: max(20, round(wallet_data[metric])) for metric in available_metrics.keys()}
        overall_score = round(wallet_data["overall_score"])  # Get overall_score separately

        # Generate title and suptitle
        chart_title = f"{username_input} Score"
        chart_suptitle = f"Overall Score: {overall_score}"

        # Use all metrics
        selected_columns = list(available_metrics.keys())
        values = [metric_values[m] for m in selected_columns]
        params = [available_metrics[m] for m in selected_columns]

        # Set fixed 25% transparency (alpha = 0.75)
        alpha = 0.75

        # Set specific colors for each pair of metrics with fixed transparency
        slice_colors = [
            f'#{0x00:02x}{0x85:02x}{0xCA:02x}{int(alpha * 255):02x}',  # First two metrics (Gambling, Perpetuals)
            f'#{0x00:02x}{0x85:02x}{0xCA:02x}{int(alpha * 255):02x}',
            f'#{0xf2:02x}{0x4a:02x}{0x4a:02x}{int(alpha * 255):02x}',  # Second two metrics (Lending, NFTs)
            f'#{0xf2:02x}{0x4a:02x}{0x4a:02x}{int(alpha * 255):02x}',
            f'#{0x00:02x}{0xad:02x}{0x2b:02x}{int(alpha * 255):02x}',  # Last two metrics (DEX, Staking)
            f'#{0x00:02x}{0xad:02x}{0x2b:02x}{int(alpha * 255):02x}'
        ]

        # Pizza Chart
        if st.button("Generate Chart"):
            baker = PyPizza(
                params=params,
                background_color="#020103",  # Dark background
                straight_line_color="white",  # White lines
                straight_line_lw=1,
                last_circle_color="white",  # White circle
                last_circle_lw=2,
                other_circle_lw=1,  # Enable other circles
                other_circle_ls='--',  # Make them dashed
                other_circle_color='#333333',  # Subtle gray color
                inner_circle_size=15
            )

            fig, ax = baker.make_pizza(
                values,
                figsize=(9.5, 11),
                blank_alpha=0.1,
                param_location=111,
                kwargs_slices=dict(edgecolor="white", zorder=2, linewidth=1, color=slice_colors),
                kwargs_params=dict(color="white", fontsize=22, fontproperties=font_r, zorder=2, va="center"),
                kwargs_values=dict(
                    color="white", fontsize=16, fontproperties=font_b, zorder=3,
                    bbox=dict(edgecolor="white", facecolor='#181818', boxstyle="round,pad=0.2", lw=1.5)
                )
            )

            # Add dashed circles at 20, 40, 60, 80
            circle_radii = [0.2, 0.4, 0.6, 0.8]  # Normalized radii for the circles
            for radius in circle_radii:
                circle = plt.Circle((0, 0), radius, fill=False, color='#333333', 
                                  linestyle='--', linewidth=0.5, alpha=0.5)
                ax.add_patch(circle)

            ax.set_facecolor('#020103')

            # Titles
            fig.text(
                0.04, 0.960, chart_title, size=30,
                ha="left", fontproperties=font_b, color='white'
            )
        
            fig.text(
                0.04, 0.920,
                chart_suptitle,
                size=18,
                ha="left", fontproperties=font_r, color='white', alpha=0.8
            )

            # Create center circle with blended colors
            center_radius = 0.25
            angles = np.linspace(0, 2*np.pi, 100)
            
            # Create solid background circle first
            background_circle = plt.Circle((0, -15), center_radius, facecolor='#020103', edgecolor='white', 
                                        linewidth=1, zorder=1)
            ax.add_patch(background_circle)
            
            # Create three circles with radial gradients for each color
            for i, color in enumerate(['#0085CA', '#f24a4a', '#00ad2b']):
                angle_start = i * 2*np.pi/3
                angle_end = (i + 1) * 2*np.pi/3
                mask_angles = angles[(angles >= angle_start) & (angles < angle_end)]
                
                # Create radial gradient for each section
                for r in np.linspace(0, center_radius * 0.95, 10):  # Slightly smaller to show border
                    alpha = 0.3 * (r/center_radius)  # Fade towards center
                    circle = plt.Circle((0, -15), r, color=color, alpha=alpha, zorder=2)
                    ax.add_patch(circle)
            
            # Center the overall score with adjusted position (on top of the blended circle)
            ax.text(
                0, -15, f"{overall_score}", fontsize=32, alpha=1, fontproperties=font_b,
                ha="center", va="center", color="white", zorder=3
            )

            # Lines
            fig.add_artist(plt.Line2D((0.0425, 0.9575), (0.900, 0.900), color='white', linewidth=8, alpha=1, transform=fig.transFigure))
            fig.add_artist(plt.Line2D((0, 1), (0.88, 0.88), color="#020103", linewidth=0.0001, alpha=0, zorder=-10, transform=fig.transFigure))

            fig.patch.set_facecolor('#020103')  # Set figure background to dark

            # Display
            st.pyplot(fig)

# Run
if __name__ == "__main__":
    run()