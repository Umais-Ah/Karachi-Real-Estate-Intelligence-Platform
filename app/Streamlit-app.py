import streamlit as st

# Set the page title and layout.
st.set_page_config(
    page_title="Karachi Real Estate AI",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Keep the app sections together so the links are easy to update.
MODULES = [
    {
        "icon": "📊",
        "title": "Market Analytics",
        "text": "See how prices, sizes and demand differ across Karachi "
                "with interactive charts, maps and area comparisons.",
        "page": "pages/01_Analytics.py",
        "cta": "Open analytics",
    },
    {
        "icon": "💰",
        "title": "Price Prediction",
        "text": "Enter a property's location, size and features to get an "
                "estimated price from a model trained on Karachi listings.",
        "page": "pages/02_Price_Prediction.py",
        "cta": "Estimate a price",
    },
    {
        "icon": "🏠",
        "title": "Property Recommender",
        "text": "Set your budget, area, property type and must-have features "
                "to get a ranked shortlist of matching properties.",
        "page": "pages/03_Property_Recommender.py",
        "cta": "Find properties",
    },
]

AUDIENCES = [
    ("Buyers", "Check whether a listing is fairly priced before you make an offer."),
    ("Sellers", "Get a data-backed price range before you list."),
    ("Researchers", "Compare neighbourhoods and track market patterns."),
]

PIPELINE = [
    ("Raw data", "Property listings collected from Karachi real estate sources."),
    ("Data cleaning", "Duplicates, missing values and outliers removed."),
    ("Feature engineering", "Location, size and amenity signals turned into model inputs."),
    ("ML & analytics", "Models power the predictions, charts and recommendations."),
]

# Add the styles used by the landing page.
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Source+Sans+3:wght@400;500;600&display=swap');

    :root {
        --ink: #0B2A33;
        --muted: #4F6870;
        --sea: #14747A;
        --sea-deep: #0B4F55;
        --amber: #E2A32B;
        --surface: #F2F6F7;
        --line: #D3DFE2;
    }

    html, body, [class*="css"], .stMarkdown, p, li {
        font-family: 'Source Sans 3', sans-serif;
    }
    .block-container { padding-top: 2.5rem; max-width: 1150px; }
    #MainMenu, footer { visibility: hidden; }

    h1, h2, h3, .hero-title {
        font-family: 'Bricolage Grotesque', sans-serif !important;
        color: var(--ink);
        letter-spacing: -0.02em;
    }

    /* Hero */
    .hero {
        background: linear-gradient(135deg, var(--sea-deep) 0%, var(--sea) 100%);
        border-radius: 20px;
        padding: 3.2rem 3rem 2.8rem;
        color: #fff;
        border-bottom: 6px solid var(--amber);
    }
    .hero-title {
        color: #fff !important;
        font-size: clamp(2.2rem, 5vw, 3.6rem);
        font-weight: 800;
        line-height: 1.05;
        margin: 0 0 1rem 0;
    }
    .hero-sub {
        font-size: 1.2rem;
        line-height: 1.55;
        max-width: 42rem;
        color: #DCEEF0;
        margin: 0;
    }

    /* Section headings */
    .section-title {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-size: 1.7rem;
        font-weight: 700;
        color: var(--ink);
        margin: 2.6rem 0 0.4rem;
    }
    .section-lead {
        color: var(--muted);
        margin: 0 0 1.2rem;
        max-width: 40rem;
    }

    /* Module cards (Streamlit bordered containers) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: var(--line) !important;
        border-radius: 14px !important;
        background: #fff;
    }
    .card-icon { font-size: 1.8rem; margin-bottom: .2rem; }
    .card-title {
        font-family: 'Bricolage Grotesque', sans-serif;
        font-size: 1.3rem; font-weight: 700; color: var(--ink);
        margin: 0 0 .4rem;
    }
    .card-text { color: var(--muted); min-height: 5.2rem; margin: 0 0 .6rem; }

    /* Audience */
    .aud {
        border-left: 4px solid var(--amber);
        padding: .2rem 0 .2rem 1rem;
    }
    .aud b { color: var(--ink); font-size: 1.05rem; }
    .aud span { color: var(--muted); display: block; }

    /* Pipeline: a real sequence, so steps are numbered */
    .pipe {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 1.1rem 1.2rem;
        height: 100%;
    }
    .pipe .n {
        display: inline-flex; align-items: center; justify-content: center;
        width: 1.9rem; height: 1.9rem; border-radius: 50%;
        background: var(--sea); color: #fff; font-weight: 700;
        font-family: 'Bricolage Grotesque', sans-serif;
        margin-bottom: .5rem;
    }
    .pipe b { display: block; color: var(--ink); margin-bottom: .2rem; }
    .pipe span { color: var(--muted); font-size: .95rem; }

    .note {
        color: var(--muted); font-size: .9rem;
        border-top: 1px solid var(--line);
        margin-top: 2.5rem; padding-top: 1rem;
    }

    @media (max-width: 640px) {
        .hero { padding: 2rem 1.4rem; }
        .card-text { min-height: 0; }
    }
    a:focus-visible, button:focus-visible {
        outline: 3px solid var(--amber); outline-offset: 2px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Show the introduction and the two main actions.
st.markdown(
    """
    <div class="hero">
        <h1 class="hero-title">Know what a Karachi property is really worth.</h1>
        <p class="hero-sub">
            Explore market trends, estimate prices with machine learning,
            and get property recommendations that fit your budget and preferences.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")
cta1, cta2, _ = st.columns([1, 1, 2])
with cta1:
    st.page_link(MODULES[1]["page"], label="Estimate a price", icon="💰",
                 use_container_width=True)
with cta2:
    st.page_link(MODULES[2]["page"], label="Find properties", icon="🏠",
                 use_container_width=True)

# Add a card for each tool.
st.markdown(
    '<div class="section-title">Explore the platform</div>'
    '<p class="section-lead">Three tools built on the same Karachi property data.</p>',
    unsafe_allow_html=True,
)

for col, m in zip(st.columns(3, gap="medium"), MODULES):
    with col:
        with st.container(border=True):
            st.markdown(
                f"""
                <div class="card-icon">{m['icon']}</div>
                <div class="card-title">{m['title']}</div>
                <p class="card-text">{m['text']}</p>
                """,
                unsafe_allow_html=True,
            )
            st.page_link(m["page"], label=m["cta"], use_container_width=True)

# Explain who the platform is useful for.
st.markdown(
    '<div class="section-title">Who it\'s for</div>',
    unsafe_allow_html=True,
)
for col, (who, what) in zip(st.columns(3, gap="medium"), AUDIENCES):
    with col:
        st.markdown(
            f'<div class="aud"><b>{who}</b><span>{what}</span></div>',
            unsafe_allow_html=True,
        )

# Summarize how the data becomes the final insights.
st.markdown(
    '<div class="section-title">How it works</div>'
    '<p class="section-lead">From raw listings to the insights you see here.</p>',
    unsafe_allow_html=True,
)
for col, (i, (name, desc)) in zip(st.columns(4, gap="small"), enumerate(PIPELINE, 1)):
    with col:
        st.markdown(
            f'<div class="pipe"><div class="n">{i}</div><b>{name}</b><span>{desc}</span></div>',
            unsafe_allow_html=True,
        )

# Add a note about how the estimates should be interpreted.
st.markdown(
    '<div class="note">Estimates and recommendations are based on historical '
    "listing data and are meant as guidance, not a formal valuation.</div>",
    unsafe_allow_html=True,
)
st.caption("Karachi Real Estate AI • Data Analytics • Machine Learning • Recommendations")