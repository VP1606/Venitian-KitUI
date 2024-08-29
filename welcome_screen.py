import tkinter as tk
from PIL import Image, ImageTk
from pin_entry_page import PinEntryPage

class WelcomeScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        
        self.canvas = tk.Canvas(self, width=1024, height=600, bg="black")
        self.canvas.pack()
        
        # Load the background image
        background_image = Image.open("backboard.png")
        background_image = background_image.resize((1024, 600))
        background_photo = ImageTk.PhotoImage(background_image)
        
        # Create a background image on the self.canvas
        self.canvas.create_image(0, 0, image=background_photo, anchor="nw")  
        
        font_settings = ("Avenir", 25)
        
        self.canvas.create_text(1024 // 2, 220, text="W   E   L   C   O   M   E", fill="white", font=("Avenir-Heavy", 25))
        tk.Label(self, text='Scan Your Card or Enter Your PIN', fg='#B2B2B2', bg='black', font=font_settings).place(x=328, y=248)
        
        enter_pin_box = self.canvas.create_rectangle(387, 349, 637, 399, fill="#1A1A1A", outline="")
        enter_pin_title = self.canvas.create_text((387 + 637) // 2, (349 + 399) // 2, text="Enter PIN", fill="#C6C6C6", font=("Avenir-Heavy", 20))\
            
        self.canvas.tag_bind(enter_pin_box, "<Button-1>", self.enter_pin_btn)
        self.canvas.tag_bind(enter_pin_title, "<Button-1>", self.enter_pin_btn)
    
    def enter_pin_btn(self, event):
        self.master.show_screen(PinEntryPage)
