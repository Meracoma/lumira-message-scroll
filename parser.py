
def parse_markdown(entry):
    name = entry.get("name", "Unknown")
    category = entry.get("category", "Unlabeled")
    timestamp = entry.get("timestamp", "")
    tags = entry.get("tags", [])
    message = entry.get("message", "")

    tag_display = ", ".join([f"`{tag}`" for tag in tags]) if tags else "No tags"
    return f"""
**{name}** · *{category}* · *{timestamp}*  
Tags: {tag_display}  
> {message}
"""
