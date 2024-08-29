import openai
import sys
import os
import json
import pyttsx3
from stringcolor import *

openai.api_key = ""  # Replace with your actual API key
model = "gpt-4o-mini"

# Initialize text-to-speech engine (its a bad one, there are better but more expensive like elevenlabs)
engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Load roles from JSON file 
script_path = os.path.dirname(os.path.realpath(__file__))
roles_file = os.path.join(script_path, 'roles.json')
with open(roles_file, 'r') as file:
    roles_data = json.load(file)

# printing available roles
def print_roles():
    for role in roles_data:
        print(role)

# getting a specific roles content (role description for system role of gpt)
def get_role(role_name):
    try:
        return roles_data[role_name]
    except KeyError:
        return None

# GETTING A RESPONSE FROM OPENAI GPT
def get_response(messages):
    response = openai.chat.completions.create(
        model=model, # chosen model (vary between chat.completions and .completion)
        messages=messages,  # List of message dictionaries
        temperature=0.5,  # Sampling temperature, between 0 and 1. Controls the creativity of the response. Lower values make the output more focused and deterministic, while higher values make it more random.
        max_tokens=100,  # Maximum number of tokens to generate by model in the chat completion
    )
    print(response)
    return response.choices[0].message.content

def chat_between_bots(bot1_name, bot2_name, conversation_turns):
    role1 = get_role(bot1_name)
    role2 = get_role(bot2_name)

    if not role1 or not role2:
        print(cs("One of the roles not found. Exiting.", "red"))
        return

    messages_bot1 = [{"role": "system", "content": role1}]
    messages_bot2 = [{"role": "system", "content": role2}]

    bot1_voice = voices[10].id
    bot2_voice = voices[11].id

    bot1_input = "Hey, how's it going?"

    for _ in range(conversation_turns):
        # Bot2 responds
        messages_bot2.append({"role": "user", "content": bot1_input})
        bot2_response = get_response(messages_bot2)
        messages_bot2.append({"role": "assistant", "content": bot2_response})
        
        print(cs(f"{bot1_name}: ", "LIGHTRED") + cs(bot1_input, "RED"))
        engine.setProperty('voice', bot1_voice)
        engine.say(bot1_input)
        engine.runAndWait()

        print(cs(f"{bot2_name}: ", "LIGHTBLUE") + cs(bot2_response, "BLUE"))
        engine.setProperty('voice', bot2_voice)
        engine.say(bot2_response)
        engine.runAndWait()

        # Bot1 responds
        messages_bot1.append({"role": "user", "content": bot2_response})
        bot1_input = get_response(messages_bot1)
        messages_bot1.append({"role": "assistant", "content": bot1_input})

def user_interacts_with_bot(bot_name):
    role = get_role(bot_name)

    if not role:
        print(cs("Role not found. Exiting.", "red"))
        return

    messages = [{"role": "system", "content": role}]
    bot_voice = voices[10].id

    while True:
        user_input = input(cs("You: ", "LIGHTGREEN"))
        if user_input.lower() in ['exit', 'quit']:
            break

        messages.append({"role": "user", "content": user_input})
        bot_response = get_response(messages)
        messages.append({"role": "assistant", "content": bot_response})

        print(cs(f"{bot_name}: ", "LIGHTBLUE") + cs(bot_response, "BLUE"))
        engine.setProperty('voice', bot_voice)
        engine.say(bot_response)
        engine.runAndWait()

def main_menu():
    os.system("clear") # need to apply more all over
    print("Welcome to the ChatBot Program")
    print("1. Chat between two bots")
    print("2. User interacts with one bot")
    print("3. Exit")

    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        print("Available roles:")
        print_roles()
        bot1_name = input("Enter role for bot1: ")
        bot2_name = input("Enter role for bot2: ")
        conversation_turns = int(input("Enter number of conversation turns: "))
        chat_between_bots(bot1_name, bot2_name, conversation_turns)
    elif choice == '2':
        print("Available roles:")
        print_roles()
        bot_name = input("Enter role for bot: ")
        user_interacts_with_bot(bot_name)
    elif choice == '3':
        print("Exiting program.")
        sys.exit()
    else:
        print(cs("Invalid choice. Try again.", "red"))

if __name__ == "__main__":
    while True:
        main_menu()