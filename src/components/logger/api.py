import datetime

def log_operation(operation, result):
    timestamp = datetime.datetime.now().isoformat()
    return f"{timestamp} - {operation}: {result}"
