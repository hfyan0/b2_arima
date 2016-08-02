#!/bin/bash

if [[ ! -f common.sh ]]
then
    echo "cannot find common.sh"
    exit
fi
source common.sh

source $POPULATE_SYM_SCT

date
cd $SYMBOLS_FOLDER
ls | time parallel -j+0 --progress --eta python $GEN_HIST_SGNL_WITH_RPY $CONFIG_HIST
date

