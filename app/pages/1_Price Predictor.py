import streamlit as st
import pickle
from pathlib import Path
import pandas as pd
import numpy as np


# Page setup

st.set_page_config(
    page_title="Property Price Predictor",
    page_icon="🏠",
    layout="wide"
)


# Load the property data and trained model.

project_root = Path(__file__).resolve().parents[2]
df_path = project_root / "data" / "processed" / "df.pkl"
pipeline_path = project_root / "model" / "pipeline.pkl"

with open(df_path, "rb") as file:
    df = pickle.load(file)

with open(pipeline_path, "rb") as file:
    pipeline = pickle.load(file)


# Page styling

st.html(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --ink: #17242b;
        --muted: #617078;
        --paper: #f6f3ed;
        --card: #fffdfa;
        --teal: #0d6b69;
        --teal-dark: #084b4c;
        --coral: #e4775d;
        --gold: #d7a53d;
        --line: #dce2dc;
    }

    html, body, [class*="css"], .stMarkdown, p, li, button {
        font-family: 'Manrope', sans-serif;
    }

    [data-testid="stAppViewContainer"] {
        background: #0d1218;
    }

    [data-testid="stSidebar"] {
        background: #111b21;
        border-right: 1px solid #2c3b40;
    }

    [data-testid="stSidebar"] [data-testid="stSidebarNav"] {
        padding-top: 1.2rem;
    }

    [data-testid="stSidebar"] a {
        color: #aebfc0;
        border-radius: 8px;
    }

    [data-testid="stSidebar"] a:hover {
        background: #1b3033;
        color: #f4f1e8;
    }

    [data-testid="stSidebar"] a[aria-current="page"] {
        background: #0d6b69;
        color: #fffdfa;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 4rem;
        padding-bottom: 4rem;
    }

    .predictor-hero {
        position: relative;
        overflow: hidden;
        padding: 2.8rem 3.2rem;
        border-radius: 24px;
        margin-bottom: 2.2rem;
        background: var(--teal-dark);
        box-shadow: 0 18px 45px rgba(25, 48, 48, 0.18);
    }

    .predictor-hero::after {
        content: '';
        position: absolute;
        width: 260px;
        height: 260px;
        right: -80px;
        top: -130px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 50%;
        box-shadow: 0 0 0 28px rgba(255, 255, 255, 0.04),
                    0 0 0 56px rgba(255, 255, 255, 0.03);
    }

    .hero-kicker {
        position: relative;
        z-index: 1;
        color: #f3c86d;
        font-family: 'DM Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }

    .main-title {
        position: relative;
        z-index: 1;
        color: #fffdfa;
        font-size: clamp(2.2rem, 5vw, 4rem);
        font-weight: 800;
        letter-spacing: -0.06em;
        line-height: 1;
        margin: 0 0 0.9rem;
    }

    .subtitle {
        position: relative;
        z-index: 1;
        max-width: 600px;
        color: #cfe1dc;
        font-size: 1rem;
        line-height: 1.7;
        margin: 0;
    }

    .section-title {
        color: #f4f1e8;
        font-size: 1.55rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        margin: 2rem 0 1rem;
    }

    [data-testid="stWidgetLabel"] p {
        color: #d7e3df !important;
        font-weight: 600;
    }

    div[data-baseweb="select"] > div,
    div[data-testid="stNumberInput"] input {
        border: 1px solid #44545a;
        border-radius: 9px;
        background: #17242b;
        color: #f4f1e8;
    }

    div[data-baseweb="select"] > div:hover,
    div[data-testid="stNumberInput"] input:focus {
        border-color: var(--gold);
    }

    .stButton > button {
        min-height: 3rem;
        border: 1px solid var(--coral);
        border-radius: 10px;
        background: var(--coral);
        color: #fff;
        font-weight: 800;
        transition: background 160ms ease, transform 160ms ease;
    }

    .stButton > button:hover {
        border-color: #c95e48;
        background: #c95e48;
        color: #fff;
        transform: translateY(-1px);
    }

    [data-testid="stAlert"] {
        border-radius: 14px;
        border: 1px solid rgba(215, 165, 61, 0.55);
        background: #263c3b;
        color: #fffdfa;
        margin-top: 1.5rem;
    }

    @media (max-width: 640px) {
        .block-container { padding-top: 2rem; }
        .predictor-hero {
            padding: 1.8rem 1.25rem;
            border-radius: 18px;
            margin-bottom: 1.5rem;
            margin-top: 1rem;
        }
        .predictor-hero::after {
            width: 190px;
            height: 190px;
            right: -75px;
            top: -95px;
        }
        .hero-kicker {
            font-size: 0.62rem;
            line-height: 1.4;
            margin-bottom: 0.65rem;
            overflow-wrap: anywhere;
        }
        .main-title {
            font-size: 2.2rem;
            line-height: 1.04;
            letter-spacing: -0.03em;
            margin-bottom: 0.75rem;
        }
        .subtitle {
            font-size: 0.9rem;
            line-height: 1.55;
        }
    }

    @media (max-width: 400px) {
        .predictor-hero { padding: 1.5rem 1rem; }
        .main-title { font-size: 2rem; }
    }

    </style>
    """
)


# Page heading

st.html(
    """
    <div class="predictor-hero">
        <div class="hero-kicker">Karachi property intelligence · price model</div>
        <div class="main-title">Find the price a property deserves.</div>
        <div class="subtitle">
            Add the property's location, size, and features to get a model-based
            estimate with a practical price range.
        </div>
    </div>
    """
)


# Basic property details

st.html(
    '<div class="section-title">Property Information</div>',
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    property_type = st.selectbox(
        "Property Type",
        ["Flat", "House"]
    )

    district = st.selectbox(
        "District",
        sorted(df["district"].dropna().unique().tolist())
    )

with col2:
    location_values = (
        df[df["district"] == district]["location"]
        .dropna()
        .unique()
        .tolist()
    )

    if district == "Karachi East":
        location_values = [
            value for value in location_values
            if str(value).casefold() != "gadap"
        ]
    elif district == "Korangi":
        location_values = [
            value for value in location_values
            if str(value).casefold() != "jamshed town"
        ]

    location = st.selectbox(
        "Location",
        sorted(location_values)
    )

    sub_location_values = (
        df[df["location"] == location]["sub_location"]
        .dropna()
        .unique()
        .tolist()
    )

    if location == "Gulshan-e-Iqbal Town":
        sub_location_values = [
            value for value in sub_location_values
            if str(value).casefold() != "gadap"
        ]

    sub_location = st.selectbox(
        "Sub Location",
        sorted(sub_location_values)
    )

with col3:
    area_input = st.number_input(
        "Area",
        min_value=1,
        value=1500,
        step=100
    )

    area_unit = st.segmented_control(
        "Area Unit",
        ["Square Feet", "Square Yards"],
        default="Square Feet",
        selection_mode="single",
        label_visibility="collapsed"
    )

    area = area_input if area_unit == "Square Feet" else area_input * 9

with col4:
    bedroom_values = sorted(df["bedrooms"].dropna().unique().tolist())

    bedrooms = st.selectbox(
        "Bedrooms",
        bedroom_values,
        format_func=lambda value: str(int(value))
    )


# Property features

st.html(
    '<div class="section-title">Property Features</div>',
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    bathrooms = st.selectbox(
        "Bathrooms",
        sorted(df["bathrooms"].dropna().unique().tolist()),
        format_func=lambda value: str(int(value))
    )

with col2:
    kitchen = st.selectbox(
        "Kitchen",
        sorted(df["kitchen"].dropna().unique().tolist()),
        format_func=lambda value: str(int(value))
    )

with col3:
    total_floors = st.selectbox(
        "Total Floors",
        sorted(df["total_floors"].dropna().unique().tolist()),
        format_func=lambda value: str(int(value))
    )

with col4:
    floor_order = [
        "Ground Floor",
        "Low Floor",
        "Mid Floor",
        "High Floor",
        "Very High Floor",
        "Unknown"
    ]

    floor_labels = {
        "Ground Floor": "Ground Floor (0)",
        "Low Floor": "Low Floor (1-3)",
        "Mid Floor": "Mid Floor (4-7)",
        "High Floor": "High Floor (8-15)",
        "Very High Floor": "Very High Floor (16+)",
        "Unknown": "Unknown"
    }

    if property_type == "House":
        floor_category = "Not Applicable"
    else:
        floor_category = st.selectbox(
            "Floor Category",
            floor_order,
            format_func=lambda value: floor_labels[value]
        )


# Additional details

st.html(
    '<div class="section-title">Additional Features</div>',
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    age_order = [
        "Under Construction",
        "New",
        "Relatively New",
        "Moderately Old",
        "Old"
    ]

    age_labels = {
        "Under Construction": "Under Construction (< 0 years)",
        "New": "New (0 years)",
        "Relatively New": "Relatively New (1-5 years)",
        "Moderately Old": "Moderately Old (6-10 years)",
        "Old": "Old (> 10 years)"
    }

    age_category = st.selectbox(
        "Age Category",
        age_order,
        format_func=lambda value: age_labels[value]
    )

with col2:
    furnished = st.selectbox(
        "Furnished",
        sorted(df["furnished"].dropna().unique().tolist()),
        format_func=lambda value: "Yes" if int(value) == 1 else "No"
    )

with col3:
    parking_order = [
        "No Parking",
        "Basic Parking",
        "Good Parking",
        "Premium Parking",
        "Luxury Parking"
    ]

    parking_labels = {
        "No Parking": "No Parking (0)",
        "Basic Parking": "Basic Parking (1)",
        "Good Parking": "Good Parking (2)",
        "Premium Parking": "Premium Parking (3-4)",
        "Luxury Parking": "Luxury Parking (5+)"
    }

    parking_category = st.selectbox(
        "Parking",
        parking_order,
        format_func=lambda value: parking_labels[value]
    )

with col4:
    servant_quarters = st.selectbox(
        "Servant Quarters",
        sorted(df["servant_quarters"].dropna().unique().tolist())
    )


col1, col2, col3, col4 = st.columns(4)

with col1:
    electricity_backup = st.selectbox(
        "Electricity Backup",
        sorted(df["electricity_backup"].dropna().unique().tolist()),
        format_func=lambda value: "Yes" if int(value) == 1 else "No"
    )

with col2:
    st.write("")
    st.write("")

with col3:
    st.write("")
    st.write("")

with col4:
    st.write("")
    st.write("")


# Calculate the extra values required by the model.

sub_location_data = df[df["sub_location"] == sub_location]

sub_location_category = (
    sub_location_data["sub_location_category"].iloc[0]
)

sub_location_type = (
    sub_location_data["sub_location_type"].iloc[0]
)

location_data = df[df["location"] == location]

location_category = (
    location_data["location_category"].iloc[0]
)

area_per_bedroom = area / bedrooms


# Let the user start a prediction.

st.markdown("---")

predict_button = st.button(
    "🔮 Predict Property Price",
    use_container_width=True
)


# Build the input row and show the predicted price range.

if predict_button:

    data = [[
        age_category,
        area,
        bedrooms,
        bathrooms,
        kitchen,
        total_floors,
        servant_quarters,
        electricity_backup,
        furnished,
        area_per_bedroom,
        district,
        location,
        sub_location,
        sub_location_type,
        floor_category,
        property_type,
        location_category,
        sub_location_category,
        parking_category
    ]]

    columns = [
        "age_category",
        "area",
        "bedrooms",
        "bathrooms",
        "kitchen",
        "total_floors",
        "servant_quarters",
        "electricity_backup",
        "furnished",
        "area_per_bedroom",
        "district",
        "location",
        "sub_location",
        "sub_location_type",
        "floor_category",
        "property_type",
        "location_category",
        "sub_location_category",
        "parking_category"
    ]

    one_df = pd.DataFrame(
        data,
        columns=columns
    )

    # Convert the model output back to rupees.
    base_price = np.expm1(
        pipeline.predict(one_df)
    )[0]

    # Use a wider error range for more expensive properties.
    if base_price < 2e7:
        mae = 2_359_149

    elif base_price < 5e7:
        mae = 4_430_644

    elif base_price < 1e8:
        mae = 9_545_127

    elif base_price < 2.5e8:
        mae = 23_551_330

    elif base_price < 5e8:
        mae = 62_754_090

    else:
        mae = 139_722_100

    error = mae * 0.5

    low = max(
        0,
        base_price - error
    )

    high = base_price + error

    low_crore = round(low / 1e7, 2)
    high_crore = round(high / 1e7, 2)

    st.success(
    f"Estimated Price: {low_crore} Cr - {high_crore} Cr"
    )



