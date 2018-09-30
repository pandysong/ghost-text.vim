import server_thread
import test_websocket_handler

st = None


def start_server(websocket_handler):
    '''todo:
    check if the server is alreayd running
    start the http and websocket server in separate thread so
    it is not blocking here
    '''
    global st
    if st != None:
        print("server already started")
        return

    st = server_thread.ServerThread(
        websocket_handler)
    st.start()
    print("server started")


def stop_server():
    '''todo:
    check if the server is running
    stopping the server and stop the server thread
    '''
    global st
    if st == None:
        print("server not started yet")
        return

    st.stop()
    print("server stoped")
    st = None
