import streamlit as st
import pandas as pd
import pickle
from pathlib import Path
import pydeck as pdk
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

def get_turbo_cmap():
    return plt.get_cmap("turbo")

# Configure the analytics page.

st.set_page_config(
    page_title="Karachi Real Estate Analytics",
    page_icon="🗺️",
    layout="wide"
)

st.html(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --ink: #17242b;
        --muted: #617078;
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

    .block-container {
        max-width: 1240px;
        padding-top: 3rem;
        padding-bottom: 4rem;
    }

    .analytics-hero {
        position: relative;
        overflow: hidden;
        padding: 2.8rem 3.2rem;
        border-radius: 24px;
        margin-bottom: 2.2rem;
        background: var(--teal-dark);
        box-shadow: 0 18px 45px rgba(25, 48, 48, 0.18);
    }

    .analytics-hero::after {
        content: '';
        position: absolute;
        width: 280px;
        height: 280px;
        right: -90px;
        top: -140px;
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

    .analytics-hero h1 {
        position: relative;
        z-index: 1;
        color: #fffdfa;
        font-size: clamp(2.2rem, 5vw, 4rem);
        font-weight: 800;
        letter-spacing: -0.06em;
        line-height: 1;
        margin: 0 0 0.9rem;
    }

    .analytics-hero p {
        position: relative;
        z-index: 1;
        max-width: 650px;
        color: #cfe1dc;
        font-size: 1rem;
        line-height: 1.7;
        margin: 0;
    }

    h1, h2, h3, h4 {
        color: #f4f1e8 !important;
        letter-spacing: -0.04em;
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

    [data-testid="stSidebar"] {
        background: #111b21;
        border-right: 1px solid #2c3b40;
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #f4f1e8 !important;
    }

    [data-testid="stCaptionContainer"] p {
        color: #aebfc0;
    }

    [data-testid="stAlert"] {
        border-radius: 14px;
    }

    @media (max-width: 640px) {
        .block-container { padding-top: 1.25rem; }
        .analytics-hero { padding: 2.3rem 1.5rem; border-radius: 20px; }
        .analytics-hero h1 { font-size: 2.65rem; }
    }
    </style>
    """
)

st.html(
    """
    <div class="analytics-hero">
        <div class="hero-kicker">Karachi property intelligence · market view</div>
        <h1>See where Karachi property value is moving.</h1>
        <p>
            Compare districts, locations, and sub-locations through interactive
            maps and market metrics built from real property listings.
        </p>
    </div>
    """
)


# Load the cleaned property data from the project folder.

project_root = Path(__file__).resolve().parents[2]
data_path = project_root / "data" / "processed" / "df_analytical_module.pkl"

with open(data_path, "rb") as file:
    df = pickle.load(file)

df = df.copy()


# Make sure map coordinates are stored as numbers.

coordinate_columns = [
    "location_latitude",
    "location_longitude",
    "sub_location_latitude",
    "sub_location_longitude",
    "district_latitude",
    "district_longitude"
]

for col in coordinate_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")


# Check that the dataset contains everything this page needs.

required_columns = [
    "district",
    "property_type",
    "price",
    "location",
    "sub_location",
    "area",
    "price_per_sqft",
    "location_latitude",
    "location_longitude",
    "sub_location_latitude",
    "sub_location_longitude",
    "location_category"
]

missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    st.error(f"These columns are missing from your dataset: {missing_columns}")
    st.stop()


# Add filters for the district, property type, and price range.

st.sidebar.header("Filters")

district_options = ["All"] + sorted(df["district"].dropna().astype(str).unique().tolist())
selected_district = st.sidebar.selectbox("District", district_options)

property_options = ["All"] + sorted(df["property_type"].dropna().astype(str).unique().tolist())
selected_property = st.sidebar.selectbox("Property Type", property_options)

price_options = ["All", "< 2 Crore", "2-5 Crore", "5-10 Crore", "10-25 Crore", "25+ Crore"]
selected_price = st.sidebar.selectbox("Price Range", price_options)


# Apply the selected filters before building the charts.

filtered_df = df.copy()

if selected_district != "All":
    filtered_df = filtered_df[filtered_df["district"].astype(str) == selected_district]

if selected_property != "All":
    filtered_df = filtered_df[filtered_df["property_type"].astype(str) == selected_property]

if selected_price != "All":
    if selected_price == "< 2 Crore":
        filtered_df = filtered_df[filtered_df["price"] < 2e7]
    elif selected_price == "2-5 Crore":
        filtered_df = filtered_df[(filtered_df["price"] >= 2e7) & (filtered_df["price"] < 5e7)]
    elif selected_price == "5-10 Crore":
        filtered_df = filtered_df[(filtered_df["price"] >= 5e7) & (filtered_df["price"] < 1e8)]
    elif selected_price == "10-25 Crore":
        filtered_df = filtered_df[(filtered_df["price"] >= 1e8) & (filtered_df["price"] < 2.5e8)]
    elif selected_price == "25+ Crore":
        filtered_df = filtered_df[filtered_df["price"] >= 2.5e8]

st.caption(f"Showing {len(filtered_df):,} property listings")


# Let the user choose the map grouping and displayed metric.

col1, col2 = st.columns(2)

with col1:
    analyze_by = st.selectbox("Analyze By", ["District", "Location", "Sub-location"])

with col2:
    metric = st.selectbox("Metric", ["Median Price/sqft", "Median Price", "Number of Listings"])

if metric == "Median Price/sqft":
    color_column = "median_price_per_sqft"
elif metric == "Median Price":
    color_column = "median_price"
else:
    color_column = "listings"


# Reuse these helpers to draw maps and their legends consistently.

def render_pydeck_map(
    data,
    color_column,
    hover_name_field,
    title,
    radius_min_meters=500,
    radius_max_meters=2000,
    radius_min_pixels=5,
    radius_max_pixels=35,
):
    """Renders a pydeck ScatterplotLayer map with a matching gradient legend."""

    st.subheader(title)

    if data.empty:
        st.warning("No data available to plot for the current filters.")
        return

    min_val = data[color_column].min()
    max_val = data[color_column].max()
    norm = mcolors.Normalize(vmin=min_val, vmax=max_val)
    cmap = get_turbo_cmap()

    def get_color(value):
        r, g, b, a = cmap(norm(value))
        return [int(r * 255), int(g * 255), int(b * 255), 180]

    data = data.copy()
    data["color"] = data[color_column].apply(get_color)

    listings_min = data["listings"].min()
    listings_max = data["listings"].max()
    listings_range = listings_max - listings_min

    if listings_range == 0:
        data["radius"] = (radius_min_meters + radius_max_meters) / 2
    else:
        data["radius"] = (
            (data["listings"] - listings_min) / listings_range
            * (radius_max_meters - radius_min_meters) + radius_min_meters
        )

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=data,
        get_position=["longitude", "latitude"],
        get_fill_color="color",
        get_radius="radius",
        radius_min_pixels=radius_min_pixels,
        radius_max_pixels=radius_max_pixels,
        pickable=True,
        opacity=0.85,
        stroked=True,
        get_line_color=[255, 255, 255],
        line_width_min_pixels=1,
    )

    view_state = pdk.ViewState(
        latitude=data["latitude"].mean(),
        longitude=data["longitude"].mean(),
        zoom=10,
        pitch=0,
    )

    tooltip = {
        "html": f"""
            <b>{{{hover_name_field}}}</b><br/>
            Listings: {{listings}}<br/>
            Median Price: {{median_price}}<br/>
            Price/Sqft: {{median_price_per_sqft}}<br/>
            Median Area: {{median_area}}
        """,
        "style": {"backgroundColor": "#1e1e2f", "color": "white"}
    }

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style="dark",
    )

    col_map, col_legend = st.columns([6, 1])

    with col_map:
        st.pydeck_chart(deck)

    with col_legend:
        n_stops = 10
        stops = []
        for i in range(n_stops + 1):
            frac = i / n_stops
            r, g, b, a = cmap(frac)
            stops.append(f"rgb({int(r*255)},{int(g*255)},{int(b*255)}) {frac*100:.0f}%")
        gradient_css = ", ".join(stops)

        st.markdown(f"""
            <div style="display:flex; flex-direction:column; align-items:center; height:400px; padding-top:20px;">
                <div style="font-size:12px; color:white; margin-bottom:4px;">{max_val:,.0f}</div>
                <div style="
                    width:24px;
                    height:340px;
                    background: linear-gradient(to top, {gradient_css});
                    border-radius:4px;
                    border: 1px solid #444;
                "></div>
                <div style="font-size:12px; color:white; margin-top:4px;">{min_val:,.0f}</div>
                <div style="font-size:11px; color:#aaa; margin-top:10px; text-align:center;">
                    {color_column}
                </div>
            </div>
        """, unsafe_allow_html=True)


def render_3d_skyline_map(
    data,
    color_column,
    hover_name_field,
    title,
    min_height_meters=200,
    max_height_meters=3000,
    radius_meters=400,
):
    """Renders a pydeck 3D ColumnLayer 'skyline' where bar height = color_column value."""

    st.subheader(title)

    if data.empty:
        st.warning("No data available to plot for the current filters.")
        return

    min_val = data[color_column].min()
    max_val = data[color_column].max()
    norm = mcolors.Normalize(vmin=min_val, vmax=max_val)
    cmap = get_turbo_cmap()

    def get_color(value):
        r, g, b, a = cmap(norm(value))
        return [int(r * 255), int(g * 255), int(b * 255), 200]

    data = data.copy()
    data["color"] = data[color_column].apply(get_color)

    value_range = max_val - min_val
    if value_range == 0:
        data["elevation"] = (min_height_meters + max_height_meters) / 2
    else:
        data["elevation"] = (
            (data[color_column] - min_val) / value_range
            * (max_height_meters - min_height_meters) + min_height_meters
        )

    layer = pdk.Layer(
        "ColumnLayer",
        data=data,
        get_position=["longitude", "latitude"],
        get_elevation="elevation",
        elevation_scale=1,
        radius=radius_meters,
        get_fill_color="color",
        pickable=True,
        auto_highlight=True,
        extruded=True,
    )

    view_state = pdk.ViewState(
        latitude=data["latitude"].mean(),
        longitude=data["longitude"].mean(),
        zoom=10,
        pitch=50,
        bearing=-20,
    )

    tooltip = {
        "html": f"""
            <b>{{{hover_name_field}}}</b><br/>
            Listings: {{listings}}<br/>
            Median Price: {{median_price}}<br/>
            Price/Sqft: {{median_price_per_sqft}}<br/>
            Median Area: {{median_area}}
        """,
        "style": {"backgroundColor": "#1e1e2f", "color": "white"}
    }

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style="dark",
    )

    col_map, col_legend = st.columns([6, 1])

    with col_map:
        st.pydeck_chart(deck)

    with col_legend:
        n_stops = 10
        stops = []
        for i in range(n_stops + 1):
            frac = i / n_stops
            r, g, b, a = cmap(frac)
            stops.append(f"rgb({int(r*255)},{int(g*255)},{int(b*255)}) {frac*100:.0f}%")
        gradient_css = ", ".join(stops)

        st.markdown(f"""
            <div style="display:flex; flex-direction:column; align-items:center; height:400px; padding-top:20px;">
                <div style="font-size:12px; color:white; margin-bottom:4px;">{max_val:,.0f}</div>
                <div style="
                    width:24px;
                    height:340px;
                    background: linear-gradient(to top, {gradient_css});
                    border-radius:4px;
                    border: 1px solid #444;
                "></div>
                <div style="font-size:12px; color:white; margin-top:4px;">{min_val:,.0f}</div>
                <div style="font-size:11px; color:#aaa; margin-top:10px; text-align:center;">
                    {color_column}
                </div>
            </div>
        """, unsafe_allow_html=True)


# Compare property prices across districts.

if analyze_by == "District":

    has_district_coords = (
        "district_latitude" in filtered_df.columns
        and "district_longitude" in filtered_df.columns
    )

    if has_district_coords:

        district_groupby = (
            filtered_df
            .groupby("district")
            .agg(
                listings=("district", "size"),
                median_price=("price", "median"),
                median_price_per_sqft=("price_per_sqft", "median"),
                median_area=("area", "median"),
                latitude=("district_latitude", "first"),
                longitude=("district_longitude", "first")
            )
            .reset_index()
        )

    else:

        # Use the average location coordinates when district coordinates
        # are not available in the dataset.

        district_groupby = (
            filtered_df
            .groupby("district")
            .agg(
                listings=("district", "size"),
                median_price=("price", "median"),
                median_price_per_sqft=("price_per_sqft", "median"),
                median_area=("area", "median"),
                latitude=("location_latitude", "mean"),
                longitude=("location_longitude", "mean")
            )
            .reset_index()
        )

        st.caption(
            "ℹ️ No dedicated district coordinates found — district positions "
            "are approximated from the average location coordinates within each district."
        )

    district_groupby = district_groupby.dropna(subset=["latitude", "longitude"])

    district_view_mode = st.radio(
        "Map View",
        ["Flat", "3D Skyline"],
        horizontal=True,
        key="district_view_mode"
    )

    if district_view_mode == "Flat":
        render_pydeck_map(
            district_groupby,
            color_column,
            hover_name_field="district",
            title="District Price per Sqft Geomap"
        )
    else:
        render_3d_skyline_map(
            district_groupby,
            color_column,
            hover_name_field="district",
            title="District Price per Sqft — 3D Skyline",
            radius_meters=800
        )

    # Show detailed statistics for the selected district.

    st.divider()

    district_options = sorted(filtered_df["district"].dropna().astype(str).unique().tolist())

    if district_options:

        selected_district_detail = st.selectbox("📍 Select a district to explore", district_options)

        district_data = filtered_df[filtered_df["district"].astype(str) == selected_district_detail]

        listings = len(district_data)
        median_price = district_data["price"].median()
        median_area = district_data["area"].median()
        median_ppsf = district_data["price_per_sqft"].median()

        st.subheader(f"📍 {selected_district_detail}")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric("Listings", f"{listings:,}")
        with c2:
            st.metric("Median Price", f"{median_price / 1e7:.2f} Cr")
        with c3:
            st.metric("Median Price/sqft", f"Rs. {median_ppsf:,.0f}")
        with c4:
            st.metric("Median Area", f"{median_area:,.0f} sqft")


# Compare property prices across locations.

elif analyze_by == "Location":

    location_groupby = (
        filtered_df
        .groupby("location")
        .agg(
            listings=("location", "size"),
            median_price=("price", "median"),
            median_price_per_sqft=("price_per_sqft", "median"),
            median_area=("area", "median"),
            latitude=("location_latitude", "first"),
            longitude=("location_longitude", "first"),
            market_category=("location_category", "first")
        )
        .reset_index()
    )

    view_mode = st.radio(
        "Map View",
        ["Flat", "3D Skyline"],
        horizontal=True,
        key="location_view_mode"
    )

    if view_mode == "Flat":
        render_pydeck_map(
            location_groupby,
            color_column,
            hover_name_field="location",
            title="Location Price per Sqft Geomap"
        )
    else:
        render_3d_skyline_map(
            location_groupby,
            color_column,
            hover_name_field="location",
            title="Location Price per Sqft — 3D Skyline"
        )

    # Show detailed statistics for the selected location.

    st.divider()

    location_options = sorted(filtered_df["location"].dropna().astype(str).unique().tolist())

    if location_options:

        selected_location = st.selectbox("📍 Select a location to explore", location_options)

        location_data = filtered_df[filtered_df["location"].astype(str) == selected_location]

        listings = len(location_data)
        median_price = location_data["price"].median()
        median_area = location_data["area"].median()
        median_ppsf = location_data["price_per_sqft"].median()

        market_category_data = location_data["location_category"].dropna()
        market_category = market_category_data.iloc[0] if len(market_category_data) > 0 else "Unknown"

        st.subheader(f"📍 {selected_location}")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric("Listings", f"{listings:,}")
        with c2:
            st.metric("Median Price", f"{median_price / 1e7:.2f} Cr")
        with c3:
            st.metric("Median Price/sqft", f"Rs. {median_ppsf:,.0f}")
        with c4:
            st.metric("Median Area", f"{median_area:,.0f} sqft")

        st.info(f"⭐ Market Category: **{market_category}**")


# Compare prices within each location's sub-locations.

else:  # analyze_by == "Sub-location"

    sub_location_groupby = (
        filtered_df
        .groupby(["location", "sub_location"])
        .agg(
            listings=("sub_location", "size"),
            median_price=("price", "median"),
            median_price_per_sqft=("price_per_sqft", "median"),
            median_area=("area", "median"),
            latitude=("sub_location_latitude", "first"),
            longitude=("sub_location_longitude", "first")
        )
        .reset_index()
    )

    location_options = ["All"] + sorted(sub_location_groupby["location"].dropna().astype(str).unique().tolist())

    if len(location_options) == 1:
        st.warning("No locations available for the selected filters.")
        st.stop()

    selected_location = st.selectbox("📍 Select Location", location_options)

    if selected_location == "All":
        sub_df = sub_location_groupby.copy()
        st.subheader("🗺️ All Locations — Sub-locations")
    else:
        sub_df = sub_location_groupby[
            sub_location_groupby["location"].astype(str) == selected_location
        ].copy()
        st.subheader(f"🗺️ {selected_location} — Sub-locations")

    st.caption("Explore individual sub-locations within this area.")

    sub_view_mode = st.radio(
        "Map View",
        ["Flat", "3D Skyline"],
        horizontal=True,
        key="sub_location_view_mode"
    )

    if sub_view_mode == "Flat":
        render_pydeck_map(
            sub_df,
            color_column,
            hover_name_field="sub_location",
            title="Sub-location Price per Sqft Geomap",
            radius_min_meters=150,
            radius_max_meters=600,
            radius_min_pixels=4,
            radius_max_pixels=20,
        )
    else:
        render_3d_skyline_map(
            sub_df,
            color_column,
            hover_name_field="sub_location",
            title="Sub-location Price per Sqft — 3D Skyline",
            min_height_meters=100,
            max_height_meters=1500,
            radius_meters=150,
        )

    # Show detailed statistics for the selected sub-location.

    st.divider()

    sub_location_options = sorted(sub_df["sub_location"].dropna().astype(str).unique().tolist())

    if sub_location_options:

        selected_sub_location = st.selectbox("📍 Select Sub-location", sub_location_options)

        if selected_location == "All":
            sub_location_data = filtered_df[
                filtered_df["sub_location"].astype(str) == selected_sub_location
            ]
        else:
            sub_location_data = filtered_df[
                (filtered_df["location"].astype(str) == selected_location)
                & (filtered_df["sub_location"].astype(str) == selected_sub_location)
            ]

        listings = len(sub_location_data)
        median_price = sub_location_data["price"].median()
        median_area = sub_location_data["area"].median()
        median_ppsf = sub_location_data["price_per_sqft"].median()

        st.subheader(f"📍 {selected_sub_location}")

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric("Listings", f"{listings:,}")
        with c2:
            st.metric("Median Price", f"{median_price / 1e7:.2f} Cr")
        with c3:
            st.metric("Median Price/sqft", f"Rs. {median_ppsf:,.0f}")
        with c4:
            st.metric("Median Area", f"{median_area:,.0f} sqft")

    else:
        st.warning("No sub-locations available for this location.")

# Compare selected districts using a radar chart.

st.divider()
st.header("🕸️ District Fingerprint Comparison")
st.caption(
    "Compare districts across price, size, and room count. "
    "Values are normalized 0–1 per metric so shapes can be compared directly."
)

fingerprint_metrics = ["price", "area", "bedrooms", "bathrooms", "price_per_sqft"]

district_profile = (
    filtered_df
    .groupby("district")[fingerprint_metrics]
    .median()
)

all_districts_fp = sorted(district_profile.index.tolist())
default_districts_fp = all_districts_fp[:3] if len(all_districts_fp) >= 3 else all_districts_fp

selected_districts_fp = st.multiselect(
    "Select districts to compare",
    all_districts_fp,
    default=default_districts_fp
)

if selected_districts_fp:

    # Normalize only the selected districts so an outlier elsewhere does not
    # flatten the comparison.
    subset_profile = district_profile.loc[selected_districts_fp]
    metric_range = subset_profile.max() - subset_profile.min()
    normalized_profile = (subset_profile - subset_profile.min()) / metric_range.replace(0, 1)
    normalized_profile = normalized_profile.fillna(0.5)  # if only 1 district selected, center it

    categories = fingerprint_metrics + [fingerprint_metrics[0]]  # close the polygon loop

    fig_fp = go.Figure()

    for district_name in selected_districts_fp:
        norm_values = normalized_profile.loc[district_name, fingerprint_metrics].tolist()
        norm_values += norm_values[:1]

        raw_values = subset_profile.loc[district_name, fingerprint_metrics].tolist()
        raw_values += raw_values[:1]

        fig_fp.add_trace(go.Scatterpolar(
            r=norm_values,
            theta=categories,
            fill="toself",
            name=district_name,
            customdata=raw_values,
            hovertemplate="<b>%{theta}</b><br>%{customdata:,.0f}<extra>" + district_name + "</extra>",
        ))

    fig_fp.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1], color="white"),
            angularaxis=dict(color="white"),
            bgcolor="rgba(0,0,0,0)",
        ),
        showlegend=True,
        legend=dict(font=dict(color="white")),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        height=550,
        margin=dict(l=60, r=60, t=40, b=40),
    )

    st.plotly_chart(fig_fp, width="stretch")

    with st.expander("📋 View raw median values"):
        st.dataframe(
            district_profile.loc[selected_districts_fp].style.format("{:,.0f}")
        )

else:
    st.info("Select at least one district above to see the fingerprint chart.")

# Explore the relationship between property area and price.
 
st.divider()
st.header("Area Vs Price")

st.caption(
    "Property Type is controlled by the sidebar filter. "
    "Use the filters below to narrow this chart further."
)

location_options_scatter = ["All"] + sorted(filtered_df["location"].dropna().unique().tolist())
selected_location_scatter = st.selectbox("📍 Filter by Location", location_options_scatter)

bedroom_options = sorted(filtered_df["bedrooms"].dropna().unique().tolist())
selected_bedrooms = st.multiselect(
    "🛏️ Filter by Bedrooms (leave empty for all)",
    bedroom_options
)

scatter_df = filtered_df.copy()

if selected_location_scatter != "All":
    scatter_df = scatter_df[scatter_df["location"] == selected_location_scatter]

if selected_bedrooms:
    scatter_df = scatter_df[scatter_df["bedrooms"].isin(selected_bedrooms)]

if scatter_df.empty:
    st.warning("No listings match the selected filters.")
else:

    area_min, area_max = float(scatter_df["area"].min()), float(scatter_df["area"].max())

    if area_min < area_max:
        selected_area_range = st.slider(
            "📐 Area Range (sqft)",
            min_value=area_min,
            max_value=area_max,
            value=(area_min, area_max)
        )
    else:
        selected_area_range = (area_min, area_max)
        st.caption(f"📐 All matching listings have the same area: {area_min:,.0f} sqft")

    price_min, price_max = float(scatter_df["price"].min()), float(scatter_df["price"].max())

    if price_min < price_max:
        selected_price_range = st.slider(
            "💰 Price Range",
            min_value=price_min,
            max_value=price_max,
            value=(price_min, price_max)
        )
    else:
        selected_price_range = (price_min, price_max)
        st.caption(f"💰 All matching listings have the same price: Rs. {price_min:,.0f}")

    scatter_df = scatter_df[
        (scatter_df["area"] >= selected_area_range[0])
        & (scatter_df["area"] <= selected_area_range[1])
        & (scatter_df["price"] >= selected_price_range[0])
        & (scatter_df["price"] <= selected_price_range[1])
    ]

    if scatter_df.empty:
        st.warning("No listings match the selected filters.")
    else:
        chart_title = "Area Vs Price"
        if selected_property != "All":
            chart_title += f" — {selected_property}"

        fig1 = px.scatter(
            scatter_df,
            x="area",
            y="price",
            color="bedrooms",
            color_continuous_scale="Turbo",
            title=chart_title
        )

        st.plotly_chart(fig1, width="stretch")

# Show bedroom proportions for the selected location.
st.divider()
st.header("BHK Pie Chart")

location_options=filtered_df['location'].unique().tolist()
location_options.insert(0,'Overall')
sub_location_options=filtered_df['location'].unique().tolist()
sub_location_options.insert(0,'Overall')

selected_location=st.selectbox("Enter location",location_options)
if selected_location =='Overall':
    fig2=px.pie(filtered_df,names='bedrooms')
    st.plotly_chart(fig2,use_container_width=True)
else:
    sub_location_options=filtered_df[filtered_df['location']==selected_location]['sub_location'].unique().tolist()
    sub_location_options.insert(0,'Overall')
    selected_sub_location=st.selectbox("Enter sub location",sub_location_options)
    if selected_sub_location=='Overall':
        fig2=px.pie(filtered_df[filtered_df['location']==selected_location],names='bedrooms')
        st.plotly_chart(fig2,use_container_width=True)
    else:
        fig2=px.pie(filtered_df[(filtered_df['location']==selected_location) & (filtered_df['sub_location']==selected_sub_location)],names='bedrooms')
        st.plotly_chart(fig2,use_container_width=True)
    
# Compare the distribution of prices, areas, or price per square foot.
st.divider()

st.subheader("📊 Property Distribution Analysis")

x_column = st.selectbox("Group By",["District","Property Type","Location Category","Age Category","Bedrooms"])
y_column = st.selectbox("Measure",["Price","Area","Price/sqft"])

if x_column == "District":
    x = "district"
elif x_column == "Property Type":
    x = "property_type"
elif x_column == "Location Category":
    x = "location_category"
elif x_column == "Age Category":
    x = "age_category"
elif x_column == "Bedrooms":
    x = "bedrooms"

if y_column == "Price":
    y = "price"
elif y_column == "Area":
    y = "area"
elif y_column == "Price/sqft":
    y = "price_per_sqft"

plot_df = filtered_df.copy()

# Limit bedroom groups to the common 1-to-4 bedroom range.
if x_column == "Bedrooms":
    plot_df = plot_df[plot_df["bedrooms"].between(1,4)].copy()

if y_column == "Price":
    plot_df["price_crore"] = plot_df["price"] / 1e7
    y = "price_crore"
    y_title = "Price (Crore PKR)"
else:
    y_title = y_column

fig = px.box(plot_df,x=x,y=y,points="outliers",title=f"{y_column} Distribution by {x_column}", color_discrete_sequence=px.colors.qualitative.Set2)

fig.update_layout(height=600,xaxis_title=x_column,yaxis_title=y_title,title_x=0.5,margin=dict(l=20,r=20,t=60,b=20),template="plotly_white")

fig.update_traces(marker_size=3,line_width=1.5)

st.plotly_chart(fig,use_container_width=True)
import seaborn as sns
st.divider()

st.subheader("📈 Distribution Analysis")

select_variable = st.selectbox("Select Variable",["Price","Area","Price/sqft"],key="distplot_variable")

plot_df = filtered_df.copy()

group = "property_type"


if select_variable == "Price":

    plot_df["price_crore"] = plot_df["price"] / 1e7

    plot_df = plot_df[
        plot_df["price_crore"] <= 25
    ]

    value = "price_crore"
    x_title = "Price (Crore PKR)"

elif select_variable == "Area":

    plot_df = plot_df[
        plot_df["area"] <=
        plot_df["area"].quantile(0.99)
    ]

    value = "area"
    x_title = "Area (sqft)"

else:

    plot_df = plot_df[
        plot_df["price_per_sqft"] <=
        plot_df["price_per_sqft"].quantile(0.99)
    ]

    value = "price_per_sqft"
    x_title = "Price/sqft (PKR)"


plot_df = plot_df[
    plot_df[group].notna() &
    plot_df[value].notna()
].copy()


sns.set_theme(
    style="white",
    palette="deep"
)

fig, ax = plt.subplots(
    figsize=(11,5.5)
)


sns.kdeplot(
    data=plot_df,
    x=value,
    hue=group,
    common_norm=False,
    fill=False,
    linewidth=2.5,
    bw_adjust=1.0,
    ax=ax
)


ax.set_title(
    f"{select_variable} Distribution by Property Type",
    fontsize=15,
    fontweight="bold",
    pad=18
)

ax.set_xlabel(
    x_title,
    fontsize=11,
    labelpad=10
)

ax.set_ylabel(
    "Density",
    fontsize=11,
    labelpad=10
)

ax.grid(
    axis="y",
    linestyle="--",
    linewidth=0.7,
    alpha=0.25
)

ax.grid(
    axis="x",
    visible=False
)

sns.despine(
    top=True,
    right=True
)

legend = ax.get_legend()

if legend is not None:
    legend.set_title("Property Type")
    legend.set_frame_on(False)

plt.tight_layout()

st.pyplot(
    fig,
    use_container_width=True
)