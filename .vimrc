" Use UTF-8 encoding
set encoding=utf8

" Stop being compatible with Vi
set nocompatible

" Enable syntax highlighting
syntax on

" Enable line numbers plus relative numbers
set number relativenumber

" Set tabs as 4 spaces
set tabstop=4
set shiftwidth=4
set expandtab
set smarttab

" Show trailing tabs and spaces
set list listchars=tab:»·,trail:·
set list

" Enable spellcheck
set spell

" Highlight search results
:set hlsearch

" Finding files:
" Add all subdirectories to path, allowing for searching through them
set path+=**
" Display all matching files when we tab complete
set wildmenu

" Short keys:
" Enable highlight line
:hi CursorLine   cterm=NONE ctermbg=darkred ctermfg=white guibg=darkred guifg=white
:nnoremap <Leader>c :set cursorline! cursorcolumn!<CR>

" GUI:
" Set evening color scheme on windows
if has('win64')
    colorscheme evening
endif
" Set readable fonts for every OS
if has("gui_gtk2")
    set guifont=Inconsolata\ 12
elseif has("gui_macvim")
    set guifont=Menlo\ Regular:h14
elseif has("gui_win32")
    set guifont=Consolas:h11:cANSI
endif
