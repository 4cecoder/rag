import os
import json
import requests
import importlib.util

class AIAgent:
    def __init__(self):
        self.plugins = {}
        self.plugin_directory = 'plugins'
        if not os.path.exists(self.plugin_directory):
            os.makedirs(self.plugin_directory)
        self.load_plugins()

    def load_plugins(self):
        """Load all plugins from the plugin directory."""
        for filename in os.listdir(self.plugin_directory):
            if filename.endswith('.py'):
                plugin_name = filename[:-3]
                plugin_path = os.path.join(self.plugin_directory, filename)

                spec = importlib.util.spec_from_file_location(plugin_name, plugin_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                self.plugins[plugin_name] = module

    def process_input(self, user_input):
        """Process user input using available plugins or create a new plugin."""
        for plugin in self.plugins.values():
            if hasattr(plugin, 'can_handle') and callable(plugin.can_handle):
                if plugin.can_handle(user_input):
                    if hasattr(plugin, 'handle') and callable(plugin.handle):
                        return plugin.handle(user_input)
                    else:
                        continue  # Skip if 'handle' is missing
            else:
                continue  # Skip if 'can_handle' is missing

        # If no plugin can handle the input, create a new plugin
        self.create_plugin_for_input(user_input)
        self.load_plugins()  # Reload plugins after adding a new one
        return self.process_input(user_input)

    def create_plugin_for_input(self, user_input):
        """Generate and save a new plugin capable of handling the user input."""
        plugin_code = self.generate_plugin_code(user_input)
        plugin_name = f'plugin_{len(self.plugins) + 1}'
        plugin_path = os.path.join(self.plugin_directory, f'{plugin_name}.py')

        # Print the generated code for debugging
        print(f"Generated plugin code:\n{plugin_code}\n")

        with open(plugin_path, 'w') as f:
            f.write(plugin_code)

    def generate_plugin_code(self, user_input):
        """Use Ollama's API to generate code for a new plugin."""
        prompt = f'''
You are an AI assistant tasked with generating a Python plugin module for an AI agent.
The plugin should handle the following user input: "{user_input}".

Requirements:
- Provide only the code for a Python module.
- Define two functions: can_handle(task) and handle(task).
- can_handle(task) should return True if the plugin can handle the task.
- handle(task) should perform the task and return the result.
- Ensure that the code is valid and handles potential exceptions.
- Do not include any explanations or additional text.

Output:
'''

        # Send the request to the local Ollama server
        response = self.call_ollama_api(prompt)

        # Extract the code block from the response
        code = self.extract_code(response)
        return code

    def call_ollama_api(self, prompt):
        """Call the Ollama server API to generate plugin code."""
        url = 'http://localhost:11434/api/generate'

        payload = {
            'model': 'llama3.2',
            'prompt': prompt,
            'options': {
                'temperature': 0.7,
                'max_tokens': 512,
            },
            'stream': False
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
            return result.get('response', '')
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Ollama server: {e}")
            return ''

    def extract_code(self, text):
        """Extract the code block from the AI's response."""
        import re
        code_block = re.search(r'```python\n(.*?)```', text, re.DOTALL)
        if code_block:
            return code_block.group(1).strip()
        else:
            return text.strip()

# Chat loop
if __name__ == "__main__":
    agent = AIAgent()
    print("Assistant: Hi there! I'm your AI assistant. How can I help you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Assistant: It was nice chatting with you! Bye! 😊")
            break
        response = agent.process_input(user_input)
        print(f"Assistant: {response}")