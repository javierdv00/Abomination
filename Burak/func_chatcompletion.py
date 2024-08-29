from openai import OpenAI

client = OpenAI(api_key='')
from stringcolor import *

# Make sure to set up your API key

# Use AI to generate a response
def get_chatgpt_response(messages):
    # messages is the whole conversation
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # set model here
        messages=messages,   # The ongoing conversation      [{'role':'system','content':'You are a helpful assistant.'},{'role':'user','content':''Hey whats upppp'}]
        temperature=1.0,
        max_tokens=1000,)
    return response.choices[0].message.content

# The chat interface loop
def chat_interface():
    print(cs("Welcome to ChatGPT!","blue"))
    print(cs("Type 'quit' to exit the chat.\n","darkblue"))
    system_role = """ You are santa claus""" # DEFINE SYSTEM ROLE HERE
    messages = [{"role": "system", "content": system_role}] 
    while True:
        user_input = input("YOU: ")
        if user_input.lower() == 'quit':
            break

        # Append user message to the messages list
        messages.append({"role": "user", "content": user_input})

        # Get AI response and append to messages
        response = get_chatgpt_response(messages)          
        print(cs(f"CHAT GPT: {response}","green"))
        messages.append({"role": "assistant", "content": response})

# Run the chat interface
if __name__ == '__main__':
    chat_interface()