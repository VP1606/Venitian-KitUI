import tkinter as tk
from PIL import Image, ImageTk
from welcome_screen import WelcomeScreen
# from pin_entry_page import PinEntryPage as WelcomeScreen
#empty commit angellou Sutharsan
class Baseboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Baseboard")
        self.geometry("1024x600")
        self.attributes("-fullscreen", True)
        self.attributes("-type", "splash")
        self.current_frame = None
        self.show_screen(WelcomeScreen)

    def show_screen(self, screen_class, *args, **kwargs):
        new_frame = screen_class(self, *args, **kwargs)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack()
        
    def back_to_start(self):
        new_frame = WelcomeScreen(self)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack()

if __name__ == "__main__":
    app = Baseboard()
    app.mainloop()
