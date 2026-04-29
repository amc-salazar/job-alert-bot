# 💼 Job Alert Automation System (24/7 Bot)

An end-to-end automated job scraping and notification system that monitors job listings and sends real-time alerts via Telegram.

The system runs continuously in the cloud and uses a PostgreSQL database to prevent duplicate alerts and ensure data persistence.

---

## 🚀 Live System Overview

This project is a fully automated pipeline that:

- Scrapes job postings from OnlineJobs.ph
- Extracts structured job data (title, salary, type, date)
- Stores jobs in a PostgreSQL database
- Detects new job postings using database constraints
- Sends real-time alerts via Telegram
- Runs 24/7 on cloud deployment (Railway)

---

## 🏗️ System Architecture
            ┌────────────────────────────┐
            │   Railway Cloud (24/7)     │
            │   Scheduler / Loop         │
            └────────────┬───────────────┘
                         ↓
            ┌────────────────────────────┐
            │  Python Scraper Bot        │
            └────────────┬───────────────┘
                         ↓
            ┌────────────────────────────┐
            │  Job Website (OnlineJobs)  │
            └────────────┬───────────────┘
                         ↓
            ┌────────────────────────────┐
            │  Data Parsing / Cleaning   │
            └────────────┬───────────────┘
                         ↓
            ┌────────────────────────────┐
            │ PostgreSQL Database        │
            │ (Deduplication Layer)      │
            └────────────┬───────────────┘
                         ↓
            ┌────────────────────────────┐
            │ Telegram Bot API           │
            └────────────┬───────────────┘
                         ↓
            ┌────────────────────────────┐
            │ User Notifications         │
            └────────────────────────────┘

---

## ☁️ Deployment

- Hosted on Railway
- Runs continuously (24/7 background worker)
- Uses environment variables for secure credentials
- Connected to managed PostgreSQL database

---

## 🛠️ Tech Stack

- Python
- BeautifulSoup (Web Scraping)
- Requests (HTTP calls)
- PostgreSQL (Cloud database)
- psycopg2 (PostgreSQL adapter)
- Telegram Bot API (Notifications)
- Railway (Cloud deployment)

---

## 🔔 Example Alert

💼 Customer Experience Associate  
💰 $4.50/hour  
🕒 Part-Time  
📅 Posted: 2026-04-28  

🔗 Apply: https://www.onlinejobs.ph/jobseekers/job/...

---

## ⚙️ How It Works

1. The scraper runs every 5 minutes
2. Extracts job listings from the website
3. Attempts to insert jobs into PostgreSQL
4. Database enforces uniqueness (`PRIMARY KEY`)
5. Only new jobs are successfully inserted
6. New jobs trigger Telegram alerts

---

## 🧠 Key Features

- ✔ Fully automated job tracking system
- ✔ 24/7 cloud execution
- ✔ PostgreSQL-backed persistence
- ✔ Duplicate prevention using database constraints
- ✔ Real-time Telegram notifications
- ✔ Lightweight and scalable design

---

---

## 🔒 Environment Variables

The system uses secure environment variables:

- `DATABASE_URL` → PostgreSQL connection
- `BOT_TOKEN` → Telegram bot token
- `CHAT_ID` → Telegram chat ID

---

## 📌 Purpose

This project demonstrates:

- Web scraping automation
- Backend data pipeline design
- Cloud deployment and continuous execution
- Database-driven deduplication logic
- Real-time notification systems

---

## 📈 Future Improvements

- Multi-source job scraping (LinkedIn, 104, etc.)
- Keyword-based filtering (Data / Python / Analyst)
- AI-based job relevance scoring
- Web dashboard for monitoring
- Salary and job trend analytics

---

## 📜 License

MIT License
