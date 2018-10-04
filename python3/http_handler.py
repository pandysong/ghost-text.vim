class GhostTextHttpHandlerFactory:
    '''callable class to handle http request
    '''

    def __init__(self, websocket_port):
        self.websocket_port = websocket_port

    def handler(self):
        '''this create a connection handler
        '''
        async def http_handler(reader, writer):
            data = await reader.read(1024)
            if data:
                lines = [
                    'HTTP/1.1 200 Ok',
                    'Connection: close',
                    'Content-Type: application/json',
                    '',
                    '{',
                    '    "ProtocolVersion": 1,',
                    '    "WebSocketPort": ' + str(self.websocket_port),
                    '}']
                response = '\r\n'.join(lines) + '\r\n'
                writer.write(response.encode())
                await writer.drain()
            writer.close()
        return http_handler
