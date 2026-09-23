
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CSMVS Heritage Visitor Intelligence", page_icon="🏛️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
html, body, [class*="css"] {font-family:'DM Sans',sans-serif;}
.stApp {background:linear-gradient(180deg,#faf7f1,#f2ede4);}
.block-container {max-width:1450px;padding-top:1.2rem;}
.hero {background:linear-gradient(135deg,#24150f,#54301e,#81502e);padding:32px;border-radius:24px;color:white;margin-bottom:22px;box-shadow:0 12px 35px rgba(63,39,25,.18);}
.hero h1 {font-family:'Playfair Display',serif;font-size:38px;margin:0 0 6px;}
.hero p {color:#eadccf;margin:0;}
.eyebrow {color:#e7b86a;font-weight:700;letter-spacing:2px;font-size:12px;text-transform:uppercase;margin-bottom:7px;}
.kpi {background:white;border:1px solid #e6ddd0;border-radius:18px;padding:18px 20px;box-shadow:0 5px 18px rgba(53,37,25,.06);}
.kpi-label {color:#77695f;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;}
.kpi-value {color:#342117;font-size:28px;font-weight:700;margin-top:5px;}
.kpi-note {color:#9a6a39;font-size:12px;margin-top:4px;}
.section-title {font-family:'Playfair Display',serif;font-size:25px;color:#332017;margin:22px 0 8px;}
div[data-testid="stSidebar"] {background:#24150f;}
div[data-testid="stSidebar"] * {color:#f5eee7 !important;}
.footer {text-align:center;color:#7d6d60;font-size:12px;padding:25px 0 5px;}
</style>
""", unsafe_allow_html=True)

FILE="CSMVS_Heritage_Survey_Responses.csv"
df=pd.read_csv(FILE)
df.columns=df.columns.str.strip()

def col(*phrases):
    for p in phrases:
        for c in df.columns:
            if p.lower() in c.lower(): return c
    return None

def counts(s,n=10):
    if s is None: return pd.DataFrame()
    d=s.dropna().astype(str).str.strip().replace("","Unknown").value_counts().head(n).reset_index()
    d.columns=["Category","Visitors"]; return d

def bar(s,title,h=False,n=10):
    d=counts(s,n)
    if d.empty: return
    fig=px.bar(d,x="Visitors",y="Category",orientation="h",text="Visitors") if h else px.bar(d,x="Category",y="Visitors",text="Visitors")
    fig.update_layout(title=title,height=350,margin=dict(l=10,r=10,t=55,b=10),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)")
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig,use_container_width=True)

def donut(s,title):
    d=counts(s,8)
    if d.empty: return
    fig=px.pie(d,names="Category",values="Visitors",hole=.6,title=title)
    fig.update_layout(height=340,margin=dict(l=10,r=10,t=55,b=10),paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig,use_container_width=True)

age=col("age group"); gender=col("gender")
tourist=col("indian or international tourist","international tourist")
first=col("first visit to the museum")
reason=col("main reason for visiting")
interest=col("aspects of the museum interest")
crowd=col("excessive crowding")
experience=col("visit experience do you prefer")
issue=col("what issues did you face")
appcol=col("tourist-planning app","tourist planning app")
score=col("score"); group=col("how many people are in your group")
attractions=col("nearby attractions")

st.markdown("""
<div class="hero">
<div class="eyebrow">Cultural Heritage • Visitor Intelligence</div>
<h1>CSMVS Heritage Visitor Dashboard</h1>
<p>Visitor profiles, motivations, experiences, crowding, attractions and digital-tourism needs.</p>
</div>
""",unsafe_allow_html=True)

st.sidebar.markdown("## 🏛️ CSMVS")
st.sidebar.caption("Heritage Visitor Intelligence")
st.sidebar.divider()

filtered=df.copy()
for label,c in [("Age Group",age),("Gender",gender),("Tourist Type",tourist),("First Visit",first)]:
    if c:
        opts=sorted(df[c].dropna().astype(str).unique())
        chosen=st.sidebar.multiselect(label,opts,default=opts)
        if chosen: filtered=filtered[filtered[c].astype(str).isin(chosen)]

avg_score=pd.to_numeric(filtered[score],errors="coerce").mean() if score else None
avg_group=pd.to_numeric(filtered[group],errors="coerce").mean() if group else None

k1,k2,k3,k4=st.columns(4)
for container,label,value,note in [
    (k1,"Visitors in view",f"{len(filtered):,}","Filtered responses"),
    (k2,"Average score",f"⭐ {avg_score:.1f}" if pd.notna(avg_score) else "—","Available score data"),
    (k3,"Average group size",f"👥 {avg_group:.1f}" if pd.notna(avg_group) else "—","People per group"),
    (k4,"Survey records",f"📋 {len(df):,}","Complete dataset")]:
    with container:
        st.markdown(f'<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-note">{note}</div></div>',unsafe_allow_html=True)

st.markdown('<div class="section-title">Visitor Snapshot</div>',unsafe_allow_html=True)
a,b=st.columns(2)
with a: bar(filtered[age],"Age profile") if age else None
with b: donut(filtered[gender],"Gender distribution") if gender else None
a,b=st.columns(2)
with a: donut(filtered[tourist],"Tourist composition") if tourist else None
with b: bar(filtered[first],"First-time vs repeat visitors") if first else None

st.markdown('<div class="section-title">Why People Visit</div>',unsafe_allow_html=True)
if reason: bar(filtered[reason],"Top visitor motivations",True,10)

st.markdown('<div class="section-title">Museum Experience</div>',unsafe_allow_html=True)
a,b=st.columns(2)
with a: bar(filtered[interest],"Most interesting museum aspects",True,10) if interest else None
with b: bar(filtered[experience],"Preferred visit experience",True,10) if experience else None
if crowd: donut(filtered[crowd],"Crowding experience")

st.markdown('<div class="section-title">Tourism & Nearby Attractions</div>',unsafe_allow_html=True)
if attractions:
    s=filtered[attractions].dropna().astype(str).str.split(",").explode().str.strip()
    bar(s,"Attractions visitors want to explore",True,12)

st.markdown('<div class="section-title">Pain Points & Digital Needs</div>',unsafe_allow_html=True)
a,b=st.columns(2)
with a: bar(filtered[issue],"Common visitor issues",True,10) if issue else None
with b: bar(filtered[appcol],"What visitors want from a tourist app",True,10) if appcol else None

with st.expander("📊 Open detailed visitor data"):
    st.dataframe(filtered,use_container_width=True,height=420)
    st.download_button("⬇️ Download filtered CSV",filtered.to_csv(index=False),"CSMVS_filtered_data.csv","text/csv")

st.markdown('<div class="footer">CSMVS Heritage Survey • Visitor Behaviour & Tourism Analysis<br>Academic Data-Visualisation Dashboard</div>',unsafe_allow_html=True)

