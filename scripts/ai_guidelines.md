# AI Guidelines for README Generation

This document guides AI (like Claude) when generating or modifying the README.

## 🎯 Core Principles

1. **Be Intelligent, Not Rigid**: Choose what to display based on actual data
2. **Stay Safe**: Only use helpers from `constants.py` for images/badges
3. **Be Relevant**: Show what matters, hide what doesn't
4. **Stay Fresh**: Emphasize recent, active contributions

## 🛠️ Available Tools

### Badge Generation

All badge functions guarantee working URLs. Use them freely:

```python
from constants import get_skill_badge, COMMON_TECH, COLORS

# Basic usage - always works
badge = get_skill_badge("Python", "python", "3776AB")

# Use color names
badge = get_skill_badge("Coder", "coder", COLORS["coder_blue"])

# No icon needed
badge = get_skill_badge("Custom Tool", "none", "FF5733")

# Different style
badge = get_skill_badge("Python", "python", "3776AB", style="flat")
```

### Stats Images

```python
from constants import get_stats_image

# These always work - reliable Vercel services
stats = get_stats_image(username, "stats")
streak = get_stats_image(username, "streak")
langs = get_stats_image(username, "languages")
```

### Social Badges

```python
from constants import get_social_badge, SOCIAL_PLATFORMS

# For known platforms - guaranteed to work
badge = get_social_badge("Twitter", username, url)

# For custom platforms
badge = get_social_badge("CustomSite", username, url)
```

## 🧠 Decision Making

### When to Show Sections

**Coder Registry Stats** - Show if:
- User has any PRs to coder/registry
- User has commits to registry modules
- Emphasize this - it's their main focus!

**Recent Activity** - Always show, but:
- Filter to meaningful events only
- Prioritize: releases > PRs > issues > commits
- Skip boring events (star notifications, etc.)

**Tech Stack** - Show if:
- Detected from repos, OR
- Using COMMON_TECH as reference

Be smart: If user primarily codes in Python/Go, emphasize those!

**GitHub Stats** - Always show (reliable service)

### Choosing Technologies

**Option 1: Use COMMON_TECH reference**
```python
from constants import COMMON_TECH

# Pick technologies the user actually uses
for tech_name, (icon, color) in COMMON_TECH["Languages"].items():
    if tech_name in user_languages:
        badge = get_skill_badge(tech_name, icon, color)
```

**Option 2: Dynamic discovery**
```python
from constants import get_skill_badge, is_simple_icon_available

# Discovered from GitHub data
language = "Python"
icon_slug = language.lower()

# Validate before using
if is_simple_icon_available(icon_slug):
    badge = get_skill_badge(language, icon_slug, "3776AB")
else:
    # Fallback: no icon
    badge = get_skill_badge(language, "none", "3776AB")
```

## ✅ Safe Patterns

### ✅ Good: Dynamic with validation

```python
# Discover user's actual languages
user_languages = get_language_stats(repos)

for lang in user_languages:
    slug = lang.lower()
    if lang in COMMON_TECH["Languages"]:
        # Use known config
        icon, color = COMMON_TECH["Languages"][lang]
    elif is_simple_icon_available(slug):
        # Trust Simple Icons
        icon, color = slug, "999999"  # Default color
    else:
        # No icon
        icon, color = "none", "999999"
    
    badge = get_skill_badge(lang, icon, color)
```

### ✅ Good: Conditional sections

```python
# Only show Coder stats if relevant
coder_stats = get_coder_registry_stats(repos, events)
if coder_stats["total_prs"] > 0 or coder_stats["total_commits"] > 0:
    readme += generate_coder_section(coder_stats)
```

### ✅ Good: Smart categorization

```python
# Group by activity level
very_active = [tech for tech, count in tech_counts.items() if count > 10]
active = [tech for tech, count in tech_counts.items() if 3 < count <= 10]
learning = [tech for tech, count in tech_counts.items() if count <= 3]

# Show different sections
if very_active:
    readme += "### Core Technologies\n\n"
    # ... badges
if learning:
    readme += "### Currently Exploring\n\n"
    # ... badges
```

## ❌ Unsafe Patterns

### ❌ Bad: External image URLs

```python
# NEVER - not from trusted service
readme += "![Logo](https://random-site.com/logo.png)"

# NEVER - might not exist
readme += "![Icon](./local-file.png)"
```

### ❌ Bad: Unvalidated URLs

```python
# NEVER - might construct invalid URL
url = f"https://img.shields.io/badge/{raw_user_input}"
```

### ❌ Bad: Hardcoded everything

```python
# Works but boring - use actual data!
readme += "### Tech Stack\n\n"
readme += "Python, JavaScript, Go"  # Static list
```

## 💡 Creative Freedom

### DO Feel Free To:

1. **Reorganize sections** based on what's most interesting
2. **Add emojis** that fit the context (but don't overdo it)
3. **Choose colors** that match the brand/technology
4. **Highlight recent work** in creative ways
5. **Write engaging descriptions** from the data
6. **Skip empty sections** (don't show "Recent Activity: None")
7. **Adjust heading levels** for better flow
8. **Group related items** intelligently
9. **Add context** from commit messages, PR titles
10. **Make it personal** to the user's actual work

### DON'T:

1. **Invent fake data** (no made-up stats)
2. **Use unverified image URLs**
3. **Break markdown syntax**
4. **Add external dependencies**
5. **Make it too long** (keep it scannable)
6. **Copy exactly** from templates

## 🎨 Style Guidelines

### Tone
- Professional but friendly
- Enthusiastic about Coder ecosystem
- Technical but accessible

### Structure
- Clear hierarchy (H1 → H2 → H3)
- Scannable sections
- Visual breaks with `---`
- Balanced text and images

### Content
- Lead with most impressive/recent work
- Show, don't just tell
- Use active voice
- Keep paragraphs short

## 📊 Example Decision Tree

```
Is user active in Coder Registry?
├─ Yes → Prominent Coder section at top
│   ├─ Recent PRs? → Show list with status
│   ├─ Recent commits? → Show with messages
│   └─ Add Coder badge to header
└─ No → General open source section

What are primary languages?
├─ From GitHub API language stats
├─ Cross-reference with COMMON_TECH
├─ Generate badges for top 5-8
└─ Group by usage level

Any recent activity?
├─ Filter to meaningful events
├─ Format by type (PR/Issue/Release)
├─ Show 8-10 most interesting
└─ Skip if older than 3 months

Social links available?
├─ Check USER_SOCIAL_LINKS
├─ Generate badges with proper icons
└─ Add to footer
```

## 🔄 Iteration

When updating the README:

1. **Check what changed** - new repos? new activity?
2. **Keep what works** - don't change just to change
3. **Refresh stats** - always use latest numbers
4. **Update timestamps** - show when last generated
5. **Maintain consistency** - same structure unless improving

## 🎓 Learning

If you need to add a new technology/badge:

1. Check [Simple Icons](https://simpleicons.org/) for the slug
2. Add to `COMMON_TECH` in constants.py for reuse
3. Or use dynamically with `get_skill_badge()`

## ✨ Remember

**You're creating a living document that represents a real developer.**

- Make it accurate (use actual data)
- Make it impressive (highlight achievements)
- Make it current (recent activity matters)
- Make it reliable (use trusted services)
- Make it personal (not generic template)

**The tools in constants.py are your safety net - use them freely and creatively!**

