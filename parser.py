# === ✨ LUMIRA SCROLL PARSER (parser.py) ===

import re

# === 🧠 Echo Tags Parser ===
def extract_tags(text):
    """Extract #hashtags or {::TAG::} formats for sorting or signals."""
    hashtag_tags = re.findall(r"#(\w+)", text)
    echo_tags = re.findall(r"{::(.*?)::}", text)
    return list(set(hashtag_tags + echo_tags))


# === 📜 Stylized Scroll Display Parser ===
def parse_markdown(text):
    """Convert raw text to formatted markdown with extra enhancements."""
    
    # — Bold: **text**
    text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
    
    # — Italic: *text*
    text = re.sub(r"\*(.*?)\*", r"<em>\1</em>", text)
    
    # — Inline code: `code`
    text = re.sub(r"`(.*?)`", r"<code>\1</code>", text)

    # — Optional: replace ::brackets:: with stylized inline tags
    text = re.sub(r"{::(.*?)::}", r"<span style='background:#333;border-radius:4px;padding:2px 6px;color:#fff;'>\1</span>", text)

    return text
