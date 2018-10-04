import vim


class VimBufferChannelMan:
    def __init__(channel_man, channel):
        channel_man.chanenl = channel

    class VimBuffer:
        def __init__(self, name):
            self._name = name

        @property
        def name(self):
            return self._name

        async def create(self):
            print("create a buffer with name", self._name)
            vim.command(":new {}".format(self._name))
            vim.command(":set buftype=nofile")
            vim.command(":set bufhidden=hide")
            vim.command(":set noswapfile")
            return True

        async def make_current(self):
            vim.command(":b {}".format(self._name))
            return True

        async def update(self, lines, selections):
            '''update the buffer with lines

            `lines` is usually from remote/browser side, is a list of line
            `selections` :refer to :help cursor
               [{lnum}, {col}, {off}, {curswant}]
            '''
            vim.current.buffer[:] = lines
            vim.command(":redraw")
            vim.command(":call cursor({})".format(selections))
            return True
