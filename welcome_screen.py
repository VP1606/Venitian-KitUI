import tkinter as tk
from PIL import Image, ImageTk
from pin_entry_page import PinEntryPage
import os
import websockets
import threading
import json
import time
import asyncio
import mysql.connector
from final_page import FinalPage
from PairCard import PairCardPage
#from pin_entry_page import PinEntryPage as PairCardPage

from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

class WelcomeScreen(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        
        self.canvas = tk.Canvas(self, width=1024, height=600, bg="black")
        self.canvas.pack()
        
        # Load the background image
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, "backboard.png")
        background_image = Image.open(image_path)
        background_image = background_image.resize((1024, 600))
        self.background_photo = ImageTk.PhotoImage(background_image)
        
        # Create a background image on the self.canvas
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")  
        
        font_settings = ("Avenir", 25)
        
        self.canvas.create_text(1024 // 2, 220, text="W   E   L   C   O   M   E", fill="white", font=("Avenir-Heavy", 25))
        tk.Label(self, text='Scan Your Card or Enter Your PIN', fg='#B2B2B2', bg='black', font=font_settings).place(x=328, y=248)
        
        enter_pin_box = self.canvas.create_rectangle(387, 349, 637, 399, fill="#1A1A1A", outline="")
        enter_pin_title = self.canvas.create_text((387 + 637) // 2, (349 + 399) // 2, text="Enter PIN", fill="#C6C6C6", font=("Avenir-Heavy", 20))\
            
        self.canvas.tag_bind(enter_pin_box, "<Button-1>", self.enter_pin_btn)
        self.canvas.tag_bind(enter_pin_title, "<Button-1>", self.enter_pin_btn)
        
        self.start_background_scanning()
        
    def start_background_scanning(self):
        # Create and start a thread to run the general_scan main function
        thread = threading.Thread(target=asyncio.run, args=(self.general_scan(),))
        thread.daemon = True  # This ensures the thread will close when the main program exits
        thread.start()
        
    # async def general_scan(self):
    #     while True:
    #         if self.master.accessible_current_frame == WelcomeScreen:
    #             print(f"XYZ WELCOME {count}")
    #             self.master.test_variable = f"WELCOMESCR {count}"
    #         elif self.master.accessible_current_frame == PairCardPage:
    #             print(f"XYZ PINCARD {count}")
    #             self.master.test_variable = f"PINCARD {count}"
    #         else:
    #             pass
        
    async def general_scan(self):
        reader = SimpleMFRC522()
        async with websockets.connect("ws://73.157.88.153:8000/wss") as websocket:
            try:
                while True:
                    
                    if self.master.accessible_current_frame == WelcomeScreen:
                        
                        print("Hold a tag near the reader")
                        id, text = reader.read()
                        # id = "523"
                        print(f"ID: {id}")
                        
                        print("WELCOME SCREEN")
                        data = {
                            "identityCode": id,
                            "cmd": "user_scanned"
                        }
                        try:
                            await websocket.send(json.dumps(data))
                        except (websocket.WebSocketConnectionClosedException, BrokenPipeError):
                            print("Connection lost, reconnecting...")
                            # ws = connect_websocket()
                            await websocket.send(json.dumps(data))
                        
                        mydb = mysql.connector.connect(
                            host="73.157.88.153",
                            user="piuser",
                            password="password",
                            database="venitian"
                        )
            
                        mycursor = mydb.cursor()
                        sql = f"SELECT * FROM employees WHERE identity_code = {id}"
                        mycursor.execute(sql)
                        
                        results = mycursor.fetchall()
                        if len(results) == 1:
                            print("VALID PIN")
                            print(results)
                            mydb.close()
                            GPIO.cleanup()
                            reader.read_no_block()
                            self.master.show_screen(FinalPage, name=results[0][1])
                            return
                        else:
                            print("INVALID PIN")
                            
                        GPIO.cleanup()
                        reader.read_no_block()
                        reader = None
                    
                    elif self.master.accessible_current_frame == PairCardPage:
                        print("PIN CARD PAGE")
                        print("Hold a tag near the reader PC WC")
                        id, text = reader.read()
                        # id = "523"
                        print(f"ID: {id}")
                        # self.master.pc_card_id = id
                        self.master.current_frame.update_card_id(id=id)
                    
                    else:
                        #ignore
                        pass
                    
                    await asyncio.sleep(1)
                    
            except KeyboardInterrupt:
                GPIO.cleanup()
                await websocket.close()
            except Exception as e:
                print(f"Unexpected error: {e}")
                # GPIO.cleanup()
                await websocket.close()
    
    def enter_pin_btn(self, event):
        self.master.show_screen(PinEntryPage)
