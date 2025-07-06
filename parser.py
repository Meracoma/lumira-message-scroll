def parse_markdown(entry):
    return f'''
**{entry["name"]}** · *{entry["category"]}* · `{entry["timestamp"]}`  
> {entry["message"]}
'''