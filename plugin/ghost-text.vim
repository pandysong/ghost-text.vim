let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

py3 << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python3'))
sys.path.insert(0, python_root_dir)
import ghost_text
EOF

function! GhostTextStartServer()
    py3 ghost_text.start_server()
endfunction

function! GhostTextStopServer()
    py3 ghost_text.stop_server()
endfunction

function! s:GhostTextChanged()
    py3 ghost_text.text_changed_from_vim()
endfunction

autocmd TextChangedI,TextChanged * call s:GhostTextChanged()

command! -bar GhostTextStartServer :call GhostTextStartServer()
command! -bar GhostTextStopServer :call GhostTextStopServer()
