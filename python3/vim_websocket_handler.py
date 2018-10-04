import websockets
import json
import ghost_log


def _buf_name_from_title_name(title):
    return "GhostText_{}".format(title.replace(' ', '+'))


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
            while True:
                try:
                    msg = await websocket.recv()
                    json_msg = json.loads(msg)  # todo: add exception handling

                    # map to buffer name
                    # todo: we may map websocket to buffer name
                    buf_name = _buf_name_from_title_name(json_msg['title'])
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
