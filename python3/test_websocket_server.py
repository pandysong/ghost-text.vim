import asyncio
import websockets


# class WebsocketServer:
#    def __init__(self):
#        pass
#    def _handler

# wakeup hack for windows
async def wakeup():
    while True:
        await asyncio.sleep(1)


async def hello(websocket, path):
    msg = await websocket.recv()
    print(msg)

    # greeting = f"Hello {name}!"

    # await websocket.send(greeting)
    # print(f"> {greeting}")

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
