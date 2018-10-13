if has('python3')  == 0
    echom 'this plugin needs python3 compiled.'
    finish
endif

if exists('*ch_open') == 0
    echom 'this plugin needs channel support in vim. try using latest vim.'
    finish
endif

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

let g:ghost_text_verbose = 0

function! GhostTextUpdateText(name, text, selections)
    py3 vim_ghost_text.update_text(vim.eval("a:name"), vim.eval("a:text"), vim.eval("a:selections"))
endfunction

" local callback when text changed 
function! s:GhostTextChanged()
    py3 vim_ghost_text.text_changed_from_vim()
endfunction

autocmd TextChangedI,TextChanged * call s:GhostTextChanged()
autocmd VimLeavePre * py3 vim_ghost_text.stop_server()

command! -bar GhostTextStart :py3 vim_ghost_text.start_server()
command! -bar GhostTextStop :py3 vim_ghost_text.stop_server()
command! -bar GhostTextDebug0 :let g:ghost_text_verbose = 0
command! -bar GhostTextDebug1 :let g:ghost_text_verbose = 1
command! -bar GhostTextDebug2 :let g:ghost_text_verbose = 2
