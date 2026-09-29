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

st.markdown(
    """
    <style>

    .main-title {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 17px;
        color: #666;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 22px;
        font-weight: 600;
        margin-top: 10px;
        margin-bottom: 15px;
    }

    .result-box {
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #ddd;
        background-color: #f8f9fa;
        text-align: center;
        margin-top: 25px;
    }

    .result-label {
        font-size: 16px;
        color: #666;
        margin-bottom: 5px;
    }

    .result-price {
        font-size: 32px;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# Page heading

st.markdown(
    '<div class="main-title">🏠 Karachi Property Price Predictor</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Enter the property details below to estimate its market price.'
    '</div>',
    unsafe_allow_html=True
)


# Basic property details

st.markdown(
    '<div class="section-title">Property Information</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

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
    location = st.selectbox(
        "Location",
        sorted(
            df[df["district"] == district]["location"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    sub_location = st.selectbox(
        "Sub Location",
        sorted(
            df[df["location"] == location]["sub_location"]
            .dropna()
            .unique()
            .tolist()
        )
    )

with col3:
    area = st.number_input(
        "Area (sqft)",
        min_value=1,
        value=1500,
        step=100
    )

    bedrooms = st.selectbox(
        "Bedrooms",
        sorted(df["bedrooms"].dropna().unique().tolist())
    )


# Property features

st.markdown(
    '<div class="section-title">Property Features</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    bathrooms = st.selectbox(
        "Bathrooms",
        sorted(df["bathrooms"].dropna().unique().tolist())
    )

with col2:
    kitchen = st.selectbox(
        "Kitchen",
        sorted(df["kitchen"].dropna().unique().tolist())
    )

with col3:
    total_floors = st.selectbox(
        "Total Floors",
        sorted(df["total_floors"].dropna().unique().tolist())
    )

with col4:
    floor_order = [
        "Ground Floor",
        "Low Floor",
        "Mid Floor",
        "High Floor",
        "Very High Floor",
        "Unknown",
        "Not Applicable"
    ]

    floor_category = st.selectbox(
        "Floor Category",
        floor_order
    )


# Additional details

st.markdown(
    '<div class="section-title">Additional Features</div>',
    unsafe_allow_html=True
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

    age_category = st.selectbox(
        "Age Category",
        age_order
    )

with col2:
    furnished = st.selectbox(
        "Furnished",
        sorted(df["furnished"].dropna().unique().tolist())
    )

with col3:
    parking_category = st.selectbox(
        "Parking",
        sorted(df["parking_category"].dropna().unique().tolist())
    )

with col4:
    servant_quarters = st.selectbox(
        "Servant Quarters",
        sorted(df["servant_quarters"].dropna().unique().tolist())
    )


col1, col2 = st.columns(2)

with col1:
    electricity_backup = st.selectbox(
        "Electricity Backup",
        sorted(df["electricity_backup"].dropna().unique().tolist())
    )

with col2:
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



