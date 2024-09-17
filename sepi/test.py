import customtkinter as ctk
import json
import requests
from PIL import Image, ImageTk
from io import BytesIO
from db_for_ai import conectorDatabase
from openai import OpenAI
import os

# Load settings
with open('/home/dci-student/Abomination/sepi/setings.json', 'r') as file:
    data = json.load(file)

# Class from your code that connects to DB and interacts with OpenAI API
class Oaica2(conectorDatabase):
    def __init__(self, image_name="image") -> None:
        super().__init__()
        curs, conn = self.conect_to_database("userki43")
        query = "SELECT prompt FROM KI_Role;"
        curs.execute(query)
        self.system_prompt = [prompt[0] for prompt in curs.fetchall()]
        self.image_name = image_name

    def get_text_response(self, message, decision_maker=None) -> str:
        global data
        messages = []
        messages.append({"role": "system", "content": self.system_prompt[decision_maker]})
        messages.append({"role": "user", "content": message})
        print(data["API-Key"])
        client = OpenAI(api_key=data["API-Key"])
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=1.0,
            max_tokens=4000
        )
        return response.choices[0].message.content

    def get_image_response(self, description_for_image, how_many_image=1, how_many_try=None):
        global data
        if how_many_try is None:
            how_many_try = how_many_image * 2
            if how_many_try < 5:
                how_many_try = 5

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

# GUI for the AI Chat and Image Generation
class AIAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Chat & Image Generator")
        self.root.geometry("800x600")

        self.ai_handler = Oaica2()

        # Input frame
        self.input_frame = ctk.CTkFrame(self.root)
        self.input_frame.pack(pady=20, padx=20, fill="x")

        # User input
        self.prompt_label = ctk.CTkLabel(self.input_frame, text="Enter your message or description:")
        self.prompt_label.pack(anchor="w")

        self.user_input = ctk.CTkEntry(self.input_frame, width=500)
        self.user_input.pack(pady=10)

        # Dropdown for role selection
        self.role_label = ctk.CTkLabel(self.input_frame, text="Select Role:")
        self.role_label.pack(anchor="w")

        self.role_selector = ctk.CTkComboBox(self.input_frame, values=["Journalist", "Football Player", "Fan", "Hater"])
        self.role_selector.pack(pady=10)

        # Text Generation Button
        self.text_button = ctk.CTkButton(self.input_frame, text="Generate Text", command=self.generate_text)
        self.text_button.pack(pady=10)

        # Image Generation Button
        self.image_button = ctk.CTkButton(self.input_frame, text="Generate Image", command=self.generate_image)
        self.image_button.pack(pady=10)

        # Result Display
        self.result_frame = ctk.CTkFrame(self.root)
        self.result_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.result_text = ctk.CTkTextbox(self.result_frame, width=750, height=200)
        self.result_text.pack(pady=10)

        # Image Display
        self.image_label = ctk.CTkLabel(self.result_frame, text="")
        self.image_label.pack(pady=10)

    def generate_text(self):
        user_message = self.user_input.get()
        selected_role = self.role_selector.get()

        # Match role selection to the correct system prompt index
        role_map = {
            "Journalist": 0,
            "Football Player": 1,
            "Fan": 2,
            "Hater": 3
        }
        role_index = role_map.get(selected_role, 0)

        # Get the response from AI
        response = self.ai_handler.get_text_response(user_message, decision_maker=role_index)
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", response)

    def generate_image(self):
        description = self.user_input.get()
        images = self.ai_handler.get_image_response(description, how_many_image=1)

        if images:
            image = Image.open(images[0])
            img_resized = image.resize((400, 300), Image.ANTIALIAS)
            img_tk = ImageTk.PhotoImage(img_resized)

            self.image_label.configure(image=img_tk)
            self.image_label.image = img_tk

# Initialize CustomTkinter App
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    app = AIAppGUI(root)
    root.mainloop()
