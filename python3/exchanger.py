import weakref
import ghost_log


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


class Exchanger:
    _command_template = '["call", "GhostTextUpdateText", ["{}","{}",{}]]'

    def __init__(self):
        '''both channel and ws has send() message to send string to remote
        '''
    @property
    def channel(self):
        return self.channel_wr

    @channel.setter
    def channel(self, c):
        self.channel_wr = weakref.ref(c)

    @property
    def ws_manager(self):
        return self.ws_manager_wr

    @ws_manager.setter
    def ws_manager(self, wm):
        self.ws_manager_wr = weakref.ref(wm)

    def channel_rx_coro(self):
        async def coro(json_from_vim):
            buf_name = json_from_vim['buf_name']
            msg = json_from_vim['text']
            ws_man = self.ws_manager_wr()
            if not ws_man:
                ghost_log.p(
                    'warning: no connection to browswer, ignore msg from vim')
                return

            ghost_log.p('vim -> browser, {}'.format(json_from_vim))
            await ws_man.send(buf_name, msg, None)
        return coro

    def websocket_rx_coro(self):
        async def coro(buf_name, msg_from_browser):
            ''' msg_from_browser is the json from browser
            '''
            ghost_log.p('vim <- browser, {}'.format(msg_from_browser))
            text = msg_from_browser['text']
            try:
                cursor_pos = msg_from_browser['selections'][0]['end']
                pos = _cursor_pos(text, cursor_pos)
            except:
                pos = (1, 1)
            chnl = self.channel_wr()
            if not chnl:
                ghost_log.p(
                    'error: no connection to vim, ignore msg from browser')
                return
            # using the name to update text in vim
            await chnl.send(self._command_template.format(
                buf_name, text, list(pos)))

        return coro
