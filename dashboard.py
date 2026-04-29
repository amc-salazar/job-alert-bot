import streamlit as st
import sqlite3

st.set_page_config(page_title="Job Dashboard", layout="wide")

# =========================
# DB
# =========================
conn = sqlite3.connect("jobs.db")
c = conn.cursor()

c.execute("SELECT * FROM jobs")
rows = c.fetchall()

jobs = [
    {"id": r[0], "title": r[1], "link": r[2]}
    for r in rows
]

# =========================
# HEADER
# =========================
st.title("💼 Job Alert Dashboard")
st.caption(f"Total Jobs: {len(jobs)}")

st.divider()

# =========================
# SEARCH
# =========================
search = st.text_input("🔍 Search jobs (keyword, company, etc.)")

if search:
    jobs = [j for j in jobs if search.lower() in j["title"].lower()]

# =========================
# CARDS UI
# =========================
for job in jobs:
    with st.container():
        st.markdown(
            f"""
            <div style="
                padding:15px;
                border-radius:10px;
                border:1px solid #ddd;
                margin-bottom:10px;
                background-color:#fafafa;
            ">
                <h4 style="margin-bottom:5px;">💼 {job['title']}</h4>
                <a href="{job['link']}" target="_blank">🔗 Open Job</a>
            </div>
            """,
            unsafe_allow_html=True
        )