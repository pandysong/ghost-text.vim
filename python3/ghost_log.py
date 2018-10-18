import vim


log_file = None


def try_open_or_close_log_file():
    global log_file
    if (int(vim.eval('exists("g:ghost_text_log_file")')) == 1
            and not log_file):
        fn = vim.eval('g:ghost_text_log_file')
        try:
            log_file = open(fn, 'w+')
        except:
            pass

    elif (int(vim.eval('exists("g:ghost_text_log_file")')) != 1
            and log_file):
        try:
            log_file.close()
        finally:
            log_file = None


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
        try_open_or_close_log_file()
        global log_file
        if log_file:
            log_file.write((' {}'*len(args)+'\n').lstrip().format(*args))
            log_file.flush()
