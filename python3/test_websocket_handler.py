import json


class GhostTextWebsocketConnectionHandler:
    def __init__(self):
        pass

    async def __call__(self, message):
        msg = json.loads(message)
        print("In connection ", msg)


class GhostTextWebsocketHandler:
    '''callable class to handle websocket message
    '''

    def __init__(self, *args, **kwargs):
        pass

    async def __call__(self, message):
        msg = json.loads(message)
        print("create a connection with ", msg)
        return GhostTextWebsocketConnectionHandler()
