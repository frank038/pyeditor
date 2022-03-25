#!/bin/bash

thisdir=$(dirname "$0")
cd $thisdir

if [[ $# -eq 0 ]]; then
    ./pyeditor.py
elif [[ $# -eq 1 ]]; then
    ./pyeditor.py $1
elif [[ $# -eq 2 ]]; then
    ./pyeditor.py $1 $2
fi

cd $HOME
