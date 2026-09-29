import streamlit as st

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Karachi Real Estate AI",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

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
        --shadow: 0 18px 45px rgba(25, 48, 48, 0.10);
    }

    html, body, [class*="css"], .stMarkdown, p, li, button {
        font-family: 'Manrope', sans-serif;
    }

    body {
        background: var(--paper);
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
        background: var(--teal);
        color: #fffdfa;
    }

    .block-container {
        max-width: 1240px;
        padding-top: 3rem;
        padding-bottom: 4rem;
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 4.4rem 4.5rem 4rem;
        border-radius: 28px;
        margin-bottom: 2.3rem;
        background: var(--teal-dark);
        color: #fffdfa;
        box-shadow: var(--shadow);
    }

    .hero::after {
        content: '';
        position: absolute;
        width: 360px;
        height: 360px;
        right: -100px;
        top: -150px;
        border: 1px solid rgba(255, 255, 255, 0.20);
        border-radius: 50%;
        box-shadow: 0 0 0 34px rgba(255, 255, 255, 0.04),
                    0 0 0 68px rgba(255, 255, 255, 0.03);
        pointer-events: none;
    }

    .hero-kicker {
        position: relative;
        z-index: 1;
        color: #f3c86d;
        font-family: 'DM Mono', monospace;
        font-size: 0.76rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
    }

    .hero h1 {
        position: relative;
        z-index: 1;
        max-width: 760px;
        font-size: clamp(2.5rem, 6vw, 5.1rem);
        line-height: 0.98;
        letter-spacing: -0.06em;
        margin: 0 0 1.4rem;
        font-weight: 800;
        color: #fffdfa;
    }

    .hero p {
        position: relative;
        z-index: 1;
        max-width: 650px;
        margin: 0;
        color: #cfe1dc;
        font-size: 1.08rem;
        line-height: 1.75;
    }

    .hero-note {
        position: relative;
        z-index: 1;
        display: inline-block;
        margin-top: 2rem;
        padding-top: 0.8rem;
        border-top: 1px solid rgba(255, 255, 255, 0.25);
        color: #f5dfab;
        font-size: 0.83rem;
    }

    .section-title {
        color: #f4f1e8;
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.05em;
        line-height: 1.1;
        margin: 2.8rem 0 0.45rem;
    }

    .section-description {
        max-width: 650px;
        color: #aebfc0;
        font-size: 1rem;
        line-height: 1.7;
        margin-bottom: 1.6rem;
    }

    .card {
        height: 400px;
        box-sizing: border-box;
        padding: 1.8rem 1.75rem 1.65rem;
        border: 1px solid var(--line);
        border-radius: 18px;
        background: var(--card);
        box-shadow: 0 8px 24px rgba(25, 48, 48, 0.04);
        transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
    }

    .card:hover {
        border-color: rgba(13, 107, 105, 0.45);
        box-shadow: var(--shadow);
        transform: translateY(-4px);
    }

    .card h3 {
        color: var(--ink);
        font-size: 1.22rem;
        letter-spacing: -0.03em;
        margin: 0 0 0.8rem;
    }

    .card p {
        color: var(--muted);
        font-size: 0.9rem;
        line-height: 1.7;
    }

    .card b { color: var(--teal-dark); }

    .stButton > button {
        min-height: 2.75rem;
        border: 1px solid var(--teal);
        border-radius: 10px;
        background: var(--teal);
        color: white;
        font-weight: 700;
        transition: background 160ms ease, transform 160ms ease;
    }

    .stButton > button:hover {
        border-color: var(--teal-dark);
        background: var(--teal-dark);
        color: white;
        transform: translateY(-1px);
    }

    .pipeline {
        height: 175px;
        box-sizing: border-box;
        padding: 1.3rem 1.25rem;
        border: 1px solid var(--line);
        border-radius: 15px;
        background: rgba(255, 253, 250, 0.74);
    }

    .pipeline-number {
        color: var(--coral);
        font-family: 'DM Mono', monospace;
        font-size: 0.88rem;
        font-weight: 700;
    }

    .pipeline h4 { color: var(--ink); margin: 1rem 0 0.35rem; }
    .pipeline p { color: var(--muted); font-size: 0.86rem; line-height: 1.55; }

    .footer {
        text-align: center;
        padding-top: 2rem;
        margin-top: 3rem;
        border-top: 1px solid var(--line);
        color: var(--muted);
        font-family: 'DM Mono', monospace;
        font-size: 0.72rem;
        letter-spacing: 0.04em;
    }

    [data-testid="stMarkdownContainer"] ul {
        color: var(--muted);
    }

    @media (max-width: 640px) {
        .block-container { padding-top: 1.25rem; }
        .hero { padding: 2.5rem 1.5rem 2.3rem; border-radius: 20px; }
        .hero h1 { font-size: 2.7rem; }
        .section-title { font-size: 1.85rem; }
        .card { height: auto; min-height: 0; }
        .pipeline { height: auto; min-height: 0; }
    }
    </style>
    """
)


# ============================================================
# HERO SECTION
# ============================================================

st.html(
    """
    <div class="hero">

        <div class="hero-kicker">Karachi property intelligence · 2026</div>

        <h1>Make a smarter move in Karachi real estate.</h1>

        <p>
            Explore the market, estimate a fair price, and find properties
            that fit the way you actually want to live.
        </p>

        <div class="hero-note">One place for market context, machine learning, and better shortlists.</div>

    </div>
    """
)


# ============================================================
# INTRODUCTION
# ============================================================

st.markdown(
    '<div class="section-title">Explore Karachi Real Estate</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="section-description">
        Turn real estate data into useful insights. Explore market patterns,
        estimate property prices using machine learning, and find properties
        that match your requirements.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# THREE MAIN MODULES
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.html(
        """
        <div class="card">

            <h3>📊 Real Estate Analytics</h3>

            <p>
                Explore Karachi's real estate market through interactive
                charts, maps, property distributions, price analysis,
                and location-based insights.
            </p>

            <p>
                <b>Explore:</b><br>
                • Property prices<br>
                • Price per square foot<br>
                • Districts and locations<br>
                • Property types<br>
                • Area and bedroom patterns<br>
                • Interactive maps
            </p>

        </div>
        """
    )

    st.write("")

    if st.button(
        "Explore Analytics →",
        key="analytics_button",
        use_container_width=True
    ):
        st.switch_page("pages/2_Analytical_App.py")


with col2:

    st.html(
        """
        <div class="card">

            <h3>💰 Price Prediction</h3>

            <p>
                Estimate the expected price of a property using a
                machine learning model trained on Karachi real estate
                data.
            </p>

            <p>
                <b>Provide details such as:</b><br>
                • Property type<br>
                • Location<br>
                • Area<br>
                • Bedrooms and bathrooms<br>
                • Floor information<br>
                • Parking and other features
            </p>

        </div>
        """
    )

    st.write("")

    if st.button(
        "Predict Property Price →",
        key="prediction_button",
        use_container_width=True
    ):
        st.switch_page("pages/1_Price Predictor.py")


with col3:

    st.html(
        """
        <div class="card">

            <h3>🏠 Property Recommender</h3>

            <p>
                Discover properties that match your requirements by
                specifying your budget, preferred location, property
                type, size, and other features.
            </p>

            <p>
                <b>Customize your search:</b><br>
                • Budget<br>
                • Location<br>
                • Property type<br>
                • Area<br>
                • Bedrooms<br>
                • Amenities and features
            </p>

        </div>
        """
    )

    st.write("")

    if st.button(
        "Find Properties →",
        key="recommender_button",
        use_container_width=True
    ):
        st.switch_page("pages/3_Recommender_App.py")


# ============================================================
# DATA PIPELINE
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">From Real Estate Data to Insights</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="section-description">
        The platform processes real estate listing data through a series
        of data preparation and machine learning steps.
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.html(
        """
        <div class="pipeline">
            <div class="pipeline-number">01</div>
            <h4>Raw Data</h4>
            <p>Real estate listings collected from Karachi.</p>
        </div>
        """
    )

with col2:
    st.html(
        """
        <div class="pipeline">
            <div class="pipeline-number">02</div>
            <h4>Data Cleaning</h4>
            <p>Missing values, duplicates, and inconsistencies are handled.</p>
        </div>
        """
    )

with col3:
    st.html(
        """
        <div class="pipeline">
            <div class="pipeline-number">03</div>
            <h4>Feature Engineering</h4>
            <p>Relevant features are created and prepared for analysis.</p>
        </div>
        """
    )

with col4:
    st.html(
        """
        <div class="pipeline">
            <div class="pipeline-number">04</div>
            <h4>AI & Analytics</h4>
            <p>Machine learning and analytical methods generate insights.</p>
        </div>
        """
    )


# ============================================================
# PROJECT OVERVIEW
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">About This Platform</div>',
    unsafe_allow_html=True
)

about_col1, about_col2 = st.columns([1.5, 1])

with about_col1:

    st.write(
        """
        **Karachi Real Estate AI** is a machine learning and data
        analytics project focused on the Karachi property market.

        The platform combines data processing, exploratory data analysis,
        feature engineering, machine learning, and recommendation
        techniques into a single application.

        The goal is to make a large collection of real estate listings
        easier to understand and use through an interactive interface.
        """
    )

with about_col2:

    st.info(
        """
        **Platform Modules**

        📊 Market Analytics

        💰 Property Price Prediction

        🏠 Property Recommendation

        🗺️ Location-based Insights

        🤖 Machine Learning
        """
    )


# ============================================================
# NAVIGATION HELP
# ============================================================

st.markdown("---")

st.markdown(
    """
    ### 🚀 Get Started

    Use the **sidebar** to navigate between the different modules,
    or select one of the options above to start exploring Karachi's
    real estate market.
    """
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Karachi Real Estate AI
        <br>
        Data Analytics • Machine Learning • Property Recommendation
    </div>
    """,
    unsafe_allow_html=True
)