import vim


def start_server():
    '''todo:
    check if the server is alreayd running
    start the http and websocket server in separate thread so
    it is not blocking here
    '''
    print("server started")


def stop_server():
    '''todo:
    check if the server is running
    stopping the server and stop the server thread
    '''
    print("server stoped")


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
