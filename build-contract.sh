#!/bin/bash

solc contract/trustery.sol --abi | tail -2 > pytrustery/trustery/trustery_abi.json
