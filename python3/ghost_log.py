import vim


def p(*args):
    _p(1, *args)


def p2(*args):
    _p(2, *args)


def _p(level, *args):
    e = vim.eval('exists("g:ghost_text_verbose")')
    if e == 0:
        return

    v = vim.eval('g:ghost_text_verbose')
    if int(v) >= level:
        print(*args)
