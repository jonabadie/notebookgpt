from conversation import LlmConversation


conversation = LlmConversation(model="gpt-4")

response = conversation.openai_api_call(
    "I've got a dataset with the path 'titanic_train.csv'."
    "Write a numbered step by step plan to perform exploratory data analysis."
)
print(response)
response_message = response["choices"][0]["message"]