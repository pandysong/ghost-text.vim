class GhostTextHttpHandler:
    '''callable class to handle http request
    '''

    def __init__(self, websocket_port):
        self.websocket_port = websocket_port

    async def __call__(self, message):
        lines = [
            'HTTP/1.1 200 Ok',
            'Connection: close',
            'Content-Type: application/json',
            '',
            '{',
            '    "ProtocolVersion": 1,',
            '    "WebSocketPort": ' + str(self.websocket_port),
            '}']
        # True indicates the caller to close the connection
        print('request {}'.format(message))
        return '\r\n'.join(lines) + '\r\n', True
