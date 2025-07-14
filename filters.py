# === 🧠 LUMIRA FILTER SYSTEM (filters.py) ===
from datetime import datetime

def filter_by_time_range(scrolls, start_date, end_date):
    """Filter scrolls within a time range."""
    if not start_date or not end_date:
        return scrolls
    result = []
    for s in scrolls:
        try:
            ts = datetime.fromisoformat(s.get("timestamp", "").replace("Z", "+00:00"))
            if start_date <= ts <= end_date:
                result.append(s)
        except Exception:
            continue
    print(f"[FILTER] Time Range: {start_date} → {end_date} → {len(result)} match(es)")
    return result


def filter_by_zodiac(scrolls, zodiac_sign):
    """Filter scrolls by zodiac sign."""
    if not zodiac_sign:
        return scrolls
    result = [s for s in scrolls if s.get("zodiac", "").strip().lower() == zodiac_sign.strip().lower()]
    print(f"[FILTER] Zodiac: {zodiac_sign} → {len(result)} match(es)")
    return result


def filter_by_moon_phase(scrolls, moon_phase):
    """Filter scrolls by moon phase."""
    if not moon_phase:
        return scrolls
    result = [s for s in scrolls if s.get("moon_phase", "").strip().lower() == moon_phase.strip().lower()]
    print(f"[FILTER] Moon Phase: {moon_phase} → {len(result)} match(es)")
    return result


def sort_scrolls(scrolls, order="desc"):
    """Sort scrolls by timestamp (newest or oldest first)."""
    def get_time(s):
        try:
            return datetime.fromisoformat(s.get("timestamp", "").replace("Z", "+00:00"))
        except Exception:
            return datetime.min
    sorted_scrolls = sorted(scrolls, key=get_time, reverse=(order == "desc"))
    print(f"[SORT] Order: {order} → {len(sorted_scrolls)} sorted")
    return sorted_scrolls

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
