import customtkinter as ctk

from PIL import Image, ImageTk
from io import BytesIO
from model_database_chatter_mine import *
import datetime
from backe_openai_inter_chatter_mine import Oaica2

class AIAppGUI:
    def __init__(self, root):
        self.database = databaseModel("userki910") # als database object -> settings
        self.root = root
        self.root.title("AI Chat & Image Generator") 
        self.root.geometry("800x600") #
        self.database.insert_to_Database("USERKI_RoleChat", ["ID_user", "ID_Ki_role"], [2, 1])
        self.ai_handler = Oaica2()
        self.role_model = 1
        
        self.background_image = Image.open("blue2.jpg") 
        self.background_image = self.background_image.resize((1920, 1080), Image.LANCZOS)  # Resize to fit
        self.bg_image_tk = ImageTk.PhotoImage(self.background_image)

    # Create a label to display the background image
        self.bg_label = ctk.CTkLabel(self.root, image=self.bg_image_tk)
        self.bg_label.place(relwidth=1, relheight=1)

        # Input frame
        self.result_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.result_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Input frame
        self.input_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.input_frame.pack(pady=2, padx=20, fill="both", expand=True)

        self.role_label = ctk.CTkLabel(self.input_frame, text="Select Role:")
        self.role_label.pack(pady=2)

        self.role_selector = ctk.CTkComboBox(self.input_frame, values=["Football Player", "Fan", "Hater"])
        self.role_selector.pack(pady=10,padx=10)

        self.prompt_label = ctk.CTkLabel(self.input_frame, text="Enter your message or description:", font=("helvetica", 18))
        self.prompt_label.pack(pady=1, padx=10,)

        self.user_input = ctk.CTkEntry(self.input_frame, width=500)
        self.user_input.pack(pady=1, padx=10)

        self.text_button = ctk.CTkButton(self.input_frame, text="Send Message - New Way", command=lambda: self.generate_text(0), font=("helvetica", 15), fg_color="#527BF4", text_color="black",corner_radius=12)
        self.text_button.pack(pady=10)
        
        self.text_button2 = ctk.CTkButton(self.input_frame, text="Send Message - Old Way", command=lambda: self.generate_text(1), font=("helvetica", 15), fg_color="#527BF4", text_color="black",corner_radius=12)
        self.text_button2.pack(pady=10)

        self.image_button = ctk.CTkButton(self.input_frame, text="Generate Image", command=self.generate_image, font=("helvetica", 15), fg_color="#527BF4", text_color="black",corner_radius=12)
        self.image_button.pack(pady=10)

        self.message_canvas = ctk.CTkScrollableFrame(self.result_frame)
        self.message_canvas.pack(fill="both", expand=True)

        self.image_label = ctk.CTkLabel(root)
        self.image_label.pack(pady=200)

    def generate_text(self, value_way):
        user_message = self.user_input.get() # F
        selected_role = self.role_selector.get() #f
        # Match role selection to the correct system prompt index
        role_map = { 
            "Football Player": 1,   
            "Fan": 2,
            "Hater": 3
        } # -> become it out the database 
        current_date = datetime.date.today() #b

        if self.role_model != role_map.get(selected_role, 0): # Checks if a different role is being used, as before.
            self.database.insert_to_Database("USERKI_RoleChat", ["ID_user", "ID_Ki_role"], [2, role_map.get(selected_role, 0)]) # create a new chat
        self.role_model = role_map.get(selected_role, 0)
        # Get the response from AI
        id_chat = self.database.id_chat() # search for the last chat id (for the new chat)
        self.database.insert_to_Database("USER_Message", ["ID_User", "ID_USERKI_RoleChat", "Message", "Date"], [2, id_chat, user_message, current_date]) # insert the user message
        response = self.ai_handler.get_text_response(user_message, decision_maker=self.role_model)
        self.database.insert_to_Database("USER_Message", ["ID_User", "ID_USERKI_RoleChat", "Message", "Date"], [2, id_chat, response, current_date]) # insert the ai message
        self.user_input.delete(0, "end") # clear user field

        chat_history = ""
        x = 1
        if value_way == 1:
            data = self.database.load_old_chat() # use the function for the old methodds with subquery
        else:
            data = self.database.load_chat() # use the new version of the function with using the view 
        for value in data: # for all messaege in the chat
            _message = value[0] # take the massage
            if x != 1:
                chat_history = chat_history + f"{selected_role}: {_message} - date: {value[1]}\n" # put name of ai his message and the date into the string
                x = 1 # change it to 1 for the switch to user
            else:
                chat_history = chat_history + f"user: {_message}  - date: {value[1]}\n" # same like the first onlly with the user
                x = x +1 # change it to 2 for the switch with ai
            
        for widget in self.message_canvas.winfo_children():
            widget.destroy()

        result_label = ctk.CTkLabel(self.message_canvas, text=chat_history, font=("helvetica", 16))

        result_label.pack(pady=10, padx=10)

        #self.result_text.insert("1.0", chat_history)

    def generate_image(self):                                                        
        description = self.user_input.get()
        images = self.ai_handler.get_image_response(description, how_many_image=1)

        if images:
            image = Image.open(images[0])
            img_resized = image.resize((1400, 800), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img_resized)
            self.image_label.configure(image=img_tk)
            self.image_label.image = img_tk

    def display_bubble_message(self, message, is_user):
        bubble_frame = ctk.CTkFrame(self.message_canvas)
        bubble_frame.pack(pady=5, padx=10, fill="x")

        if is_user:
            message_label = ctk.CTkLabel(bubble_frame, text=message, wraplength=400, justify="right", fg_color="#527BF4", font=("Arial", 12, "bold"), text_color="#527BF4", corner_radius=15,bg_color="darkblue")
            message_label.pack(pady=5, padx=10)
        else:
            message_label = ctk.CTkLabel(bubble_frame, text=message, wraplength=400, justify="left", fg_color="lightgrey", font=("Arial", 18, "bold"), text_color="black", corner_radius=15)
            message_label.pack(pady=5, padx=10)

        self.animate_message(message_label)

    def animate_message(self, frame, start_opacity=0.0):
        """Fade-in animation for new message bubbles."""
        if start_opacity <= 1.0:
            frame.configure(fg_color=f"#{int(255*start_opacity):02x}{int(255*start_opacity):02x}{int(255*start_opacity):02x}")
            start_opacity += 0.05
            frame.after(50, lambda: self.animate_message(frame, start_opacity))

# Initialize CustomTkinter App
if __name__ == "__main__":

    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    app = AIAppGUI(root)
    root.mainloop()
