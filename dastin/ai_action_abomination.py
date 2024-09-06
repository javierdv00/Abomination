from openai import OpenAI
import json

with open('setings.json','r') as file:
    data = json.load(file)
print(data["API-Key"])

class Oaica2():
    def __init__(self, ) -> None:
        self.system_prompt = []
        # Jornalist for wrting text about Football
        self.system_prompt.append("You are an AI assistant specializing in writing articles about football. You create informative, engaging, and well-researched texts about teams, players, coaches, tactics, and current events in football. Make sure to write clearly, precisely, and in an entertaining manner.")
        # For Chating with a Footballplayer
        self.system_prompt.append("You are a football (soccer) player. You enjoy writing about football with others. You participate in football discussions with a lot of passion.")
        # for chatting with a other footballfan
        self.system_prompt.append("You are a football (soccer) fan. You enjoy talking about football. Remember, you are just a fan and not a professional, so you sometimes express partial knowledge. You can be a know-it-all.")
        # for chatting with a Football hater
        self.system_prompt.append("You don't like football (soccer). You speak negatively about it. You easily get emotional in discussions and conversations. When responding, you tend to write slightly longer texts.")

    
    # message:output.append({"role": "system", message})
    # decision_maker for right role
    def main (self, message, decision_maker):
        output = []
        output.append({"role": "system", "content": self.system_prompt[decision_maker]})
        output.append({"role": "user", "content": message})
        return self.get_response(messages=output)
        
    def get_response(self, messages) -> str:
        global data
        client = OpenAI(api_key=data["API-Key"]) 
        response = client.chat.completions.create(
        model="gpt-4o",  # set model here
        messages=messages,   
        # The ongoing conversation[{'role':'system','content':'You are a helpful assistant.'},{'role':'user','content':''Hey whats upppp'}]
        temperature=1.0,
        max_tokens=4000,)
        #print(response)
        return response.choices[0].message.content

# only for testing 

def main():
    obj = Oaica2()
    answer = obj.main(message="Write a articel with 200 Words about Leoni Messi", decision_maker=0)
    print(answer)
    with open("answer.json", "w") as json_file:
        json.dump(answer, json_file)

main()
