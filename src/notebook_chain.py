import json
import sys

from notebook import Notebook
from conversation import LlmConversation


class NotebookChain():
    def __init__(self, filename, steps=10):
        self.notebook = Notebook()
        self.conversation = LlmConversation(model="gpt-3.5-turbo")
        self.steps = steps
        self.available_functions = {
            "python": self.notebook.create_code
        }
        self.chain = [
            "You can execute Python code in a stateful Jupyter notebook environment. The code execution result will be provided, or a timeout will occur after 120.0 seconds."
            f"I've got a dataset at path '{filename}'."
            "Perform exploratory data analysis and model building."
            "Execute the first step then announce what the next step will be."
            "Explain what you do as you go in markdown format.",
            "Continue the analysis and model building."
            "Explain what you do as you go in markdown format.",
        ]

    def _handle_content(self, content):
        self.notebook.create_markdown(content)
        self.notebook.save_file()

    def _handle_function_call(self, function_call):
        function_name = function_call["name"]
        fuction_to_call = self.available_functions[function_name]

        function_args = json.loads(function_call["arguments"], strict=False)
        fuction_to_call(text=function_args.get("code"))
        self.notebook.save_file()
        execution_output = self.notebook.execute_notebook()
        self.conversation.add_message(execution_output, role="assistant")

    def run(self):
        for i in range(self.steps):
            human_message = self.chain[0] if i == 0 else self.chain[1]
            response = self.conversation.openai_api_call(human_message)
            print(response)
            response_message = response["choices"][0]["message"]

            if response_message.content:
                self._handle_content(response_message.content)

            function_call = response_message.get("function_call")
            if function_call:
                self._handle_function_call(function_call)
                
            print(self.conversation.messages)
