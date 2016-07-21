#!/bin/bash

if [ "$1" == "--alt" ]
then
    solc contract/trustery-alt.sol --abi | tail -2 | python -m json.tool > pytrustery/trustery/trustery_abi.json
elif [ "$1" == "--blindsigs-alt" ]
then
    solc contract/trustery-blindsigs-alt.sol --abi | tail -2 | python -m json.tool > pytrustery/trustery/trustery_abi.json
else
    solc contract/trustery.sol --abi | tail -2 | python -m json.tool > pytrustery/trustery/trustery_abi.json
fi
