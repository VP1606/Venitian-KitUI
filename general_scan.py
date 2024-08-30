import websocket
import json
# from mfrc522 import SimpleMFRC522
# import RPi.GPIO as GPIO
import time

# reader = SimpleMFRC522()

def connect_websocket():
    ws = websocket.WebSocket()
    ws.connect("ws://")
    return ws


def main():
    ws = connect_websocket()

    try:
        while True:
            print("Hold a tag near the reader")
            # id, text = reader.read()
            id = "523"
            print(f"ID: {id}")
            data = {
                "identityCode": id,
                "cmd": "user_scanned"
            }
            try:
                ws.send(json.dumps(data))
            except (websocket.WebSocketConnectionClosedException, BrokenPipeError):
                print("Connection lost, reconnecting...")
                ws = connect_websocket()
                ws.send(json.dumps(data))
            time.sleep(0.5)
    except KeyboardInterrupt:
        # GPIO.cleanup()
        ws.close()
    except Exception as e:
        print(f"Unexpected error: {e}")
        # GPIO.cleanup()
        ws.close()

if __name__ == "__main__":
    main()