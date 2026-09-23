
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CSMVS Heritage Survey Dashboard", page_icon="🏛️", layout="wide")

FILE = "CSMVS_Heritage_Survey_Responses.csv"
df = pd.read_csv(FILE)
df.columns = df.columns.str.strip()

st.title("🏛️ CSMVS Heritage Survey Dashboard")
st.markdown("### Visitor Behaviour, Experience & Tourism Analysis")
st.divider()

st.sidebar.header("🔎 Filters")

def options(col):
    return sorted(df[col].dropna().astype(str).unique()) if col in df.columns else []

age_col = "Age Group"
gender_col = "Gender"
tourist_col = "Are you an Indian or International Tourist?"
first_col = "Is it your first visit to the museum?"

selected_age = st.sidebar.multiselect("Age Group", options(age_col), default=options(age_col))
selected_gender = st.sidebar.multiselect("Gender", options(gender_col), default=options(gender_col))
selected_tourist = st.sidebar.multiselect("Tourist Type", options(tourist_col), default=options(tourist_col))
selected_first = st.sidebar.multiselect("First Visit?", options(first_col), default=options(first_col))

filtered = df.copy()
if selected_age:
    filtered = filtered[filtered[age_col].astype(str).isin(selected_age)]
if selected_gender:
    filtered = filtered[filtered[gender_col].astype(str).isin(selected_gender)]
if selected_tourist:
    filtered = filtered[filtered[tourist_col].astype(str).isin(selected_tourist)]
if selected_first:
    filtered = filtered[filtered[first_col].astype(str).isin(selected_first)]

def numeric_mean(col):
    if col in filtered.columns:
        return pd.to_numeric(filtered[col], errors="coerce").mean()
    return 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("👥 Visitors", len(filtered))
c2.metric("⭐ Average Score", f"{numeric_mean('Score'):.2f}" if 'Score' in filtered.columns else "N/A")
c3.metric("👨‍👩‍👧 Avg. Group Size", f"{numeric_mean('How many people are in your group?'):.2f}" if 'How many people are in your group?' in filtered.columns else "N/A")
c4.metric("📊 Total Responses", len(df))

st.divider()

def bar_chart(col, title, n=10, horizontal=False):
    if col not in filtered.columns:
        return
    d = filtered[col].dropna().astype(str).value_counts().head(n).reset_index()
    d.columns = ["Category", "Visitors"]
    if horizontal:
        fig = px.bar(d, x="Visitors", y="Category", orientation="h", title=title, text="Visitors")
    else:
        fig = px.bar(d, x="Category", y="Visitors", title=title, text="Visitors")
    st.plotly_chart(fig, use_container_width=True)

def pie_chart(col, title):
    if col not in filtered.columns:
        return
    d = filtered[col].dropna().astype(str).value_counts().reset_index()
    d.columns = ["Category", "Visitors"]
    fig = px.pie(d, names="Category", values="Visitors", title=title, hole=.4)
    st.plotly_chart(fig, use_container_width=True)

st.header("👥 Visitor Demographics")
a, b = st.columns(2)
with a:
    bar_chart(age_col, "Visitors by Age Group")
with b:
    pie_chart(gender_col, "Gender Distribution")

st.header("🌍 Tourist Profile")
a, b = st.columns(2)
with a:
    pie_chart(tourist_col, "Indian vs International Tourists")
with b:
    bar_chart(first_col, "First-Time vs Repeat Visitors")

st.header("🎯 Visit Analysis")
reason_col = "What was your main reason for visiting?"
bar_chart(reason_col, "Top Reasons for Visiting", 10, True)

interest_col = "Which aspects of the museum interest you the most?"
bar_chart(interest_col, "Most Interesting Museum Aspects", 10, True)

st.header("👥 Crowding & Experience")
crowd_col = "Did you experience excessive crowding?"
pie_chart(crowd_col, "Visitors Experiencing Excessive Crowding")

experience_col = "What type of visit experience do you prefer?"
bar_chart(experience_col, "Preferred Visit Experience", 10, True)

st.header("📍 Nearby Attractions")
attraction_col = "Which nearby attractions would you be interested in visiting?  \n(Select all that you would be interested in visiting)"
if attraction_col in filtered.columns:
    d = (filtered[attraction_col].dropna().astype(str).str.split(",").explode().str.strip().value_counts().head(10).reset_index())
    d.columns = ["Attraction", "Visitors"]
    fig = px.bar(d, x="Visitors", y="Attraction", orientation="h", title="Popular Nearby Attractions", text="Visitors")
    st.plotly_chart(fig, use_container_width=True)

st.header("⚠️ Visitor Issues")
issue_col = "What issues did you face today?"
bar_chart(issue_col, "Most Common Visitor Issues", 10, True)

st.header("📱 Tourist-Planning App Requirements")
app_col = "If a tourist-planning app were available, what would you want it to tell you?"
bar_chart(app_col, "Information Visitors Want in a Tourist App", 10, True)

st.header("📋 Visitor Data")
st.dataframe(filtered, use_container_width=True, height=400)

st.download_button(
    "⬇️ Download Filtered Data",
    filtered.to_csv(index=False),
    "CSMVS_filtered_data.csv",
    "text/csv"
)

st.divider()
st.caption("CSMVS Heritage Survey | Visitor Behaviour & Tourism Analysis Dashboard")
