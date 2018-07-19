#!/bin/bash

alias rebase='rebasefunc'
alias gpush='git push -u origin master'
alias gclone='git clone https://github.com/AdirO11/SufashAndAdir.git'
alias gdiff='git diff HEAD~1'
alias gdifftool='git difftool HEAD~1'

function rebasefunc() {
     git config --local include.path ../.gitconfig 2>/dev/null
     branch="master"
     if [ -z $branch ] ; then
         branch=`git branch | \grep -a "\*" | awk '{ print $2 }'`
     fi
     echo "rebasing branch $branch"
     find . -name "CMake*" | \grep -av Lists | xargs rm -rf
     git fetch origin && git fetch origin --tags && git fetch origin $branch &&
     git rebase --merge FETCH_HEAD
     git submodule update --init --recursive
     return $?
}

