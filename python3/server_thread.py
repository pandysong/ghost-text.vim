import time
import asyncio
import threading
import websocket_server
import tcp_server
import http_handler
import exchanger
import vim_channel_handler
import vim_websocket_handler


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
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            ex = exchanger.Exchanger()

            # start http server for browser
            hh = http_handler.GhostTextHttpHandlerFactory(8765)
            http_svr = tcp_server.TcpServer(loop, hh)
            http_svr.start()

            # start tcp server for vim channel to connect
            ch = vim_channel_handler.Channel(
                ex.channel_rx_coro())
            ch_svr = tcp_server.TcpServer(loop, ch)
            ch_svr.start(host='localhost', port='4002')

            # exchanger needs channel to send message
            ex.channel = ch

            # start websockets server
            ws_manager = vim_websocket_handler.Manager(
                ex.websocket_rx_coro())
            ws_svr = websocket_server.WebsocketServer(loop,
                                                      ws_manager)
            ws_svr.start()

            # exchanger needs ws_manager to send message
            ex.ws_manager = ws_manager

            # run until the stop request event will be set
            loop.run_until_complete(wait_for_stop(loop))

            # teardown
            ws_svr.close()
            ch_svr.close()
            http_svr.close()
            loop.close()
            self.stop_response_event.set()

        return thread_function

    def start(self):
        self.thread = threading.Thread(target=self._threaded_function())
        self.thread.start()

    def stop(self):
        self.stop_request_event.set()
        self.stop_response_event.wait()
