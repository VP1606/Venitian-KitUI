import tkinter as tk
from PIL import Image, ImageTk
import os
# from welcome_screen import WelcomeScreen
#empty commits
class FinalPage(tk.Frame):
    def __init__(self, master, name="Schnozz Bob"):
        super().__init__(master)
        self.master = master
        
        self.canvas = tk.Canvas(self, width=1024, height=600, bg="black")
        self.canvas.pack()
        
        # Load the background image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "final_backboard.png")
        background_image = Image.open(image_path)
        background_image = background_image.resize((1024, 600))
        self.background_photo = ImageTk.PhotoImage(background_image)
        
        # Create a background image on the self.canvas
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")  
        
        font_settings = ("Avenir", 25)
        
        self.canvas.create_text(1024 // 2, (265+11.5), text="Welcome In,", fill="#999999", font=("Avenir-Light", 17))
        self.canvas.create_text(1024 // 2, (293+20.5), text=name, fill="white", font=("Avenir-Heavy", 30))
        self.canvas.create_text(1024 // 2, (364+11.5), text="Entered at 10:20am", fill="#999999", font=("Avenir-Roman", 17))
        
        self.after(5000, self.go_to_next_screen)

    def go_to_next_screen(self):
        self.master.back_to_start()
