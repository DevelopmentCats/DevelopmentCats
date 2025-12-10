#!/usr/bin/env python3
"""
Generate a dynamic GitHub profile README with AI-powered content generation.
This script fetches data from GitHub APIs and generates a beautiful README.

All image URLs use reliable, trusted services (shields.io, vercel.app) that
don't require runtime verification.
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Any
from pathlib import Path

# Import our constants and helpers
try:
    from constants import (
        TECH_STACK, SOCIAL_LINKS, get_skill_badge, 
        get_social_badge, get_stats_image, CODER_BLUE
    )
except ImportError:
    # If running from different directory
    sys.path.insert(0, str(Path(__file__).parent))
    from constants import (
        TECH_STACK, SOCIAL_LINKS, get_skill_badge,
        get_social_badge, get_stats_image, CODER_BLUE
    )

# Configuration
GITHUB_USERNAME = "DevelopmentCats"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
DATA_DIR = Path("data")
TEMPLATES_DIR = Path("templates")

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)


def fetch_github_data() -> Dict[str, Any]:
    """Fetch comprehensive GitHub data for the user."""
    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
    
    print("Fetching GitHub user data...")
    user_response = requests.get(
        f"https://api.github.com/users/{GITHUB_USERNAME}",
        headers=headers
    )
    user_data = user_response.json()
    
    print("Fetching repositories...")
    repos_response = requests.get(
        f"https://api.github.com/users/{GITHUB_USERNAME}/repos?sort=updated&per_page=100",
        headers=headers
    )
    repos = repos_response.json()
    
    print("Fetching recent activity...")
    events_response = requests.get(
        f"https://api.github.com/users/{GITHUB_USERNAME}/events/public?per_page=100",
        headers=headers
    )
    events = events_response.json()
    
    return {
        "user": user_data,
        "repos": repos,
        "events": events,
        "fetched_at": datetime.utcnow().isoformat()
    }


def get_coder_registry_stats(repos: List[Dict], events: List[Dict]) -> Dict[str, Any]:
    """Extract Coder Registry specific contributions."""
    print("Analyzing Coder Registry contributions...")
    
    # Find coder/registry related activity
    registry_prs = []
    registry_commits = []
    registry_issues = []
    
    for event in events:
        repo_name = event.get("repo", {}).get("name", "")
        
        if "coder/registry" in repo_name:
            event_type = event.get("type", "")
            payload = event.get("payload", {})
            created_at = event.get("created_at", "")
            
            if event_type == "PullRequestEvent":
                pr = payload.get("pull_request", {})
                registry_prs.append({
                    "action": payload.get("action", ""),
                    "title": pr.get("title", ""),
                    "number": pr.get("number", ""),
                    "state": pr.get("state", ""),
                    "url": pr.get("html_url", ""),
                    "created_at": created_at
                })
            
            elif event_type == "PushEvent":
                commits = payload.get("commits", [])
                for commit in commits:
                    registry_commits.append({
                        "message": commit.get("message", ""),
                        "sha": commit.get("sha", "")[:7],
                        "created_at": created_at
                    })
            
            elif event_type == "IssuesEvent":
                issue = payload.get("issue", {})
                registry_issues.append({
                    "action": payload.get("action", ""),
                    "title": issue.get("title", ""),
                    "number": issue.get("number", ""),
                    "url": issue.get("html_url", ""),
                    "created_at": created_at
                })
    
    return {
        "prs": registry_prs[:5],  # Latest 5 PRs
        "commits": registry_commits[:10],  # Latest 10 commits
        "issues": registry_issues[:5],  # Latest 5 issues
        "total_prs": len(registry_prs),
        "total_commits": len(registry_commits),
        "total_issues": len(registry_issues)
    }


def get_language_stats(repos: List[Dict]) -> Dict[str, int]:
    """Calculate language usage across repositories."""
    print("Calculating language statistics...")
    
    languages = {}
    for repo in repos:
        if repo.get("fork", False):
            continue  # Skip forked repos
        
        lang = repo.get("language")
        if lang:
            languages[lang] = languages.get(lang, 0) + 1
    
    # Sort by usage
    return dict(sorted(languages.items(), key=lambda x: x[1], reverse=True))


def get_recent_activity(events: List[Dict]) -> List[Dict[str, str]]:
    """Get recent meaningful activity."""
    print("Processing recent activity...")
    
    activity = []
    seen_events = set()
    
    for event in events:
        event_type = event.get("type", "")
        repo_name = event.get("repo", {}).get("name", "")
        created_at = event.get("created_at", "")
        payload = event.get("payload", {})
        
        # Create a unique key to avoid duplicates
        event_key = f"{event_type}_{repo_name}_{created_at}"
        if event_key in seen_events:
            continue
        seen_events.add(event_key)
        
        activity_item = None
        
        if event_type == "PushEvent":
            commits = payload.get("commits", [])
            if commits:
                activity_item = {
                    "type": "push",
                    "icon": "📝",
                    "description": f"Pushed {len(commits)} commit(s) to {repo_name}",
                    "date": created_at
                }
        
        elif event_type == "PullRequestEvent":
            pr = payload.get("pull_request", {})
            action = payload.get("action", "")
            if action in ["opened", "closed"]:
                status = "merged" if pr.get("merged", False) else action
                activity_item = {
                    "type": "pr",
                    "icon": "🔀" if status == "merged" else "🎯",
                    "description": f"Pull Request {status}: {pr.get('title', '')} in {repo_name}",
                    "date": created_at,
                    "url": pr.get("html_url", "")
                }
        
        elif event_type == "IssuesEvent":
            issue = payload.get("issue", {})
            action = payload.get("action", "")
            if action in ["opened", "closed"]:
                activity_item = {
                    "type": "issue",
                    "icon": "🐛" if action == "opened" else "✅",
                    "description": f"Issue {action}: {issue.get('title', '')} in {repo_name}",
                    "date": created_at,
                    "url": issue.get("html_url", "")
                }
        
        elif event_type == "CreateEvent":
            ref_type = payload.get("ref_type", "")
            if ref_type in ["repository", "branch", "tag"]:
                activity_item = {
                    "type": "create",
                    "icon": "🎉",
                    "description": f"Created {ref_type} in {repo_name}",
                    "date": created_at
                }
        
        elif event_type == "ReleaseEvent":
            release = payload.get("release", {})
            activity_item = {
                "type": "release",
                "icon": "🚀",
                "description": f"Released {release.get('tag_name', '')} in {repo_name}",
                "date": created_at,
                "url": release.get("html_url", "")
            }
        
        if activity_item:
            activity.append(activity_item)
            
            if len(activity) >= 10:  # Limit to 10 activities
                break
    
    return activity


def format_date(date_str: str) -> str:
    """Format ISO date string to readable format."""
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        now = datetime.now(dt.tzinfo)
        diff = now - dt
        
        if diff.days == 0:
            if diff.seconds < 3600:
                minutes = diff.seconds // 60
                return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
            else:
                hours = diff.seconds // 3600
                return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif diff.days == 1:
            return "yesterday"
        elif diff.days < 7:
            return f"{diff.days} days ago"
        elif diff.days < 30:
            weeks = diff.days // 7
            return f"{weeks} week{'s' if weeks != 1 else ''} ago"
        else:
            return dt.strftime("%b %d, %Y")
    except:
        return date_str


def generate_ai_instructions() -> str:
    """Generate instructions for AI to use when generating README content."""
    return """
