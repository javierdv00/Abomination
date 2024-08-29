from openai import OpenAI

client = OpenAI(api_key='') # api key here


# just information for the user
def display_welcome_message():
    print("Welcome to ChatGPT!")
    print("Type 'quit' to exit the chat.\n")

# getting user input and return whatever he typed in
def get_user_input():
    return input("You: ")

# USING AI TO GET RESPONSE
def get_chatgpt_response(user_input, completions:int):
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",    # choosing model of openai's AI
        prompt=user_input,                  # choosing what to use for prompting
        max_tokens=150,                     # limit the maximum response tokens
        temperature=1.0,                    # choosing temperature (more random/creative here)
        n=completions,                      # modifiable completion number
        best_of=3,                          # Generates n * best_of completions and returns the best n.
        echo=False,                         # Return the user's input in the response if set to True
        presence_penalty=0.5,               # higher value = more likely to introduce new topics
        frequency_penalty=0.5               # higher value = more likely to repeat information
        )
    choices = []
    for i in range(completions):
        choices.append(response.choices[i].text.strip())
    return choices

# chat loop
def chat_interface():
    display_welcome_message()
    while True: # its not actually a chat, Completion can not remember
        user_input = get_user_input()
        if user_input.lower() == 'quit':
            break
        response = get_chatgpt_response(user_input, 1)
        print("CHAT GPT: ")
        for i in response:
            print(i)


# running the whole thing (explain name main thing?)
if __name__ == '__main__':
    chat_interface()