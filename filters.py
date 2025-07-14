# === 🧠 LUMIRA FILTER SYSTEM (filters.py) ===

def filter_by_category(scrolls, category):
    """Filter scrolls by category (case-insensitive)."""
    if not category:
        return scrolls
    result = [s for s in scrolls if s.get("category", "").strip().lower() == category.strip().lower()]
    print(f"[FILTER] Category: {category} → {len(result)} match(es)")
    return result


def filter_by_name(scrolls, name):
    """Filter scrolls by name (case-insensitive)."""
    if not name:
        return scrolls
    result = [s for s in scrolls if name.strip().lower() in s.get("name", "").lower()]
    print(f"[FILTER] Name: {name} → {len(result)} match(es)")
    return result


def filter_by_keyword(scrolls, keyword):
    """Filter scrolls by keyword (search in name + message)."""
    if not keyword:
        return scrolls
    keyword = keyword.strip().lower()
    result = [
        s for s in scrolls
        if keyword in s.get("name", "").lower() or keyword in s.get("message", "").lower()
    ]
    print(f"[FILTER] Keyword: {keyword} → {len(result)} match(es)")
    return result


def filter_by_tag(scrolls, tag):
    """Filter scrolls by tags — hashtags or echo-style."""
    if not tag:
        return scrolls
    tag = tag.strip().lower()
    result = [
        s for s in scrolls
        if tag in [t.lower() for t in s.get("tags", [])]
    ]
    print(f"[FILTER] Tag: {tag} → {len(result)} match(es)")
    return result
