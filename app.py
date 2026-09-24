import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="HeritageLens | CSMVS",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CULTURAL COLOUR PALETTE
# ============================================================

TERRACOTTA = "#A44A2A"
GOLD = "#C49A45"
PEACOCK = "#174A43"
MAROON = "#641F2A"
IVORY = "#F5E9D0"
BROWN = "#3A2418"
CREAM = "#FFF8EA"
WHITE = "#FFFFFF"
MUTED = "#806B58"

CHART_COLORS = [
    TERRACOTTA,
    GOLD,
    PEACOCK,
    MAROON,
    "#D48A5C",
    "#8B6B35",
    "#376C63",
    "#91515B"
]

# ============================================================
# CUSTOM CSS — INDIAN HERITAGE / MUSEUM THEME
# ============================================================

st.markdown(
    f"""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

    /* ---------------- GLOBAL ---------------- */

    html, body, [class*="css"] {{
        font-family: 'DM Sans', sans-serif;
    }}

    .stApp {{
        background:
            radial-gradient(circle at 10% 10%, rgba(196,154,69,0.10), transparent 22%),
            radial-gradient(circle at 90% 20%, rgba(164,74,42,0.08), transparent 25%),
            {IVORY};
        color: {BROWN};
    }}

    /* Subtle heritage pattern */

    .stApp::before {{
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        opacity: 0.035;
        background-image:
            radial-gradient(circle at 25% 25%, {BROWN} 1px, transparent 1px),
            radial-gradient(circle at 75% 75%, {GOLD} 1px, transparent 1px);
        background-size: 28px 28px;
        z-index: 0;
    }}

    /* ---------------- SIDEBAR ---------------- */

    section[data-testid="stSidebar"] {{
        background:
            linear-gradient(
                180deg,
                {PEACOCK} 0%,
                #123D37 55%,
                {BROWN} 100%
            );
        border-right: 4px solid {GOLD};
    }}

    section[data-testid="stSidebar"] * {{
        color: {IVORY} !important;
    }}

    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] .stSelectbox label {{
        font-weight: 600;
    }}

    /* ---------------- MAIN CONTAINER ---------------- */

    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }}

    /* ---------------- HERO ---------------- */

    .heritage-hero {{
        background:
            linear-gradient(
                135deg,
                {PEACOCK} 0%,
                #205A51 45%,
                {MAROON} 100%
            );
        border: 2px solid {GOLD};
        border-radius: 24px;
        padding: 38px 45px;
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 12px 35px rgba(58,36,24,0.20);
    }}

    .heritage-hero::before {{
        content: "✦  ❈  ✦  ❈  ✦";
        position: absolute;
        top: 12px;
        right: 28px;
        color: {GOLD};
        font-size: 22px;
        letter-spacing: 8px;
        opacity: 0.75;
    }}

    .heritage-hero::after {{
        content: "❈";
        position: absolute;
        right: 45px;
        bottom: 15px;
        font-size: 110px;
        color: rgba(196,154,69,0.12);
    }}

    .hero-kicker {{
        color: {GOLD};
        font-size: 15px;
        font-weight: 700;
        letter-spacing: 4px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }}

    .hero-title {{
        font-family: 'Cormorant Garamond', serif;
        color: {IVORY};
        font-size: 54px;
        font-weight: 700;
        line-height: 1;
        margin: 0;
    }}

    .hero-subtitle {{
        color: #E8DCC5;
        font-size: 17px;
        margin-top: 13px;
        max-width: 760px;
        line-height: 1.6;
    }}

    .gold-line {{
        width: 90px;
        height: 3px;
        background: {GOLD};
        margin: 18px 0;
        border-radius: 5px;
    }}

    /* ---------------- SECTION HEADERS ---------------- */

    .section-title {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 32px;
        font-weight: 700;
        color: {PEACOCK};
        margin-top: 30px;
        margin-bottom: 3px;
    }}

    .section-subtitle {{
        color: {MUTED};
        font-size: 14px;
        margin-bottom: 18px;
    }}

    .ornament {{
        color: {GOLD};
        font-size: 20px;
        letter-spacing: 5px;
    }}

    /* ---------------- KPI CARDS ---------------- */

    .kpi-card {{
        background: rgba(255,248,234,0.92);
        border: 1px solid rgba(196,154,69,0.55);
        border-top: 5px solid {GOLD};
        border-radius: 17px;
        padding: 22px;
        min-height: 145px;
        box-shadow: 0 8px 22px rgba(58,36,24,0.10);
        position: relative;
        overflow: hidden;
    }}

    .kpi-card::after {{
        content: "❈";
        position: absolute;
        right: 12px;
        bottom: -10px;
        font-size: 70px;
        color: rgba(196,154,69,0.10);
    }}

    .kpi-icon {{
        font-size: 25px;
    }}

    .kpi-label {{
        color: {MUTED};
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-top: 5px;
    }}

    .kpi-value {{
        font-family: 'Cormorant Garamond', serif;
        color: {PEACOCK};
        font-size: 36px;
        font-weight: 700;
        margin-top: 3px;
    }}

    /* ---------------- CHART CARDS ---------------- */

    .chart-card {{
        background: rgba(255,248,234,0.90);
        border: 1px solid rgba(58,36,24,0.10);
        border-left: 5px solid {TERRACOTTA};
        border-radius: 17px;
        padding: 10px 15px 5px 15px;
        box-shadow: 0 7px 20px rgba(58,36,24,0.08);
    }}

    /* ---------------- INFO BOX ---------------- */

    .heritage-note {{
        background: rgba(196,154,69,0.13);
        border-left: 5px solid {GOLD};
        padding: 16px 20px;
        border-radius: 10px;
        color: {BROWN};
        margin: 15px 0;
    }}

    /* ---------------- DATA TABLE ---------------- */

    .data-title {{
        font-family: 'Cormorant Garamond', serif;
        color: {MAROON};
        font-size: 28px;
        font-weight: 700;
    }}

    /* ---------------- BUTTONS ---------------- */

    .stButton > button {{
        background: {TERRACOTTA};
        color: white;
        border: 1px solid {GOLD};
        border-radius: 10px;
        font-weight: 600;
    }}

    .stButton > button:hover {{
        background: {MAROON};
        color: white;
    }}

    /* ---------------- SELECT BOX ---------------- */

    div[data-baseweb="select"] > div {{
        background: {CREAM};
        border-color: rgba(196,154,69,0.6);
    }}

    /* ---------------- FOOTER ---------------- */

    .footer {{
        margin-top: 50px;
        padding: 25px;
        text-align: center;
        color: {MUTED};
        border-top: 1px solid rgba(196,154,69,0.5);
        font-size: 13px;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# LOAD DATA
# ============================================================

FILE_PATH = "/content/CSMVS_Heritage_Survey_Responses.csv"

try:
    df = pd.read_csv(FILE_PATH)
except FileNotFoundError:
    st.error("⚠️ CSV file not found.")
    st.info(
        "Upload `CSMVS_Heritage_Survey_Responses.csv` to your Colab session "
        "and restart the app."
    )
    st.stop()

# Clean column names
df.columns = (
    df.columns
    .astype(str)
    .str.replace("\n", " ", regex=False)
    .str.strip()
)

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def find_col(keywords):
    """
    Find a dataframe column using one or multiple keywords.
    Makes the dashboard resistant to small differences in CSV headers.
    """
    if isinstance(keywords, str):
        keywords = [keywords]

    for col in df.columns:
        col_lower = col.lower()

        if all(k.lower() in col_lower for k in keywords):
            return col

    # Second attempt: any keyword
    for col in df.columns:
        col_lower = col.lower()

        if any(k.lower() in col_lower for k in keywords):
            return col

    return None


def clean_series(column):
    if column is None:
        return pd.Series(dtype="object")

    return (
        df[column]
        .fillna("Not specified")
        .astype(str)
        .str.strip()
        .replace("", "Not specified")
    )


def get_counts(column):
    if column is None:
        return pd.DataFrame(columns=["Answer", "Count"])

    s = clean_series(column)

    result = (
        s.value_counts()
        .reset_index()
    )

    result.columns = ["Answer", "Count"]

    return result


def multi_value_counts(column):
    """
    Used for questions where respondents can select multiple options.
    """

    if column is None:
        return pd.DataFrame(columns=["Answer", "Count"])

    values = clean_series(column)

    expanded = []

    for value in values:

        parts = re.split(r",|;|\n|\|", value)

        for part in parts:
            part = part.strip()

            if part:
                expanded.append(part)

    if not expanded:
        return pd.DataFrame(columns=["Answer", "Count"])

    result = (
        pd.Series(expanded)
        .value_counts()
        .head(12)
        .reset_index()
    )

    result.columns = ["Answer", "Count"]

    return result


def cultural_bar(data, title, horizontal=False):

    if data.empty:
        st.info("No data available for this section.")
        return

    if horizontal:

        fig = px.bar(
            data,
            x="Count",
            y="Answer",
            orientation="h",
            text="Count",
            color="Answer",
            color_discrete_sequence=CHART_COLORS
        )

    else:

        fig = px.bar(
            data,
            x="Answer",
            y="Count",
            text="Count",
            color="Answer",
            color_discrete_sequence=CHART_COLORS
        )

    fig.update_traces(
        textposition="outside",
        marker_line_width=0
    )

    fig.update_layout(
        title=title,
        title_font=dict(
            family="Cormorant Garamond",
            size=22,
            color=PEACOCK
        ),
        font=dict(
            family="DM Sans",
            color=BROWN
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(l=20, r=20, t=60, b=40),
        xaxis=dict(
            showgrid=False,
            title=""
        ),
        yaxis=dict(
            showgrid=False,
            title=""
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


def cultural_pie(data, title):

    if data.empty:
        st.info("No data available.")
        return

    fig = px.pie(
        data,
        names="Answer",
        values="Count",
        hole=0.48,
        color_discrete_sequence=CHART_COLORS
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent",
        hovertemplate="<b>%{label}</b><br>%{value} visitors<extra></extra>"
    )

    fig.update_layout(
        title=title,
        title_font=dict(
            family="Cormorant Garamond",
            size=22,
            color=PEACOCK
        ),
        font=dict(
            family="DM Sans",
            color=BROWN
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            y=-0.15
        ),
        margin=dict(l=20, r=20, t=60, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


# ============================================================
# IDENTIFY DATASET COLUMNS
# ============================================================

AGE = find_col(["Age Group"])
GENDER = find_col(["Gender"])
LOCATION = find_col(["Where are you from"])
AWARENESS = find_col(["How did you learn about this museum"])
REASON = find_col(["main reason for visiting"])
INTEREST = find_col(["aspects of the museum interest"])
CROWD = find_col(["excessive crowding"])
OCCUPATION = find_col(["Occupation"])
TOURIST = find_col(["Indian or International Tourist"])
FIRST = find_col(["first visit"])
COMPANY = find_col(["visiting with"])
GROUP_SIZE = find_col(["how many people are in your group"])
ATTRACTIONS = find_col(["nearby attractions"])
ISSUES = find_col(["issues did you face"])
APP = find_col(["tourist-planning app"])
EXPERIENCE = find_col(["preferred visit experience"])

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        f"""
        <div style="text-align:center;padding:12px 5px 22px 5px;">
            <div style="font-size:42px;">🏛️</div>
            <div style="
                font-family:'Cormorant Garamond';
                font-size:28px;
                font-weight:700;
                color:{GOLD};
            ">
                HeritageLens
            </div>
            <div style="
                font-size:12px;
                letter-spacing:2px;
                opacity:0.8;
            ">
                CSMVS VISITOR INSIGHTS
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ❈ FILTER COLLECTION")

    # Gender filter
    if GENDER:
        gender_options = sorted(
            clean_series(GENDER).unique().tolist()
        )

        selected_gender = st.multiselect(
            "Gender",
            gender_options,
            default=[]
        )

    else:
        selected_gender = []

    # Age filter
    if AGE:
        age_options = sorted(
            clean_series(AGE).unique().tolist()
        )

        selected_age = st.multiselect(
            "Age Group",
            age_options,
            default=[]
        )

    else:
        selected_age = []

    # Tourist type
    if TOURIST:
        tourist_options = sorted(
            clean_series(TOURIST).unique().tolist()
        )

        selected_tourist = st.multiselect(
            "Visitor Type",
            tourist_options,
            default=[]
        )

    else:
        selected_tourist = []

    # First visit
    if FIRST:
        first_options = sorted(
            clean_series(FIRST).unique().tolist()
        )

        selected_first = st.multiselect(
            "Visit Type",
            first_options,
            default=[]
        )

    else:
        selected_first = []

    st.markdown("---")

    st.markdown(
        f"""
        <div style="
            padding:15px;
            border:1px solid rgba(196,154,69,0.45);
            border-radius:12px;
            background:rgba(196,154,69,0.08);
        ">
            <div style="font-size:13px;color:{GOLD};">
                DATA SOURCE
            </div>
            <div style="
                font-family:'Cormorant Garamond';
                font-size:21px;
                font-weight:700;
                margin-top:5px;
            ">
                CSMVS Heritage Survey
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# APPLY FILTERS
# ============================================================

filtered_df = df.copy()

if GENDER and selected_gender:
    filtered_df = filtered_df[
        filtered_df[GENDER]
        .fillna("Not specified")
        .astype(str)
        .str.strip()
        .isin(selected_gender)
    ]

if AGE and selected_age:
    filtered_df = filtered_df[
        filtered_df[AGE]
        .fillna("Not specified")
        .astype(str)
        .str.strip()
        .isin(selected_age)
    ]

if TOURIST and selected_tourist:
    filtered_df = filtered_df[
        filtered_df[TOURIST]
        .fillna("Not specified")
        .astype(str)
        .str.strip()
        .isin(selected_tourist)
    ]

if FIRST and selected_first:
    filtered_df = filtered_df[
        filtered_df[FIRST]
        .fillna("Not specified")
        .astype(str)
        .str.strip()
        .isin(selected_first)
    ]

# Temporarily use filtered data for visualisations
original_df = df.copy()
df = filtered_df

# ============================================================
# HERO SECTION
# ============================================================

st.markdown(
    f"""
    <div class="heritage-hero">

        <div class="hero-kicker">
            ❈ CHHATRAPATI SHIVAJI MAHARAJ VASTU SANGRAHALAYA ❈
        </div>

        <div class="hero-title">
            HeritageLens
        </div>

        <div class="gold-line"></div>

        <div class="hero-subtitle">
            An interactive cultural intelligence dashboard exploring
            visitor profiles, motivations, museum experiences and
            heritage tourism insights.
        </div>

        <div style="
            margin-top:18px;
            color:#DCCBAE;
            font-size:13px;
            letter-spacing:1.5px;
        ">
            HERITAGE • CULTURE • VISITOR INSIGHTS
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# KPI CALCULATIONS
# ============================================================

TOTAL = len(df)

def percentage_for(column, keyword):
    if column is None or TOTAL == 0:
        return 0

    s = clean_series(column).str.lower()

    return round(
        s.str.contains(keyword.lower(), regex=False).mean() * 100,
        1
    )


first_visit_pct = percentage_for(FIRST, "yes")
international_pct = percentage_for(TOURIST, "international")
crowding_pct = percentage_for(CROWD, "yes")

# ============================================================
# KPI SECTION
# ============================================================

st.markdown(
    """
    <div class="section-title">
        ❈ Visitor Heritage Profile
    </div>
    <div class="section-subtitle">
        A snapshot of the people experiencing the museum.
    </div>
    """,
    unsafe_allow_html=True
)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">👥</div>
            <div class="kpi-label">Survey Responses</div>
            <div class="kpi-value">{TOTAL:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">🪷</div>
            <div class="kpi-label">First-Time Visitors</div>
            <div class="kpi-value">{first_visit_pct}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">🌏</div>
            <div class="kpi-label">International Visitors</div>
            <div class="kpi-value">{international_pct}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-icon">🏛️</div>
            <div class="kpi-label">Crowding Reported</div>
            <div class="kpi-value">{crowding_pct}%</div>
        </div>
