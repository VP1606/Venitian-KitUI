import tkinter as tk
from PIL import Image, ImageTk
from final_page import FinalPage
import mysql.connector
import os
import websockets
import json
import asyncio

class PairCardPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        
        asyncio.run(self.send_wss_confirmation())
        
        self.canvas = tk.Canvas(self, width=1024, height=600, bg="black")
        self.canvas.pack()
        
        # Load the background image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "backboard.png")
        background_image = Image.open(image_path)
        background_image = background_image.resize((1024, 600))
        self.background_photo = ImageTk.PhotoImage(background_image)
        
        # Create a background image on the canvas
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")
        
    async def send_wss_confirmation(self):
        async with websockets.connect("ws://73.157.88.153:8000/wss") as websocket:
            print("HI WSS PC")
            try:
                data = {
                        "cmd": "paircard_code_entered"
                }
                await websocket.send(json.dumps(data))
                print("DONE!!!")
            except Exception as e:
                print(f"Error sending confirmation: {e}")
        return
