# parser.py

import markdown
import html

def parse_markdown(entry):
    """
    Convert a scroll entry into HTML format using markdown.
    """
    name = html.escape(entry.get("name", "Unknown"))
    category = html.escape(entry.get("category", "General"))
    timestamp = html.escape(entry.get("timestamp", ""))
    message = entry.get("message", "")

    # Render markdown safely
    rendered_message = markdown.markdown(message)

    return f"""
    <div class="scroll-entry">
        <strong>{name}</strong> · <em>{category}</em> · <small>{timestamp}</small><br/>
        <div>{rendered_message}</div>
    </div>
    """# Markdown and HTML parsing utilities
