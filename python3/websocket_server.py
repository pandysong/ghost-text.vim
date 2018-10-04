import websockets
import ghost_log


class WebsocketServer:
    '''Aysnc WebsocketServer
    '''

    def __init__(self, loop, ws_manager):
        self.loop = loop
        self.ws_manager = ws_manager

    def start(self, host='localhost', port='8765'):
        start_server = websockets.serve(
            self.ws_manager.handler(), host, port)
        self.server = self.loop.run_until_complete(start_server)
        ghost_log.p('websockets server listen on {}:{}'.format(host, port))

    def close(self):
        self.server.close()
        ghost_log.p('websocket server requested to close')
        self.loop.run_until_complete(self.server.wait_closed())
        ghost_log.p('websocket server all closed')
