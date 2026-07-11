# 🚀 GitHub HealthCheck Dashboard

An intelligent web application that analyzes GitHub user profiles and provides insights into repository health, activity, and community engagement.

---

## ✨ Features

* 🔍 Analyze all public repositories of any GitHub user
* 📊 Interactive dashboard with Chart.js visualizations
* 🤖 Repository health summaries
* 🌙 Dark/Light mode support
* 📱 Responsive design for desktop and mobile
* 🚀 Cloud deployment with Docker and CI/CD

---

## 🛠️ Tech Stack

### Backend

* Python 3.9
* Flask
* GitHub REST API

### Frontend

* HTML
* CSS
* JavaScript
* Chart.js

### DevOps & Cloud

* Docker
* AWS EC2
* Render
* Jenkins (CI/CD)

---

## 📋 Project Phases

### ✅ Phase 1 – Backend Development

* Flask web application
* GitHub API integration
* Repository health scoring
* Error handling

### ✅ Phase 2 – Dashboard UI

* Responsive interface
* Interactive charts
* Dark/Light mode
* Repository health summaries
* Card-based layout

### ✅ Phase 3 – DevOps & Deployment

* Docker containerization
* AWS EC2 deployment
* Render deployment
* Jenkins CI/CD pipeline

---

## 🚀 Installation

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/github-healthcheck-dashboard.git
cd github-healthcheck-dashboard
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python app.py
```

Open your browser and visit:

```text
http://localhost:5000
```

---

## 🐳 Run with Docker

Build the Docker image:

```bash
docker build -t github-health-dashboard .
```

Run the container:

```bash
docker run -p 5000:5000 github-health-dashboard
```

---

## 📊 Repository Scoring

Each repository receives three scores (0–10):

| Metric         | Based On               |
| -------------- | ---------------------- |
| ⭐ Activity     | Repository stars       |
| 👥 Community   | Stars + forks          |
| 🔧 Maintenance | Recent commit activity |

**Overall Health Score = Average of the three scores**

---

## ⚙️ How It Works

1. Enter a GitHub username.
2. The application fetches all public repositories.
3. Repository metrics are analyzed.
4. Health scores are calculated.
5. Interactive charts and summaries are displayed.

---

## 📸 Dashboard Preview

> Add screenshots or a GIF of your application here.

---

## 📈 Future Enhancements

* GitHub OAuth login
* AI-generated repository insights
* Export reports as PDF
* GitHub Webhooks
* Advanced filtering and sorting
* Language-wise analytics
* Contributor insights

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

Built as a portfolio project to demonstrate:

* Full-Stack Development
* API Integration
* Docker & Containerization
* Cloud Deployment
* DevOps & CI/CD

---

**⭐ If you found this project useful, consider giving it a star!**
