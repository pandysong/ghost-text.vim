import server_thread
import ghost_log

st = None
channel = None


def start_server():
    '''todo:
    check if the server is alreayd running
    start the http and websocket server in separate thread so
    it is not blocking here
    '''
    global st
    if st != None:
        ghost_log.p("server already started")
        return True

    st = server_thread.ServerThread()
    ret = st.start()
    if not ret:
        st = None
    return ret


def stop_server():
    '''todo:
    check if the server is running
    stopping the server and stop the server thread
    '''
    global st
    if st == None:
        ghost_log.p("server not started yet")
        return

    st.stop()
    ghost_log.p("server stoped")
    st = None
