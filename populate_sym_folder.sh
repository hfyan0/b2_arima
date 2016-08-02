#!/bin/bash

if [[ ! -f common.sh ]]
then
    echo "cannot find common.sh"
    exit
fi
source common.sh

[[ ! -d $SYMBOLS_FOLDER ]] && mkdir -p $SYMBOLS_FOLDER

for sym in $SYMBOLS
do
    touch $SYMBOLS_FOLDER/$sym
done
