set encoding=utf8

set number relativenumber

set tabstop=4
set shiftwidth=4
set expandtab 
set smarttab 

set list listchars=tab:»·,trail:·
set list

syntax on
colorscheme evening

:set hlsearch

:hi CursorLine   cterm=NONE ctermbg=darkred ctermfg=white guibg=darkred guifg=white
:nnoremap <Leader>c :set cursorline! cursorcolumn!<CR>

if has("gui_gtk2")
    set guifont=Inconsolata\ 12
elseif has("gui_macvim")
    set guifont=Menlo\ Regular:h14
elseif has("gui_win32")
    set guifont=Consolas:h11:cANSI
endif
