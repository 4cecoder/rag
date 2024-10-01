class Plugin:
    def can_handle(self, task):
        if task == "can you access the internet?":
            return True
        else:
            return False

    def handle(self, task):
        try:
            if task == "can you access the internet?":
                import requests
                response = requests.head("https://www.google.com")
                return f"Internet connection available. Status code: {response.status_code}"
            else:
                return "Unknown task"
        except Exception as e:
            return f"An error occurred: {str(e)}"