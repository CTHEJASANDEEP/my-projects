import tkinter as tk
from tkinter import scrolledtext, END
from PIL import Image, ImageTk, ImageSequence
import webbrowser
from datetime import datetime

def get_response(text_data):
    """
    Handles powerful local commands.
    Returns a tuple: (response_text, should_exit_flag)
    """
    text_data_lower = text_data.lower()
    
    # --- Priority 1: Local Exit Command ---
    if text_data_lower in ['exit', 'quit', 'goodbye']:
        return "Going offline. Goodbye!", True

    # --- Priority 2: Powerful Local Action Commands ---
    # GOOGLE SEARCH: "google", "search for", "find"
    if any(keyword in text_data_lower for keyword in ["google", "search for", "find"]):
        query = text_data_lower.replace("google", "").replace("search for", "").replace("find", "").strip()
        if not query:
            return "What would you like to search for on Google?", False
        webbrowser.open(f"https://google.com/search?q={query}")
        return f"Searching Google for '{query}'...", False

    # YOUTUBE SEARCH: "youtube", "play on youtube"
    if "youtube" in text_data_lower:
        query = text_data_lower.replace("youtube", "").replace("play on", "").strip()
        if not query:
            return "What would you like to search for on YouTube?", False
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        return f"Searching YouTube for '{query}'...", False

    # SPOTIFY: "spotify", "play on spotify"
    if "spotify" in text_data_lower:
        query = text_data_lower.replace("spotify", "").replace("play on", "").replace("play","").strip()
        if query:
            webbrowser.open(f"spotify:search:{query}")
            return f"Searching for '{query}' on Spotify.", False
        else:
            webbrowser.open('spotify:')
            return "Opening Spotify.", False
    
    # --- Default fallback response ---
    return "I'm not sure how to answer that. Try a search command like 'search for cats'.", False

class ChatInterface:
    """The main class for the Tkinter Chat UI."""
    def __init__(self, root):
        self.root = root
        self.root.title("MAX Assistant")
        self.root.geometry("520x700")
        self.root.resizable(False, False)

        # --- UI Elements ---
        try:
            self.bg_image = Image.open("naruto_bg.gif")
            self.bg_frames = [ImageTk.PhotoImage(frame.copy().resize((520, 700))) for frame in ImageSequence.Iterator(self.bg_image)]
            self.bg_label = tk.Label(self.root)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.animate_bg(0)
        except Exception as e:
            print("Info: Background GIF not found. Using solid color. Error:", e)
            self.root.config(bg="#1c1c1c")

        self.chat_area = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, bg="#1c1c1c", fg="#ffffff",
            font=("Consolas", 12), state='disabled', padx=10, pady=10, relief=tk.FLAT,
            borderwidth=0
        )
        self.chat_area.place(x=10, y=50, width=500, height=530)

        input_frame = tk.Frame(self.root, bg="#1c1c1c")
        input_frame.place(x=10, y=600, width=500, height=50)

        self.entry_box = tk.Entry(
            input_frame, bg="#2e2e2e", fg="#ffffff",
            font=("Consolas", 12), relief=tk.FLAT, insertbackground="#ffffff"
        )
        self.entry_box.pack(side=tk.LEFT, fill='both', expand=True, ipady=8, padx=(0,5))
        self.entry_box.bind("<Return>", self.send_message)

        self.send_button = tk.Button(
            input_frame, text="Send", font=("Helvetica", 11, "bold"),
            bg="#b30000", fg="#ffffff", command=self.send_message,
            relief=tk.FLAT, padx=10, activebackground="#ff0000", activeforeground="#ffffff",
            cursor="hand2"
        )
        self.send_button.pack(side=tk.RIGHT, fill='y')

        self.display_message("MAX: Hello! I'm MAX. You can ask me to search Google, YouTube, or Spotify.")

    def animate_bg(self, index):
        """Cycles through the frames of the background GIF."""
        frame = self.bg_frames[index]
        self.bg_label.configure(image=frame)
        self.root.after(100, self.animate_bg, (index + 1) % len(self.bg_frames))

    def display_message(self, message):
        """Displays a message in the chat area instantly."""
        self.chat_area.config(state='normal')
        self.chat_area.insert(END, message + "\n\n")
        self.chat_area.config(state='disabled')
        self.chat_area.yview(END)

    def send_message(self, event=None):
        """Handles the user sending a message."""
        user_input = self.entry_box.get()
        if not user_input.strip():
            return
        
        self.display_message(f"You: {user_input}")
        self.entry_box.delete(0, END)
        
        # Get response directly since commands are instant
        bot_response, should_exit = get_response(user_input)
        self.display_message(f"MAX: {bot_response}")

        if should_exit:
            self.root.after(2000, self.root.destroy)

if __name__ == '__main__':
    root = tk.Tk()
    app = ChatInterface(root)
    root.mainloop()
