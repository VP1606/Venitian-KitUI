import tkinter as tk
from PIL import Image, ImageTk
from final_page import FinalPage

class PinEntryPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        
        self.canvas = tk.Canvas(self, width=1024, height=600, bg="black")
        self.canvas.pack()
        
        # Load the background image
        background_image = Image.open("backboard.png")
        background_image = background_image.resize((1024, 600))
        self.background_photo = ImageTk.PhotoImage(background_image)
        
        # Create a background image on the canvas
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")  
        
        # create_canvas_button(canvas, 100 + j * 100, 450 + i * 100, str(num), lambda e, num=num: print(f"Button {num} clicked"))
        
        self.pin_circles = []
        self.pin_numbers = []
        self.pin_string = ""
        
        start_x = 322
        start_y = 242
        # I -> EACH ROW
        for i in range(3):
            _start_y = start_y + (i * 60)
            #J -> BUILD EACH BTN FOR ROW
            for j in range(3):
                _start_x = start_x + (j * 130)
                num = i * 3 + j + 1
                self.create_canvas_button(_start_x, _start_y, str(num), lambda e, num=num: self.hit_keypad_number(num))
                
        self.create_canvas_button(start_x, 422, str("X"), lambda e, num="X": self.remove_number_pin(), rect_fill="#330C0C", text_fill="#C22D2D")
        self.create_canvas_button(start_x+130, 422, str(0), lambda e, num=0: self.hit_keypad_number(num))
        self.create_canvas_button(start_x+260, 422, str("Y"), lambda e, num="Y": self.validate_pin(), rect_fill="#1B3322", text_fill="#68C281")
                        
        self.update_pin_ui()
        
    def validate_pin(self):
        self.master.show_screen(FinalPage)
    
    def remove_number_pin(self):
        if len(self.pin_string) > 0:
            self.pin_string = self.pin_string[:-1]
            self.update_pin_ui()
        
    def hit_keypad_number(self, number):
        if len(self.pin_string) < 6:
            print(f"Button {number} clicked")
            self.pin_string += str(number)
            self.update_pin_ui()
        else:
            print(f"Button {number} ignored")
            pass
        
    def update_pin_ui(self):
        
        for text_id in self.pin_numbers:
            self.canvas.delete(text_id)
        for text_id in self.pin_circles:
            self.canvas.delete(text_id)
            
        self.pin_circles = []
        start_x = 347+15
        start_y = 140
        for i in range(6):
            _start_x = start_x + (i * 60)
            if i < len(self.pin_string):
                pass
            else:
                self.pin_circles.append(self.create_pin_circle(_start_x, start_y))
            
        self.pin_numbers = []
        start_x = 347+15
        start_y = 127+15
        for i in range(len(self.pin_string)):
            _start_x = start_x + (i * (36+24))
            self.pin_numbers.append(self.canvas.create_text(_start_x, start_y, text=str(self.pin_string[i]), fill="white", font=("Avenir-Black", 40)))
        
    def create_pin_circle(self, x, y):
        radius = 15
        x1 = x - radius
        y1 = y - radius
        x2 = x + radius
        y2 = y + radius
        
        # Create the circle (oval) on the canvas
        circle = self.canvas.create_oval(x1, y1, x2, y2, fill="#161616", outline="")
        return circle
        
    def create_canvas_button(self, x1, y1, text, callback, rect_fill="#1A1A1A", text_fill="#BABABA"):
        button_width = 120
        button_height = 50
        
        x2 = x1 + button_width
        y2 = y1 + button_height
        
        # Create a rectangle
        rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=rect_fill, outline="")
        # Create text on top of the rectangle
        text_id = self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=text, fill=text_fill, font=("Avenir-Black", 30))
        # Bind the click event to the rectangle and text
        self.canvas.tag_bind(rect, "<Button-1>", callback)
        self.canvas.tag_bind(text_id, "<Button-1>", callback)
        return rect, text_id
