import tkinter as tk
from PIL import Image, ImageTk
from final_page import FinalPage
import mysql.connector
import os
import websockets
import json
import asyncio
import random

import threading
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

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
        
        tk.Label(self, text='Place New Card', fg='#FFFFFF', bg='black', font=("Avenir-Heavy", 30)).place(x=400, y=173)
        tk.Label(self, text='Place the new card on the RFID sensor to scan.', fg='#B2B2B2', bg='black', font=("Avenir", 18)).place(x=323, y=233)
        tk.Label(self, text='You can assign the card to a user using the mobile app.', fg='#B2B2B2', bg='black', font=("Avenir", 18)).place(x=290, y=258)
        
        tk.Label(self, text='CARD ID', fg='#FFFFFF', bg='black', font=("Avenir-Light", 18)).place(x=476, y=354)
        # self.card_number_shower = tk.Label(self, text='PENDING', fg='#FFFFFF', bg='black', font=("Avenir-Heavy", 30)).place(x=442, y=385)
        self.card_number_shower = self.canvas.create_text(1024/2, 405, text='PENDING', fill="#FFFFFF", font=("Avenir-Heavy", 30))
        
        self.simulate_card_numbers = [427984682468, 497802935349, 769039985930, 894395552477]
        
        self.simulate_box = self.canvas.create_rectangle(362, 442, 662, 482, fill="#1924FF", outline="")
        self.simulate_title = self.canvas.create_text((362 + 662) // 2, (442 + 482) // 2, text="Simulate", fill="#FFFFFF", font=("Avenir-Heavy", 20))
        
        self.exit_box = self.canvas.create_rectangle(362, 492, 662, 532, fill="#FF1934", outline="")
        self.exit_title = self.canvas.create_text((362 + 662) // 2, (492 + 532) // 2, text="Exit", fill="#FFFFFF", font=("Avenir-Heavy", 20))
        
        self.canvas.tag_bind(self.simulate_box, "<Button-1>", self.simulate_card)
        self.canvas.tag_bind(self.simulate_title, "<Button-1>", self.simulate_card)
        
        self.canvas.tag_bind(self.exit_box, "<Button-1>", self.exit_pc)
        self.canvas.tag_bind(self.exit_title, "<Button-1>", self.exit_pc)
        
        self.selected_card = None
        # self.start_background_scanning()
        
    def update_card_id_master(self, value):
        print("UPDATING CARD ID MASTER")
        self.selected_card = value.__name__
        self.canvas.itemconfig(self.card_number_shower, text=str(self.selected_card))
        asyncio.run(self.send_wss_cardscan())
        
    def start_background_scanning(self):
        # Create and start a thread to run the general_scan main function
        thread = threading.Thread(target=asyncio.run, args=(self.general_scan(),))
        thread.daemon = True  # This ensures the thread will close when the main program exits
        thread.start()
        
    async def general_scan(self):
        reader = SimpleMFRC522()
        try:
            while True:
                
                if self.master.accessible_current_frame != PairCardPage:
                    break
                
                print("Hold a tag near the reader FROM PAIRCARD")
                id, text = reader.read()
                # id = "523"
                print(f"ID: {id}")
                self.selected_card = id
                self.canvas.itemconfig(self.card_number_shower, text=str(self.selected_card))
                asyncio.run(self.send_wss_cardscan())
        except KeyboardInterrupt:
            GPIO.cleanup()
        
    def exit_pc(self, event):
        self.master.back_to_start()
        
    def simulate_card(self, event):
        card_number = random.choice(self.simulate_card_numbers)
        self.selected_card = card_number
        self.canvas.itemconfig(self.card_number_shower, text=str(self.selected_card))
        asyncio.run(self.send_wss_cardscan())
        
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
    
    async def send_wss_cardscan(self):
        async with websockets.connect("ws://73.157.88.153:8000/wss") as websocket:
            print("HI WSS PC CS")
            try:
                data = {
                        "cmd": "paircard_idcode_submit",
                        "idcode": str(self.selected_card)
                }
                await websocket.send(json.dumps(data))
                print("DONE!!!")
            except Exception as e:
                print(f"Error sending confirmation: {e}")
        return
