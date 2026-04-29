import requests
from bs4 import BeautifulSoup
import sqlite3

# =========================
# CONFIG (FILL THIS IN)
# =========================
BOT_TOKEN = "8651840623:AAGnTssUlg8CWOT7ix9xmjElrO7I0RmYH7M"
CHAT_ID = "7320711615"

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
# DATABASE SETUP
# =========================
conn = sqlite3.connect("jobs.db")
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

        # LINK
        a_tag = job.find("a", href=True)
        if not a_tag:
            continue

        link = "https://www.onlinejobs.ph" + a_tag["href"]
        job_id = link.split("-")[-1]

        if job_id in seen:
            continue
        seen.add(job_id)

        # TITLE
        title_tag = job.select_one("h4")
        title = title_tag.get_text(" ", strip=True) if title_tag else "N/A"

        # TYPE OF WORK
        type_tag = job.select_one("span.badge")
        job_type = type_tag.text.strip() if type_tag else "N/A"

        # SALARY
        salary_tag = job.select_one("dd.col")
        salary = salary_tag.text.strip() if salary_tag else "N/A"

        # POSTED DATE
        date_tag = job.select_one("p em")
        posted = date_tag.text.replace("Posted on", "").strip() if date_tag else "N/A"

        # DESCRIPTION (short)
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
# HELPERS
# =========================
def is_new(job_id):
    c.execute("SELECT 1 FROM jobs WHERE id=?", (job_id,))
    return c.fetchone() is None


def save_job(job):
    c.execute("INSERT INTO jobs VALUES (?, ?, ?)",
              (job["id"], job["title"], job["link"]))
    conn.commit()


def format_job(job):
    return f"""
💼 {job['title']}

💰 Salary: {job['salary']}
🕒 Type: {job['type']}
📅 Posted: {job['posted']}

🔗 Apply:
{job['link']}
"""


# =========================
# MAIN RUNNER
# =========================
def run():
    print("Scraping jobs...")

    jobs = scrape_jobs()
    new_jobs = []

    for job in jobs:
        if is_new(job["id"]):
            save_job(job)
            new_jobs.append(job)

    if new_jobs:
        print(f"New jobs found: {len(new_jobs)}")

        for job in new_jobs:
            send_telegram(format_job(job))
    else:
        print("No new jobs.")


# =========================
# EXECUTE
# =========================
import time

if __name__ == "__main__":
    while True:
        try:
            run()
        except Exception as e:
            print("Error:", e)

        time.sleep(300)  # every 5 minutes