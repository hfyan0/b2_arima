#!/bin/bash

if [[ ! -f common.sh ]]
then
    echo "cannot find common.sh"
    exit
fi
source common.sh

python $B2_ARIMA_CLIENT $CONFIG_LIVE
