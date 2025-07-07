
import datetime

def filter_scrolls(scrolls, name=None, category=None, date=None):
    filtered = scrolls
    if name:
        filtered = [s for s in filtered if s.get("name", "").lower() == name.lower()]
    if category:
        filtered = [s for s in filtered if s.get("category", "").lower() == category.lower()]
    if date:
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        filtered = [s for s in filtered if datetime.datetime.fromisoformat(s.get("timestamp")).date() == date_obj]
    return filtered
