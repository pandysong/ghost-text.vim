import json
import ghost_log


class Channel:

    def __init__(self, channel_rx_coro):
        self.channel_rx_coro = channel_rx_coro
        self.seq_num = 1
        self.writer = None

    async def send(self, message):
        '''send a message to vim
        '''
        if self.writer:
            self.writer.write(message.encode())
            await self.writer.drain()
        else:
            ghost_log.p('error: vim channel not connected')

    def handler(self):
        async def channel_handler(reader, writer):
            ghost_log.p('vim channel connected')
            if not self.writer == None:
                ghost_log.p('error, only one vim channel connection allowed')
                return

            self.writer = writer
            while True:
                # todo: to allow abitry length of jason
                data = await reader.read(1024*1024)
                if not data:
                    break
                try:
                    json_data = json.loads(data.decode())
                except ValueError:
                    ghost_log.p("json decoding failed")
                    continue

                # todo: send to remote via websocket
                await self.channel_rx_coro(json_data)

            ghost_log.p('vim channel closed')
            writer.close()
            self.writer = None

        return channel_handler
