import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# ─── PAGE CONFIG ─────────────────────────────────────────────
st.set_page_config(
    page_title="Web Gap Analysis Dashboard",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 Web Gap Analysis Dashboard")
st.markdown("### High-Potential Website Intelligence & Gap Insights")
st.divider()

# ─── WEBSITE LIST ────────────────────────────────────────────
websites = {
    "Agriculture Industry": "https://vasanthats228.github.io/agriculture-Industry/",
    "Internet Site": "https://vasanthats228.github.io/Internet-Site1/",
    "Information Technology": "https://vasanthats228.github.io/InformationTechnology1/"
}

# ─── SESSION FOR SPEED ───────────────────────────────────────
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) WebGapBot/1.0"
})

# ─── SAFE WEBSITE ANALYZER ───────────────────────────────────
@st.cache_data(ttl=3600)
def analyze_website(name, url):

    try:
        response = session.get(url, timeout=8)
        soup = BeautifulSoup(response.text, "html.parser")

        title_tag = soup.title.string.strip() if soup.title and soup.title.string else "No Title"

        links = len(soup.find_all("a"))
        images = len(soup.find_all("img"))
        forms = len(soup.find_all("form"))

        status = "Active" if response.status_code == 200 else "Inactive"

        return {
            "Industry": name,
            "URL": url,
            "Title": title_tag,
            "Total Links": links,
            "Images": images,
            "Forms": forms,
            "Status": status
        }

    except Exception as e:
        return {
            "Industry": name,
            "URL": url,
            "Title": "Error",
            "Total Links": 0,
            "Images": 0,
            "Forms": 0,
            "Status": "Inactive"
        }

# ─── PARALLEL SCRAPING (HIGH PERFORMANCE) ────────────────────
def load_data():
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(lambda x: analyze_website(*x), websites.items()))
    return pd.DataFrame(results)

with st.spinner("🔄 Analyzing websites..."):
    df = load_data()

# ─── SAFETY CHECK ────────────────────────────────────────────
if df.empty:
    st.error("No data found")
    st.stop()

# ─── KPI METRICS ─────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Websites", len(df))
col2.metric("Active Sites", (df["Status"] == "Active").sum())
col3.metric("Total Links", int(df["Total Links"].sum()))
col4.metric("Total Images", int(df["Images"].sum()))

st.divider()

# ─── CHARTS ──────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Website Status")
    status_df = df["Status"].value_counts().reset_index()
    status_df.columns = ["Status", "Count"]

    fig = px.pie(status_df, names="Status", values="Count", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🔗 Link Distribution")
    fig2 = px.bar(df, x="Industry", y="Total Links", text="Total Links")
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("🖼 Image Density")
    fig3 = px.bar(df, x="Industry", y="Images", text="Images")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("📋 Form Availability")
    fig4 = px.bar(df, x="Industry", y="Forms", text="Forms")
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ─── SMART GAP INSIGHTS ENGINE ───────────────────────────────
st.subheader("📌 AI-Level Gap Insights")

def insights(row):
    issues = []

    if row["Status"] != "Active":
        issues.append("❌ Site Down / Inactive")

    if row["Forms"] == 0:
        issues.append("⚠ No Lead Capture System")

    if row["Images"] < 3:
        issues.append("⚠ Weak Visual Engagement")

    if row["Total Links"] < 5:
        issues.append("⚠ Poor Navigation Structure")

    if not issues:
        return "✅ Strong Digital Presence"

    return " | ".join(issues)

df["Insights"] = df.apply(insights, axis=1)

st.dataframe(df, use_container_width=True)

# ─── SIDEBAR FILTER ──────────────────────────────────────────
st.sidebar.header("🔍 Filter Panel")

industry = st.sidebar.selectbox(
    "Select Industry",
    ["All"] + list(df["Industry"])
)

filtered_df = df if industry == "All" else df[df["Industry"] == industry]

st.sidebar.write("### Filtered View")
st.sidebar.dataframe(filtered_df, use_container_width=True)

# ─── ACTIONABLE STRATEGY OUTPUT ──────────────────────────────
st.divider()
st.subheader("🚀 Executive Action Plan")

for _, row in filtered_df.iterrows():
    st.markdown(f"""
### 🏢 {row['Industry']}

- 🔗 Links: **{row['Total Links']}**
- 🖼 Images: **{row['Images']}**
- 📋 Forms: **{row['Forms']}**
- 📊 Insight: **{row['Insights']}**
- 🌐 [Open Website]({row['URL']})
""")

# ─── FOOTER ──────────────────────────────────────────────────
st.markdown("---")
st.markdown("⚡ Built with Streamlit | High-Potential Web Intelligence System")
