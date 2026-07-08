from flask import Flask, render_template, request
import requests
import os
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
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

    token = os.environ.get('GITHUB_TOKEN')

    repos = fetch_repos(username, token)

    if repos is None:
        return render_template('error.html', message=f"User '{username}' not found on GitHub"), 404

    scored_repos = score_repos(repos, username, token)
    return render_template('results.html', username=username, repos=scored_repos)


def fetch_repos(username, token=None):
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

        return response.json()

    except Exception as e:
        print(f"Error fetching repos: {e}")
        return None


def fetch_repo_details(username, repo_name, token=None):
    """
    Pulls deeper signals for a single repo: recent commit activity,
    contributor count, and issue close ratio.

    NOTE: GitHub's /stats/commit_activity endpoint can return a 202 status
    on the first request for a repo, meaning it's still computing stats in
    the background rather than returning real data immediately. This code
    treats any non-200 response as "0 recent commits" for now, which will
    understate activity the first time a repo is analyzed. A retry-with-delay
    would fix this properly but isn't implemented here.
    """
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'

    base_url = f"https://api.github.com/repos/{username}/{repo_name}"
    details = {
        'recent_commits': 0,
        'contributors_count': 0,
        'closed_issue_ratio': 0,
        'has_license': False
    }

    try:
        commit_resp = requests.get(f"{base_url}/stats/commit_activity", headers=headers)
        if commit_resp.status_code == 200:
            weekly_data = commit_resp.json()
            if isinstance(weekly_data, list) and len(weekly_data) >= 4:
                details['recent_commits'] = sum(week['total'] for week in weekly_data[-4:])

        contrib_resp = requests.get(f"{base_url}/contributors", headers=headers)
        if contrib_resp.status_code == 200:
            details['contributors_count'] = len(contrib_resp.json())

        issues_resp = requests.get(f"{base_url}/issues?state=all&per_page=100", headers=headers)
        if issues_resp.status_code == 200:
            issues = [i for i in issues_resp.json() if 'pull_request' not in i]
            if issues:
                closed = sum(1 for i in issues if i['state'] == 'closed')
                details['closed_issue_ratio'] = closed / len(issues)

    except Exception as e:
        print(f"Error fetching details for {repo_name}: {e}")

    return details


