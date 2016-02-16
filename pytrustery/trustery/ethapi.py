import json
import os

import eth_rpc_client
from rlp.utils import encode_hex

import trustery

TRUSTERY_DEFAULT_ADDRESS = '0xd7f4a7b264ff1e5d25d12566c60ec726872a8a09'
TRUSTERY_ABI = json.load(open(os.path.join(os.path.dirname(trustery.__file__), 'trustery_abi.json')))

ethclient = eth_rpc_client.Client(host='127.0.0.1', port='8545')


def encode_api_data(data):
    if data is None:
        return None
    elif type(data) == str and data.startswith('0x'):
        return data
    elif type(data) in [bool, int]:
        return hex(data)
    else:
        return '0x' + encode_hex(data)
