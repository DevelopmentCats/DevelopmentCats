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
    """Calculate comprehensive language usage across all repositories."""
    print("Calculating language statistics...")
    
    languages = {}
    
    # Get languages from each repo
    for repo in repos:
        if repo.get("fork", False):
            continue  # Skip forked repos
        
        # Primary language
        primary_lang = repo.get("language")
        if primary_lang:
            languages[primary_lang] = languages.get(primary_lang, 0) + 1
        
        # Try to get detailed language breakdown if available
        # Note: This would require additional API calls per repo
        # For now, we count primary languages which is what GitHub shows
    
    # Sort by usage (most used first)
    return dict(sorted(languages.items(), key=lambda x: x[1], reverse=True))


def get_all_languages_comprehensive(repos: List[Dict]) -> List[str]:
    """
    Get ALL languages detected across repos, even if used rarely.
    This gives Claude the full picture of what you know.
    """
    print("Collecting all languages (comprehensive)...")
    
    all_languages = set()
    
    for repo in repos:
        if repo.get("fork", False):
            continue
        
        lang = repo.get("language")
        if lang:
            all_languages.add(lang)
    
    # Return sorted list (alphabetically for consistency)
    return sorted(list(all_languages))


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
    """
    Generate README data for AI to use.
    
    This function now focuses on preparing clean data for the AI to use
    when crafting the actual README. The AI has creative freedom to
    format and present this information in an engaging way.
    """
    print("Preparing README data for AI generation...")
    
    user = github_data["user"]
    repos = github_data["repos"]
    events = github_data["events"]
    
    # Extract statistics
    coder_stats = get_coder_registry_stats(repos, events)
    language_stats = get_language_stats(repos)
    all_languages = get_all_languages_comprehensive(repos)
    recent_activity = get_recent_activity(events)
    
    # Save comprehensive data for AI to use
    readme_data = {
        "user": {
            "username": user.get("login"),
            "name": user.get("name"),
            "bio": user.get("bio"),
            "public_repos": user.get("public_repos"),
            "followers": user.get("followers"),
            "following": user.get("following"),
        },
        "coder_stats": coder_stats,
        "languages": {
            "by_repo_count": language_stats,  # Languages sorted by how many repos use them
            "all_detected": all_languages,     # ALL languages found (comprehensive list)
            "top_8": list(language_stats.keys())[:8],  # Top 8 most used
            "total_count": len(all_languages)
        },
        "recent_activity": recent_activity,
        "updated_at": datetime.utcnow().isoformat(),
        "instructions": {
            "note": "Use constants.py helpers for all badges - they guarantee working URLs",
            "guidelines": "Read scripts/ai_guidelines.md for styling and creative patterns",
            "social_links": "Defined in constants.USER_SOCIAL_LINKS",
            "tech_reference": "Use constants.COMMON_TECH for icon slugs and colors",
            "all_languages_available": "languages.all_detected has EVERY language detected"
        }
    }
    
    with open(DATA_DIR / "github_stats.json", "w") as f:
        json.dump(readme_data, f, indent=2)
    
    print(f"✅ Data saved to {DATA_DIR / 'github_stats.json'}")
    print(f"   - {coder_stats['total_prs']} Coder Registry PRs")
    print(f"   - {len(recent_activity)} recent activities")
    print(f"   - {len(all_languages)} total languages detected")
    print(f"   - Top languages: {', '.join(list(language_stats.keys())[:5])}")
    print("\n🎨 AI can now generate README with this data!")
    
    # Return a simple confirmation instead of a full README
    # The AI will generate the actual README using the data file
    return f"""# Data Generated Successfully

The GitHub stats have been saved to `data/github_stats.json`.

## Summary:
- **Coder Registry**: {coder_stats['total_prs']} PRs, {coder_stats['total_commits']} commits
- **Languages**: {', '.join(list(language_stats.keys())[:5])}
- **Recent Activity**: {len(recent_activity)} events

## Next Steps:
The AI should now read `data/github_stats.json` and create an engaging README.md file.

## Guidelines:
- Use helpers from `scripts/constants.py` for all badges
- Read `scripts/ai_guidelines.md` for creative patterns
- Make it visually appealing and not generic
- Highlight Coder Registry work prominently
- Show personality!

Generated at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}
"""


def main():
    """
    Main execution: Fetch GitHub data and prepare it for AI generation.
    
    This script now focuses on data collection, not README generation.
    The AI (Claude) will use this data to create a creative, engaging README.
    """
    try:
        print("=" * 70)
        print("GitHub Data Fetcher - README Generator Helper")
        print("=" * 70)
        print()
        
        # Fetch fresh data from GitHub
        print("📡 Fetching GitHub data...")
        github_data = fetch_github_data()
        
        # Save raw data for reference
        print("💾 Saving raw data...")
        with open(DATA_DIR / "github_data.json", "w") as f:
            json.dump(github_data, f, indent=2)
        
        # Process and prepare data for AI
        print("🔄 Processing statistics...")
        status_message = generate_readme(github_data)
        
        print()
        print("=" * 70)
        print(status_message)
        print("=" * 70)
        print()
        print("✨ Data ready! AI can now generate the README.")
        print("   Read: data/github_stats.json")
        print("   Guidelines: scripts/ai_guidelines.md")
        print("   Helpers: scripts/constants.py")
        print()
        
        return 0
    
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

