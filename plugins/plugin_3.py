import logging

logging.basicConfig(level=logging.INFO)

class Plugin:
    @staticmethod
    def can_handle(task):
        return "conversation context" in task.lower()

    @staticmethod
    def handle(task):
        try:
            logging.info(f"Updating conversation context: {task}")
            # Here you would implement the logic to update the conversation context
            return "Conversation context updated successfully."
        except Exception as e:
            logging.error(f"Error updating conversation context: {e}")
            return "I'm sorry, but I couldn't update the conversation context."