from datetime import datetime

def parse_markdown(entry):
    timestamp = datetime.fromisoformat(entry['timestamp']).strftime('%Y-%m-%d %H:%M')
    return f"""
    <div style='padding: 10px; border-left: 4px solid #ccc; background: #f9f9f9;'>
        <strong>{entry['user']}</strong> <em style='color:gray;'>[{timestamp}]</em><br>
        <p>{entry['message']}</p>
    </div>
    """
