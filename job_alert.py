import requests
from bs4 import BeautifulSoup
import os
import psycopg2
import time

# =========================
# ENV VARIABLES
# =========================
DATABASE_URL = os.getenv("DATABASE_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found")

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("BOT_TOKEN or CHAT_ID missing")

URL = "https://www.onlinejobs.ph/jobseekers/jobsearch?jobkeyword=data"
headers = {"User-Agent": "Mozilla/5.0"}

# =========================
# TELEGRAM FUNCTION
# =========================
def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "disable_web_page_preview": True
    }

    requests.post(url, data=payload)

# =========================
# DATABASE SETUP (POSTGRES)
# =========================
conn = psycopg2.connect(DATABASE_URL, sslmode="require")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    id TEXT PRIMARY KEY,
    title TEXT,
    link TEXT
)
""")
conn.commit()

# =========================
# SCRAPER
# =========================
def scrape_jobs():
    res = requests.get(URL, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    jobs = []
    seen = set()

    job_cards = soup.select("div.jobpost-cat-box")

    for job in job_cards:
        a_tag = job.find("a", href=True)
        if not a_tag:
            continue

        link = "https://www.onlinejobs.ph" + a_tag["href"]
        job_id = link.split("-")[-1]

        if job_id in seen:
            continue
        seen.add(job_id)

        title_tag = job.select_one("h4")
        title = title_tag.get_text(" ", strip=True) if title_tag else "N/A"

        type_tag = job.select_one("span.badge")
        job_type = type_tag.text.strip() if type_tag else "N/A"

        salary_tag = job.select_one("dd.col")
        salary = salary_tag.text.strip() if salary_tag else "N/A"

        date_tag = job.select_one("p em")
        posted = date_tag.text.replace("Posted on", "").strip() if date_tag else "N/A"

        desc_tag = job.select_one("div.desc")
        desc = desc_tag.get_text(" ", strip=True)[:200] if desc_tag else ""

        jobs.append({
            "id": job_id,
            "title": title,
            "type": job_type,
            "salary": salary,
            "posted": posted,
            "description": desc,
            "link": link
        })

    return jobs

# =========================
# SAVE (POSTGRES SAFE)
# =========================
def save_job(job):
    c.execute("""
        INSERT INTO jobs (id, title, link)
        VALUES (%s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, (job["id"], job["title"], job["link"]))
    conn.commit()

    return c.rowcount > 0  # True if inserted

# =========================
# FORMAT MESSAGE
# =========================
def format_job(job):
    return (
        f"💼 {job.get('title','N/A')}\n"
        f"💰 {job.get('salary','N/A')}\n"
        f"🕒 {job.get('type','N/A')}\n"
        f"📅 {job.get('posted','N/A')}\n\n"
        f"🔗 {job.get('link','')}"
    )

# =========================
# MAIN RUNNER
# =========================
def run():
    print("Scraping jobs...")

    jobs = scrape_jobs()
    new_jobs = []

    for job in jobs:
        inserted = save_job(job)
        if inserted:
            new_jobs.append(job)

    if new_jobs:
        print(f"New jobs found: {len(new_jobs)}")

        for job in new_jobs:
            send_telegram(format_job(job))
    else:
        print("No new jobs.")

# =========================
# LOOP (24/7)
# =========================
if __name__ == "__main__":
    while True:
        try:
            run()
        except Exception as e:
            print("Error:", e)

        time.sleep(300)  # every 5 minutes