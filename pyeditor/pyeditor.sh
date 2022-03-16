#!/bin/bash

thisdir=$(dirname "$0")
cd $thisdir
./pyeditor.py &
cd $HOME
