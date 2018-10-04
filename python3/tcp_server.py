import asyncio
import ghost_log


class TcpServer:
    '''Async TcpServer
    '''

    def __init__(self, loop, handler_factory):
        '''  Create a TcpServer with an event loop and message handler
        handler is a async function which get data and return result
        '''
        self.loop = loop
        self.handler_factory = handler_factory

    def start(self, host='localhost', port='4001'):
        coro = asyncio.start_server(
            self.handler_factory.handler(), host, port, loop=self.loop)
        self.server = self.loop.run_until_complete(coro)
        ghost_log.p('server listen on {}:{}'.format(host, port))

    def close(self):
        self.server.close()
        ghost_log.p('tcp server requested to close')
        self.loop.run_until_complete(self.server.wait_closed())
        ghost_log.p('tcp server all closed')
