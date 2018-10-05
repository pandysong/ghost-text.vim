import vim


def p(*args):
    e = vim.eval('exists("g:ghost_text_verbose")')
    if e == 0:
        return

    v = vim.eval('g:ghost_text_verbose')
    if int(v) == 1:
        print(*args)
