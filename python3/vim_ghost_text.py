import vim

from single_server import start_server as _start_server
from single_server import stop_server
import vim_websocket_handler


def start_server():
    _start_server(vim_websocket_handler.GhostTextWebsocketHandler)


def text_changed_from_vim():
    '''
    send the lines to  server thread to asynchronizely
    communicate to browser plugin
    or we could just wakeup unblock server thread so server thread could access buffer directly?
    this may cause unsync issue? The first method looks safe and robust. anyway, we could not expect
    huge buffer size.
    '''
    print("{} lines".format(len(vim.current.buffer)))

# when the server started
# and remote try to connect, we will need to create a new buffer
# set the buffertype to nofile?
#
