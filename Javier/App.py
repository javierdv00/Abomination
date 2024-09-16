import tkinter as tk
from tkinter import scrolledtext
import random
import multiprocessing
import secondary_file  # Import your secondary file that contains the function to run
from gpt import get_chatgpt_response

run_secondary_file_varible = False
machine_role = {
    "Football Player": """
    You are a football (soccer) player. 
    You enjoy writing about football with others.
    You participate in football discussions with a lot of passion.""",

    "Football Fan": """
    You are a football (soccer) fan. You enjoy talking about football.
    Remember, you are just a fan and not a professional, so you sometimes express partial knowledge.
    You can be a know-it-all.""",

    "Football Hater": """
    You don't like football (soccer). You speak negatively about it.
    You easily get emotional in discussions and conversations.
    When responding, you tend to write slightly longer texts."""
}

# Global variables to manage the secondary process and animation
secondary_process = None
secondary_process_started = False
animation_running = True  # Flag to control the animation

# Function to handle the start button action
def start_chat():
    user_name = name_entry.get().strip() or "You"  # Default to "You" if no name is entered
    selected_machine = machine_var.get()  # Get the selected machine option
    if selected_machine and selected_machine != "Select someone to talk":
        name_window.destroy()  # Close the name window
        open_chat_window(user_name, selected_machine)  # Open the chat window with the selected machine

# Function to create the Matrix-style background animation
def matrix_background(canvas, width, height):
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    drops = [0 for _ in range(width)]

    def animate_matrix():
        if not animation_running:
            return
        canvas.delete("matrix")  # Clear previous frame
        for i in range(len(drops)):
            text = random.choice(characters)
            x = i * 10  # Position each character column-wise
            y = drops[i] * 10
            canvas.create_text(x, y, text=text, fill="green", font=("Courier", 12), tag="matrix")
            if random.random() > 0.95:  # Randomly reset drop height
                drops[i] = 0
            drops[i] += 1
        canvas.after(50, animate_matrix)

    animate_matrix()

# Function to open the chat window with Matrix background
def open_chat_window(user_name, selected_machine):
    global messages, animation_running
    # Create the main chat window
    chat_window = tk.Tk()
    chat_window.title(f"Chat with the {selected_machine} - User: {user_name}")
    chat_window.geometry("1400x1000")  # Around 10"x15" size

    # Dark theme colors
    background_color = "#1e1e1e"
    input_background_color = "#333333"
    text_color = "#ffffff"
    user_text_color = "#7CFC00"  # Green for user
    machine_text_color = "#00BFFF"  # Blue for machine

    chat_window.configure(bg=background_color)

    # Create a canvas for the Matrix background
    canvas = tk.Canvas(chat_window, width=1000, height=600, bg="black", highlightthickness=0)
    canvas.place(x=0, y=0, relwidth=1, relheight=1)

    # Start the Matrix animation in the background
    matrix_background(canvas, 100, 60)

    # Upper block: conversation display (with scrolling)
    conversation_area = scrolledtext.ScrolledText(
        chat_window, wrap=tk.WORD, state='disabled', height=20,
        bg=background_color, fg=text_color, insertbackground='white',
        font=("Arial", 16),  # Increased font size for better readability
        highlightthickness=1
    )
    conversation_area.place(relx=0.05, rely=0.07, relwidth=0.9, relheight=0.7)

    # Lower block: input field and send button
    input_frame = tk.Frame(chat_window, bg=background_color)
    input_frame.place(relx=0.05, rely=0.85, relwidth=0.9, relheight=0.1)

    input_field = tk.Text(input_frame, height=2, bg=input_background_color, fg=text_color, insertbackground='white',
                          font=("Arial", 14))  # Larger font for the input field
    input_field.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

    # Function to send a message and display in the conversation area
    def send_message():
        user_message = input_field.get("1.0", tk.END).strip()
        if user_message:
            # Display user message in the conversation area with bold username and green text
            conversation_area.config(state='normal')
            conversation_area.insert(tk.END, f"{user_name}: ", ('user_bold'))
            conversation_area.insert(tk.END, f"{user_message}\n", ('user_text'))
            conversation_area.tag_config('user_bold', foreground=user_text_color, font=("Arial", 16, "bold"))
            conversation_area.tag_config('user_text', foreground=user_text_color)
            conversation_area.yview(tk.END)  # Auto-scroll
            conversation_area.config(state='disabled')
            input_field.delete("1.0", tk.END)

            # Simulate machine response
            messages.append({"role": "user", "content": user_message})
            machine_response = get_chatgpt_response(messages)
            messages.append({"role": "assistant", "content": machine_response})
            conversation_area.insert(tk.END, f"{machine_response}\n", ('machine_text'))

            conversation_area.config(state='normal')
            conversation_area.insert(tk.END, "Machine: ", ('machine_bold'))
            conversation_area.insert(tk.END, f"{machine_response}\n", ('machine_text'))
            conversation_area.tag_config('machine_bold', foreground=machine_text_color, font=("Arial", 16, "bold"))
            conversation_area.tag_config('machine_text', foreground=machine_text_color)
            conversation_area.yview(tk.END)  # Auto-scroll
            conversation_area.config(state='disabled')

    # Bind the Enter key to trigger sending the message, but only when the input field is focused and non-empty
    def on_enter_key(event):
        if input_field.get("1.0", tk.END).strip():
            send_message()

    input_field.bind("<Return>", on_enter_key)

    send_button = tk.Button(input_frame, text="Send", command=send_message, bg='#444444', fg=text_color, bd=0,
                            font=("Arial", 14))  # Button with bigger text
    send_button.pack(side=tk.LEFT, padx=5, pady=5)

    # Back button to return to the first window
    back_button = tk.Button(chat_window, text="<--", command=lambda: back_to_start(chat_window), bg='#444444', fg=text_color, bd=0,
                            font=("Arial", 14))  # Button to go back
    back_button.place(relx=0.01, rely=0.01)  # Position the back button

    # Function to stop the secondary process when closing the GUI
    def on_closing():
        global secondary_process
        if secondary_process and secondary_process.is_alive():  # Check if the secondary process is still running
            secondary_process.terminate()  # Terminate the process
        chat_window.destroy()  # Close the chat window

    chat_window.protocol("WM_DELETE_WINDOW", on_closing)  # Bind the close event to stop the process

    # Insert the machine's initial message
    conversation_area.config(state='normal')
    conversation_area.insert(tk.END, "Machine: ", ('machine_bold'))

    system_role = machine_role[selected_machine]  # Get the role for the selected machine
    messages = [{"role": "system", "content": system_role}]
    machine_response = get_chatgpt_response(messages)
    messages.append({"role": "assistant", "content": machine_response})
    conversation_area.insert(tk.END, f"{machine_response}\n", ('machine_text'))

    conversation_area.tag_config('machine_bold', foreground=machine_text_color, font=("Arial", 16, "bold"))
    conversation_area.tag_config('machine_text', foreground=machine_text_color)
    conversation_area.config(state='disabled')

    chat_window.mainloop()

