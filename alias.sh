#!/bin/bash

alias grebase='rebasefunc' #rebase: putting you commit on to of remote repo changes (always rebase before pushing.). 

alias gpush='git push -u origin master' #push your commit

alias gclone='git clone https://github.com/AdirO11/SufashAndAdir.git' #clone our project.

alias gdiff='git diff HEAD~1' #shows the diff in your commit compare to the prev commit on shell.

alias gdifftool='git difftool HEAD~'  #shows the diff in your commit, compare to the prev commit in vim files.

alias my_aliases='cat alias.sh | grep alias' #shows the aliases

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

