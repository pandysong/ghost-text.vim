class Vim:
    def __init__(self):
        pass

    def create_buf(core, name):
        core.send_to_vim('["call","GhostTextCreateBuffer({})"]'.format(name))
        # todo: check if command is executed successfully

    def update(core, name, text, selections):
        core.send_to_vim('["call", GhostTextUpdateText, [{}, {}, {}]]'.format(
            name, text, selection))


class Core:
    '''the core top level business logic to integrate the channel server and
    websocket server
    '''

    def __init__(self):
        self.writer_to_vim = None
        self.name2ws = {}
        self.vim = Vim()

    def channle_handler(self):
        async def channel_handler(reader, writer):
            print('vim channel connected')
            self.writer = writer
            while True:
                # todo: to allow abitry length of jason
                data = await reader.read(4096)
                if not data:
                    break

                try:
                    decoded = json.loads(message)
                except ValueError:
                    print("json decoding failed")

                # todo: send to remote via websocket
                self.send_to_browser(buf_name, message)

            writer.close()

        return channel_handler

    def send_to_browser(self, buf_name, message):
        ''' find the corresponding websocket and send
        '''
        ws = self.name2ws[buf_name]
        ws.send(message)

    def send_to_vim(self, message):
        self.writer_to_vim.write(message)
        self.writer_to_vim.drain()

    def websocket_handler(self):
        async def ws_handler(websocket, path):
            flag_first_message = True
            buf_name = None
            while True:
                try:
                    msg = await websocket.recv()
                    json_msg = json.loads(msg)  # todo: add exception handling

                    # map to buffer name
                    # todo: we may map websocket to buffer name
                    buf_name = _buf_name_from_title_name(json_msg['title'])
                    if flag_first_message:
                        # on first message, create a map
                        self.name2ws[buf_name] = websocket
                        await self.vim.create_buf(self, buf_name)
                        flag_first_message = False

                    text = msg['text']
                    # todo: make use of a list of selections
                    cursor_pos = msg['selections'][0]['end']
                    pos = _cursor_pos(text, cursor_pos)

                    await self.vim.update(self, buf_name, text.split('\n'), list(pos))

                except websockets.exceptions.ConnectionClosed:
                    break
            print("connection closed")
            del self.name2ws[buf_name]
        return ws_handler
