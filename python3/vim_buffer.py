import vim


class VimBuffer:
    def __init__(self, name):
        vim.command(":new {}".format(name))
        vim.command(":set buftype=nofile")
        vim.command(":set bufhidden=hide")
        vim.command(":set noswapfile")
        self._name = name

    @property
    def name(self):
        return self._name

    def make_current(self):
        vim.command(":b {}".format(self._name))
        return self

    def update(self, lines):
        '''update the buffer with lines

        `lines` is usually from remote/browser side, is a list of line
        '''
        vim.current.buffer[:] = lines
        vim.command(":redraw")

    def cursor(self, selection):
        '''refer to :help cursor
           [{lnum}, {col}, {off}, {curswant}]
        '''
        vim.command(":call cursor({})".format(selection))
