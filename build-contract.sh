#!/bin/bash

solc contract/trustery.sol --abi | tail -2 | python -m json.tool > pytrustery/trustery/trustery_abi.json
