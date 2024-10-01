import requests
from bs4 import BeautifulSoup

class Plugin:
    def can_handle(self, task):
        if 'get request' in str(task) and 'bs4 beautiful soup' in str(task) and 'summarize tldr' in str(task):
            return True
        else:
            return False

    def handle(self, task):
        try:
            url = task['url']
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            tokens = text.split()
            tldr = " ".join(tokens[:10])
            summary = " ".join(tokens[10:])
            return {'tldr': tldr, 'summary': summary}
        except Exception as e:
            return str(e)