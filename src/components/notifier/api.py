from .notifier import Notifier

def notify(message:str) -> None:
    notifier = Notifier()
    notifier.notify(message)