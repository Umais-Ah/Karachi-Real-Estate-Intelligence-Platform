import streamlit as st 
import pandas as pd 
from pathlib import Path
from importlib.util import module_from_spec, spec_from_file_location

project_root = Path(__file__).resolve().parents[2]

recommender_path = project_root / "src" / "recommender.py"
recommender_spec = spec_from_file_location("recommender", recommender_path)
if recommender_spec is None or recommender_spec.loader is None:
    raise ImportError(f"Could not load recommender module from {recommender_path}")

recommender_module = module_from_spec(recommender_spec)
recommender_spec.loader.exec_module(recommender_module)
recommend_properties = recommender_module.recommend_properties
 
st.set_page_config( 
    page_title="Real Estate Recommender", 
    layout="wide", 
    initial_sidebar_state="expanded" 
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

    [data-testid="stAppViewContainer"] { background: #0d1218; }

    .block-container {
        max-width: 1240px;
        padding-top: 4rem;
        padding-bottom: 4rem;
    }

    .recommender-hero {
        position: relative;
        overflow: hidden;
        padding: 2.8rem 3.2rem;
        border-radius: 24px;
        margin-bottom: 2.2rem;
        background: var(--teal-dark);
        box-shadow: 0 18px 45px rgba(25, 48, 48, 0.18);
    }

    .recommender-hero::after {
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

    .recommender-hero h1 {
        position: relative;
        z-index: 1;
        color: #fffdfa;
        font-size: clamp(2.2rem, 5vw, 4rem);
        font-weight: 800;
        letter-spacing: -0.06em;
        line-height: 1;
        margin: 0 0 0.9rem;
    }

    .recommender-hero p {
        position: relative;
        z-index: 1;
        max-width: 650px;
        color: #cfe1dc;
        font-size: 1rem;
        line-height: 1.7;
        margin: 0;
    }

    h1, h2, h3, h4 { color: #f4f1e8 !important; letter-spacing: -0.04em; }

    [data-testid="stSidebar"] {
        background: #111b21;
        border-right: 1px solid #2c3b40;
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #f4f1e8 !important;
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
        min-height: 2.8rem;
        border: 1px solid var(--coral);
        border-radius: 10px;
        background: var(--coral);
        color: white;
        font-weight: 800;
    }

    .stButton > button:hover {
        border-color: #c95e48;
        background: #c95e48;
        color: white;
    }

    [data-testid="stMetric"] {
        padding: 1rem;
        border: 1px solid #2c3b40;
        border-radius: 12px;
        background: #17242b;
    }

    [data-testid="stMetricLabel"] p { color: #aebfc0; }
    [data-testid="stMetricValue"] { color: #f4f1e8; }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #34464b !important;
        border-radius: 16px !important;
        background: #121c22;
        padding: 0.35rem;
    }

    [data-testid="stAlert"] { border-radius: 14px; }

    @media (max-width: 640px) {
        .block-container { padding-top: 2rem; }
        .recommender-hero {
            padding: 1.8rem 1.25rem;
            border-radius: 18px;
            margin-bottom: 1.5rem;
            margin-top: 1rem;
        }
        .recommender-hero::after {
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
        .recommender-hero h1 {
            font-size: 2.2rem;
            line-height: 1.04;
            letter-spacing: -0.03em;
            margin-bottom: 0.75rem;
        }
        .recommender-hero p {
            font-size: 0.9rem;
            line-height: 1.55;
        }
    }

    @media (max-width: 400px) {
        .recommender-hero { padding: 1.5rem 1rem; }
        .recommender-hero h1 { font-size: 2rem; }
    }
    </style>
    """
)

st.html(
    """
    <div class="recommender-hero">
        <div class="hero-kicker">Karachi property intelligence · smart shortlist</div>
        <h1>Find a home that fits your life.</h1>
        <p>
            Set your budget, preferred areas, and must-have features to turn
            thousands of listings into a focused shortlist worth exploring.
        </p>
    </div>
    """
)
 
@st.cache_data 
def load_data():
    path = project_root / "data" / "cleaned" / "recommender_dataset.csv"
    return pd.read_csv(path)
 
try:
    df = load_data()
except FileNotFoundError:
    st.error("The recommender dataset was not found in data/cleaned.")
    st.stop()
 
st.sidebar.header("Search preferences")

if df is not None:
    # Start by letting the user choose the main area.
    locations = sorted(df['location'].unique().tolist()) 
    selected_location = st.sidebar.selectbox( 
        "Select Main Location", 
        options=locations, 
        help="Choose the main area you're interested in" 
    ) 
     
    # Narrow the sub-location choices to the selected area.
    sub_locations = df[df['location'] == selected_location]['sub_location'].unique().tolist() 
    sub_locations = sorted([str(x) for x in sub_locations if pd.notna(x)]) 
     
    include_sub = st.sidebar.checkbox("Search specific sub-location?", value=False) 
    selected_sub_location = None 
    if include_sub and sub_locations: 
        selected_sub_location = st.sidebar.selectbox( 
            "Select Sub-Location", 
            options=sub_locations, 
            help="Choose a specific area within the location" 
        ) 
     
    st.sidebar.subheader("Property details")
     
    property_type = st.sidebar.selectbox( 
        "Property Type", 
        options=['Flat', 'House'], 
        help="Type of property you're looking for" 
    ) 
     
    bedrooms = st.sidebar.slider( 
        "Number of Bedrooms", 
        min_value=1, 
        max_value=11, 
        value=3, 
        step=1 
    ) 
     
    col1, col2 = st.sidebar.columns(2) 
    with col1: 
        area_min = st.number_input( 
            "Min Area (sqft)", 
            min_value=100, 
            max_value=36000, 
            value=1000, 
            step=100 
        ) 
    with col2: 
        area_max = st.number_input( 
            "Max Area (sqft)", 
            min_value=100, 
            max_value=36000, 
            value=2000, 
            step=100 
        ) 
     
    if area_min > area_max: 
        st.sidebar.error("Minimum area must not exceed maximum area") 
        area_min, area_max = area_max, area_min 
     
    age_category = st.sidebar.selectbox( 
        "Property Age", 
        options=[ 
            'under construction', 
            'new', 
            'relatively new', 
            'moderately old', 
            'old' 
        ], 
        index=2 
    ) 
     
    st.sidebar.subheader("Price range")
     
    col1, col2 = st.sidebar.columns(2) 
    with col1: 
        price_min = st.number_input( 
            "Min Price (PKR)", 
            min_value=1_000_000, 
            max_value=2_000_000_000, 
            value=10_000_000, 
            step=1_000_000, 
            format="%d" 
        ) 
    with col2: 
        price_max = st.number_input( 
            "Max Price (PKR)", 
            min_value=1_000_000, 
            max_value=2_000_000_000, 
            value=50_000_000, 
            step=1_000_000, 
            format="%d" 
        ) 
     
    if price_min > price_max: 
        st.sidebar.error("Minimum price must not exceed maximum price") 
        price_min, price_max = price_max, price_min 
     
    st.sidebar.subheader("Amenities")
     
    parking_options = ['Any', 'Luxury Parking', 'Premium Parking', 'Good Parking', 'Basic Parking', 'No Parking'] 
    parking = st.sidebar.selectbox( 
        "Parking", 
        options=parking_options, 
        index=0 
    ) 
    parking = None if parking == 'Any' else parking 
     
    furnished = st.sidebar.radio( 
        "Furnished", 
        options=['No preference', 'Yes', 'No'], 
        index=0 
    ) 
    furnished = None if furnished == 'No preference' else (1 if furnished == 'Yes' else 0) 
     
    kitchen = st.sidebar.radio( 
        "Kitchen", 
        options=['No preference', 'Yes', 'No'], 
        index=0 
    ) 
    kitchen = None if kitchen == 'No preference' else (1 if kitchen == 'Yes' else 0) 
     
    electricity = st.sidebar.radio( 
        "Electricity Backup", 
        options=['No preference', 'Yes', 'No'], 
        index=0 
    ) 
    electricity = None if electricity == 'No preference' else (1 if electricity == 'Yes' else 0) 
     
    servant_quarters_options = ['No preference', 'None', '1-2', '3+'] 
    servant_quarters = st.sidebar.selectbox( 
        "Servant Quarters", 
        options=servant_quarters_options, 
        index=0 
    ) 
    servant_quarters = None if servant_quarters == 'No preference' else servant_quarters 
     
    top_n = st.sidebar.slider( 
        "Number of Results", 
        min_value=5, 
        max_value=50, 
        value=10, 
        step=5 
    ) 
     
    search_button = st.sidebar.button("Search properties", use_container_width=True) 
     
    if search_button: 
        with st.spinner("Searching for properties..."): 
            try: 
                recommendations = recommend_properties( 
                    df=df, 
                    user_location=selected_location, 
                    user_sub_location=selected_sub_location, 
                    user_property_type=property_type, 
                    user_bedrooms=bedrooms, 
                    user_area_min=area_min, 
                    user_area_max=area_max, 
                    user_age_category=age_category, 
                    user_price_min=price_min, 
                    user_price_max=price_max, 
                    user_parking=parking, 
                    user_furnished=furnished, 
                    user_kitchen=kitchen, 
                    user_electricity=electricity, 
                    user_servant_quarters=servant_quarters, 
                    top_n=top_n 
                ) 
                 
                if recommendations.empty:
                    st.warning("No properties found. Try changing your search.")
                else: 
                    col1, col2, col3, col4 = st.columns(4) 
                     
                    with col1: 
                        st.metric("Found", len(recommendations)) 
                    with col2: 
                        avg_price = recommendations['price'].mean() 
                        st.metric("Avg Price", f"PKR {avg_price/1e6:.1f}M") 
                    with col3: 
                        avg_area = recommendations['area'].mean() 
                        st.metric("Avg Area", f"{int(avg_area)} sqft") 
                    with col4: 
                        best_score = recommendations['final_score'].max() 
                        st.metric("Best Score", f"{best_score:.1f}/100") 
                     
                    st.markdown("---") 
                     
                    st.markdown(f"## Top {len(recommendations)} Results") 
                     
                    for idx, (_, row) in enumerate(recommendations.iterrows(), 1): 
                        with st.container(border=True): 
                            col1, col2 = st.columns([2, 1]) 
                             
                            with col1: 
                                st.markdown(f"### #{idx} - {row['property_name']}") 
                                 
                                col_a, col_b, col_c, col_d = st.columns(4) 
                                with col_a: 
                                    st.metric("Bedrooms", f"{int(row['bedrooms'])} BR") 
                                with col_b: 
                                    st.metric("Area", f"{int(row['area'])} sqft") 
                                with col_c: 
                                    st.metric("Price", f"PKR {row['price']/1e6:.1f}M") 
                                with col_d: 
                                    st.metric("Price/sqft", f"PKR {int(row['price_per_sqft'])}") 
                                 
                                st.write("") 
                                col_1, col_2, col_3, col_4 = st.columns(4) 
                                with col_1: 
                                    st.write(f"**Location:** {row['sub_location']}") 
                                with col_2: 
                                    st.write(f"**Parking:** {row['parking_category']}") 
                                with col_3: 
                                    furnished_status = "Yes" if row['furnished'] == 1 else "No" 
                                    st.write(f"**Furnished:** {furnished_status}") 
                                with col_4: 
                                    elec_status = "Yes" if row['electricity_backup'] == 1 else "No" 
                                    st.write(f"**Electricity:** {elec_status}") 
                             
                            with col2: 
                                st.markdown("### Scores") 
                                score_data = { 
                                    'Location': row['location_final_score'], 
                                    'Property': row['property_score'], 
                                    'Amenity': row['amenity_score'], 
                                    'Final': row['final_score'] 
                                } 
                                 
                                for metric, value in score_data.items(): 
                                    if metric == 'Final': 
                                        st.markdown(f"**{metric}:** `{value:.1f}/100`") 
                                        if value >= 90: 
                                            st.success("Excellent match") 
                                        elif value >= 80: 
                                            st.info("Good match") 
                                        else: 
                                            st.warning("Fair match") 
                                    else: 
                                        st.write(f"**{metric}:** {value:.1f}") 
                             
                            st.markdown("---") 
             
            except Exception as error:
                st.error(f"Error: {error}")
                st.info("Please check your inputs and try again.") 
     
    else: 
        # Explain how to begin when no search has been submitted yet.
        st.info("Set your search preferences in the sidebar and click Search properties.") 
         
        # Give the user a quick overview of the available listings.
        st.markdown("---") 
        st.markdown("## Dataset overview") 
         
        col1, col2, col3, col4, col5 = st.columns(5) 
         
        with col1: 
            st.metric("Total Properties", f"{len(df):,}") 
        with col2: 
            st.metric("Locations", df['location'].nunique()) 
        with col3: 
            st.metric("Sub-Locations", df['sub_location'].nunique()) 
        with col4: 
            st.metric("Price Range", f"PKR {df['price'].min()/1e6:.1f}M - PKR {df['price'].max()/1e6:.0f}M") 
        with col5: 
            st.metric("Bedrooms Range", f"1 - {int(df['bedrooms'].max())}") 
         
        # Show a few example listings while the user is choosing filters.
        st.markdown("### Sample properties") 
        sample_df = df.sample(n=5)[['property_name', 'bedrooms', 'area', 'price', 'location', 'parking_category']] 
         
        display_df = sample_df.copy() 
        display_df['price'] = display_df['price'].apply(lambda x: f"PKR {x/1e6:.1f}M") 
        display_df['area'] = display_df['area'].apply(lambda x: f"{int(x)} sqft") 
        display_df['bedrooms'] = display_df['bedrooms'].apply(lambda x: f"{int(x)} BR") 
         
        st.dataframe(display_df, use_container_width=True, hide_index=True) 
 
else: 
    st.error("❌ Unable to load dataset. Please check the file location.") 
    st.info("Make sure data/cleaned/recommender_dataset.csv is available.")