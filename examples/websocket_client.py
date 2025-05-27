import asyncio
import websockets
import sys

# Prerequisites
# sudo apt-get install -y git python3-pip python3-venv
# venv creation : python3 -m venv ~/venv_websocket
# venv activation : source ~/venv_websocket/bin/activate
# packages installations :
#  pip install websockets


# Execution
# python3 ~/websocket_client.py


async def send_cmds():
    uri = "ws://<YOUR_WEBSOCKET_SERVER_IP>:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send("move:100,100")
        await websocket.send("move:100,-100")
        await websocket.send("move:100,100")
        await websocket.send("move:100,-100")

asyncio.run(send_cmds())
