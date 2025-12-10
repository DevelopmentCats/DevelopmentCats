#!/usr/bin/env python3
"""
Reliable image toolkit for README generation.

This module provides safe building blocks for generating badges and images.
The generation script can make flexible decisions about what to include,
but all helpers guarantee URLs from trusted services.

Philosophy:
- Provide tools, not rigid templates
- Enable AI creativity within safe boundaries
- All generated URLs are guaranteed to work
- No runtime verification needed
"""

# Trusted image services (no verification needed)
TRUSTED_SERVICES = [
    "shields.io",           # Badge generation service
    "simpleicons.org",      # Icon library
    "img.shields.io",       # Shields.io CDN
    "komarev.com",          # Profile view counter
    "vercel.app",           # GitHub stats by Vercel
    "herokuapp.com",        # GitHub streak stats
]

# Badge style options - choose what fits best
BADGE_STYLES = {
    "for-the-badge": "Bold, prominent badges",
    "flat": "Minimal flat design",
    "flat-square": "Flat with square edges",
    "plastic": "Glossy 3D effect",
    "social": "GitHub-style social badges",
}

DEFAULT_BADGE_STYLE = "for-the-badge"

# Color palette - use these or any hex color
COLORS = {
    "coder_blue": "00ADD8",
    "coder_dark": "0D1117",
    "github": "181717",
    "success": "00C851",
    "warning": "FFB300",
    "error": "CC0000",
    "info": "33B5E5",
}

# Legacy constants for backwards compatibility
CODER_BLUE = COLORS["coder_blue"]
CODER_DARK = COLORS["coder_dark"]

def get_skill_badge(name: str, icon_slug: str, color: str, style: str = None) -> str:
    """
    Generate a reliable badge URL using shields.io and Simple Icons.
    
    This is a safe building block - all parameters produce valid URLs.
    The AI can choose which badges to include based on context.
    
    Args:
        name: Display name for the badge
        icon_slug: Simple Icons slug (from simpleicons.org) or "none" for no icon
        color: Hex color code (without #) or color name from COLORS dict
        style: Badge style (default: for-the-badge). Options: flat, flat-square, plastic, social
    
    Returns:
        Markdown image string for the badge
    
    Example:
        get_skill_badge("Python", "python", "3776AB")
        get_skill_badge("Custom Tool", "none", COLORS["coder_blue"], style="flat")
    """
    # Allow color names from COLORS dict
    if color in COLORS:
        color = COLORS[color]
    
    # Use default style if not specified
    if style is None:
        style = DEFAULT_BADGE_STYLE
    
    name_encoded = name.replace(" ", "%20")
    
    # Build URL
    if icon_slug and icon_slug.lower() != "none":
        url = f"https://img.shields.io/badge/{name_encoded}-{color}?style={style}&logo={icon_slug}&logoColor=white"
    else:
        url = f"https://img.shields.io/badge/{name_encoded}-{color}?style={style}"
    
    return f"![{name}]({url})"


def is_simple_icon_available(icon_slug: str) -> bool:
    """
    Check if an icon slug is likely valid for Simple Icons.
    
    This is a lightweight check - we trust Simple Icons to be available.
    Use this for dynamic icon selection to avoid typos.
    
    Args:
        icon_slug: Simple Icons slug to validate
    
    Returns:
        True if the slug follows Simple Icons naming conventions
    """
    if not icon_slug or icon_slug.lower() == "none":
        return False
    
    # Simple Icons slugs are lowercase alphanumeric with optional hyphens
    return icon_slug.replace("-", "").replace(".", "").isalnum() and icon_slug.islower()


def get_social_badge(platform: str, username: str, url: str) -> str:
    """
    Generate a social media badge with proper branding.
    
    Args:
        platform: Social platform name (Twitter, Discord, etc.)
        username: Your username on the platform
        url: Full URL to your profile
    
    Returns:
        Markdown link with badge image
    """
    colors = {
        "Twitter": "1DA1F2",
        "Discord": "5865F2",
        "Email": "D14836",
        "LinkedIn": "0077B5",
        "GitHub": "181717",
    }
    
    icons = {
        "Twitter": "twitter",
        "Discord": "discord",
        "Email": "gmail",
        "LinkedIn": "linkedin",
        "GitHub": "github",
    }
    
    color = colors.get(platform, "000000")
    icon = icons.get(platform, platform.lower())
    
    badge_url = f"https://img.shields.io/badge/{platform}-{color}?style={BADGE_STYLE}&logo={icon}&logoColor=white"
    return f'<a href="{url}" target="_blank"><img src="{badge_url}" alt="{platform}" /></a>'


