import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from bs4 import BeautifulSoup

# ─── PAGE CONFIG ─────────────────────────────────────────────
st.set_page_config(
    page_title="Web Gap Analysis Dashboard",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 Web Gap Analysis Dashboard")
st.markdown("### Actionable Insights from Website Analysis")
st.divider()

# ─── WEBSITE LINKS ───────────────────────────────────────────
websites = {
    "Agriculture Industry": "https://vasanthats228.github.io/agriculture-Industry/",
    "Internet Site": "https://vasanthats228.github.io/Internet-Site1/",
    "Information Technology": "https://vasanthats228.github.io/InformationTechnology1/"
}

# ─── FUNCTION TO SCRAPE BASIC DATA ───────────────────────────
@st.cache_data
def analyze_website(name, url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string if soup.title else "No Title"
        links = len(soup.find_all("a"))
        images = len(soup.find_all("img"))
        forms = len(soup.find_all("form"))

        return {
            "Industry": name,
            "URL": url,
            "Title": title,
            "Total Links": links,
            "Images": images,
            "Forms": forms,
            "Status": "Active" if response.status_code == 200 else "Inactive"
        }
    except:
        return {
            "Industry": name,
            "URL": url,
            "Title": "Error",
            "Total Links": 0,
            "Images": 0,
            "Forms": 0,
            "Status": "Inactive"
        }

# ─── LOAD DATA ───────────────────────────────────────────────
data = [analyze_website(name, url) for name, url in websites.items()]
df = pd.DataFrame(data)

# ─── KPI METRICS ─────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Websites", len(df))
col2.metric("Active Sites", int((df["Status"] == "Active").sum()))
col3.metric("Total Links", df["Total Links"].sum())
col4.metric("Total Images", df["Images"].sum())

st.divider()

# ─── CHARTS ──────────────────────────────────────────────────
col1, col2 = st.columns(2)

# Status Chart
with col1:
    st.subheader("📊 Website Status")
    status_counts = df["Status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    fig = px.pie(status_counts, names="Status", values="Count", hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

# Links per Industry
with col2:
    st.subheader("🔗 Links Distribution")
    fig2 = px.bar(df, x="Industry", y="Total Links", text="Total Links")
    st.plotly_chart(fig2, use_container_width=True)

# ─── ADVANCED ANALYSIS ───────────────────────────────────────
col3, col4 = st.columns(2)

# Images
with col3:
    st.subheader("🖼️ Images per Website")
    fig3 = px.bar(df, x="Industry", y="Images", color="Industry", text="Images")
    st.plotly_chart(fig3, use_container_width=True)

# Forms (Conversion Indicator)
with col4:
    st.subheader("📋 Forms (Conversion Potential)")
    fig4 = px.bar(df, x="Industry", y="Forms", color="Industry", text="Forms")
    st.plotly_chart(fig4, use_container_width=True)

# ─── GAP ANALYSIS INSIGHTS ───────────────────────────────────
st.divider()
st.subheader("📌 Gap Analysis Insights")

def generate_insights(row):
    insights = []

    if row["Forms"] == 0:
        insights.append("No lead capture form ❌")

    if row["Images"] < 3:
        insights.append("Low visual content ⚠️")

    if row["Total Links"] < 5:
        insights.append("Poor navigation ⚠️")

    if row["Status"] != "Active":
        insights.append("Site inactive ❌")

    return ", ".join(insights) if insights else "Good Performance ✅"

df["Insights"] = df.apply(generate_insights, axis=1)

st.dataframe(df, use_container_width=True)

# ─── FILTER SECTION ──────────────────────────────────────────
st.sidebar.header("🔍 Filter")

industry_filter = st.sidebar.selectbox("Select Industry", ["All"] + list(df["Industry"]))

filtered_df = df if industry_filter == "All" else df[df["Industry"] == industry_filter]

st.sidebar.write("### Filtered Data")
st.sidebar.write(filtered_df)

# ─── ACTIONABLE KPI SUMMARY ──────────────────────────────────
st.divider()
st.subheader("🚀 Actionable KPIs")

for index, row in df.iterrows():
    st.markdown(f"""
    ### {row['Industry']}
    - 🔗 Links: {row['Total Links']}
    - 🖼 Images: {row['Images']}
    - 📋 Forms: {row['Forms']}
    - 📊 Insight: {row['Insights']}
    - 🌐 [Visit Site]({row['URL']})
    """)

# ─── FOOTER ──────────────────────────────────────────────────
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit | Web Gap Analysis Dashboard")