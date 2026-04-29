# 💼 Job Alert Automation System (24/7)

An automated job scraping and notification system that monitors remote job listings and sends real-time alerts via Telegram.

The system runs continuously in the cloud and prevents duplicate alerts using a database layer.

---

## 🚀 Live System Overview

This project is a fully automated pipeline that:

- Scrapes job postings from OnlineJobs.ph
- Extracts structured job data (title, salary, type, date)
- Stores jobs in a SQLite database for deduplication
- Detects new job postings only
- Sends real-time alerts via Telegram
- Runs 24/7 on cloud deployment (Railway)

---

## 🏗️ System Architecture
Job Source Website
↓
Python Scraper
↓
Data Parser / Cleaner
↓
SQLite Database (Deduplication)
↓
New Job Detection
↓
Telegram Bot API
↓
User Notifications

---

## ☁️ Deployment

The system is deployed on a cloud runtime using Railway for continuous 24/7 execution.

---

## 🛠️ Tech Stack

- Python
- BeautifulSoup (Web Scraping)
- Requests (HTTP calls)
- SQLite (Local database storage)
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

1. The scraper runs every few minutes
2. Extracts job listings from the website
3. Compares results with stored database
4. Filters only NEW jobs
5. Sends formatted message to Telegram
6. Stores job to prevent duplicates

---

## 🧠 Key Features

- ✔ Fully automated job tracking
- ✔ Duplicate prevention system
- ✔ Real-time Telegram alerts
- ✔ Cloud-based 24/7 execution
- ✔ Lightweight and scalable design

---

## 📌 Purpose

This project was built to demonstrate:

- Web scraping automation
- Backend pipeline design
- Cloud deployment (CI-style execution)
- Real-time notification systems
- Data deduplication logic

---

## 📁 Project Structure
job-alert-bot/
│── job_alert.py
│── requirements.txt
│── README.md
│── jobs.db (ignored in production)
│── .gitignore

---

## 🔒 Security Note

Sensitive credentials (Telegram bot token and chat ID) are stored using environment variables in production deployment.

---

## 📈 Future Improvements

- Multi-platform job scraping (LinkedIn, 104, etc.)
- AI-based job filtering (skills matching)
- Web dashboard for monitoring
- Advanced analytics (salary trends, job types)

---

## 📜 License

MIT License
