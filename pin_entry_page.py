import tkinter as tk
from PIL import Image, ImageTk

def main():
    global root
    # Create the main window with specified size and background color
    root = tk.Tk()
    root.geometry("1024x600")
    # root.configure(bg='black')
    
    # Create a Canvas widget
    canvas = tk.Canvas(root, width=1024, height=600, bg="black")
    canvas.pack()
    
    # Load the background image
    background_image = Image.open("backboard.png")
    background_image = background_image.resize((1024, 600))
    background_photo = ImageTk.PhotoImage(background_image)
    
    # Create a background image on the canvas
    canvas.create_image(0, 0, image=background_photo, anchor="nw")  
    
    # create_canvas_button(canvas, 100 + j * 100, 450 + i * 100, str(num), lambda e, num=num: print(f"Button {num} clicked"))
    global pin_circles, pin_numbers, pin_string
    
    pin_circles = []
    pin_numbers = []
    pin_string = ""
    
    start_x = 322
    start_y = 242
    # I -> EACH ROW
    for i in range(3):
        _start_y = start_y + (i * 60)
        #J -> BUILD EACH BTN FOR ROW
        for j in range(3):
            _start_x = start_x + (j * 130)
            num = i * 3 + j + 1
            create_canvas_button(canvas, _start_x, _start_y, str(num), lambda e, num=num: hit_keypad_number(num, canvas))
            
    create_canvas_button(canvas, start_x, 422, str("X"), lambda e, num="X": remove_number_pin(canvas), rect_fill="#330C0C", text_fill="#C22D2D")
    create_canvas_button(canvas, start_x+130, 422, str(0), lambda e, num=0: hit_keypad_number(num, canvas))
    create_canvas_button(canvas, start_x+260, 422, str("Y"), lambda e, num="Y": print(f"Button {num} clicked"), rect_fill="#1B3322", text_fill="#68C281")
                    
    pin_numbers, pin_circles = update_pin_ui(canvas=canvas)
    
    # Start the GUI event loop
    root.mainloop()
    
def remove_number_pin(canvas):
    global pin_circles, pin_numbers, pin_string
    if len(pin_string) > 0:
        pin_string = pin_string[:-1]
        update_pin_ui(canvas)
    
def hit_keypad_number(number, canvas):
    global pin_circles, pin_numbers, pin_string
    if len(pin_string) < 6:
        print(f"Button {number} clicked")
        pin_string += str(number)
        update_pin_ui(canvas=canvas)
    else:
        print(f"Button {number} ignored")
        pass
    
    return pin_string
    
def update_pin_ui(canvas):
    global pin_string, pin_numbers, pin_circles
    
    for text_id in pin_numbers:
        canvas.delete(text_id)
    for text_id in pin_circles:
        canvas.delete(text_id)
        
    pin_circles = []
    start_x = 347+15
    start_y = 140
    for i in range(6):
        _start_x = start_x + (i * 60)
        if i < len(pin_string):
            pass
        else:
            pin_circles.append(create_pin_circle(canvas, _start_x, start_y))
        
    pin_numbers = []
    start_x = 347+15
    start_y = 127+15
    for i in range(len(pin_string)):
        _start_x = start_x + (i * (36+24))
        pin_numbers.append(canvas.create_text(_start_x, start_y, text=str(pin_string[i]), fill="white", font=("Avenir-Black", 40)))
    
    return pin_numbers, pin_circles
    
def create_pin_circle(canvas, x, y):
    radius = 15
    x1 = x - radius
    y1 = y - radius
    x2 = x + radius
    y2 = y + radius
    
    # Create the circle (oval) on the canvas
    circle = canvas.create_oval(x1, y1, x2, y2, fill="#161616", outline="")
    return circle
    
def create_canvas_button(canvas, x1, y1, text, callback, rect_fill="#1A1A1A", text_fill="#BABABA"):
    button_width = 120
    button_height = 50
    
    x2 = x1 + button_width
    y2 = y1 + button_height
    
    # Create a rectangle
    rect = canvas.create_rectangle(x1, y1, x2, y2, fill=rect_fill, outline="")
    # Create text on top of the rectangle
    text_id = canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=text, fill=text_fill, font=("Avenir-Black", 30))
    # Bind the click event to the rectangle and text
    canvas.tag_bind(rect, "<Button-1>", callback)
    canvas.tag_bind(text_id, "<Button-1>", callback)
    return rect, text_id

if __name__ == "__main__":
    main()