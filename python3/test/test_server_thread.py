import time
from single_server import start_server
from single_server import stop_server
import test_websocket_handler


def print_usage():
    print("s: start")
    print("t: stop")
    print("q: quit")


while True:
    print_usage()
    i = input()
    if i == 's':
        start_server(
            test_websocket_handler.GhostTextWebsocketHandler)
    elif i == 't':
        stop_server()
    elif i == 'q':
        stop_server()
        break
