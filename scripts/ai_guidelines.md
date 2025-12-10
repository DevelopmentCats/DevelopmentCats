# AI Guidelines for README Generation

This document guides AI (like Claude) when generating or modifying the README.
Based on GitHub README best practices from 2024-2025.

## 🎯 Core Principles (Industry Best Practices)

1. **Scannable in 10 Seconds**: Visitors decide quickly if they're interested
2. **Visual Over Text**: Badges, stats, and images > paragraphs
3. **No Redundancy**: GitHub already shows bio, followers, repo count
4. **Stay Safe**: Only use helpers from `constants.py` for images/badges
5. **Professional but Personal**: Show personality without being unprofessional
6. **Mobile-Friendly**: Works on all screen sizes
7. **Accessible**: Proper alt text, good contrast, clear structure
8. **Updated**: Show recent activity and current work

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

### ✅ Best Practices (Do These):

1. **Start Strong**: Eye-catching header with role/focus
2. **Lead with Unique**: Coder Registry work at the top (not common!)
3. **Be Visual**: More badges and images, less text
4. **Group Logically**: Languages together, tools together, etc.
5. **Add Alt Text**: Every image needs descriptive alt text (accessibility!)
6. **Use Emojis Wisely**: 1 per section header for quick scanning
7. **Keep Sections Short**: 3-5 lines of content per section
8. **Center Key Elements**: Headers, intro badges, stats
9. **Add Separators**: Use `---` between major sections
10. **Show Personality**: Brief, authentic, not corporate-speak
11. **Make it Scannable**: Someone should "get" you in 10 seconds
12. **Test Both Themes**: Works in light and dark mode

### ❌ Common Mistakes (Avoid These):

1. **Walls of Text**: No one reads paragraphs on GitHub profiles
2. **Redundancy**: Repeating what's already visible (bio, followers, etc.)
3. **Too Many Stats**: 3-4 stat images max, more is overwhelming
4. **Poor Contrast**: Light gray text on white background
5. **Missing Alt Text**: Accessibility fail
6. **Outdated Content**: "Currently learning React" from 2020
7. **Generic Statements**: "Passionate developer" means nothing
8. **No Visual Hierarchy**: Everything same size/importance
9. **Broken Images**: Always use trusted sources (constants.py!)
10. **Too Long**: Over 150 lines is excessive
11. **Left-Aligned Everything**: Looks unpolished
12. **Random Order**: Put impressive stuff first!

## 🎨 Style Guidelines

### Tone
- Professional but friendly
- Enthusiastic about Coder ecosystem
- Direct and to the point

### Structure & Alignment (GitHub Best Practices)

