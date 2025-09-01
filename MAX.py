import tkinter as tk
from tkinter import scrolledtext, END
from PIL import Image, ImageTk
import webbrowser
import speech_recognition as sr
import threading

# ==============================================================================
# 1. COMMAND HANDLERS
# ==============================================================================

def handle_exit(query):
    """Prepares the exit message."""
    return "Going offline. Goodbye!", True

def handle_google_search(query):
    """Opens Google search in a browser."""
    if not query:
        return "What would you like to search for on Google?", False
    webbrowser.open(f"https://google.com/search?q={query}")
    return f"Searching Google for '{query}'...", False

def handle_youtube_search(query):
    """Opens YouTube search in a browser."""
    if not query:
        return "What would you like to search for on YouTube?", False
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
    return f"Searching YouTube for '{query}'...", False

def handle_spotify_search(query):
    """Opens Spotify search or the app itself."""
    if query:
        webbrowser.open(f"spotify:search:{query}")
        return f"Searching for '{query}' on Spotify.", False
    else:
        webbrowser.open('spotify:')
        return "Opening Spotify.", False

# ==============================================================================
# 2. MAIN RESPONSE ROUTER
# ==============================================================================

def get_response(text_data):
    """
    Processes user input and routes to the appropriate handler.
    Returns a tuple: (response_text, should_exit_flag)
    """
    text_data_lower = text_data.lower()
    
    # Command registry: Maps keywords to handler functions
    # The order determines priority.
    COMMANDS = {
        ('exit', 'quit', 'goodbye'): handle_exit,
        ('google', 'search for', 'find'): handle_google_search,
        ('youtube', 'play on youtube'): handle_youtube_search,
        ('spotify', 'play on spotify', 'play'): handle_spotify_search,
    }

    for keywords, handler in COMMANDS.items():
        for keyword in keywords:
            if text_data_lower.startswith(keyword):
                query = text_data.lower().replace(keyword, "", 1).strip()
                return handler(query)

    # --- Default fallback response ---
    return "I'm not sure how to answer that. Try a search command like 'search for cats'.", False

# ==============================================================================
# 3. TKINTER GUI CLASS
# ==============================================================================

class ChatInterface:
    """The main class for the Tkinter Chat UI."""
    def __init__(self, root):
        self.root = root
        self.root.title("MAX Assistant")
        self.root.geometry("520x700")
        self.root.resizable(False, False)
        self.root.config(bg="#1c1c1c")

        # --- UI Elements ---
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

        # Voice search button
        try:
            self.mic_icon = ImageTk.PhotoImage(Image.open("mic_icon.png").resize((32, 32)))
            self.listen_button = tk.Button(input_frame, image=self.mic_icon, bg="#1c1c1c", command=self.start_listening_thread, relief=tk.FLAT, activebackground="#3e3e3e", cursor="hand2", borderwidth=0)
        except Exception:
            self.listen_button = tk.Button(input_frame, text="Mic", font=("Helvetica", 11, "bold"), bg="#3e3e3e", fg="#ffffff", command=self.start_listening_thread, relief=tk.FLAT, padx=10, activebackground="#5e5e5e", cursor="hand2")
        self.listen_button.pack(side=tk.RIGHT, fill='y', padx=(0, 5))

        self.display_message("MAX: Hello! I'm MAX. You can ask me to search Google, YouTube, or Spotify.")

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
        
        bot_response, should_exit = get_response(user_input)
        self.display_message(f"MAX: {bot_response}")

        if should_exit:
            self.root.after(2000, self.root.destroy)

    def start_listening_thread(self):
        """Starts the listening process in a new thread to avoid freezing the GUI."""
        threading.Thread(target=self.listen_and_process, daemon=True).start()

    def listen_and_process(self):
        """Listens for voice input and processes it."""
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.entry_box.delete(0, END)
            self.entry_box.insert(0, "Listening...")
            self.root.update_idletasks()
            r.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=10)
                self.entry_box.delete(0, END)
                self.entry_box.insert(0, "Recognizing...")
                text = r.recognize_google(audio)
                self.entry_box.delete(0, END)
                self.entry_box.insert(0, text)
                self.send_message()
            except sr.UnknownValueError:
                self.entry_box.delete(0, END)
                self.display_message("MAX: Sorry, I couldn't understand the audio.")
            except sr.RequestError as e:
                self.entry_box.delete(0, END)
                self.display_message(f"MAX: Could not request results; {e}")
            except Exception as e:
                self.entry_box.delete(0, END)
                self.display_message("MAX: Sorry, I didn't catch that.")

# ==============================================================================
# 4. APPLICATION ENTRY POINT
# ==============================================================================

if __name__ == '__main__':
    root = tk.Tk()
    app = ChatInterface(root)
    root.mainloop()