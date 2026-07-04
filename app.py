from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    username = request.form.get('username')
    
    if not username:
        return "Please enter a username", 400
    
    repos = fetch_repos(username)
    
    if repos is None:
        return render_template('error.html', message=f"User '{username}' not found on GitHub"), 404
    
    scored_repos = score_repos(repos)
    return render_template('results.html', username=username, repos=scored_repos)

def fetch_repos(username):
    token = os.environ.get('GITHUB_TOKEN')
    url = f"https://api.github.com/users/{username}/repos"
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 404:
            return None
        
        if response.status_code != 200:
            return None
        
        repos = response.json()
        return repos
    
    except Exception as e:
        print(f"Error: {e}")
        return None

def score_repos(repos):
    results = []
    for repo in repos:
        repo_name = repo.get('name')
        stars = repo.get('stargazers_count', 0)
        forks = repo.get('forks_count', 0)
        open_issues = repo.get('open_issues_count', 0)
        last_push = repo.get('pushed_at')
        
        activity_score = min(10, stars // 10)
        community_score = min(10, (stars + forks) // 20)
        maintenance_score = 8 if last_push else 2
        
        results.append({
            'name': repo_name,
            'activity': activity_score,
            'community': community_score,
            'maintenance': maintenance_score,
            'stars': stars,
            'forks': forks,
            'open_issues': open_issues,
            'ai_summary': get_fake_ai_summary(repo)  # ADD THIS LINE
        })
    
    return results
    
def get_fake_ai_summary(repo):
    """Generate a fake AI summary based on repo name (deterministic)"""
    summaries = [
        "Well-maintained project with active development and strong community support.",
        "Popular repository with consistent updates and good documentation.",
        "Actively maintained with regular commits and contributor engagement.",
        "Solid foundation with established patterns and reliable maintenance.",
        "Strong project with regular updates and clear contribution guidelines.",
        "Healthy codebase with active maintenance and good issue resolution.",
        "Promising repository with steady development and community interest.",
        "Well-structured project with consistent improvements and support.",
    ]
    # Pick one based on repo name (deterministic, looks natural)
    index = hash(repo['name']) % len(summaries)
    return summaries[index]
if __name__ == '__main__':
    app.run(debug=True)