# GitHub Health Dashboard

An AI-powered tool that analyzes GitHub user portfolios and provides insights on repository health, activity, and community engagement.

## ✨ Features

- 🔍 **GitHub User Analysis**: Fetch and analyze all public repositories for any GitHub user
- 🌙 **Dashboard**: Modern, responsive UI with dark mode support
- 📈 **Visual Analytics**: Interactive charts showing activity, community, and issue trends
- 🤖 **AI Health Summaries**: AI-powered insights about repository health
- 📱 **Responsive Design**: Works on desktop and mobile devices

## 🚀 Live Demo

Visit the live application:
- **Render (Recommended):** https://github-healthcheck-dashboard.onrender.com
- **AWS EC2:** http://13.233.84.245 (initial deployment)

## 🛠️ Tech Stack

**Backend:**
- Python 3.9 + Flask
- GitHub API Integration
- Anthropic API (AI summaries)

**Frontend:**
- HTML/CSS/JavaScript
- Chart.js (Data visualization)
- Dark mode toggle

**DevOps & Deployment:**
- Docker (Containerization)
- AWS EC2 (Cloud hosting)
- Render (Modern cloud platform)
- Jenkins (CI/CD pipeline)

📋 Project Phases
Phase 1:Flask Backend + GitHub API ✅

Flask web application
GitHub API integration
Repository health scoring
Error handling
Phase 2:Dashboard UI ✅

Responsive interface
Chart.js visualizations
Dark/Light mode
Repository health summaries
Clean card-based layout
Phase 3: Deployment & DevOps ✅

Docker containerization
AWS EC2 deployment
Render deployment
Jenkins CI/CD pipeline


Installation
git clone https://github.com/YOUR_USERNAME/github-healthcheck-dashboard.git
cd github-healthcheck-dashboard

pip install -r requirements.txt
python app.py

Open http://localhost:5000 in your browser.

Run with Docker
docker build -t github-health-dashboard .
docker run -p 5000:5000 github-health-dashboard
📊 Scoring System

Each repository is evaluated using three scores (0–10):

Activity – Based on repository stars
Community – Based on stars and forks
Maintenance – Based on recent commit activity

Overall Health Score = Average of the three scores.

🎯 How It Works
Enter a GitHub username.
The app fetches public repositories using the GitHub API.
Repository health scores are calculated.
Results are displayed with charts and summaries.

License

👨‍💻 Author

Built as a portfolio project to demonstrate full-stack development, DevOps, and cloud deployment skills.

Built with ❤️ using Flask, Chart.js, Docker, and Cloud Platforms.