import tkinter as tk
from PIL import Image, ImageTk
from welcome_screen import WelcomeScreen
# from pin_entry_page import PinEntryPage as WelcomeScreen
from PairCard import PairCardPage
import websockets
import os
import json
import asyncio
class Baseboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Baseboard")
        self.geometry("1024x600")
        self.attributes("-fullscreen", True)
        self.attributes("-type", "splash")
        self.current_frame = None
        asyncio.run(self.updater())
        self.show_screen(WelcomeScreen)
        # self.show_screen(PairCardPage)

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
            except Exception as e:
                print(f"Error sending confirmation: {e}")
        return



if __name__ == "__main__":
    app = Baseboard()
    app.mainloop()



