import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from mplsoccer import PyPizza, FontManager
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
from io import BytesIO

# Set page config
st.set_page_config(
    page_title="Advanced Pizza Chart Generator",
    page_icon="🍕",
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
            background-color: #F63366 !important;
        }
        .stDataFrame {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        input, textarea {
            background-color: #2C2C2C !important;
            color: #FFFFFF !important;
        }
    </style>
    """, unsafe_allow_html=True)

# Apply dark theme
apply_dark_theme()

# App title and description
st.title("🍕 Advanced Pizza Chart Generator")
st.markdown("Create customized pizza charts for data visualization in a sleek dark mode theme")

# Create tabs for different sections
tabs = st.tabs(["Data Input", "Chart Styling", "Advanced Options", "About"])

with tabs[0]:
    st.header("Data Input")
    
    # Data input method selection
    input_method = st.radio("Select data input method:", 
                           ["Example Data", "Manual Entry", "CSV Upload"], 
                           horizontal=True)
    
    if input_method == "Example Data":
        example_data = {
            "Player Comparison": {
                "metrics": ["Passing", "Dribbling", "Shooting", "Defending", "Pace", 
                           "Physical", "Vision", "Crossing", "Finishing", "Positioning"],
                "values": [85, 92, 78, 56, 88, 72, 90, 83, 79, 86],
                "min_range": 0,
                "max_range": 100
            },
            "Team Performance": {
                "metrics": ["Goals", "Possession", "Pass Accuracy", "Shots on Target", 
                           "Tackles", "Interceptions", "Clean Sheets", "Set Pieces"],
                "values": [75, 62, 88, 70, 65, 55, 80, 72],
                "min_range": 0,
                "max_range": 100
            }
        }
        
        selected_example = st.selectbox("Choose an example:", list(example_data.keys()))
        metrics = example_data[selected_example]["metrics"]
        values = example_data[selected_example]["values"]
        min_range = example_data[selected_example]["min_range"]
        max_range = example_data[selected_example]["max_range"]
        
        # Display the example data
        example_df = pd.DataFrame({
            "Metric": metrics,
            "Value": values
        })
        st.dataframe(example_df, hide_index=True)
        
    elif input_method == "Manual Entry":
        num_metrics = st.number_input("Number of metrics", min_value=3, max_value=20, value=8)
        
        # Create empty lists
        metrics = []
        values = []
        
        # Create two columns for input
        col1, col2 = st.columns(2)
        
        # Gather metric names and values
        with col1:
            st.subheader("Metric Names")
            for i in range(num_metrics):
                metrics.append(st.text_input(f"Metric {i+1}", value=f"Metric {i+1}"))
        
        with col2:
            st.subheader("Values")
            for i in range(num_metrics):
                values.append(st.slider(f"Value for {metrics[i] if metrics[i] != '' else f'Metric {i+1}'}", 
                                        min_value=0, max_value=100, value=np.random.randint(40, 90)))
        
        min_range = st.number_input("Minimum Range", min_value=0, max_value=50, value=0)
        max_range = st.number_input("Maximum Range", min_value=50, max_value=100, value=100)
        
    elif input_method == "CSV Upload":
        st.info("Upload a CSV file with columns 'Metric' and 'Value'")
        
        # Sample CSV template for download
        sample_data = pd.DataFrame({
            'Metric': ['Passing', 'Dribbling', 'Shooting', 'Defending', 'Pace'],
            'Value': [85, 92, 78, 56, 88]
        })
        
        buffer = BytesIO()
        sample_data.to_csv(buffer, index=False)
        buffer.seek(0)
        
        st.download_button(
            label="Download CSV Template",
            data=buffer,
            file_name="pizza_chart_template.csv",
            mime="text/csv"
        )
        
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        
        if uploaded_file is not None:
            try:
                data = pd.read_csv(uploaded_file)
                
                if 'Metric' not in data.columns or 'Value' not in data.columns:
                    st.error("CSV must contain 'Metric' and 'Value' columns")
                else:
                    st.success("Data loaded successfully!")
                    st.dataframe(data)
                    
                    metrics = data['Metric'].tolist()
                    values = data['Value'].tolist()
                    
                    # Allow setting min and max range
                    col1, col2 = st.columns(2)
                    with col1:
                        min_range = st.number_input("Minimum Range", min_value=0, max_value=50, value=0)
                    with col2:
                        max_range = st.number_input("Maximum Range", min_value=50, max_value=100, value=100)
            except Exception as e:
                st.error(f"Error reading CSV: {e}")
                metrics = []
                values = []
                min_range = 0
                max_range = 100
        else:
            metrics = []
            values = []
            min_range = 0
            max_range = 100

with tabs[1]:
    st.header("Chart Styling")
    
    # Create columns for styling options
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Colors")
        background_color = st.color_picker("Background Color", value="#121212")
        primary_color = st.color_picker("Primary Color (Highlights)", value="#F63366")
        secondary_color = st.color_picker("Secondary Color (Slices)", value="#2C2C2C")
        text_color = st.color_picker("Text Color", value="#FFFFFF")
        
        # Color scheme options
        use_color_scheme = st.checkbox("Use color gradient for slices", value=False)
        if use_color_scheme:
            gradient_start = st.color_picker("Gradient Start Color", value="#F63366")
            gradient_end = st.color_picker("Gradient End Color", value="#7D3C98")
        
    with col2:
        st.subheader("Layout & Style")
        chart_title = st.text_input("Chart Title", "Player Performance Analysis")
        show_title = st.checkbox("Show Chart Title", value=True)
        straight_line = st.checkbox("Use Straight Lines", value=False)
        show_params = st.checkbox("Show Parameter Names", value=True)
        show_values = st.checkbox("Show Values", value=True)
        show_ranges = st.checkbox("Show Range Lines", value=True)
        
        # Font size options
        title_size = st.slider("Title Font Size", 10, 30, 18)
        param_size = st.slider("Parameter Font Size", 8, 20, 12)
        value_size = st.slider("Value Font Size", 8, 20, 12)

with tabs[2]:
    st.header("Advanced Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Chart Dimensions")
        figure_width = st.slider("Chart Width", 6, 20, 12)
        figure_height = st.slider("Chart Height", 6, 20, 12)
        
        st.subheader("Value Display")
        value_format = st.selectbox("Value Format", ["Percentage", "Raw Number", "Custom"])
        if value_format == "Custom":
            value_suffix = st.text_input("Value Suffix", "%")
        else:
            value_suffix = "%" if value_format == "Percentage" else ""
            
    with col2:
        st.subheader("Additional Options")
        compare_values = st.checkbox("Compare with Second Dataset", value=False)
        
        if compare_values:
            st.info("Enter comparison values (same metrics will be used)")
            comparison_values = []
            for i, metric in enumerate(metrics) if 'metrics' in locals() else []:
                comparison_values.append(
                    st.slider(f"Comparison value for {metric}", 
                             min_value=0, max_value=100, 
                             value=min(max(values[i] - 15, 0), 100) if 'values' in locals() and i < len(values) else 50)
                )
            
            comparison_color = st.color_picker("Comparison Color", value="#3498DB")
            
        # Export options
        st.subheader("Export Settings")
        dpi_value = st.slider("DPI (Resolution)", 72, 600, 300)
        transparent_bg = st.checkbox("Transparent Background", value=False)

with tabs[3]:
    st.header("About")
    st.markdown("""
    ### About Pizza Charts
    
    Pizza charts (also known as radar charts or spider charts) are a great way to visualize multivariate data across several quantitative variables. They're particularly popular in sports analytics, performance evaluations, and skill assessments.
    
    ### How to Use This App
    
    1. **Input your data** using one of the three methods (example, manual entry, or CSV upload)
    2. **Customize the appearance** with colors, layout options, and styling preferences
    3. **Fine-tune advanced settings** if needed
    4. **Generate and download** your custom pizza chart
    
    ### Made with
    
    - [Streamlit](https://streamlit.io/)
    - [mplsoccer](https://mplsoccer.readthedocs.io/) - Python package for soccer/football visualization
    - [Matplotlib](https://matplotlib.org/)
    
    ### References
    
    This app uses the PyPizza class from mplsoccer, which was created to visualize soccer/football player statistics but can be used for any radar/pizza chart visualization.
    """)

# Create the chart
if st.button("Generate Pizza Chart", type="primary"):
    if 'metrics' in locals() and 'values' in locals() and len(metrics) > 0 and len(values) > 0:
        # Create figure
        plt.style.use("dark_background")
        fig, ax = plt.subplots(figsize=(figure_width, figure_height), 
                               facecolor=background_color if not transparent_bg else 'none')
        
        # Create slice colors based on settings
        if 'use_color_scheme' in locals() and use_color_scheme:
            # Create color gradient
            cmap = LinearSegmentedColormap.from_list("custom", [gradient_start, gradient_end], N=len(metrics))
            slice_colors = [mpl.colors.rgb2hex(cmap(i)) for i in range(len(metrics))]
        else:
            slice_colors = [primary_color] * len(metrics)
        
        # Set value format
        if 'value_format' in locals():
            if value_format == "Percentage":
                value_format_func = lambda x: f"{x}%"
            elif value_format == "Raw Number":
                value_format_func = lambda x: f"{x}"
            else:  # Custom
                value_format_func = lambda x: f"{x}{value_suffix}"
        else:
            value_format_func = lambda x: f"{x}%"
            
        # Instantiate PyPizza class
        baker = PyPizza(
            params=metrics,                      # list of parameters
            background_color=background_color,   # background color
            straight_line=straight_line,         # straight lines or curves
            min_range=min_range,                 # min range of the parameter
            max_range=max_range,                 # max range of the parameter
            range_fontsize=param_size - 2,       # font size of the range labels
            param_fontsize=param_size,           # font size of the parameters
            show_params=show_params,             # whether to show parameters or not
            show_values=show_values,             # whether to show values or not
            value_fontsize=value_size,           # font size of the parameter values
            value_format=value_format_func,      # format of the values
            outer_color=text_color,              # color for the outer circle
            inner_display=show_ranges,           # display range circles or not
            inner_color=text_color,              # color for the inner circles
        )
        
        # Plot pizza
        baker.make_pizza(
            values,                              # list of values
            figsize=(figure_width, figure_height), # figsize
            color_blank_space=secondary_color,   # color for blank space
            slice_colors=slice_colors,           # color for individual slices
            value_colors=[text_color] * len(metrics),  # color for the value-text
            param_colors=[text_color] * len(metrics),  # color for the parameters
            ax=ax,                               # matplotlib axis
        )
        
        # Add comparison layer if selected
        if 'compare_values' in locals() and compare_values and 'comparison_values' in locals():
            baker.make_pizza(
                comparison_values,
                figsize=(figure_width, figure_height),
                color_blank_space="None",
                slice_colors=[comparison_color] * len(metrics),
                value_colors=[text_color] * len(metrics),
                param_colors=[text_color] * len(metrics),
                ax=ax,
                kwargs_slices=dict(alpha=0.6, zorder=2, edgecolor="#000000"),
                kwargs_params=dict(color="none"),
                kwargs_values=dict(color="none")
            )
        
        # Add title
        if 'show_title' in locals() and show_title and 'chart_title' in locals():
            ax.set_title(chart_title, fontsize=title_size, color=text_color, pad=15)
        
        plt.tight_layout()
        
        # Display chart in Streamlit
        st.pyplot(fig)
        
        # Add download buttons
        download_col1, download_col2 = st.columns(2)
        
        with download_col1:
            # Download as PNG
            buf = BytesIO()
            fig.savefig(buf, format='png', dpi=dpi_value, bbox_inches='tight', 
                       transparent=transparent_bg)
            buf.seek(0)
            st.download_button(
                label="Download as PNG",
                data=buf,
                file_name="pizza_chart.png",
                mime="image/png"
            )
            
            # Download as SVG
            buf = BytesIO()
            fig.savefig(buf, format='svg', bbox_inches='tight', 
                       transparent=transparent_bg)
            buf.seek(0)
            st.download_button(
                label="Download as SVG",
                data=buf,
                file_name="pizza_chart.svg",
                mime="image/svg+xml"
            )
        
        with download_col2:
            # Download as PDF
            buf = BytesIO()
            fig.savefig(buf, format='pdf', dpi=dpi_value, bbox_inches='tight', 
                       transparent=transparent_bg)
            buf.seek(0)
            st.download_button(
                label="Download as PDF",
                data=buf,
                file_name="pizza_chart.pdf",
                mime="application/pdf"
            )
            
            # Download data
            data_df = pd.DataFrame({
                "Metric": metrics,
                "Value": values
            })
            if 'compare_values' in locals() and compare_values and 'comparison_values' in locals():
                data_df["Comparison"] = comparison_values
                
            buffer = BytesIO()
            data_df.to_csv(buffer, index=False)
            buffer.seek(0)
            
            st.download_button(
                label="Download Data as CSV",
                data=buffer,
                file_name="pizza_chart_data.csv",
                mime="text/csv"
            )
    else:
        st.error("Please enter data before generating the chart")

# Add footer
st.markdown("---")
st.caption("Created with ❤️ using Streamlit and mplsoccer")
