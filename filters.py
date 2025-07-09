
import datetime
# filters.py

def tag_echo(name, message, echo_tag):
    with open("echoes.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp}|{name}|{echo_tag}|{message}\n")

def list_echoes():
    echoes = []
    if not os.path.exists("echoes.txt"):
        return echoes
    with open("echoes.txt", "r", encoding="utf-8") as f:
        for line in f:
            timestamp, name, tag, message = line.strip().split("|", 3)
            echoes.append({"timestamp": timestamp, "name": name, "tag": tag, "message": message})
    return echoes

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
def filter_by_tag(entries, tag):
    return [e for e in entries if tag.lower() in [t.lower() for t in e.get("tags", [])]]
