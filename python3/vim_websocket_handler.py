import vim_buffer
import vim_buffers
import json


def _buf_name_from_title_name(title):
    return "GhostText_{}".format(title.replace(' ', '+'))


def _cursor_pos(text, offset):
    t = text[0:offset]
    n_linebreak = t.count('\n')
    row = n_linebreak + 1
    offset_lastbreak = t.rfind('\n')
    if offset_lastbreak == -1:
        col = len(t)
    else:
        col = offset - offset_lastbreak
    return row, col


class GhostTextWebsocketConnectionHandler:
    def __init__(self, buf):
        self.buf = buf
        pass

    async def __call__(self, message):
        print("In connection ", message)
        msg = json.loads(message)
        text = msg['text']
        self.buf.update(text.split('\n'))

        # todo: make use of a list of selections
        cursor_pos = msg['selections'][0]['end']
        pos = _cursor_pos(text, cursor_pos)
        self.buf.cursor(list(pos))


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
