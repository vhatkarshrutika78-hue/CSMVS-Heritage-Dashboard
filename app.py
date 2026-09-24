import streamlit as st
import pandas as pd
import plotly.express as px
import re

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="HeritageLens | CSMVS",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# COLOURS
# ============================================================

TERRACOTTA = "#A44A2A"
GOLD = "#C49A45"
PEACOCK = "#174A43"
MAROON = "#641F2A"
IVORY = "#F5E9D0"
BROWN = "#3A2418"
CREAM = "#FFF8EA"
MUTED = "#806B58"

COLORS = [
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
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=DM+Sans:wght@400;500;600;700&display=swap');

    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(196,154,69,0.12), transparent 25%),
            radial-gradient(circle at 90% 20%, rgba(164,74,42,0.08), transparent 25%),
            #F5E9D0;
        color: #3A2418;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #174A43 0%,
            #123D37 55%,
            #3A2418 100%
        );
        border-right: 4px solid #C49A45;
    }

    section[data-testid="stSidebar"] * {
        color: #F5E9D0 !important;
    }

    .hero {
        background: linear-gradient(
            135deg,
            #174A43,
            #205A51,
            #641F2A
        );
        border: 2px solid #C49A45;
        border-radius: 25px;
        padding: 42px;
        margin-bottom: 25px;
        box-shadow: 0 12px 35px rgba(58,36,24,0.22);
        position: relative;
        overflow: hidden;
    }

    .hero:after {
        content: "❈";
        position: absolute;
        right: 40px;
        bottom: -20px;
        font-size: 150px;
        color: rgba(196,154,69,0.12);
    }

    .hero-small {
        color: #C49A45;
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 4px;
    }

    .hero-title {
        color: #F5E9D0;
        font-family: 'Cormorant Garamond', serif;
        font-size: 58px;
        font-weight: 700;
        margin: 5px 0;
    }

    .hero-subtitle {
        color: #E8DCC5;
        font-size: 17px;
        line-height: 1.6;
        max-width: 850px;
    }

    .gold-line {
        width: 90px;
        height: 3px;
        background: #C49A45;
        margin: 15px 0;
    }

    .section-title {
        color: #174A43;
        font-family: 'Cormorant Garamond', serif;
        font-size: 32px;
        font-weight: 700;
        margin-top: 30px;
    }

    .section-subtitle {
        color: #806B58;
        font-size: 14px;
        margin-bottom: 15px;
    }

    .kpi {
        background: rgba(255,248,234,0.95);
        border: 1px solid rgba(196,154,69,0.6);
        border-top: 5px solid #C49A45;
        border-radius: 17px;
        padding: 20px;
        min-height: 135px;
        box-shadow: 0 8px 22px rgba(58,36,24,0.10);
    }

    .kpi-icon {
        font-size: 25px;
    }

    .kpi-label {
        color: #806B58;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 6px;
    }

    .kpi-value {
        color: #174A43;
        font-family: 'Cormorant Garamond', serif;
        font-size: 38px;
        font-weight: 700;
    }

    .chart-card {
        background: rgba(255,248,234,0.90);
        border: 1px solid rgba(58,36,24,0.10);
        border-left: 5px solid #A44A2A;
        border-radius: 17px;
        padding: 8px 15px;
        box-shadow: 0 7px 20px rgba(58,36,24,0.08);
    }

    .heritage-note {
        background: rgba(196,154,69,0.13);
        border-left: 5px solid #C49A45;
        padding: 18px;
        border-radius: 10px;
        line-height: 1.7;
    }

    .footer {
        margin-top: 45px;
        padding: 25px;
        text-align: center;
        color: #806B58;
        border-top: 1px solid rgba(196,154,69,0.5);
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# LOAD CSV
# ============================================================

FILE_PATH = "/content/CSMVS_Heritage_Survey_Responses.csv"

try:
    df = pd.read_csv(FILE_PATH)
except FileNotFoundError:
    st.error("CSMVS_Heritage_Survey_Responses.csv was not found.")
    st.stop()

df.columns = (
    df.columns
    .astype(str)
    .str.replace("\n", " ", regex=False)
    .str.strip()
)

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def find_col(words):
    if isinstance(words, str):
        words = [words]

    for col in df.columns:
        text = col.lower()

        if all(word.lower() in text for word in words):
            return col

    for col in df.columns:
        text = col.lower()

        if any(word.lower() in text for word in words):
            return col

    return None


def clean_col(col):
    if col is None:
        return pd.Series(dtype="object")

    return (
        df[col]
        .fillna("Not specified")
        .astype(str)
        .str.strip()
        .replace("", "Not specified")
    )


def counts(col):
    if col is None:
        return pd.DataFrame(columns=["Answer", "Count"])

    result = clean_col(col).value_counts().reset_index()
    result.columns = ["Answer", "Count"]

    return result


def multi_counts(col):
    if col is None:
        return pd.DataFrame(columns=["Answer", "Count"])

    values = clean_col(col)
    items = []

    for value in values:
        parts = re.split(r",|;|\n|\|", value)

        for part in parts:
            part = part.strip()

            if part:
                items.append(part)

    if not items:
        return pd.DataFrame(columns=["Answer", "Count"])

    result = pd.Series(items).value_counts().head(12).reset_index()
    result.columns = ["Answer", "Count"]

    return result


def bar_chart(data, title, horizontal=False):

    if data.empty:
        st.info("No data available.")
        return

    if horizontal:
        fig = px.bar(
            data,
            x="Count",
            y="Answer",
            orientation="h",
            text="Count",
            color="Answer",
            color_discrete_sequence=COLORS
        )
    else:
        fig = px.bar(
            data,
            x="Answer",
            y="Count",
            text="Count",
            color="Answer",
            color_discrete_sequence=COLORS
        )

    fig.update_traces(
        textposition="outside",
        marker_line_width=0
    )

    fig.update_layout(
        title=title,
        title_font=dict(
            family="Cormorant Garamond",
            size=23,
            color=PEACOCK
        ),
        font=dict(
            family="DM Sans",
            color=BROWN
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        margin=dict(l=20, r=20, t=65, b=40),
        xaxis=dict(
            title="",
            showgrid=False
        ),
        yaxis=dict(
            title="",
            showgrid=False
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


def pie_chart(data, title):

    if data.empty:
        st.info("No data available.")
        return

    fig = px.pie(
        data,
        names="Answer",
        values="Count",
        hole=0.48,
        color_discrete_sequence=COLORS
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent"
    )

    fig.update_layout(
        title=title,
        title_font=dict(
            family="Cormorant Garamond",
            size=23,
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
        margin=dict(l=20, r=20, t=65, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )


def yes_percentage(col, word="yes"):

    if col is None or len(df) == 0:
        return 0

    values = clean_col(col).str.lower()

    return round(
        values.str.contains(word.lower(), regex=False).mean() * 100,
        1
    )


# ============================================================
# FIND COLUMNS
# ============================================================

AGE = find_col("Age Group")
GENDER = find_col("Gender")
LOCATION = find_col("Where are you from")
AWARENESS = find_col("How did you learn")
REASON = find_col("main reason for visiting")
INTEREST = find_col("aspects of the museum interest")
CROWD = find_col("excessive crowding")
OCCUPATION = find_col("Occupation")
TOURIST = find_col("Indian or International Tourist")
FIRST = find_col("first visit")
COMPANY = find_col("visiting with")
GROUP_SIZE = find_col("people are in your group")
ATTRACTIONS = find_col("nearby attractions")
ISSUES = find_col("issues did you face")
APP = find_col("tourist-planning app")
EXPERIENCE = find_col("preferred visit experience")

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center;padding:15px 5px 25px 5px;">
            <div style="font-size:45px;">🏛️</div>
            <div style="
                font-family:'Cormorant Garamond';
                font-size:30px;
                font-weight:700;
                color:#C49A45;
            ">
                HeritageLens
            </div>
            <div style="
                font-size:11px;
                letter-spacing:2px;
            ">
                CSMVS VISITOR INSIGHTS
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ❈ FILTER COLLECTION")

    selected_gender = []
    selected_age = []
    selected_tourist = []
    selected_first = []

    if GENDER:
        options = sorted(clean_col(GENDER).unique().tolist())
        selected_gender = st.multiselect(
            "Gender",
            options
        )

    if AGE:
        options = sorted(clean_col(AGE).unique().tolist())
        selected_age = st.multiselect(
            "Age Group",
            options
        )

    if TOURIST:
        options = sorted(clean_col(TOURIST).unique().tolist())
        selected_tourist = st.multiselect(
            "Visitor Type",
            options
        )

    if FIRST:
        options = sorted(clean_col(FIRST).unique().tolist())
        selected_first = st.multiselect(
            "Visit Type",
            options
        )

    st.markdown("---")

    st.markdown(
        """
        <div style="
            padding:15px;
            border:1px solid rgba(196,154,69,0.45);
            border-radius:12px;
            background:rgba(196,154,69,0.08);
        ">
            <div style="font-size:12px;color:#C49A45;">
                DATA SOURCE
            </div>
            <div style="
                font-family:'Cormorant Garamond';
                font-size:21px;
                font-weight:700;
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

filtered = df.copy()

if GENDER and selected_gender:
    filtered = filtered[
        filtered[GENDER]
        .fillna("Not specified")
        .astype(str)
        .str.strip()
        .isin(selected_gender)
    ]

if AGE and selected_age:
    filtered = filtered[
        filtered[AGE]
        .fillna("Not specified")
        .astype(str)
        .str.strip()
        .isin(selected_age)
    ]

if TOURIST and selected_tourist:
    filtered = filtered[
        filtered[TOURIST]
        .fillna("Not specified")
        .astype(str)
        .str.strip()
        .isin(selected_tourist)
    ]

if FIRST and selected_first:
    filtered = filtered[
        filtered[FIRST]
        .fillna("Not specified")
        .astype(str)
        .str.strip()
        .isin(selected_first)
    ]

df = filtered

# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero">

        <div class="hero-small">
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
            letter-spacing:2px;
        ">
            HERITAGE • CULTURE • VISITOR INSIGHTS
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# KPI
# ============================================================

TOTAL = len(df)

FIRST_PCT = yes_percentage(FIRST)
INTERNATIONAL_PCT = yes_percentage(TOURIST, "international")
CROWD_PCT = yes_percentage(CROWD)

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
        <div class="kpi">
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
        <div class="kpi">
            <div class="kpi-icon">🪷</div>
            <div class="kpi-label">First-Time Visitors</div>
            <div class="kpi-value">{FIRST_PCT}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k3:
    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-icon">🌏</div>
            <div class="kpi-label">International Visitors</div>
            <div class="kpi-value">{INTERNATIONAL_PCT}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with k4:
    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-icon">🏛️</div>
            <div class="kpi-label">Crowding Reported</div>
            <div class="kpi-value">{CROWD_PCT}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# VISITOR PROFILE
# ============================================================

st.markdown(
    """
    <div class="section-title">❈ Visitor Profile</div>
    <div class="section-subtitle">
        Demographic and travel characteristics of museum visitors.
    </div>
    """,
    unsafe_allow_html=True
)

c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    bar_chart(
        counts(AGE),
        "Age Group Distribution"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    pie_chart(
        counts(GENDER),
        "Visitor Gender Composition"
    )
    st.markdown('</div>', unsafe_allow_html=True)

c3, c4 = st.columns(2)

with c3:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    pie_chart(
        counts(TOURIST),
        "Indian vs International Visitors"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with c4:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    bar_chart(
        counts(OCCUPATION).head(10),
        "Visitor Occupation",
        horizontal=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# VISITOR MOTIVATION
# ============================================================

st.markdown(
    """
    <div class="section-title">❈ Why People Visit</div>
    <div class="section-subtitle">
        Discovering the motivations that bring visitors into the museum.
    </div>
    """,
    unsafe_allow_html=True
)

c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    bar_chart(
        counts(REASON).head(10),
        "Main Reasons for Visiting",
        horizontal=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    bar_chart(
        multi_counts(INTEREST),
        "Museum Aspects Visitors Find Interesting",
        horizontal=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# MUSEUM EXPERIENCE
# ============================================================

st.markdown(
    """
    <div class="section-title">❈ Museum Experience</div>
    <div class="section-subtitle">
        Exploring how visitors experience the museum environment.
    </div>
    """,
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    pie_chart(
        counts(FIRST),
        "First Visit vs Repeat Visit"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    pie_chart(
        counts(CROWD),
        "Crowding Experience"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    bar_chart(
        counts(COMPANY),
        "Who Visitors Come With",
        horizontal=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# HERITAGE EXPLORATION
# ============================================================

st.markdown(
    """
    <div class="section-title">❈ Heritage Exploration</div>
    <div class="section-subtitle">
        Understanding the wider tourism ecosystem around CSMVS.
    </div>
    """,
    unsafe_allow_html=True
)

c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    bar_chart(
        multi_counts(ATTRACTIONS),
        "Nearby Attractions Visitors Want to Explore",
        horizontal=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    bar_chart(
        counts(AWARENESS).head(10),
        "How Visitors Discovered the Museum",
        horizontal=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# GROUP SIZE
# ============================================================

if GROUP_SIZE:

    st.markdown(
        """
        <div class="section-title">❈ Visitor Group Patterns</div>
        <div class="section-subtitle">
