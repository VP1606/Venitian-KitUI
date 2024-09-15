import tkinter as tk
from PIL import Image, ImageTk
from welcome_screen import WelcomeScreen
# from pin_entry_page import PinEntryPage as WelcomeScreen
from PairCard import PairCardPage
import websockets
import os
import json
import asyncio
import threading
import os

from final_page import FinalPage

from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

import mysql.connector

class Baseboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Baseboard")
        self.geometry("1024x600")
        self.attributes("-fullscreen", True)
        self.attributes("-type", "splash")
        self.current_frame = None
        
        self.current_screen = None
        
        self.start_updater_watcher()
        self.start_background_scanning()
        
        self.show_screen(WelcomeScreen)
        # self.show_screen(PairCardPage)
        
    def start_updater_watcher(self):
        # Create and start a thread to run the general_scan main function
        thread = threading.Thread(target=asyncio.run, args=(self.updater(),))
        thread.daemon = True  # This ensures the thread will close when the main program exits
        thread.start()

    def show_screen(self, screen_class, *args, **kwargs):
        self.current_screen = screen_class
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
        
    def start_background_scanning(self):
        # Create and start a thread to run the general_scan main function
        thread = threading.Thread(target=asyncio.run, args=(self.general_scan(),))
        thread.daemon = True  # This ensures the thread will close when the main program exits
        thread.start()
        
    async def general_scan(self):
        reader = SimpleMFRC522()
        try:
            while True:
                print("Hold a tag near the reader")
                id, text = reader.read()
                # id = "523"
                print(f"ID: {id}")
                
                if self.current_screen == WelcomeScreen:
                    self.welcome_screen_scan_handler(id)
                    
                GPIO.cleanup()
                reader.read_no_block()
                
        except Exception as e:
            print(f"Unexpected error: {e}")
            GPIO.cleanup()   
             
        print("Bye Bye")
    
    async def welcome_screen_scan_handler(self, id):
        async with websockets.connect("ws://73.157.88.153:8000/wss") as websocket:
            try:
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
                    
                    self.master.show_screen(FinalPage, name=results[0][1])
                    return
                else:
                    print("INVALID PIN")
            except Exception as e:
                print(f"Unexpected error: {e}")
                await websocket.close()

    async def updater(self):
        while True:
            try:
                async with websockets.connect("ws://73.157.88.153:8000/wss") as websocket:
                    print("HI WSS")
                    try:
                        commit_hash = os.popen('git rev-parse HEAD').read().strip()
                        data = {
                                "cmd": "insert_hash", 
                                "piHash": commit_hash
                        }
                        await websocket.send(json.dumps(data))
                        print("DONE!!!")
                        await self.receive_messages(websocket)
                    except Exception as e:
                        print(f"Error sending confirmation: {e}")
            except (websockets.ConnectionClosed, ConnectionRefusedError) as e:
                print(f"WebSocket connection failed: {e}. Retrying in 3 seconds...")
                await asyncio.sleep(3)
        
        print("BYE WSS -- RETURNING")
        return

    async def receive_messages(self, websocket):
        try:
            async for message in websocket:
                print(f"Received message: {message}")
                try:
                    payload = json.loads(message)
                    cmd = payload["cmd"]
                    
                    if cmd == "kit_update_now_trigger_rec":
                        print("TRIGGER UPDATE")
                        os.system("sh ./update-kit.sh")
                        print("Back out of SH.")
                
                except Exception as e:
                    print(f"Error processing message: {e}")
                
        except websockets.ConnectionClosed:
            print("WebSocket connection closed")

if __name__ == "__main__":
    app = Baseboard()
    app.mainloop()



