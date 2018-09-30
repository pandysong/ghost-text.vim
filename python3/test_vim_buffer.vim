let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

py3 << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python3'))
sys.path.insert(0, python_root_dir)
import vim_buffer
import vim_buffers
vb = vim_buffers.VimBuffers(vim_buffer.VimBuffer)
current = None
EOF

function! GhostTextVimBuffer(name)
    py3 current = vb.buffer_with_name(vim.eval("a:name")).make_current()
endfunction

function! GhostTextUpdateText(text)
    py3 current.update(vim.eval("a:text"))
endfunction

command! -nargs=1 GhostTextVimBuffer call GhostTextVimBuffer(<f-args>)
command! GhostTextUpdateText call GhostTextUpdateText(['line 1', 'line 2', 'line 3'])
