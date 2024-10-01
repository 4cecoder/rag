import requests

def can_handle(task):
    return task.lower() == "hi can you access the internet?"

def handle(task):
    try:
        response = requests.head("https://www.google.com")
        if response.status_code == 200:
            return "Yes, I can access the internet."
        else:
            return "No, I am not able to access the internet."
    except requests.RequestException as e:
        return f"Error: {e}"