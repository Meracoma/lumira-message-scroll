
import datetime
# filters.py

def filter_by_category(messages, selected_category):
    if selected_category == "All":
        return messages
    return [msg for msg in messages if msg.get("category") == selected_category]

def filter_by_name(messages, name_query):
    name_query = name_query.lower().strip()
    if not name_query:
        return messages
    return [msg for msg in messages if name_query in msg.get("name", "").lower()]

def filter_by_keyword(messages, keyword_query):
    keyword_query = keyword_query.lower().strip()
    if not keyword_query:
        return messages
    return [msg for msg in messages if keyword_query in msg.get("message", "").lower()]
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