# GitHub Profile README Generation Instructions

You are generating a GitHub profile README for DevelopmentCats, a full-stack developer who actively contributes to the Coder Registry.

## Key Points to Highlight:
1. Active contributions to Coder Registry (coder/registry)
2. Full-stack development expertise
3. Focus on cloud development environments and developer tooling
4. Community engagement and open source contributions

## Tone & Style:
- Professional yet approachable
- Clear and easy to understand
- Highlight technical skills without jargon overload
- Show genuine passion for developer tools and Coder ecosystem

## Content Sections:
1. Engaging header with role and focus area
2. Current work (Coder Registry contributions)
3. Recent activity highlights
4. Technical skills (organized by category)
5. GitHub statistics
6. How to connect

## Design Principles:
- Use emojis sparingly and meaningfully
- Keep content scannable with clear sections
- Include visual elements (badges, stats, graphs)
- Make it easy to understand what you do and what you're working on

Use the provided data to create an informative and visually appealing README.
"""


def generate_readme(github_data: Dict[str, Any]) -> str:
    """Generate the README content."""
    print("Generating README content...")
    
    user = github_data["user"]
    repos = github_data["repos"]
    events = github_data["events"]
    
    # Extract statistics
    coder_stats = get_coder_registry_stats(repos, events)
    language_stats = get_language_stats(repos)
    recent_activity = get_recent_activity(events)
    
    # Save data for reference
    with open(DATA_DIR / "github_stats.json", "w") as f:
        json.dump({
            "coder_stats": coder_stats,
            "language_stats": language_stats,
            "recent_activity": recent_activity,
            "updated_at": datetime.utcnow().isoformat()
        }, f, indent=2)
    
    # Get top languages (limit to 8)
    top_languages = list(language_stats.keys())[:8]
    
    # Build README content
    readme = f"""<h1 align="center">Hi 👋, I'm DevelopmentCats</h1>
