# === ✨ LUMIRA SCROLL PARSER (parser.py) ===

import re

# === 🧠 TAG EXTRACTOR: Hashtag + Echo Style ===
def extract_tags(text):
    """
    Extract tags from scroll text. Supports:
    - Hashtags: #keyword
    - Echo Tags: {::TAG::}
    """
    hashtag_tags = re.findall(r"#(\w+)", text)
    echo_tags = re.findall(r"{::(.*?)::}", text)
    combined = list(set(hashtag_tags + echo_tags))

    print(f"[PARSER] Extracted Tags → {combined}")
    return combined


# === 📜 MARKDOWN FORMATTER: Rich Scroll Display ===
def parse_markdown(text):
    """
    Convert scroll content into styled HTML using markdown conventions.

    Supported:
    - **bold** → <strong>
    - *italic* → <em>
    - `inline code` → <code>
    - {::tag::} → Styled inline badge span
    """
    original = text  # optional: keep for echo log stream if needed

    # Bold
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)

    # Italic
    text = re.sub(r"\*(.*?)\*", r"<em>\1</em>", text)

    # Inline Code
    text = re.sub(r"`(.*?)`", r"<code>\1</code>", text)

    # Echo Tags → Inline badge styling
    text = re.sub(
        r"{::(.*?)::}",
        r"<span style='background:#333;border-radius:4px;padding:2px 6px;color:#fff;font-size:0.8rem;'>\1</span>",
        text
    )

    print(f"[PARSER] Markdown parsed.")
    return text