**✅ DO:**
- Center headers, intro badges, and stats for professional look
- Use HTML `align="center"` for centering (markdown doesn't support it well)
- Add horizontal rules `---` to separate sections
- Use emojis in section headers for quick visual scanning
- Keep sections short (3-5 lines of actual content)
- Use white space generously
- Make it work on light AND dark themes

**❌ DON'T:**
- Left-align everything (looks amateur)
- Cram badges together without spacing
- Use walls of text
- Skip alt text on images
- Use colors that only work in one theme

### Formatting Rules (Follow These Exactly)

**Centered Header (recommended):**
```markdown
<h1 align="center">Hi 👋, I'm [Name]</h1>
<h3 align="center">Role | Specialization</h3>
```

**Centered Badge Group:**
```markdown
<p align="center">
  <img src="badge-url" alt="description" />
  <img src="badge-url" alt="description" />
</p>
```

**Or for markdown badges:**
```markdown
<p align="center">
  
![Badge1](url) ![Badge2](url) ![Badge3](url)
  
</p>
```

**Section Headers (use emojis for scanning):**
```markdown
## 🚀 What I'm Working On
## 🛠️ Tech Stack
## 📊 GitHub Stats
## 🤝 Connect With Me
```

**Horizontal Rule Between Sections:**
```markdown
---
```

**Images with Alt Text (accessibility!):**
```markdown
<img src="url" alt="GitHub Stats showing 500+ contributions" />
```

### Content Rules (Best Practices 2024)

**❌ Skip (GitHub Already Shows):**
- Name/username (at top of profile)
- Bio (already visible)
- Follower/following counts (redundant)
- Total repo count (already displayed)
- Location, company (in sidebar)

**✅ Include (Makes You Stand Out):**

1. **Brief Tagline** (1 line max)
   - What you do or focus on
   - Example: "Building cloud dev tools | Coder Registry Contributor"

2. **Current Work** (2-3 lines)
   - What you're actively working on NOW
   - Coder Registry contributions (unique!)
   - Link to specific project/organization

3. **Tech Stack** (show everything!)
   - ALL languages from `languages.all_detected`
   - Group logically: Languages, Frameworks, Cloud, Tools
   - Use badges for visual impact
   - Don't limit to 8 - show your full skillset!

4. **GitHub Stats** (2-3 visualizations)
   - Contribution stats
   - Language breakdown
   - Streak (optional)
   - These are dynamic and interesting!

5. **Contact/Social** (badges only)
   - Twitter, Discord, Email, etc.
   - Make them clickable badges

**How to Show Languages:**
- Read `languages.all_detected` from data file
- Use `constants.COMMON_TECH` to get icon slugs and colors
- If a language isn't in COMMON_TECH, use lowercase name as slug
- Group logically: Languages, Frameworks, Tools, Cloud, etc.
- Show ALL of them, not just top 8!

## 📊 Example Decision Tree

```
RECOMMENDED STRUCTURE (Following GitHub Best Practices):

╔════════════════════════════════════════════════════════════╗
║  <h1 align="center">Hi 👋, I'm DevelopmentCats</h1>       ║
║  <h3 align="center">Full-Stack Developer | Coder          ║
║                     Registry Contributor</h3>              ║
║                                                            ║
║  <p align="center">                                        ║
║    [Profile views] [Coder badge] [Other badges]           ║
║  </p>                                                      ║
╚════════════════════════════════════════════════════════════╝

---

## 🚀 What I'm Working On

Building Terraform modules for the [Coder Registry](link) that help 
developers create cloud dev environments.

---

## 🛠️ Tech Stack

### Languages

<p align="center">
  
![Python](badge) ![TypeScript](badge) ![JavaScript](badge)
![Go](badge) ![Bash](badge) ![Java](badge)
... ALL languages from languages.all_detected ...
  
</p>

### Cloud & Infrastructure

<p align="center">
  
![Docker](badge) ![Kubernetes](badge) ![Terraform](badge)
  
</p>

### Frameworks & Tools

<p align="center">
  
![React](badge) ![Node.js](badge) ![Flask](badge)
  
</p>

---

## 📊 GitHub Stats

<p align="center">
  <img src="stats-url" alt="GitHub stats showing 500+ contributions" />
</p>

<p align="center">
  <img src="streak-url" alt="GitHub streak" />
</p>

---

## 🤝 Connect With Me

<p align="center">
  <a href="url"><img src="twitter-badge" alt="Twitter" /></a>
  <a href="url"><img src="discord-badge" alt="Discord" /></a>
  <a href="url"><img src="email-badge" alt="Email" /></a>
</p>

---

<p align="center">
  <sub>🤖 Auto-updated twice weekly via Coder Tasks</sub>
</p>

═══════════════════════════════════════════════════════════

KEY PRINCIPLES:
✓ Centered headers and key elements
✓ Visual hierarchy (important stuff stands out)
✓ Generous white space
✓ Section breaks with ---
✓ Emojis for quick section identification
✓ ALL languages shown (grouped logically)
✓ Alt text on all images
✓ ~60-100 lines total
✓ Scannable in 10 seconds
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

