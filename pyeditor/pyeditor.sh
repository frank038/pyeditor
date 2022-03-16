#!/bin/bash

thisdir=$(dirname "$0")
cd $thisdir

if [[ $# -eq 0 ]]; then
    ./pyeditor.py
else
    ./pyeditor.py $1
fi

cd $HOME
