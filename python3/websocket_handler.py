class GhostTextWebsocketHandler:
    '''callable class to handle websocket message
    '''

    def __init__(self):
        pass

    async def __call__(self, message):
        print(message)
