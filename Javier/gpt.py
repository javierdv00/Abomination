from openai import OpenAI


# Make sure to set up your API key

# Use AI to generate a response
def get_chatgpt_response(messages):
    # messages is the whole conversation
    try:
        key = ''  # PUT HERE THE KEY
        client = OpenAI(api_key=key)
        response = client.chat.completions.create(
            model="gpt-4o",  # set model here
            messages=messages,   # The ongoing conversation      [{'role':'system','content':'You are a helpful assistant.'},{'role':'user','content':''Hey whats upppp'}]
            temperature=1.0,
            max_tokens=3000,)
        return response.choices[0].message.content
    except:
        return 'Not a conection'
