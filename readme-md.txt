# Pizza Chart Generator

A Streamlit application for creating beautiful pizza charts (radar charts) with dark mode styling.

## Features

- Dark-themed interface for modern aesthetics
- Multiple data input methods (examples, manual entry, or CSV upload)
- Extensive customization options for colors, styles, and layout
- Export charts as PNG, PDF, or SVG
- Option to compare multiple datasets

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
streamlit run app.py
```

## Data Format

The app accepts data in CSV format with columns:
- `Metric`: The name of each metric/parameter
- `Value`: The corresponding value (0-100)

## Built With

- [Streamlit](https://streamlit.io/)
- [mplsoccer](https://mplsoccer.readthedocs.io/)
- [Matplotlib](https://matplotlib.org/)
