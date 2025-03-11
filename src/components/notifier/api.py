THRESHOLD = 100  # Example threshold

def send_notification(result):
    if result > THRESHOLD:
        return f"Alert: The result {result} exceeded the threshold!"
    return "No notification needed."
