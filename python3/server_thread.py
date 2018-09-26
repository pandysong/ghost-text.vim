import asyncio
import threading
import websocket_server
import tcp_server
import http_handler
import websocket_handler


class ServerThread:
    def __init__(self):
        pass

    def _threaded_function(self):
        self.stop_request_event = threading.Event()
        self.stop_response_event = threading.Event()

        async def wait_for_stop(loop):
            await loop.run_in_executor(
                None,
                self.stop_request_event.wait)

        def thread_function():
            #loop = asyncio.get_event_loop()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            hh = http_handler.GhostTextHttpHandler(8765)
            self.tcp_svr = tcp_server.TcpServer(loop, hh)
            self.tcp_svr.start()

            sh = websocket_handler.GhostTextWebsocketHandler()
            self.ws_svr = websocket_server.WebsocketServer(loop, sh)
            self.ws_svr.start()
            task = loop.create_task(wait_for_stop(loop))
            loop.run_until_complete(task)
            loop.close()
            self.stop_response_event.set()

        return thread_function

    def start(self):
        self.thread = threading.Thread(target=self._threaded_function())
        self.thread.start()

    def stop(self):
        self.stop_request_event.set()
        self.stop_response_event.wait()
