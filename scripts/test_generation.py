#!/usr/bin/env python3
"""
Test the README generation system end-to-end.
"""

import sys
import json
from pathlib import Path
from datetime import datetime


def test_imports():
    """Test that all required imports work."""
    print("Testing imports...")
    try:
        import requests
        print("  ✅ requests")
    except ImportError as e:
        print(f"  ❌ requests: {e}")
        return False
    
    try:
        from github import Github
        print("  ✅ PyGithub")
    except ImportError as e:
        print(f"  ❌ PyGithub: {e}")
        return False
    
    return True


def test_data_directory():
    """Test that data directory exists and is writable."""
    print("\nTesting data directory...")
    data_dir = Path("data")
    
    if not data_dir.exists():
        print("  📁 Creating data directory...")
        data_dir.mkdir(exist_ok=True)
    
    # Test write
    test_file = data_dir / "test.json"
    try:
        with open(test_file, "w") as f:
            json.dump({"test": True, "timestamp": datetime.utcnow().isoformat()}, f)
        test_file.unlink()
        print("  ✅ Data directory is writable")
        return True
    except Exception as e:
        print(f"  ❌ Cannot write to data directory: {e}")
        return False


def test_github_api():
    """Test GitHub API connectivity."""
    print("\nTesting GitHub API connectivity...")
    try:
        import requests
        response = requests.get("https://api.github.com/users/DevelopmentCats", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ GitHub API accessible")
            print(f"     User: {data.get('name', 'N/A')}")
            print(f"     Public repos: {data.get('public_repos', 0)}")
            return True
        elif response.status_code == 403:
            print(f"  ⚠️  GitHub API rate limited")
            print(f"     This might be temporary - generation may still work")
            return True  # Don't fail on rate limit
        else:
            print(f"  ❌ GitHub API returned status {response.status_code}")
            return False
    
    except Exception as e:
        print(f"  ❌ GitHub API error: {e}")
        return False


def test_readme_generation():
    """Test README generation."""
    print("\nTesting README generation...")
    try:
        # Import the generation script
        sys.path.insert(0, str(Path("scripts").absolute()))
        from generate_readme import fetch_github_data, generate_readme
        
        print("  📥 Fetching GitHub data...")
        github_data = fetch_github_data()
        
        print("  📝 Generating README content...")
        readme_content = generate_readme(github_data)
        
        # Basic validation
        if not readme_content:
            print("  ❌ README content is empty")
            return False
        
        if len(readme_content) < 100:
            print("  ❌ README content is too short")
            return False
        
        if "DevelopmentCats" not in readme_content:
            print("  ❌ README doesn't contain username")
            return False
        
        # Check for key sections
        required_sections = [
            "Working On",
            "Recent Activity",
            "Tech Stack",
            "GitHub Statistics",
            "Connect With Me"
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in readme_content:
                missing_sections.append(section)
        
        if missing_sections:
            print(f"  ⚠️  Missing sections: {', '.join(missing_sections)}")
        
        print(f"  ✅ README generated ({len(readme_content)} characters)")
        return True
    
    except Exception as e:
        print(f"  ❌ README generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_constants():
    """Test that constants module is properly configured."""
    print("\nTesting constants configuration...")
    
    try:
        sys.path.insert(0, str(Path("scripts").absolute()))
        from constants import TECH_STACK, SOCIAL_LINKS, get_skill_badge, get_social_badge
        
        # Check tech stack is defined
        if not TECH_STACK:
            print("  ❌ TECH_STACK is empty")
            return False
        
        print(f"  ✅ {len(TECH_STACK)} skill categories defined")
        
        # Check social links
        if not SOCIAL_LINKS:
            print("  ❌ SOCIAL_LINKS is empty")
            return False
        
        print(f"  ✅ {len(SOCIAL_LINKS)} social links defined")
        
        # Test badge generation
        badge = get_skill_badge("Python", "python", "3776AB")
        if not badge or "shields.io" not in badge:
            print("  ❌ Badge generation failed")
            return False
        
        print("  ✅ Badge generation working")
        return True
    
    except Exception as e:
        print(f"  ❌ Constants test failed: {e}")
        return False


def test_readme_structure():
    """Validate README structure."""
    print("\nTesting README structure...")
    
    if not Path("README.md").exists():
        print("  ⚠️  README.md doesn't exist yet")
        return True
    
    try:
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Check for heading structure
        lines = content.split("\n")
        h1_count = sum(1 for line in lines if line.startswith("# ") or line.startswith("<h1"))
        
        if h1_count < 1:
            print("  ❌ No H1 heading found")
            return False
        
        # Check for links
        if "[" not in content or "](" not in content:
            print("  ⚠️  No markdown links found")
        
        # Check for images
        if "![" not in content and "<img" not in content:
            print("  ⚠️  No images found")
        
        # Check line length
        if len(lines) < 20:
            print("  ⚠️  README seems short")
        
        print(f"  ✅ README structure valid ({len(lines)} lines)")
        return True
    
    except Exception as e:
        print(f"  ❌ README structure check failed: {e}")
        return False


def main():
    """Run all tests."""
    print("=" * 70)
    print("README Generation System Tests")
    print("=" * 70)
    
    tests = [
        ("Imports", test_imports),
        ("Data Directory", test_data_directory),
        ("GitHub API", test_github_api),
        ("Constants Configuration", test_constants),
        ("README Generation", test_readme_generation),
        ("README Structure", test_readme_structure),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n❌ Test '{name}' crashed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
    
    print("=" * 70)
    print(f"Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed!")
        return 0
    else:
        print(f"❌ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

