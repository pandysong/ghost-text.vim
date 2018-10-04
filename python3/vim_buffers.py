class VimBuffers:
    def __init__(self, bufferCreator):
        '''VimBuffers manages a collection of buffers

        bufferCreator accepts name as parameter and return a new buffer. A
        buffer must have `name` property, which VimBuffers use to manage
        '''
        self.buffers = []
        self.creator = bufferCreator

    async def buffer_with_name(self, name):
        '''make the current buffer with `name`

        find the buffer with `name` or create a new one if not found
        '''
        x = [b for b in self.buffers if b.name == name]
        if x:
            return x[0]
        new_buf = self.creator(name)
        success = await new_buf.create()
        if success:
            self.buffers.append(new_buf)
            return new_buf
        else:
            print('error: could not create buffer with name', name)
            return None
