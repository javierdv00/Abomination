from openai import OpenAI
import json
from model_database_chatter_mine import conectorDatabase
import requests
from PIL import Image
from io import BytesIO
import os

with open('setings_boi.json', 'r') as file:
    data = json.load(file)

class Oaica2(conectorDatabase):
    def __init__(self, image_name="image") -> None:
        super().__init__()
        curs, conn = self.conect_to_database("userki910")
        query = "SELECT prompt FROM KI_Role;" # change
        curs.execute(query)
        self.system_prompt = [prompt[0] for prompt in curs.fetchall()]
        self.image_name = image_name
        self.message = []
        self.deccision = None   

    def get_text_response(self, message, decision_maker) -> str:  
        global data
        
        if self.deccision != decision_maker:
            self.deccision = decision_maker
            self.message.clear()
            self.message.append({"role": "system", "content": self.system_prompt[decision_maker]})
        self.message.append({"role": "user", "content": message})
        client = OpenAI(api_key=data["API-Key"])
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=self.message,
            temperature=1.0,
            max_tokens=4000
        )
        answer = response.choices[0].message.content
        self.message.append({"role": "assistant", "content": answer})
        print("\n \n \n")
        return response.choices[0].message.content

    def get_image_response(self, description_for_image, how_many_image=1, how_many_try=2):
        global data

        client = OpenAI(api_key=data["API-Key"])
        if not os.path.exists("image_number.json"):
            with open("image_number.json", 'w') as file:
                json.dump({"number": 0}, file, indent=4)
        with open('image_number.json', 'r') as file:
            data1 = json.load(file)

        index = data1["number"] + 1
        how_many_image = index + how_many_image
        fail = 0
        image_list = []
        while (index < how_many_image) or ((fail + index) < how_many_try):
            try:
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=description_for_image,
                    size="1792x1024",
                    n=1
                )
            except Exception as e:
                print(f"Fail:{e}")
                fail += 1
            else:
                image_url = response.data[0].url
                response = requests.get(image_url)
                image = Image.open(BytesIO(response.content))
                image_path = f"pictureF{index}.png"
                image.save(image_path)
                data1["number"] = index
                with open('image_number.json', 'w') as file:
                    json.dump(data1, file, indent=4)
                index += 1
                image_list.append(image_path)
        return image_list
