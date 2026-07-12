# 🚀 GitHub HealthCheck Dashboard

Analyzes any GitHub user's public repos and shows health scores, charts, and an AI-generated summary.

**Live app:** [ https://github-healthcheck-dashboard.onrender.com]


**Backend / CI:** [AWS EC2 —  http://13.233.84.245]

---

## ✨ Features

- Analyzes all public repos for any GitHub username
- Repo health scores: Activity, Community, Maintenance
- Interactive Chart.js dashboard (commit trends, issue stats)
- AI-generated health summary via the Anthropic API
- Error handling for invalid users / rate limits
- Auto-deploys on every push (Jenkins → Docker Hub → Render)

---

## 🛠️ Tech Stack

**Backend:** Python, Flask, GitHub REST API, Anthropic API
**Frontend:** HTML, CSS, JavaScript, Chart.js
**DevOps:** Docker, Jenkins, AWS EC2, Render

---

## ⚙️ How It Works

1. Enter a GitHub username
2. App fetches all public repos via the GitHub API
3. Computes Activity / Community / Maintenance scores
4. Anthropic API generates a short health summary
5. Dashboard renders charts + scores + summary

---

## 🚀 Run Locally

```bash
git clone https://github.com/YOUR_USERNAME/github-healthcheck-dashboard.git
cd github-healthcheck-dashboard
pip install -r requirements.txt
python app.py
```

Visit `http://localhost:5000`

---

## 🐳 Run with Docker

```bash
docker build -t github-health-dashboard .
docker run -p 5000:5000 github-health-dashboard
```

---

## 📦 Deployment Pipeline

EC2 (Jenkins) builds the Docker image on every push → pushes to Docker Hub → Render pulls the image and serves the live app. If EC2 ever stops, Render can be pointed directly at the GitHub repo to keep auto-deploys running without it.

---

