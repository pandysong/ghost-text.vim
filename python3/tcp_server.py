import asyncio
import logging


class TcpServer:
    '''Async TcpServer
    '''

    def __init__(self, loop, handler):
        '''  Create a TcpServer with an event loop and message handler
        handler is a async function which get data and return result
        '''
        self.loop = loop
        self.handler = handler

    def _handler(self):
        async def handle_tcp(reader, writer):
            while True:
                data = await reader.read(1024)
                if not data:
                    break
                message = data.decode()
                message, close = await self.handler(message)
                writer.write(message.encode())
                await writer.drain()

                if close:
                    break

            await asyncio.sleep(0.2)
            writer.close()
        return handle_tcp

    def start(self, host='localhost', port='4001'):
        coro = asyncio.start_server(self._handler(), host, port, loop=self.loop)
        print('server listen on {}:{}'.format(host, port))
        self.server = self.loop.run_until_complete(coro)
        print('server listen on {}:{}'.format(host, port))

    def close(self):
        self.server.close()
        self.loop.run_until_complete(self.server.wait_closed())