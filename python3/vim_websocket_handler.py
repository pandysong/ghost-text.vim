import websockets
import json
import ghost_log


_buf_idx = 0


class Manager:
    '''manage websocket connections
    '''

    def __init__(self, rx_coro):
        self.rx_coro = rx_coro
        self.connections = {}

    async def send(self, buf_name, text, selection):
        ''' find the corresponding websocket and send
        '''
        for ws, info in self.connections.items():
            if info['name'] == buf_name:
                resp = info['template']
                resp['text'] = text
                ghost_log.p('vim -> browser, {}'.format(json.dumps(resp)))
                await ws.send(json.dumps(resp))

    def handler(self):
        async def ws_handler(websocket, path):
            flag_first_message = True
            global _buf_idx
            buf_name = 'GhostText_{}'.format(_buf_idx)
            _buf_idx = _buf_idx + 1
            while True:
                try:
                    msg = await websocket.recv()
                    json_msg = json.loads(msg)  # todo: add exception handling

                    if flag_first_message:
                        # on first message, create a map
                        ghost_log.p('add map from {} to {}'.format(
                            websocket, buf_name))
                        self.connections[websocket] = {
                            'name': buf_name,
                            'template': json_msg
                        }
                        flag_first_message = False

                    await self.rx_coro(buf_name, json_msg)

                except websockets.exceptions.ConnectionClosed:
                    break
            del self.connections[websocket]
            ghost_log.p("connection closed")
        return ws_handler
