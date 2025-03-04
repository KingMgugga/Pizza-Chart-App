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
font_light = "Kanit-Light.ttf"
font_regular = "Kanit-Regular.ttf"
font_bold = "Kanit-Bold.ttf"

font_l = fm.FontProperties(fname=font_light)
font_r = fm.FontProperties(fname=font_regular)
font_b = fm.FontProperties(fname=font_bold)

# Data
df = pd.read_csv('crypto_data.csv')

def run():
    st.markdown("<h1 style='font-size: 24px;'>Wallet Score</h1>", unsafe_allow_html=True)

    # Input
    search_input = st.text_input("Enter Wallet Address").strip()
    title_input = st.text_input("Enter Chart Title", "Insert The Title").strip()
    suptitle_input = st.text_input("Enter Chart Suptitle", "Insert Suptitle").strip()

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
            "lending_score": "Lending",
            "perpetuals_score": "Perpetuals",
            "nft_score": "NFTs",
            "dex_score": "DEX",
            "staking_score": "Staking"
        }

        # Extraction
        metric_values = {metric: round(wallet_data[metric]) for metric in available_metrics.keys()}
        overall_score = round(wallet_data["overall_score"])  # Get overall_score separately

        # Multiselect
        selected_metrics = st.multiselect("Available Metrics", [available_metrics[m] for m in available_metrics])

        # Columns
        selected_columns = [m for m in available_metrics if available_metrics[m] in selected_metrics]

        if len(selected_columns) < 2:
            st.warning("Select at least 2 metrics")
        else:
            # Values & lABELS
            values = [metric_values[m] for m in selected_columns]
            params = [available_metrics[m] for m in selected_columns]

            # CMAP
            norm = mcolors.Normalize(vmin=0, vmax=100)
            start_color = '#2E2E2A'
            end_color = st.color_picker("Select Color Scheme", value="#440981")
            custom_colormap = mcolors.LinearSegmentedColormap.from_list("custom_gradient", [start_color, end_color], N=100)
            slice_colors = [custom_colormap(norm(value)) for value in values]

            # Pizza Chart
            if st.button("Generate Chart"):
                baker = PyPizza(
                    params=params,
                    background_color="#e9eae3",
                    straight_line_color="white",
                    straight_line_lw=1,
                    last_circle_color="white",
                    last_circle_lw=1,
                    other_circle_lw=0,
                    inner_circle_size=15
                )

                fig, ax = baker.make_pizza(
                    values,
                    figsize=(9.5, 11),
                    blank_alpha=0.1,
                    param_location=111,
                    kwargs_slices=dict(edgecolor="white", zorder=2, linewidth=1, color=slice_colors),
                    kwargs_params=dict(color="black", fontsize=15, fontproperties=font_r, zorder=2, va="center"),
                    kwargs_values=dict(
                        color="black", fontsize=13, fontproperties=font_b, zorder=3,
                        bbox=dict(edgecolor="black", facecolor='#e9eae3', boxstyle="round,pad=0.2", lw=1.5)
                    )
                )

                ax.set_facecolor('#d9dad2')

                # Titles
                fig.text(
                    0.04, 0.960, title_input, size=30,
                    ha="left", fontproperties=font_b, color='black'
                )
            
                fig.text(
                    0.04, 0.935,
                    suptitle_input,
                    size=15,
                    ha="left", fontproperties=font_r, color='#2E2E2A', alpha=0.8
                )

                # Text effect
                text_effect = [path_effects.Stroke(linewidth=2.5, foreground=end_color), path_effects.Normal()]

                # Overall_score
                ax.text(
                    0, -15, f"{overall_score}", fontsize=32, alpha=1, fontproperties=font_b,
                    ha="center", va="center", color="black", bbox=dict(facecolor="none", edgecolor="none", boxstyle="circle,pad=0", zorder=-10),
                    path_effects=text_effect
                )

                # Lines
                fig.add_artist(plt.Line2D((0.0425, 0.9575), (0.900, 0.900), color=end_color, linewidth=8, alpha=1, transform=fig.transFigure))
                fig.add_artist(plt.Line2D((0, 1), (0.88, 0.88), color="#e9eae3", linewidth=0.0001, alpha=0, zorder=-10, transform=fig.transFigure))

                # Display
                st.pyplot(fig)

# Run
if __name__ == "__main__":
    run()