import logging

logging.basicConfig(level=logging.INFO)

class Plugin:
    @staticmethod
    def can_handle(task):
        return "hi" in task.lower()

    @staticmethod
    def handle(task):
        try:
            logging.info(f"Received task: {task}")
            return "Hello! How can I assist you today?"
        except Exception as e:
            logging.error(f"Error handling task: {e}")
            return "I apologize, but I couldn't process your request."