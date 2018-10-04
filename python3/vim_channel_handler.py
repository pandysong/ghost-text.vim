import json


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
            print('error: vim channel not connected')

    def handler(self):
        async def channel_handler(reader, writer):
            print('vim channel connected')
            if not self.writer == None:
                print('error, only one vim channel connection allowed')
                return

            self.writer = writer
            while True:
                # todo: to allow abitry length of jason
                data = await reader.read(4096)
                if not data:
                    break
                print(data.decode())
                try:
                    json_data = json.loads(data.decode())
                except ValueError:
                    print("json decoding failed")
                    continue

                # todo: send to remote via websocket
                await self.channel_rx_coro(json_data)

            print('vim channel closed')
            writer.close()
            self.writer = None

        return channel_handler
