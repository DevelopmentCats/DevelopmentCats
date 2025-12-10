# AI Guidelines for README Generation

This document guides AI (like Claude) when generating or modifying the README.

## 🎯 Core Principles

1. **Be Concise**: GitHub already shows bio, followers, repo count - don't repeat it
2. **Be Intelligent, Not Rigid**: Choose what to display based on actual data
3. **Stay Safe**: Only use helpers from `constants.py` for images/badges
4. **Be Relevant**: Show what matters, hide what doesn't
5. **Stay Fresh**: Emphasize recent, active contributions
6. **Less is More**: Keep it scannable - people won't read walls of text

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
2. **Add emojis** strategically (1-2 per section, not everywhere)
3. **Choose colors** that match the brand/technology
4. **Highlight Coder work** prominently (this is unique!)
5. **Skip empty sections** (don't show "Recent Activity: None")
6. **Group related items** intelligently
7. **Make it personal** to the user's actual work
8. **Keep it SHORT** - 3-4 sections max
9. **Use badges over text** - visual > verbose
10. **Let stats speak** - graphs instead of paragraphs

### DON'T:

1. **Invent fake data** (no made-up stats)
2. **Use unverified image URLs** (only constants.py helpers!)
3. **Repeat profile info** (no name, bio, followers - already visible)
4. **Write paragraphs** (use bullets, badges, visuals)
5. **List everything** (be selective - what's impressive?)
6. **Make it long** (keep under 100 lines total)
7. **Be generic** (focus on Coder/unique work)

## 🎨 Style Guidelines

### Tone
- Professional but friendly
- Enthusiastic about Coder ecosystem
- Direct and to the point

### Structure
- **Minimal text** - mostly visual (badges, stats)
- Clear hierarchy but not too many levels
- Visual elements > paragraphs
- White space is good

### Content
- Lead with most impressive work (Coder Registry!)
- Show, don't tell (badges > descriptions)
- Skip what GitHub already shows:
  - ❌ Name/username (already at top of profile)
  - ❌ Bio (already shown)
  - ❌ Follower/following counts (already visible)
  - ❌ Total repo count (already shown)
  - ❌ Location, company, etc. (in sidebar)
- Include what's unique:
  - ✅ Coder Registry contributions (specific!)
  - ✅ Tech stack badges
  - ✅ GitHub stats visualizations
  - ✅ Notable recent activity
  - ✅ Social links

## 📊 Example Decision Tree

```
README Structure (keep it minimal!):

1. Header (optional - GitHub shows this already)
   ├─ Skip name/bio (already visible)
   └─ Maybe: Quick tagline or focus (1 line max)

2. Coder Registry Work (MAIN FOCUS - 2-3 lines)
   ├─ Prominent badge/link
   ├─ Quick highlight of contribution (not a list!)
   └─ Example: "Building Terraform modules for cloud dev environments"

3. Tech Stack (badges only - no text!)
   ├─ Show top 6-8 technologies
   ├─ One row of badges
   └─ Use constants.py helpers

4. GitHub Stats (visual - let images do the talking)
   ├─ Stats graph
   ├─ Maybe streak or languages
   └─ Max 2-3 stat images

5. Connect (1 line of social badges)
   └─ Twitter, Discord, Email badges

Total: ~30-60 lines max, mostly badges/images
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

