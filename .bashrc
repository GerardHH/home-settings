#!/usr/bin/env bash

# If not running interactively, don't do anything
case $- in
  *i*) ;;
    *) return;;
esac

alias vi=vim
set -o vi

if [[ $(uname) =~ MINGW*|CYGWIN*|MSYS* ]]; then
    alias python='winpty python.exe';
    return;
fi

export PATH="~/bin:$PATH";

# Path to the bash it configuration
export BASH_IT="/home/$(whoami)/.bash_it";

# Lock and Load a custom theme file.
# Leave empty to disable theming.
# location /.bash_it/themes/
export BASH_IT_THEME='bakke'

# Don't check mail when opening terminal.
unset MAILCHECK

# Change this to your console based IRC client of choice.
export IRC_CLIENT='irssi'

# Set this to the command you use for todo.txt-cli
export TODO="t"

# Set this to false to turn off version control status checking within the prompt for all themes
export SCM_CHECK=true

# Load Bash It
source "$BASH_IT"/bash_it.sh

# Load bash completion
source /usr/share/bash-completion/bash_completion

# Raven env
source ~/.profile

source ~/.nvm/nvm.sh
nvm use v4.5.0
