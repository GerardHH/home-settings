set encoding=utf8

" Enable syntax highlighting
syntax on

set number relativenumber

set tabstop=4
set shiftwidth=4
set expandtab
set smarttab

set list listchars=tab:»·,trail:·
set list

if has('win64')
    colorscheme evening
endif

set spell

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
