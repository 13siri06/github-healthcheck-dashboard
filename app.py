from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Route 1: Home page (shows input form)
@app.route('/')
def index():
    return render_template('index.html')

# Route 2: Process form (gets username, fetches repos)
@app.route('/search', methods=['POST'])
@app.route('/search', methods=['POST'])
def search():
    username = request.form.get('username')
    
    if not username:
        return "Please enter a username", 400
    
    # Fetch repos from GitHub API
    repos_data = fetch_github_repos(username)
    
    if repos_data is None:
        return f"User '{username}' not found on GitHub", 404
    
    # Calculate scores for each repo
    repos_with_scores = calculate_scores(repos_data)
    
    # Pass data to HTML template
    return render_template('results.html', username=username, repos=repos_with_scores)
def fetch_github_repos(username):
    """
    Fetch all public repos for a GitHub user
    """
    token = os.environ.get('GITHUB_TOKEN')
    
    # GitHub API URL
    url = f"https://api.github.com/users/{username}/repos"
    
    # Headers (token is optional, but increases rate limit)
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 404:
            return None  # User not found
        
        if response.status_code != 200:
            return None  # Some other error
        
        # Convert JSON to Python dictionary
        repos = response.json()
        return repos
    
    except Exception as e:
        print(f"Error: {e}")
        return None

def calculate_scores(repos):
    """
    Calculate 3 scores for each repo:
    - Activity: How active is the repo (commits)
    - Community: How popular is it (stars + forks)
    - Maintenance: Is it maintained (recent commits)
    """
    results = []
    
    for repo in repos:
        repo_name = repo.get('name')
        stars = repo.get('stargazers_count', 0)
        forks = repo.get('forks_count', 0)
        open_issues = repo.get('open_issues_count', 0)
        last_push = repo.get('pushed_at')  # Last commit date
        
        # Activity Score (0-10): Based on stars
        activity_score = min(10, stars // 10)
        
        # Community Score (0-10): Based on stars + forks
        community_score = min(10, (stars + forks) // 20)
        
        # Maintenance Score (0-10): Based on having recent activity
        if last_push:
            maintenance_score = 8  # Assume maintained if has push_at
        else:
            maintenance_score = 2  # Not maintained
        
        results.append({
            'name': repo_name,
            'activity': activity_score,
            'community': community_score,
            'maintenance': maintenance_score,
            'stars': stars,
            'forks': forks
        })
    
    return results

if __name__ == '__main__':
    app.run(debug=True)