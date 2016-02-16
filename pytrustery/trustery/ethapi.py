import json
import os

import jsonrpc_requests
import rlp

import trustery

TRUSTERY_DEFAULT_ADDRESS = '0xd7f4a7b264ff1e5d25d12566c60ec726872a8a09'
TRUSTERY_ABI = json.load(open(os.path.join(os.path.dirname(trustery.__file__), 'trustery_abi.json')))

ethrpc = jsonrpc_requests.Server('http://127.0.0.1:8545')


def encode_api_data(data):
    if data is None:
        return None
    elif type(data) == str and data.startswith('0x'):
        return data
    elif type(data) in [bool, int]:
        return hex(data)
    else:
        return '0x' + rlp.utils.encode_hex(data)
