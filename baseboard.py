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

class Baseboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Baseboard")
        self.geometry("1024x600")
        self.attributes("-fullscreen", True)
        self.attributes("-type", "splash")
        self.current_frame = None
        
        self.start_updater_watcher()
        
        self.show_screen(WelcomeScreen)
        # self.show_screen(PairCardPage)
        
    def start_updater_watcher(self):
        # Create and start a thread to run the general_scan main function
        thread = threading.Thread(target=asyncio.run, args=(self.updater(),))
        thread.daemon = True  # This ensures the thread will close when the main program exits
        thread.start()

    def show_screen(self, screen_class, *args, **kwargs):
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

    async def updater(self):
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
        
        print("BYE WSS -- RETURNING")
        return

    async def receive_messages(self, websocket):
        try:
            async for message in websocket:
                print(f"Received message: {message}")
                # Handle the received message here
                # For example, you can update the UI or process the data
        except websockets.ConnectionClosed:
            print("WebSocket connection closed")

if __name__ == "__main__":
    app = Baseboard()
    app.mainloop()



