
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

def filter_by_category(entries, category):
    return [entry for entry in entries if entry["category"].lower() == category.lower()]

def filter_by_name(entries, name):
    return [entry for entry in entries if name.lower() in entry["name"].lower()]

def filter_by_keyword(entries, keyword):
    return [entry for entry in entries if keyword.lower() in entry["message"].lower()]

def filter_by_tag(entries, tag):
    return [entry for entry in entries if tag.lower() in [t.lower() for t in entry.get("tags", [])]]
    
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
    
