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
    
    font_settings = ("Avenir", 25)
    
    canvas.create_text(1024 // 2, 220, text="W   E   L   C   O   M   E", fill="white", font=("Avenir-Heavy", 25))
    tk.Label(root, text='Scan Your Card or Enter Your PIN', fg='#B2B2B2', bg='black', font=font_settings).place(x=328, y=248)
    
    enter_pin_box = canvas.create_rectangle(387, 349, 637, 399, fill="#1A1A1A", outline="")
    enter_pin_title = canvas.create_text((387 + 637) // 2, (349 + 399) // 2, text="Enter PIN", fill="#C6C6C6", font=("Avenir-Heavy", 20))\
        
    canvas.tag_bind(enter_pin_box, "<Button-1>", enter_pin_btn)
    canvas.tag_bind(enter_pin_title, "<Button-1>", enter_pin_btn)
    
    # Start the GUI event loop
    root.mainloop()
    

def enter_pin_btn(event):
    # Function to handle the click event and navigate to another page
    print("Navigating to the next page...")
    # Destroy the current window and open a new one
    for widget in root.winfo_children():
        widget.destroy()
    
    new_page()

def new_page():
    # Create a new frame for the new page
    new_frame = tk.Frame(root, width=1024, height=600, bg="white")
    new_frame.pack(fill="both", expand=True)
    
    # Add content to the new page
    tk.Label(new_frame, text="This is the new page", font=("Avenir", 25), bg="white").pack(pady=200)

if __name__ == "__main__":
    main()