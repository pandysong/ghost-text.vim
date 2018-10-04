import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_path = os.path.abspath(os.path.join(dir_path, '..'))
sys.path.insert(0, parent_path)
print(sys.path)

import asyncio
import tcp_server
import vim_channel_handler
from aioconsole import ainput


async def rx_coro(json_data):
    print(json_data)


channel = None


commands = {'1': '["call", "GhostTextUpdateText", ["hello","line1\\nline2\\nline3",[1,2]]]',
            '2': '["call", "GhostTextUpdateText", ["world","wline1\\nwline2\\nwline3",[2,4]]]'}


async def console_coro():
    while True:
        line = await ainput(">>> ")
        if line == 'q' or line == 'quit' or line == 'exit':
            break
        if channel == None:
            print('channel not connected, ignore the input')
            continue
        line = commands.get(line, line)
        await channel.send(line)


print('test_channel_server')
loop = asyncio.get_event_loop()
channel = vim_channel_handler.Channel(rx_coro)
s = tcp_server.TcpServer(loop, channel)
s.start()

print('input json message sent to vim')
print('try input following command :')
for i, c in commands.items():
    print('press "{}" for: {}'.format(i, c))

loop.run_until_complete(console_coro())

s.close()
loop.close()