<h3 align="center">Full-Stack Developer | Coder Registry Contributor</h3>

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=developmentcats&label=Profile%20views&color=0e75b6&style=flat" alt="profile views" />
  <a href="https://github.com/coder/registry"><img src="https://img.shields.io/badge/Coder-Registry-00ADD8?style=flat&logo=coder&logoColor=white" alt="Coder Registry" /></a>
</p>

---

## 🚀 What I'm Working On

I'm actively contributing to the **[Coder Registry](https://github.com/coder/registry)**, building Terraform modules that help developers create better cloud development environments.

"""

    # Add Coder Registry stats if available
    if coder_stats["total_prs"] > 0 or coder_stats["total_commits"] > 0:
        readme += f"""### 📊 Coder Registry Contributions

"""
        
        if coder_stats["prs"]:
            readme += "**Recent Pull Requests:**\n\n"
            for pr in coder_stats["prs"][:3]:
                status_emoji = "✅" if pr["state"] == "closed" else "🔄"
                readme += f"- {status_emoji} [{pr['title']}]({pr['url']}) · {format_date(pr['created_at'])}\n"
            readme += "\n"
        
        if coder_stats["commits"]:
            readme += "**Recent Commits:**\n\n"
            for commit in coder_stats["commits"][:5]:
                # Clean up commit message (first line only)
                message = commit["message"].split("\n")[0]
                if len(message) > 60:
                    message = message[:57] + "..."
                readme += f"- `{commit['sha']}` {message}\n"
            readme += "\n"

    # Recent Activity
    readme += """---

## 📈 Recent Activity

"""
    
    for activity in recent_activity[:8]:
        line = f"- {activity['icon']} {activity['description']}"
        if "url" in activity:
            # Extract last part for cleaner display
            line = f"- {activity['icon']} {activity['description']}"
        line += f" · *{format_date(activity['date'])}*"
        readme += line + "\n"
    
    readme += """
---

## 🛠️ Tech Stack

"""

    # Use predefined tech stack from constants (all verified)
    for category, tools in TECH_STACK.items():
        readme += f"### {category}\n\n"
        for name, slug, color in tools:
            readme += get_skill_badge(name, slug, color) + " "
        readme += "\n\n"

    # GitHub Stats (using helper functions for consistent, reliable URLs)
    readme += f"""---

## 📊 GitHub Statistics

<p align="center">
  {get_stats_image(GITHUB_USERNAME, "stats")}
</p>

<p align="center">
  {get_stats_image(GITHUB_USERNAME, "streak")}
</p>

<p align="center">
  {get_stats_image(GITHUB_USERNAME, "languages")}
</p>

---

## 🤝 Connect With Me

<p align="left">
"""
    
    # Add social links from constants
    for platform, url in SOCIAL_LINKS:
        readme += "  " + get_social_badge(platform, GITHUB_USERNAME, url) + "\n"
    
    readme += """</p>

---

## 💡 Featured Projects

Check out my portfolio at **[developmentcats.github.io](https://developmentcats.github.io)**

---

<p align="center">
  <i>✨ This README is automatically updated every 6 hours using GitHub Actions and Coder's create-task-action ✨</i>
</p>

<p align="center">
  <sub>Last updated: {datetime.utcnow().strftime('%B %d, %Y at %H:%M UTC')}</sub>
</p>
"""

    return readme


def main():
    """Main execution function."""
    try:
        print("=" * 60)
        print("GitHub Profile README Generator")
        print("=" * 60)
        
        # Fetch data
        github_data = fetch_github_data()
        
        # Save raw data
        with open(DATA_DIR / "github_data.json", "w") as f:
            json.dump(github_data, f, indent=2)
        
        # Generate README
        readme_content = generate_readme(github_data)
        
        # Write README
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        print("=" * 60)
        print("✅ README.md successfully generated!")
        print("=" * 60)
        
        return 0
    
    except Exception as e:
        print(f"❌ Error generating README: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

