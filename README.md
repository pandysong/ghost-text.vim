# ghost-text.vim
support for ghost-text in regular vim

# design

- server start
- on a new websocket, create a new buffer
- receives the current text from browser
- on local updates, send the text to browser
- on disconnection, leave the buffer open (just in case if the browser)
