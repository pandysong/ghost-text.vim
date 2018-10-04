import os
import vim
import time
import json
import ghost_log

from single_server import start_server
from single_server import stop_server
import vim_websocket_handler


def text_changed_from_vim():
    name = os.path.basename(vim.current.buffer.name)
    if not name.startswith("GhostText"):
        return

    ghost_log.p("{} lines".format(len(vim.current.buffer)))
    text = '\n'.join(vim.current.buffer)
    # vim.command()
    selections = [{'start': 1, 'end': 1}]
    json_dict = json.dumps(
        {
            'buf_name': name,
            'text': text,
            'selections': selections
        }
    )
    cmd = ':call ch_sendraw(g:channel,{})'.format(
        json.dumps(json_dict))

    vim.command(cmd)


def update_text(name, lines, selections):
    # todo : if current buffer is not the `name`d buffer, switch it
    vim.command(':b ' + name)
    mode = vim.eval('mode()')
    if not mode == 'n':
        ghost_log.p('mode', mode)
        vim.command('call feedkeys("\<esc>")')
        vim.command(":redraw")

    vim.current.buffer[:] = lines.split('\n')
    vim.command(":redraw")
    vim.command(":call cursor({})".format(selections))
