# parser.py

import markdown
import html


def parse_markdown(entry):
    """
    Converts a message entry dictionary into formatted markdown+HTML for Streamlit display.
    """
    name = html.escape(entry.get("name", "Unknown"))
    category = html.escape(entry.get("category", "Other"))
    timestamp = html.escape(entry.get("timestamp", ""))
    message = entry.get("message", "")

    # Convert markdown to HTML
    message_html = markdown.markdown(message)

    return f"""
    <div style="margin-bottom: 1.5em; padding: 1em; background-color: #f7f7f7; border-radius: 10px;">
        <div style="font-weight: bold;">{name} <span style="font-style: italic; color: #888;">· {category}</span></div>
        <div style="font-size: 0.85em; color: #999;">{timestamp}</div>
        <div style="margin-top: 0.5em;">{message_html}</div>
    </div>
    """
