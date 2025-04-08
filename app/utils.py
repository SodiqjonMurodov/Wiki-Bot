

def safe_callback_data(title: str) -> str:
    return ''.join(e for e in title if e.isalnum())