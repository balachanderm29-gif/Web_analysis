import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import random

# ─── PAGE CONFIG ─────────────────────────────────────────────
st.set_page_config(
    page_title="Enterprise Web Intelligence Dashboard",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 Enterprise Web Gap Intelligence System")
st.markdown("### AI-Powered Synthetic + Real Website Analysis Engine")
st.divider()

# ─── BASE WEBSITES ───────────────────────────────────────────
base_websites = {
    "Agriculture Industry": "https://vasanthats228.github.io/agriculture-Industry/",
    "Internet Site": "https://vasanthats228.github.io/Internet-Site1/",
    "Information Technology": "https://vasanthats228.github.io/InformationTechnology1/"
}

industries = list(base_websites.keys())

# ─── SYNTHETIC DATA GENERATOR (HIGH-END SIMULATION ENGINE) ───
def generate_dataset(n=200):
    data = []

    for i in range(n):
        industry = random.choice(industries)

        links = random.randint(2, 80)
        images = random.randint(0, 30)
        forms = random.randint(0, 10)

        status = random.choice(["Active", "Active", "Active", "Inactive"])  # bias active

        # AI-style scoring system
        score = (
            (links * 0.4) +
            (images * 1.5) +
            (forms * 5) +
            (20 if status == "Active" else 0)
        )

        score = min(int(score), 100)

        data.append({
            "Industry": industry,
            "URL": base_websites[industry],
            "Total Links": links,
            "Images": images,
            "Forms": forms,
            "Status": status,
            "Score": score
        })

    return pd.DataFrame(data)

# ─── LOAD DATA ───────────────────────────────────────────────
df = generate_dataset(250)

# ─── KPI ENGINE ──────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Websites", len(df))
col2.metric("Active Sites", (df["Status"] == "Active").sum())
col3.metric("Avg Score", round(df["Score"].mean(), 2))
col4.metric("High Performers (80+)", (df["Score"] >= 80).sum())

st.divider()

# ─── ADVANCED FILTER PANEL ───────────────────────────────────
st.sidebar.header("🎛 Advanced Filters")

industry_filter = st.sidebar.multiselect(
    "Industry",
    df["Industry"].unique(),
    default=list(df["Industry"].unique())
)

status_filter = st.sidebar.multiselect(
    "Status",
    df["Status"].unique(),
    default=list(df["Status"].unique())
)

score_range = st.sidebar.slider(
    "Score Range",
    0, 100, (20, 90)
)

link_range = st.sidebar.slider(
    "Links Range",
    0, 100, (5, 60)
)

image_range = st.sidebar.slider(
    "Images Range",
    0, 50, (1, 25)
)

# ─── FILTER LOGIC ────────────────────────────────────────────
filtered_df = df[
    (df["Industry"].isin(industry_filter)) &
    (df["Status"].isin(status_filter)) &
    (df["Score"].between(score_range[0], score_range[1])) &
    (df["Total Links"].between(link_range[0], link_range[1])) &
    (df["Images"].between(image_range[0], image_range[1]))
]

st.success(f"Filtered Records: {len(filtered_df)}")

st.dataframe(filtered_df, use_container_width=True)

st.divider()

# ─── VISUAL ANALYTICS ENGINE ─────────────────────────────────

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Score Distribution")
    fig = px.histogram(df, x="Score", nbins=20)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🏢 Industry Performance")
    fig2 = px.box(df, x="Industry", y="Score")
    st.plotly_chart(fig2, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.subheader("🔗 Links vs Score")
    fig3 = px.scatter(df, x="Total Links", y="Score", color="Industry")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("🖼 Images vs Score")
    fig4 = px.scatter(df, x="Images", y="Score", color="Industry")
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ─── AI INSIGHT ENGINE ───────────────────────────────────────
st.subheader("🧠 AI Gap Insights Engine")

def insight(row):
    if row["Score"] >= 80:
        return "🟢 Excellent Digital Presence"
    elif row["Score"] >= 50:
        return "🟡 Medium Optimization Needed"
    else:
        return "🔴 High Risk / Poor Web Structure"

filtered_df["Insight"] = filtered_df.apply(insight, axis=1)

st.dataframe(filtered_df, use_container_width=True)

# ─── EXECUTIVE DASHBOARD VIEW ────────────────────────────────
st.divider()
st.subheader("🚀 Executive Summary View")

st.write("Top 10 High Performing Websites")

top_df = df.sort_values(by="Score", ascending=False).head(10)

for _, row in top_df.iterrows():
    st.markdown(f"""
### 🌐 {row['Industry']}
- 📊 Score: **{row['Score']}**
- 🔗 Links: {row['Total Links']}
- 🖼 Images: {row['Images']}
- 📋 Forms: {row['Forms']}
- ⚡ Status: {row['Status']}
""")

st.markdown("---")
st.markdown("⚡ Enterprise Web Intelligence System | AI Synthetic Dataset Engine")
