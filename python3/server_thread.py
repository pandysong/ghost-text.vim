import time
import asyncio
import threading
import websocket_server
import tcp_server
import http_handler


class ServerThread:
    def __init__(self, web_socket_handler):
        self.web_socket_handler = web_socket_handler

    def _threaded_function(self):
        self.stop_request_event = threading.Event()
        self.stop_response_event = threading.Event()

        async def wait_for_stop(loop):
            await loop.run_in_executor(
                None,
                self.stop_request_event.wait)

        def thread_function():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            hh = http_handler.GhostTextHttpHandlerFactory(8765)
            tcp_svr = tcp_server.TcpServer(loop, hh)
            tcp_svr.start()

            sh = self.web_socket_handler()
            ws_svr = websocket_server.WebsocketServer(loop, sh)
            ws_svr.start()
            loop.run_until_complete(wait_for_stop(loop))

            ws_svr.close()
            tcp_svr.close()
            loop.close()
            self.stop_response_event.set()

        return thread_function

    def start(self):
        self.thread = threading.Thread(target=self._threaded_function())
        self.thread.start()

    def stop(self):
        self.stop_request_event.set()
        self.stop_response_event.wait()
