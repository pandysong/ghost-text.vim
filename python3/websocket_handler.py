class GhostTextWebsocketConnectionHandler:
    async def __call__(self, message):
        print("In connection ", message)


class GhostTextWebsocketHandler:
    '''callable class to handle websocket message
    '''

    def __init__(self):
        pass

    async def __call__(self, message):
        print("create a connection with ", message)
        return GhostTextWebsocketConnectionHandler()
