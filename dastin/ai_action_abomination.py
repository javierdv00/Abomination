from openai import OpenAI
import json
from db_for_ai import conectorDatabase
import requests
from PIL import Image
from io import BytesIO
import os

with open('setings.json','r') as file:
    data = json.load(file)

class Oaica2(conectorDatabase):
    def __init__(self, image_name="image") -> None:
        super().__init__()
        curs, conn = self.conect_to_database("userki43")
        query = "SELECT prompt FROM KI_Role;"
        curs.execute(query)
        self.system_prompt = [prompt[0] for prompt in curs.fetchall()]
        """
        # Jornalist for wrting text about Football
        self.system_prompt.append("You are an AI assistant specializing in writing articles about football. You create informative, engaging, and well-researched texts about teams, players, coaches, tactics, and current events in football. Make sure to write clearly, precisely, and in an entertaining manner.")
        # For Chating with a Footballplayer
        self.system_prompt.append("You are a football (soccer) player. You enjoy writing about football with others. You participate in football discussions with a lot of passion.")
        # for chatting with a other footballfan
        self.system_prompt.append("You are a football (soccer) fan. You enjoy talking about football. Remember, you are just a fan and not a professional, so you sometimes express partial knowledge. You can be a know-it-all.")
        # for chatting with a Football hater
        self.system_prompt.append("You don't like football (soccer). You speak negatively about it. You easily get emotional in discussions and conversations. When responding, you tend to write slightly longer texts.")
        """
        self.image_name = image_name

    # decision_maker for right role       

    def get_chating(self, message):
        client = OpenAI(api_key=data["API-Key"]) 
        response = client.chat.completions.create(
        model="gpt-4o",  # set model here
        messages=message,  
        # The ongoing conversation[{'role':'system','content':'You are a helpful assistant.'},{'role':'user','content':''Hey whats upppp'}]
        temperature=1.0,
        max_tokens=4000,)
        #print(response)
        return response.choices[0].message.content    

    def get_text_response(self, message, decision_maker=None) -> str:
        global data

        messages = []
        messages.append({"role": "system", "content": self.system_prompt[decision_maker]})
        messages.append({"role": "user", "content": message})

        #return self.get_text_response(messages=output)

        client = OpenAI(api_key=data["API-Key"]) 
        response = client.chat.completions.create(
        model="gpt-4o",  # set model here
        messages=messages, 
        response_format={ "type": "json_object" },  
        # The ongoing conversation[{'role':'system','content':'You 
        #  a helpful assistant.'},{'role':'user','content':''Hey whats upppp'}]
        temperature=1.0,
        max_tokens=4000,)
        #print(response)
        return response.choices[0].message.content

    def get_image_response(self, description_for_image, how_many_image=1, how_many_try=None, ignore_all=None):
        global data
        if how_many_try == None:
            how_many_try = how_many_image * 2
            if how_many_try < 5:
                how_many_try = 5
        client = OpenAI(api_key=data["API-Key"])        
        if not os.path.exists("image_number.json"):
            with open("image_number.json", 'w') as file:
                json.dump( {"number": 0}, file, indent=4) 
        with open('image_number.json','r') as file:
            data1 = json.load(file)             
        index = data1["number"] +1
        how_many_image = index + how_many_image
        fail = 0
        image_list = []
        while (index < how_many_image) or ((fail + index) < how_many_try):            
            try:
                response = client.images.generate(
                    model="dall-e-3",
                    prompt= description_for_image,
                    size = "1792x1024",
                    quality="hd",
                    n=1
                )
            except Exception as e:
                response = None
                print(f"Fail:{e}")
                fail = fail + 1
            if response:
                image_url = response.data[0].url
                response = requests.get(image_url)
                image = Image.open(BytesIO(response.content))
                image_path = f"pictureF{index}.png"  # Hier kannst du den gewünschten Pfad und Dateinamen angeben
                image.save(image_path)

                data1["number"] = index
                with open('image_number.json', 'w') as file:
                    json.dump(data1, file, indent=4)
                index = index + 1
                image_list.append(image_path)
        return image_list


# only for testing 

def testing_example():
    obj = Oaica2()
    answer = obj.get_text_response(message="Write a articel with 200 Words about Leoni Messi", decision_maker=0)
    print(answer)
    with open("answer.json", "w") as json_file:
        json.dump(answer, json_file)
    obj.get_image_response("A dynamic shot of Lionel Messi, dribbling past defenders with effortless grace. His intense focus and exceptional control highlight his mastery of the game. The background shows a packed stadium, capturing the excitement and admiration of fans witnessing his brilliance on the pitch.", how_many_image=4, how_many_try=12)

 #   def get_image_response(self, description_for_image, how_many_image=1, how_many_try=None, ignore_all=None):
