import os
import requests

def push(text: str):
    requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": os.getenv("PUSHOVER_TOKEN"),
            "user": os.getenv("PUSHOVER_USER"),
            "message": text,
        }
    )

def record_user_details(email: str, name: str = "Name not provided", notes: str = "not provided"):
    push(f"Recording : {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question: str):
    push(f"Recording : {question}")
    return {"recorded": "ok"}
