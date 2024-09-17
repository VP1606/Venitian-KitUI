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

class Baseboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Baseboard")
        self.geometry("1024x600")
        self.attributes("-fullscreen", True)
        self.attributes("-type", "splash")
        self.current_frame = None
        
        self.start_updater_watcher()
        
        self._pc_card_id = None
        
        self.accessible_current_frame = None
        self.show_screen(WelcomeScreen)
        self.current_frame.start_background_scanning()
        # self.show_screen(PairCardPage)
        
    @property
    def pc_card_id(self):
        return self._pc_card_id

    @pc_card_id.setter
    def pc_card_id(self, value):
        self.pc_card_id = value
        if self.current_frame and hasattr(self.current_frame, "update_card_id_master"):
            self.current_frame.update_card_id_master(value)
        
    def start_updater_watcher(self):
        # Create and start a thread to run the general_scan main function
        thread = threading.Thread(target=asyncio.run, args=(self.updater(),))
        thread.daemon = True  # This ensures the thread will close when the main program exits
        thread.start()

    def show_screen(self, screen_class, *args, **kwargs):
        self.accessible_current_frame = screen_class
        new_frame = screen_class(self, *args, **kwargs)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack()
        
    def back_to_start(self):
        self.accessible_current_frame = WelcomeScreen
        new_frame = WelcomeScreen(self)
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack()

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



