<div align="center">

<!-- 🖼️ TOP BANNER: save your banner as docs/images/banner.png (recommended size: 1280 x 320 px) -->
<img src="app/assets/Karachi-image.png" alt="Karachi Real Estate Intelligence Platform banner" width="100%">

# 🏙️ Karachi Real Estate Intelligence Platform

**Predict prices. Explore the market. Find the right property.**

An end-to-end machine-learning and analytics web app built on 20,000+ Karachi property listings.

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-Pipeline-F7931E?logo=scikit-learn&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Charts-3F4F75?logo=plotly&logoColor=white)
![PyDeck](https://img.shields.io/badge/PyDeck-3D%20Maps-0A66C2)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebooks-F37626?logo=jupyter&logoColor=white)

[Demo Video](#-demo-video) · [Screenshots](#-application-preview) · [Features](#-features) · [How It Works](#-how-it-works) · [Quick Start](#-quick-start) · [Roadmap](#-roadmap)

</div>

---

## 🎬 Demo Video

<!--
🎥 DEMO VIDEO: choose ONE option.

OPTION A (recommended): clickable thumbnail that opens your YouTube / Drive video.
  1. Save a thumbnail as docs/images/video-thumbnail.png
  2. Replace YOUR_VIDEO_LINK below with your video URL.

OPTION B: upload the video directly to GitHub.
  1. Edit this README on github.com and drag your .mp4 file into the editor.
  2. GitHub generates a link; paste it on its own line here and it will play inline.
     (Delete the Option A block below if you use this.)
-->

<div align="center">

[![Watch the demo video](docs/images/video-thumbnail.png)](YOUR_VIDEO_LINK)

▶️ **Click the image above to watch the full demo**

🔗 **Live app:** _add your deployed Streamlit link here_

</div>

---

## 📸 Application Preview

<!-- 🖼️ Save each screenshot in docs/images/ using the exact file names below. -->

<div align="center">

### 🏠 Landing Page
<img src="docs/images/landing-page.png" alt="Landing page" width="90%">

### 💰 Price Predictor
<img src="docs/images/price-predictor.png" alt="Price Predictor page" width="90%">

### 📊 Market Analytics
<img src="docs/images/market-analytics.png" alt="Market Analytics page" width="90%">

### 🗺️ Interactive and 3D Maps
<img src="docs/images/maps-3d.png" alt="Interactive and 3D property maps" width="90%">

### 🎯 Property Recommender
<img src="docs/images/recommender.png" alt="Property Recommender page" width="90%">

</div>

---

## 📖 About

Property prices in Karachi vary hugely by district, society, and sub-location, and listing data is messy and inconsistent. This project turns raw **Zameen.com** listings into a clean, structured dataset and builds three tools on top of it:

| | Module | What it does |
|---|---|---|
| 💰 | **Price Predictor** | Estimates a property's market price from its details |
| 📊 | **Market Analytics** | Compares districts, locations, and sub-locations with interactive charts and maps |
| 🎯 | **Property Recommender** | Filters and ranks listings against your preferences |

---

## ✨ Features

- **Full data-science lifecycle**: scraping → cleaning → EDA → modeling → deployment
- **Large real-world dataset**: 20,000+ flat and house listings, cleaned separately and then merged
- **Karachi-specific location standardization**: inconsistent area names mapped into parent locations and sub-locations
- **Price prediction** through a reusable scikit-learn pipeline, with an estimated price range
- **Interactive analytics** with Plotly charts and PyDeck 2D/3D maps
- **Explainable recommender** using transparent weighted scoring
- **Flexible units**: supports square feet and square yards

---

## 🧭 How It Works

```mermaid
flowchart TD
    A[Zameen.com listings] --> B[Scraper notebooks]
    B --> C[Raw CSV files]
    C --> D[Cleaning, merging, feature engineering]
    D --> E[Cleaned datasets]
    E --> F[Price prediction model]
    E --> G[Analytics and recommender data]
    F --> H[model/pipeline.pkl]
    G --> I[Streamlit app]
    H --> I
```

### 1. Data pipeline

| Step | Details | Notebooks |
|---|---|---|
| **Scrape** | Price, area, bedrooms, bathrooms, kitchen, location, address, completion year, parking, furnishing, electricity backup, servant quarters | `scraper/flats_scraper.ipynb`, `scraper/house_scraper.ipynb` |
| **Clean** | Flats and houses cleaned separately: prices, areas, rooms, years | `1_data_cleaning_flats`, `2_data_cleaning_house` |
| **Merge** | Combined into one dataset with a `property_type` column | `3_merge_flats_and_house` |
| **Standardize locations** | Spelling, road, society, and project-name variants mapped to consistent locations | location notebooks |
| **Handle missing values** | Remove, default-fill, group as `Unknown`, set to `NaN`, or estimate from related records | `8_`, `9_`, `handle_missing_values-3` |
| **Engineer features** | Derived variables for analysis and modeling | feature-engineering notebooks |
| **EDA and selection** | Univariate, multivariate, and profiling analysis; multi-method feature selection | `5_` to `7_`, `11-Feature_Selection` |

<details>
<summary><b>🧮 Engineered features</b></summary>

<br>

| Feature | Description |
|---|---|
| `price_per_sqft` | `price / area` for fair comparison across sizes |
| `property_age` | `current_year - completion_year` |
| `age_category` | Under Construction (< 0), New (0), Relatively New (1–5), Moderately Old (6–10), Old (> 10) |
| `area_per_bedroom` | `area / bedrooms` |
| `location_score` | Higher for premium locations, lower for developing ones |
| `sub_location_score` | Based on price-per-sqft statistics, with group-size handling so tiny groups don't dominate |
| `luxury_score`, `parking_score`, `servant_quarter_score` | Amenity-based scores |
| `sub_location_type`, `district` | Location categories |

</details>

<details>
<summary><b>🔍 Feature selection methods</b></summary>

<br>

To find stable predictors rather than trusting a single technique, the project compares: correlation analysis, Random Forest importance, Gradient Boosting importance, permutation importance, Lasso coefficients, Recursive Feature Elimination, and linear-model coefficients.

</details>

### 2. Price prediction model

Developed in `notebooks/11-Feature_Selection.ipynb` and `notebooks/12-Baseline_model.ipynb`.

1. Target `price` is transformed with `np.log1p` (prices are right-skewed).
2. Numerical features are scaled and categorical features are encoded.
3. A regression model is trained inside a scikit-learn `Pipeline`.
4. The model is evaluated with a train/test split and cross-validation.
5. The pipeline is saved as `model/pipeline.pkl`.

In the app, predictions are converted back with `np.expm1`, and the page displays an estimated price with a price range.

### 3. Recommendation engine

`src/recommender.py` is a **deterministic scoring system** (not a trained model), which keeps results easy to explain.

```text
Final score = 35% Location  +  35% Property  +  30% Amenities
```

| Score | Components |
|---|---|
| **Hard filters** | Property type, bedrooms, area range, price range |
| **Location (35%)** | Exact sub-location match → same parent location → nearby areas via Haversine distance |
| **Property (35%)** | Type 35% · Bedrooms 30% · Area 20% · Age 15% |
| **Amenities (30%)** | Parking 40% · Furnished 25% · Kitchen 15% · Electricity backup 12% · Servant quarters 8% |

If a user leaves some preferences blank, the active weights are rebalanced automatically.

---

## 🖥️ App Modules

<details open>
<summary><b>💰 Price Predictor</b> — <code>app/pages/1_Price Predictor.py</code></summary>

<br>

- **Inputs:** property type, district, location, sub-location, area and unit, bedrooms, bathrooms, kitchen, total floors, floor category, age category, furnished status, parking, servant quarters, electricity backup
- **Unit conversion:** `1 sq yd = 9 sq ft`
- **Smart handling:** floor category is set to `Not Applicable` for houses, and invalid location combinations (e.g. `Gadap` under Karachi East, `Jamshed Town` under Korangi) are hidden
- **Output:** estimated price and price range

</details>

<details>
<summary><b>📊 Analytical App</b> — <code>app/pages/2_Analytical_App.py</code></summary>

<br>

- Analyze by **district**, **location**, or **sub-location**
- Metrics: median price, median price per sqft, listing count, median area
- Interactive and 3D maps (PyDeck), district comparisons, price and area distributions, and property-type comparisons (Plotly)

</details>

<details>
<summary><b>🎯 Recommender App</b> — <code>app/pages/3_Recommender_App.py</code></summary>

<br>

- **Preferences:** location and sub-location, property type, bedrooms, area range, price range, age, parking, furnishing, kitchen, electricity backup, servant quarters, number of results
- **Output:** top-ranked listings with prices, sizes, features, and recommendation scores

</details>

---

## 🚀 Quick Start

**Prerequisites:** Python 3.9+ and `pip`

```bash
# 1. Clone the repository
git clone <your-repository-url>
cd <your-repository-folder>

# 2. Create a virtual environment
python -m venv .venv

# 3. Activate it
.venv\Scripts\Activate.ps1        # Windows PowerShell
# source .venv/bin/activate       # macOS / Linux

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app
streamlit run app/Streamlit-app.py
```

The app opens in your browser with the landing page and navigation to all three modules.

> **Re-running the scrapers?** The scraper notebooks also need `requests`, `beautifulsoup4`, and Jupyter, which are not in `requirements.txt`. Install them separately.

---

## 🛠️ Tech Stack

| Area | Tools |
|---|---|
| **App** | Streamlit |
| **Data** | pandas, NumPy |
| **Machine learning** | scikit-learn, category_encoders |
| **Visualization** | Plotly, PyDeck, Matplotlib, Seaborn |
| **Scraping** | requests, BeautifulSoup |
| **Workflow** | Jupyter notebooks |

---

## 📁 Project Structure

```text
.
├── app/
│   ├── Streamlit-app.py            # Landing page
│   ├── pages/
│   │   ├── 1_Price Predictor.py
│   │   ├── 2_Analytical_App.py
│   │   └── 3_Recommender_App.py
│   └── assets/                     # Images and UI assets
├── data/
│   ├── raw/                        # Scraped data (flats, houses)
│   ├── interim/                    # Intermediate cleaning outputs
│   ├── cleaned/                    # Final CSVs for app modules
│   └── processed/                  # Pickle files loaded by Streamlit
├── model/
│   └── pipeline.pkl                # Trained price prediction pipeline
├── src/
│   └── recommender.py              # Filtering, scoring, ranking, distance
├── notebooks/                      # Cleaning, EDA, feature engineering, modeling
├── scraper/                        # Flat and house scraping notebooks
├── docs/
│   └── images/                     # README banner, screenshots, video thumbnail
└── requirements.txt
```

---

## ⚠️ Limitations

- **Asking prices, not sale prices:** the data comes from listings, so it may not reflect final transaction values.
- **Market drift:** prices change over time, so the model needs periodic retraining.
- **Manual location mappings:** these may need updates as new areas appear.
- **Fixed error bands:** the price range is manually configured rather than calculated per location.
- **Schema dependency:** the model requires the same columns and category values used during training.

> 💡 Predictions are estimates for guidance only and are not a formal property valuation.

---

## 🛣️ Roadmap

- [ ] Automated tests for data cleaning and feature engineering
- [ ] Data validation before loading datasets into Streamlit
- [ ] Model versioning and a documented training/export script
- [ ] Periodic retraining on newly scraped listings
- [ ] Location-specific error estimates
- [ ] Model explainability with SHAP or permutation importance
- [ ] Database backend instead of CSV and pickle files
- [ ] User accounts and saved searches
- [ ] Scraper dependencies added to `requirements.txt`

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to open an issue or submit a pull request.

## 📜 Data Notice

Listing data was collected from Zameen.com for educational and research purposes. Please review the website's terms of use before scraping or redistributing data.

## 📄 License

Add your license here (e.g. MIT).

## 👤 Author

**Your Name** · [GitHub](https://github.com/your-username) · [LinkedIn](https://linkedin.com/in/your-profile)

---

<div align="center">

⭐ If you found this project useful, consider giving it a star!

</div>
