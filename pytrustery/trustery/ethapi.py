"""Interface for Ethereum client and Trustery contract."""

import json
import os

import eth_rpc_client
from rlp.utils import encode_hex

import trustery

# Trustery contract constants.
TRUSTERY_DEFAULT_ADDRESS = '0xd7f4a7b264ff1e5d25d12566c60ec726872a8a09'
TRUSTERY_ABI = json.load(open(os.path.join(os.path.dirname(trustery.__file__), 'trustery_abi.json')))

# Ethereum client interface.
ethclient = eth_rpc_client.Client(host='127.0.0.1', port='8545')


def encode_api_data(data):
    """
    Prepare arbitrary data to be send to the Ethereum client via the API.

    data: the data.
    """
    if data is None:
        return None
    elif type(data) == str and data.startswith('0x'):
        # Return data if it is already hex-encoded.
        return data
    elif type(data) in [bool, int]:
        # Use native hex() to encode non-string data has encode_hex() does not support it.
        return hex(data)
    elif type(data) == long:
        # Use native hex() to encode long and remove the trailing 'L'.
        return hex(data)[:-1]
    else:
        # Encode data using encode_hex(), the recommended way to encode Ethereum data.
        return '0x' + encode_hex(data)
