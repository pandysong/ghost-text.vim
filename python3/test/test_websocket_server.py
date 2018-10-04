import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.abspath(os.path.join(dir_path, '..'))
sys.path.insert(0, parent_path)
print(sys.path)

import asyncio
import websockets


async def wakeup():
    while True:
        await asyncio.sleep(1)


async def hello(websocket, path):
    while True:
        try:
            msg = await websocket.recv()
        except websockets.exceptions.ConnectionClosed:
            break
        print(msg)
    print("connection closed")

start_server = websockets.serve(hello, 'localhost', 8765)
loop = asyncio.get_event_loop()
loop.run_until_complete(start_server)

# add wakeup HACK for windows
loop.create_task(wakeup())

try:
    loop.run_forever()
except KeyboardInterrupt as e:
    pass

loop.run_forever()
