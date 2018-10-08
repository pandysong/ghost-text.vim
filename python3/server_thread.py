import time
import asyncio
import threading
import websocket_server
import tcp_server
import http_handler
import exchanger
import vim_channel_handler
import vim_websocket_handler


class ServerStartException (RuntimeError):
    pass


class ServerThread:
    def __init__(self):
        self.running = None
        self.start_event = threading.Event()

    def _threaded_function(self):
        self.stop_request_event = threading.Event()

        async def wait_for_stop(loop):
            await loop.run_in_executor(
                None,
                self.stop_request_event.wait)

        def thread_function():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            ex = exchanger.Exchanger()

            try:
                # start http server for browser
                hh = http_handler.GhostTextHttpHandlerFactory(8765)
                http_svr = tcp_server.TcpServer(loop, hh)
                try:
                    http_svr.start()
                except:
                    print('fail to start tcp svr on localhost:4001')
                    http_svr = None
                    raise ServerStartException

                # start tcp server for vim channel to connect
                ch = vim_channel_handler.Channel(
                    ex.channel_rx_coro())
                ch_svr = tcp_server.TcpServer(loop, ch)
                try:
                    ch_svr.start(host='localhost', port='4002')
                except:
                    print('fail to start channel svr on localhost:4002')
                    ch_svr = None
                    raise ServerStartException

                # exchanger needs channel to send message
                ex.channel = ch

                # start websockets server
                ws_manager = vim_websocket_handler.Manager(
                    ex.websocket_rx_coro())
                ws_svr = websocket_server.WebsocketServer(loop,
                                                          ws_manager)

                try:
                    ws_svr.start()
                except:
                    print('fail to start channel svr on localhost:4002')
                    ws_svr = None
                    raise ServerStartException

                # exchanger needs ws_manager to send message
                ex.ws_manager = ws_manager
            except ServerStartException:
                self.running = False
                self.start_event.set()
            else:
                # run until the stop request event will be set
                self.running = True
                self.start_event.set()
                loop.run_until_complete(wait_for_stop(loop))

            # teardown
            try:
                ws_svr.close()
                ch_svr.close()
                http_svr.close()
                loop.close()
            except:
                pass

        return thread_function

    def start(self):
        self.thread = threading.Thread(target=self._threaded_function())
        self.thread.start()
        self.start_event.wait()
        return self.running

    def stop(self):
        if self.running == True:
            self.stop_request_event.set()
            self.thread.join()
