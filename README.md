# ghost-text.vim
support for ghost-text in regular vim

# design

- server start
- on a new websocket, create a new buffer
- receives the current text from browser
- on local updates, send the text to browser
- on disconnection, leave the buffer open (just in case if the browser)

## tcp server

TCP server handler is designed to have a simple http handler for handle simple
http request as well as the channel request from Vim which is a bi-drectional
communication

| ----------------------- | ------------------------------------- |
| http server components  | Comments                              |
|-------------------------+---------------------------------------|
| http_handler            | return in json websocket port         |
| tcp_server              |                                       |
| ----------------------- | ------------------------------------- |

| -----------------------      | -------------------------------------------------------------      |
| websockets server components | Comments                                                           |
|------------------------------+--------------------------------------------------------------------|
| vim_buffer                   | manage a single vim buffer, it does it through vim_channel_handler |
| vim_buffers                  | manage the vim buffer through vim_buffer                           |
| vim_websocket_handler        | handle message from browser                                        |
| websocket_server             |                                                                    |
| -----------------------      | ------------------------------------------------------------       |


| -----------------------     | -----------------------------------------  |
| channel server components   | Comments                                   |
| --------------------------- | --------------------                       |
| vim_channel_handler         | handle connection to vim via vim `channel` |
| tcp_server                  |                                            |
| -----------------------     | ----------------------------------------   |

Note that there is only one connection from vim to channel server (todo: we may
protect it by a ramdon password)

So we could create `vim_channel_handler.ChannelHandler` before a connection was
created and pass it to construct `vim_buffer`

Vim   <---->  Channel Server <---> WebSocket Server  <--->  Browser
                                          |---> Browser 

The multiple websockets connections are multiplexed by unique vim buffer names.
