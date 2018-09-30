import vim_buffer
import vim_buffers
import json


def _buf_name_from_title_name(title):
    return "GhostText_{}".format(title.replace(' ', '+'))


class GhostTextWebsocketConnectionHandler:
    def __init__(self, buf):
        self.buf = buf
        pass

    async def __call__(self, message):
        print("In connection ", message)
        msg = json.loads(message)
        self.buf.update(msg['text'].split('\n'))


class GhostTextWebsocketHandler:
    '''callable class to handle websocket message
    '''

    def __init__(self):
        self.vb = vim_buffers.VimBuffers(vim_buffer.VimBuffer)

    async def __call__(self, message):
        msg = json.loads(message)
        print("create a connection with ", msg)
        buf_name = _buf_name_from_title_name(msg['title'])
        buf = self.vb.buffer_with_name(buf_name)
        return GhostTextWebsocketConnectionHandler(buf)
