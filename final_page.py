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
    background_image = Image.open("final_backboard.png")
    background_image = background_image.resize((1024, 600))
    background_photo = ImageTk.PhotoImage(background_image)
    
    # Create a background image on the canvas
    canvas.create_image(0, 0, image=background_photo, anchor="nw")  
    
    font_settings = ("Avenir", 25)
    
    canvas.create_text(1024 // 2, (265+11.5), text="Welcome In,", fill="#999999", font=("Avenir-Light", 17))
    canvas.create_text(1024 // 2, (293+20.5), text="Hector Fernandez", fill="white", font=("Avenir-Heavy", 30))
    canvas.create_text(1024 // 2, (364+11.5), text="Entered at 10:20am", fill="#999999", font=("Avenir-Roman", 17))
    
    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()