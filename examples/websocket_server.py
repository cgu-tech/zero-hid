import asyncio
import websockets
from zero_hid import Mouse

# Prerequisites
# sudo apt-get install -y git python3-pip python3-venv
# cd ~ && git clone https://github.com/cgu-tech/zero-hid.git
# venv creation : python3 -m venv ~/venv_websocket
# venv activation : source ~/venv_websocket/bin/activate
# packages installations :
#  pip install --editable ~/zero-hid
#  pip install websockets


# Execution
# python3 ~/websocket_server.py

mouse = Mouse()

async def handle_client(websocket):
    print("Client connected")
    try:
        async for message in websocket:
            print("Received:", message)

            if message.startswith("move:"):
                dx, dy = map(int, message.replace("move:", "").split(","))
                print("Mouse move in progress:", dx, dy)
                mouse.move(dx, dy)
                print("Mouse move end:", dx, dy)

            elif message == "click:left":
                mouse.click("left")

            elif message == "click:right":
                mouse.click("right")

    except websockets.ConnectionClosed:
        print("Client disconnected")

async def main():
    async with websockets.serve(handle_client, "0.0.0.0", 8765):
        print("WebSocket server running at ws://0.0.0.0:8765")
        await asyncio.Future()  # Run forever

asyncio.run(main())