def calculate_activity_score(recent_commits, last_push):
    """
    Primary signal: commits in the last 4 weeks (from GitHub's stats API).
    Falls back to days-since-last-push if commit stats are unavailable
    (e.g. GitHub hasn't cached them yet, or the repo has no commit history).

    The specific thresholds below are my own heuristic, not an official
    GitHub metric or published standard - adjust freely.
    """
    if recent_commits and recent_commits > 0:
        if recent_commits >= 20:
            return 10
        elif recent_commits >= 10:
            return 8
        elif recent_commits >= 5:
            return 6
        elif recent_commits >= 1:
            return 4

    if not last_push:
        return 0

    try:
        pushed_date = datetime.strptime(last_push, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
        days_since = (datetime.now(timezone.utc) - pushed_date).days
    except Exception:
        return 0

    if days_since <= 7:
        return 8
    elif days_since <= 30:
        return 6
    elif days_since <= 90:
        return 4
    elif days_since <= 365:
        return 2
    else:
        return 1


def calculate_community_score(stars, forks, watchers, contributors_count):
    """
    Weighted combination of stars, forks (weighted higher - forking implies
    deeper engagement than starring), watchers, and distinct contributors.

    These weights are my own heuristic, not an official GitHub metric -
    treat this as a reasonable starting point, not a "correct" formula.
    """
    total = stars + (forks * 2) + watchers + (contributors_count * 3)

    if total == 0:
        return 0
    elif total <= 2:
        return 2
    elif total <= 5:
        return 4
    elif total <= 10:
        return 6
    elif total <= 25:
        return 8
    else:
        return 10


def calculate_maintenance_score(last_push, archived, closed_issue_ratio, has_license):
    """
    Archived repos score 0 (GitHub explicitly marks these as inactive).
    Otherwise combines recency of activity, how many issues get closed,
    and whether a license is present, as a proxy for project seriousness.
    """
    if archived:
        return 0

    if not last_push:
        return 1

    try:
        pushed_date = datetime.strptime(last_push, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc)
        days_since = (datetime.now(timezone.utc) - pushed_date).days
    except Exception:
        days_since = 9999

    recency_score = 8 if days_since <= 90 else (4 if days_since <= 365 else 1)
    issue_score = closed_issue_ratio * 10  # 0 to 10 based on % of issues closed
    license_bonus = 1 if has_license else 0

    combined = (recency_score * 0.5) + (issue_score * 0.4) + license_bonus
    return round(min(10, combined))


def get_fake_ai_summary(repo):
    """
    Placeholder for the real Anthropic API call described in the original
    project brief. This currently picks a deterministic canned sentence
    based on repo name - it is NOT a real AI-generated summary yet.
    """
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
    index = hash(repo.get('name', '')) % len(summaries)
    return summaries[index]


def score_one_repo(repo, username, token=None):
    """
    Scores a single repo. Pulled out of score_repos so it can be run
    concurrently across repos via ThreadPoolExecutor.
    """
    repo_name = repo.get('name')
    stars = repo.get('stargazers_count', 0)
    forks = repo.get('forks_count', 0)
    watchers = repo.get('watchers_count', 0)
    last_push = repo.get('pushed_at')
    archived = repo.get('archived', False)
    has_license = repo.get('license') is not None

    details = fetch_repo_details(username, repo_name, token)

    activity_score = calculate_activity_score(details['recent_commits'], last_push)
    community_score = calculate_community_score(
        stars, forks, watchers, details['contributors_count']
    )
    maintenance_score = calculate_maintenance_score(
        last_push, archived, details['closed_issue_ratio'], has_license
    )

    return {
        'name': repo_name,
        'stars': stars,
        'forks': forks,
        'open_issues': repo.get('open_issues_count', 0),
        'activity': activity_score,
        'community': community_score,
        'maintenance': maintenance_score,
        'last_push': last_push,
        'recent_commits': details['recent_commits'],
        'contributors_count': details['contributors_count'],
        'closed_issue_ratio': round(details['closed_issue_ratio'] * 100),
        'has_license': has_license,
        'ai_summary': get_fake_ai_summary(repo)
    }


def score_repos(repos, username, token=None, max_workers=8):
    """
    Scores all repos concurrently instead of one at a time. Each repo still
    makes 3 API calls internally (commit activity, contributors, issues),
    but those calls now happen in parallel across repos rather than
    sequentially, which is the main source of the previous slowdown.

    max_workers=8 is a starting point, not a tuned/benchmarked number -
    raising it fetches faster but burns through your GitHub rate limit
    faster too, so adjust based on how many repos you're typically scoring
    and whether you're using an authenticated token (5000/hr) or not (60/hr).
    """
    results = [None] * len(repos)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_index = {
            executor.submit(score_one_repo, repo, username, token): i
            for i, repo in enumerate(repos)
        }

        for future in future_to_index:
            index = future_to_index[future]
            try:
                results[index] = future.result()
            except Exception as e:
                print(f"Error scoring repo at index {index}: {e}")
                repo = repos[index]
                results[index] = {
                    'name': repo.get('name', 'unknown'),
                    'stars': repo.get('stargazers_count', 0),
                    'forks': repo.get('forks_count', 0),
                    'open_issues': repo.get('open_issues_count', 0),
                    'activity': 0,
                    'community': 0,
                    'maintenance': 0,
                    'last_push': repo.get('pushed_at'),
                    'recent_commits': 0,
                    'contributors_count': 0,
                    'closed_issue_ratio': 0,
                    'has_license': False,
                    'ai_summary': 'Unable to fully analyze this repository.'
                }

    return results


if __name__ == '__main__':
    app.run(debug=True)