# ⚡ StreamPulse Analytics (Real-Time Dashboard)

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-API-000000?logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)
![Chart.js](https://img.shields.io/badge/Frontend-Chart.js-FF6384?logo=chartdotjs&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-EC2-FF9900?logo=amazon-aws&logoColor=white)

### 🚧 Project Status: Live & Deployed

StreamPulse is a full-stack cloud application that visualizes Twitch chat engagement in real-time. Unlike standard bots, it captures data points, stores them in a time-series database, and renders a live "Hype Graph" on a web dashboard via a REST API. It is designed to be embedded in OBS overlays.

---

## 🔗 VISUAL PORTFOLIO & BUSINESS CASE
**To see the Live Dashboard Demo, Architecture Diagram, and how I pitch this SaaS to streamers, please visit my Notion Portfolio:**

### [👉 VIEW FULL PROJECT DOCS ON NOTION 👈](https://www.notion.so/Alvaro-Arroyo-Cloud-Solutions-2b853608ee2980c2a382d7ecc8cc57ed)

---

## 🏗️ System Architecture
1.  **Data Collector (Backend):** A Python bot listens to IRC events and logs messages + timestamps into SQLite.
2.  **Persistence Layer (Database):** SQLite stores historical data to calculate trends (messages per minute).
3.  **API Layer (Flask):** Exposes a JSON endpoint (`/api/stats`) that aggregates SQL data.
4.  **Visualization (Frontend):** JavaScript fetches data every 3s and renders a smooth curve using Chart.js.

## ⚡ Key Features
* **Live Hype Graph:** Dynamic line chart updating in real-time without page reloads (AJAX).
* **Recent Activity Ticker:** Animated feed of the last 5 active users.
* **0% Client Load:** Runs entirely on AWS EC2, consuming no resources on the streamer's PC.
* **Dark Mode UI:** Designed to fit gaming aesthetics.

## 🛠️ Tech Stack
* **Backend:** Python 3, Flask, TwitchIO
* **Database:** SQLite3
* **Frontend:** HTML5, CSS3, Chart.js
* **Deployment:** AWS EC2 (Ubuntu 24.04 LTS) + PM2 (Process Manager)

## 🚀 Installation (Local Dev)

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/alvaroarroyov/AWS-PM2-Discord-Guardian.git]
    cd StreamPulse-Analytics
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Setup**
    Create a `.env` file with your Twitch credentials:
    ```env
    TMI_TOKEN=oauth:your_token
    PREFIX=!
    CHANNEL=target_channel
    ```

4.  **Initialize Database** (Crucial Step)
    Run this script once to create the SQLite table:
    ```bash
    python init_db.py
    ```

5.  **Run the System**
    You need two terminals (or use PM2):
    * Terminal 1 (The Spy): `python bot.py`
    * Terminal 2 (The Web): `python app.py`

    Then open `http://localhost:5000` in your browser.

---
*Built by Alvaro Arroyo - Cybersecurity Student & Cloud Builder.*
