alias vi=vim
set -o vi

if [[ $(uname) =~ MINGW*|CYGWIN*|MSYS* ]]; then
    alias python='winpty python.exe';
fi

source /usr/share/bash-completion/completions/git