# Function to return to the first window
def back_to_start(current_window):
    global animation_running
    animation_running = False  # Stop the Matrix animation
    current_window.destroy()  # Close the current chat window
    main()  # Restart the main function to show the first window again

# Function to run the secondary file (replace 'run_secondary' with the function you want to run from secondary_file.py)
def run_secondary_file():
    global secondary_process_started
    if not secondary_process_started:
        global secondary_process

        #  Run the secondary file as a multiprocessing. So together (parallel) with the rest of the code.
        secondary_process = multiprocessing.Process(target=secondary_file.run_secondary, args=(run_secondary_file_varible,))
        secondary_process.start()
        secondary_process_started = True

# Main function to start the app
def main():
    # Initial window: Ask for the user's name
    global name_window, name_entry, machine_var
    name_window = tk.Tk()
    name_window.title("Enter your name to start")
    name_window.geometry("600x400")  # Adjusted to 600x400

    # Dark theme colors
    background_color = "#1e1e1e"
    input_background_color = "#333333"
    text_color = "#ffffff"

    name_window.configure(bg=background_color)

    # Name entry prompt with larger text size
    name_label = tk.Label(name_window, text="Enter your name:", bg=background_color, fg=text_color, font=("Arial", 20))
    name_label.pack(pady=20)

    name_entry = tk.Entry(name_window, width=30, bg=input_background_color, fg=text_color, insertbackground='white', font=("Arial", 20))
    name_entry.pack(pady=10)

    # Machine selection dropdown
    machine_var = tk.StringVar()
    machine_var.set("Select someone to talk")  # Default value
    machine_options = machine_role.keys()

    machine_menu = tk.OptionMenu(name_window, machine_var, *machine_options)
    machine_menu.config(bg=input_background_color, fg=text_color, font=("Arial", 20), width=20)
    machine_menu.pack(pady=10)

    # Start button (initially disabled)
    start_button = tk.Button(name_window, text="Start", state=tk.DISABLED, command=start_chat, bg='#444444', fg=text_color, bd=0,
                             font=("Arial", 20))
    start_button.pack(pady=20)

    # Function to enable/disable the start button based on user input
    def check_name_entry(*args):
        if machine_var.get() != "Select someone to talk":  # Only check machine selection
            start_button.config(state=tk.NORMAL)
        else:
            start_button.config(state=tk.DISABLED)

    # Trace the name entry and machine selection field to check if it's empty or not
    machine_var.trace("w", check_name_entry)  # Trace dropdown changes

    # Start the secondary process if not already started
    run_secondary_file()

    # Start the Tkinter event loop
    name_window.mainloop()

# Run the main function to start the application
if __name__ == "__main__":
    main()