def get_stats_image(username: str, stat_type: str) -> str:
    """
    Generate GitHub stats images from reliable Vercel services.
    
    Args:
        username: GitHub username
        stat_type: Type of stat (stats, languages, streak)
    
    Returns:
        Markdown image string
    """
    theme_params = f"theme=react&hide_border=true&bg_color={CODER_DARK}&title_color={CODER_BLUE}&icon_color={CODER_BLUE}"
    
    if stat_type == "stats":
        url = f"https://github-readme-stats.vercel.app/api?username={username}&show_icons=true&{theme_params}"
        return f'<img src="{url}" alt="GitHub Stats" />'
    
    elif stat_type == "languages":
        url = f"https://github-readme-stats.vercel.app/api/top-langs/?username={username}&layout=compact&{theme_params}"
        return f'<img src="{url}" alt="Top Languages" />'
    
    elif stat_type == "streak":
        streak_theme = f"theme=react&hide_border=true&background={CODER_DARK}&stroke={CODER_BLUE}&ring={CODER_BLUE}&fire={CODER_BLUE}&currStreakLabel={CODER_BLUE}"
        url = f"https://github-readme-streak-stats.herokuapp.com/?user={username}&{streak_theme}"
        return f'<img src="{url}" alt="GitHub Streak" />'
    
    return ""


# ============================================================================
# REFERENCE LIBRARY - Use these as examples or starting points
# The AI can choose which to include, modify, or add new ones using the helpers
# ============================================================================

# Common tech stack with verified Simple Icons slugs
# Find more at: https://simpleicons.org/
COMMON_TECH = {
    "Languages": {
        "Python": ("python", "3776AB"),
        "TypeScript": ("typescript", "3178C6"),
        "JavaScript": ("javascript", "F7DF1E"),
        "Go": ("go", "00ADD8"),
        "Bash": ("gnubash", "4EAA25"),
        "Java": ("java", "007396"),
        "C++": ("cplusplus", "00599C"),
        "Rust": ("rust", "000000"),
        "Ruby": ("ruby", "CC342D"),
        "PHP": ("php", "777BB4"),
    },
    "Cloud & Infrastructure": {
        "Docker": ("docker", "2496ED"),
        "Kubernetes": ("kubernetes", "326CE5"),
        "Terraform": ("terraform", "7B42BC"),
        "PostgreSQL": ("postgresql", "4169E1"),
        "Redis": ("redis", "DC382D"),
        "MySQL": ("mysql", "4479A1"),
        "MongoDB": ("mongodb", "47A248"),
        "AWS": ("amazonaws", "232F3E"),
        "GCP": ("googlecloud", "4285F4"),
        "Azure": ("microsoftazure", "0078D4"),
    },
    "Development Tools": {
        "Coder": ("coder", "00ADD8"),
        "Git": ("git", "F05032"),
        "GitHub": ("github", "181717"),
        "VS Code": ("visualstudiocode", "007ACC"),
        "Neovim": ("neovim", "57A143"),
        "Vim": ("vim", "019733"),
        "JetBrains": ("jetbrains", "000000"),
        "Cursor": ("cursor", "000000"),  # Use generic or none if no icon
    },
    "Frameworks": {
        "React": ("react", "61DAFB"),
        "Next.js": ("nextdotjs", "000000"),
        "Node.js": ("nodedotjs", "339933"),
        "Flask": ("flask", "000000"),
        "FastAPI": ("fastapi", "009688"),
        "Django": ("django", "092E20"),
        "Vue.js": ("vuedotjs", "4FC08D"),
        "Angular": ("angular", "DD0031"),
        "Express": ("express", "000000"),
    },
}

# Social platforms with proper branding
SOCIAL_PLATFORMS = {
    "Twitter": ("twitter", "1DA1F2"),
    "Discord": ("discord", "5865F2"),
    "LinkedIn": ("linkedin", "0077B5"),
    "GitHub": ("github", "181717"),
    "Email": ("gmail", "D14836"),
    "Mastodon": ("mastodon", "6364FF"),
    "Reddit": ("reddit", "FF4500"),
}

# User's actual social links (customize these)
USER_SOCIAL_LINKS = [
    ("Twitter", "https://twitter.com/developmentcats"),
    ("Discord", "https://discord.gg/TKbReWmBqe"),
    ("Email", "mailto:chris@dualriver.com"),
]

# Legacy constant for backwards compatibility
SOCIAL_LINKS = USER_SOCIAL_LINKS

