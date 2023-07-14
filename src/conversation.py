import os

import openai
from dotenv import load_dotenv
load_dotenv()

class LlmConversation():
    def __init__(self, model="gpt-3.5-turbo"):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model
        self.messages=[
            {"role": "system", "content": "Only use the functions you have been provided with"},
        ]
        self.functions=[
            {
                "name": "python",
                "description": "Write python code",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "The python code",
                        }
                    },
                    "required": ["code"],
                }
            }
        ]
    
    def add_message(self, content, role="user"):
        message = {"role": role, "content": content}
        self.messages.append(message)

    def _save_assistant_message(self, response):
        response_message = response.choices[0]["message"]
        assistant_text = response_message.content
        if assistant_text:
            self.add_message(assistant_text, role="assistant")

        function_call = response_message.get("function_call")
        if function_call:
            self.add_message(function_call["arguments"], role="assistant")

    def openai_api_call(self, text):
        self.add_message(text)
        response = openai.ChatCompletion.create(

            model=self.model,
            max_tokens=1000,
            messages=self.messages,
            functions=self.functions
        )
        self._save_assistant_message(response)
        return response