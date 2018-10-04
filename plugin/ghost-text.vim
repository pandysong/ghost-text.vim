let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

py3 << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python3'))
sys.path.insert(0, python_root_dir)
import vim_ghost_text
EOF

" manage server
function! GhostTextStartServer()
    py3 vim_ghost_text.start_server()
    let c = 1
    while c <=3 
        sleep 100m
        let g:channel = ch_open('localhost:4002')
        if ch_status(g:channel) == "open"
            echom 'channel connected to localhost:4002'
            break
        endif

        echom 'could not open channel to localhost:4002, retry...'
        let c += 1

    endwhile
endfunction

function! GhostTextStopServer()
    if ch_status(g:channel) == "open"
        call ch_close(g:channel)
    endif
    py3 vim_ghost_text.stop_server()
endfunction

" Below functions called by remote via channel
function! s:GhostTextCreateBuffer(name)
    if buffer_exists(a:name)
        exec 'buf '.a:name
    else
        exec 'enew'
        exec 'file '.a:name
    endif
    set buftype=nofile
    set bufhidden=hide
    set noswapfile
endfunction

function! GhostTextUpdateText(name, text, selections)
    call s:GhostTextCreateBuffer(a:name)
    py3 vim_ghost_text.update_text(vim.eval("a:name"), vim.eval("a:text"), vim.eval("a:selections"))
endfunction

" local callback when text changed 
function! s:GhostTextChanged()
    py3 vim_ghost_text.text_changed_from_vim()
endfunction

autocmd TextChangedI,TextChanged * call s:GhostTextChanged()
autocmd VimLeavePre * call GhostTextStopServer()

command! -bar GhostTextStartServer :call GhostTextStartServer()
command! -bar GhostTextStopServer :call GhostTextStopServer()
