import websockets


class WebsocketServer:
    '''Aysnc WebsocketServer
    '''

    def __init__(self, loop, handler):
        self.loop = loop
        self.handler = handler

    def serve_coro(self):
        async def serve(websocket, path):
            while True:
                try:
                    msg = await websocket.recv()
                    await self.handler(msg)
                except websockets.exceptions.ConnectionClosed:
                    break
            print("connection closed")
        return serve

    def start(self, host='localhost', port='8765'):
        start_server = websockets.serve(self.serve_coro(), host, port)
        self.server = self.loop.run_until_complete(start_server)
        print('websockets server listen on {}:{}'.format(host, port))

    def close(self):
        self.server.close()
        self.loop.run_until_complete(self.server.wait_closed)
