import logging

logging.basicConfig(level=logging.INFO)

class Plugin:
    @staticmethod
    def can_handle(task):
        return task.lower() == "hi"

    @staticmethod
    def handle(task):
        try:
            logging.info(f"Received task: {task}")
            return "Hello, how are you?"
        except Exception as e:
            logging.error(f"Error processing task: {str(e)}")
            return "I'm sorry, but I couldn't process your request."