import numpy as np
import pandas as pd
import warnings
from pathlib import Path
warnings.filterwarnings('ignore')


# Distance calculation
def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates in km"""
    R = 6371
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    return R * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))


# Location scoring
def calculate_location_score(df, user_location, user_sub_location=None, reference_df=None):
    """
    Score properties based on location match
    - Exact sub_location match: 100
    - Same location: 70
    - Other location: distance-based (exponential decay)
    """
    result = df.copy()
    reference_df = df if reference_df is None else reference_df

    selected_location = str(user_location).strip().lower()
    selected_sub_location = str(user_sub_location).strip().lower() if user_sub_location else None

    res_loc = result["location"].fillna("").astype(str).str.strip().str.lower()
    res_sub_loc = result["sub_location"].fillna("").astype(str).str.strip().str.lower()
    ref_loc = reference_df["location"].fillna("").astype(str).str.strip().str.lower()
    ref_sub_loc = reference_df["sub_location"].fillna("").astype(str).str.strip().str.lower()

    # Hierarchy score
    result["hierarchy_score"] = np.where(res_loc == selected_location, 70, 0.0)
    if selected_sub_location:
        result.loc[res_sub_loc == selected_sub_location, "hierarchy_score"] = 100

    # Distance score
    reference = reference_df[ref_sub_loc == selected_sub_location] if selected_sub_location else reference_df[ref_loc == selected_location]
    reference = reference.dropna(subset=["location_latitude", "location_longitude"])

    result["distance_km"], result["distance_score"] = np.nan, 0.0

    if not reference.empty:
        ref_lat = reference["location_latitude"].iloc[0]
        ref_lon = reference["location_longitude"].iloc[0]
        valid_coords = result["location_latitude"].notna() & result["location_longitude"].notna()

        result.loc[valid_coords, "distance_km"] = haversine_distance(
            ref_lat, ref_lon, 
            result.loc[valid_coords, "location_latitude"], 
            result.loc[valid_coords, "location_longitude"]
        )
        result.loc[valid_coords, "distance_score"] = np.exp(-result.loc[valid_coords, "distance_km"] / 10) * 100

    # Combined location score
    result["location_final_score"] = (
        result["hierarchy_score"] * 0.50 + result["distance_score"] * 0.50
    ).clip(0, 100)

    return result


# Property scoring
def calculate_property_score(df, user_property_type, user_bedrooms, user_area_min, user_area_max, user_age_category):
    """
    Score properties based on:
    - Property type (35%)
    - Bedrooms (30%)
    - Area (20%)
    - Age category (15%)
    """
    result = df.copy()

    # Property type match (35%)
    result["property_type_score"] = (
        result["property_type"].astype(str).str.strip().str.lower() == str(user_property_type).strip().lower()
    ).astype(float) * 100

    # Bedroom match (30%)
    bedroom_difference = abs(result["bedrooms"] - user_bedrooms)
    result["bedroom_score"] = np.select(
        [bedroom_difference == 0, bedroom_difference == 1, bedroom_difference == 2],
        [100, 70, 40],
        default=0
    )

    # Area match (20%)
    result["area_score"] = 0.0
    within_area = (result["area"] >= user_area_min) & (result["area"] <= user_area_max)
    result.loc[within_area, "area_score"] = 100

    area_range = user_area_max - user_area_min
    if area_range > 0:
        below_area = result["area"] < user_area_min
        result.loc[below_area, "area_score"] = 100 - ((user_area_min - result.loc[below_area, "area"]) / area_range) * 100

        above_area = result["area"] > user_area_max
        result.loc[above_area, "area_score"] = 100 - ((result.loc[above_area, "area"] - user_area_max) / area_range) * 100

    # Age match (15%)
    age_order = {"under construction": 0, "new": 1, "relatively new": 2, "moderately old": 3, "old": 4}
    user_age = str(user_age_category).strip().lower()
    user_age_index = age_order.get(user_age)

    if user_age_index is not None:
        property_age_index = result["age_category"].astype(str).str.strip().str.lower().map(age_order)
        age_difference = abs(property_age_index - user_age_index)
        result["age_score"] = np.select(
            [age_difference == 0, age_difference == 1, age_difference == 2, age_difference == 3],
            [100, 75, 50, 25],
            default=0
        )
    else:
        result["age_score"] = 0

    # Combined property score
    result["property_score"] = (
        result["property_type_score"] * 0.35 +
        result["bedroom_score"] * 0.30 +
        result["area_score"] * 0.20 +
        result["age_score"] * 0.15
    ).clip(0, 100)

    return result


# Amenity scoring
def calculate_amenity_score(df, user_parking=None, user_furnished=None, user_kitchen=None, 
                           user_electricity=None, user_servant_quarters=None):
    """
    Score properties based on amenities:
    - Parking (40%)
    - Furnished (25%)
    - Kitchen (15%)
    - Electricity Backup (12%)
    - Servant Quarters (8%)
    """
    result = df.copy()
    
    amenity_scores = []
    score_labels = []
    total_weight = 0
    
    # Parking score (40% weight)
    if user_parking:
        parking_order = {"no parking": 0, "basic parking": 1, "good parking": 2, "premium parking": 3, "luxury parking": 4}
        
        user_parking_normalized = str(user_parking).strip().lower()
        user_parking_index = parking_order.get(user_parking_normalized, 2)
        
        property_parking = result["parking_category"].fillna("").astype(str).str.strip().str.lower()
        property_parking_index = property_parking.map(parking_order).fillna(2)
        
        parking_diff = abs(property_parking_index - user_parking_index)
        parking_score = np.select(
            [parking_diff == 0, parking_diff == 1, parking_diff == 2, parking_diff == 3],
            [100, 75, 50, 25],
            default=0
        )
        
        amenity_scores.append(parking_score)
        score_labels.append('parking_score')
        total_weight += 0.40
    
    # Furnished score (25% weight)
    if user_furnished is not None:
        # Convert 1/0 to 'yes'/'no'
        furnished_match = (
            result["furnished"].fillna(0).astype(int).astype(str).str.lower() == 
            str(int(user_furnished)).lower()
        ).astype(float) * 100
        
        amenity_scores.append(furnished_match)
        score_labels.append('furnished_score')
        total_weight += 0.25
    
    # Kitchen score (15% weight)
    if user_kitchen is not None:
        # Kitchen can be 0-4 (ordinal)
        kitchen_diff = abs(result["kitchen"].fillna(0) - user_kitchen)
        kitchen_score = np.select(
            [kitchen_diff == 0, kitchen_diff == 1, kitchen_diff == 2],
            [100, 75, 50],
            default=0
        )
        
        amenity_scores.append(kitchen_score)
        score_labels.append('kitchen_score')
        total_weight += 0.15
    
    # Electricity backup score (12% weight)
    if user_electricity is not None:
        electricity_match = (
            result["electricity_backup"].fillna(0).astype(int).astype(str).str.lower() == 
            str(int(user_electricity)).lower()
        ).astype(float) * 100
        
        amenity_scores.append(electricity_match)
        score_labels.append('electricity_score')
        total_weight += 0.12
    
    # Servant quarters score (8% weight)
    if user_servant_quarters is not None:
        servant_order = {"none": 0, "1-2": 1, "1–2": 1, "2": 1, "3+": 2, "3": 2}
        
        user_servant_normalized = str(user_servant_quarters).strip().lower()
        user_servant_index = servant_order.get(user_servant_normalized, 0)
        
        property_servant = result["servant_quarters"].fillna("").astype(str).str.strip().str.lower()
        property_servant_index = property_servant.map(servant_order).fillna(0)
        
        servant_diff = abs(property_servant_index - user_servant_index)
        servant_score = np.select(
            [servant_diff == 0, servant_diff == 1],
            [100, 50],
            default=0
        )
        
        amenity_scores.append(servant_score)
        score_labels.append('servant_score')
        total_weight += 0.08
    
    # Calculate weighted amenity score
    if amenity_scores and total_weight > 0:
        # Normalize weights
        normalized_weights = []
        if 'parking_score' in score_labels:
            normalized_weights.append(0.40 / total_weight)
        if 'furnished_score' in score_labels:
            normalized_weights.append(0.25 / total_weight)
        if 'kitchen_score' in score_labels:
            normalized_weights.append(0.15 / total_weight)
        if 'electricity_score' in score_labels:
            normalized_weights.append(0.12 / total_weight)
        if 'servant_score' in score_labels:
            normalized_weights.append(0.08 / total_weight)
        
        result["amenity_score"] = sum(
            score * weight for score, weight in zip(amenity_scores, normalized_weights)
        ).clip(0, 100)
    else:
        result["amenity_score"] = 50  # Neutral if no amenity preferences
    
    # Store individual scores
    for score, label in zip(amenity_scores, score_labels):
        result[label] = score
    
    return result


# Main recommendation function
def recommend_properties(
    df,
    user_location,
    user_sub_location,
    user_property_type,
    user_bedrooms,
    user_area_min,
    user_area_max,
    user_age_category,
    user_price_min,
    user_price_max,
    user_parking=None,
    user_furnished=None,
    user_kitchen=None,
    user_electricity=None,
    user_servant_quarters=None,
    top_n=10
):
    """
    Recommend properties based on user preferences
    
    Scoring weights:
    - Location: 35%
    - Property: 35%
    - Amenities: 30%
    """
    print("\nSearching for properties")
    print(f"Location: {user_location} - {user_sub_location if user_sub_location else 'Any'}")
    print(f"Property: {user_property_type} with {int(user_bedrooms)} bedrooms")
    print(f"Area: {int(user_area_min)}-{int(user_area_max)} sqft | Price: {user_price_min:,}-{user_price_max:,}")
    if user_parking:
        print(f"Amenities: Parking={user_parking}, Furnished={'Yes' if user_furnished else 'No'}, Electricity={'Yes' if user_electricity else 'No'}")
    
    # Apply hard filters
    result = df[
        (df["property_type"].astype(str).str.strip().str.lower() == str(user_property_type).strip().lower()) &
        (df["bedrooms"] == user_bedrooms) &
        (df["area"] >= user_area_min) &
        (df["area"] <= user_area_max) &
        (df["price"] >= user_price_min) &
        (df["price"] <= user_price_max)
    ].copy()

    print(f"\nFound {len(result)} matching properties after filters")

    if result.empty:
        print("\nNo properties found matching all criteria")
        return result

    # Calculate all scores
    result = calculate_location_score(result, user_location, user_sub_location, reference_df=df)
    result = calculate_property_score(result, user_property_type, user_bedrooms, user_area_min, user_area_max, user_age_category)
    result = calculate_amenity_score(result, user_parking, user_furnished, user_kitchen, user_electricity, user_servant_quarters)

    selected_location = str(user_location).strip().lower()
    selected_sub_location = str(user_sub_location).strip().lower() if user_sub_location else None

    result_location = result["location"].fillna("").astype(str).str.strip().str.lower()
    result_sub_location = result["sub_location"].fillna("").astype(str).str.strip().str.lower()

    # Assign location levels
    result["location_level"] = 3
    result.loc[result_location == selected_location, "location_level"] = 2
    if selected_sub_location:
        result.loc[result_sub_location == selected_sub_location, "location_level"] = 1

    # Calculate final score (35% + 35% + 30%)
    result["final_score"] = (
        result["location_final_score"] * 0.35 +
        result["property_score"] * 0.35 +
        result["amenity_score"] * 0.30
    ).clip(0, 100)

    # Sort by location level priority
    if selected_sub_location:
        exact_matches = result[result["location_level"] == 1]
        if not exact_matches.empty:
            result = exact_matches.sort_values("final_score", ascending=False).head(top_n)
            print(f"Exact sub-location matches: {len(exact_matches)}")
            return result

    same_location_matches = result[result["location_level"] == 2]
    if not same_location_matches.empty:
        result = same_location_matches.sort_values(["location_final_score", "final_score"], ascending=False).head(top_n)
        print(f"Same location matches: {len(same_location_matches)}")
        return result

    other_locations = result[result["location_level"] == 3]
    if not other_locations.empty:
        result = other_locations.sort_values(["distance_km", "final_score"], ascending=[True, False]).head(top_n)
        print(f"Other locations by distance: {len(other_locations)}")
        return result

    return result.head(top_n)


# Display results
def display_recommendations(recommendations, top_n=10):
    """Pretty print recommendations"""
    if recommendations.empty:
        print("\nNo recommendations found")
        return
    
    print(f"\nTop {min(top_n, len(recommendations))} recommendations\n")
    
    display_cols = [
        'property_id',
        'property_name',
        'sub_location',
        'bedrooms',
        'area',
        'price',
        'parking_category',
        'furnished',
        'location_final_score',
        'property_score',
        'amenity_score',
        'final_score'
    ]
    
    available_cols = [col for col in display_cols if col in recommendations.columns]
    
    # Format the dataframe for display
    df_display = recommendations[available_cols].head(top_n).copy()
    
    # Format numbers
    if 'price' in df_display.columns:
        df_display['price'] = df_display['price'].apply(lambda x: f"PKR {x/1e6:.1f}M")
    if 'area' in df_display.columns:
        df_display['area'] = df_display['area'].apply(lambda x: f"{int(x)} sqft")
    if 'bedrooms' in df_display.columns:
        df_display['bedrooms'] = df_display['bedrooms'].apply(lambda x: f"{int(x)}BR")
    
    # Round scores
    for col in ['location_final_score', 'property_score', 'amenity_score', 'final_score']:
        if col in df_display.columns:
            df_display[col] = df_display[col].apply(lambda x: f"{x:.1f}")
    
    print(df_display.to_string(index=False))
    print()


# Example usage
if __name__ == "__main__":
    # Load data
    dataset_path = Path(__file__).with_name("recommender_dataset.csv")
    df = pd.read_csv(dataset_path)
    
    print("\nReal estate recommendation system")
    print(f"Dataset loaded: {len(df)} properties")
    
    # Example 1: Premium apartment in DHA Defence
    print("\n")
    print("EXAMPLE 1: Luxury Apartment in DHA Defence")
    print()
    
    recommendations1 = recommend_properties(
        df=df,
        user_location='DHA Defence',
        user_sub_location='Phase 8',
        user_property_type='Flat',
        user_bedrooms=3,
        user_area_min=1500,
        user_area_max=2500,
        user_age_category='relatively new',
        user_price_min=80_000_000,
        user_price_max=100_000_000,
        user_parking='Premium Parking',
        user_furnished=1,  # Yes
        user_kitchen=1,
        user_electricity=1,
        user_servant_quarters='1-2',
        top_n=10
    )
    
    display_recommendations(recommendations1)
    
    
    # Example 2: Affordable house in Scheme 33
    print("\n")
    print("EXAMPLE 2: Affordable House in Scheme 33")
    print()
    
    recommendations2 = recommend_properties(
        df=df,
        user_location='Scheme 33',
        user_sub_location=None,
        user_property_type='House',
        user_bedrooms=3,
        user_area_min=1000,
        user_area_max=1500,
        user_age_category='relatively new',
        user_price_min=15_000_000,
        user_price_max=25_000_000,
        user_parking='Good Parking',
        user_furnished=0,  # No
        user_kitchen=1,
        user_electricity=1,
        top_n=10
    )
    
    display_recommendations(recommendations2)
    
    
    # Example 3: Mid-range apartment in Gulshan-e-Iqbal
    print("\n")
    print("EXAMPLE 3: Mid-Range Flat in Gulshan-e-Iqbal")
    print()
    
    recommendations3 = recommend_properties(
        df=df,
        user_location='Gulshan-e-Iqbal Town',
        user_sub_location=None,
        user_property_type='Flat',
        user_bedrooms=2,
        user_area_min=800,
        user_area_max=1200,
        user_age_category='relatively new',
        user_price_min=10_000_000,
        user_price_max=18_000_000,
        user_parking='Basic Parking',
        user_furnished=0,
        user_kitchen=1,
        user_electricity=1,
        top_n=10
    )
    
    display_recommendations(recommendations3)
    
    print("\nRecommendation system ready")
    print("Use recommend_properties() with your own parameters.\n")
