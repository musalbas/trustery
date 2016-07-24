"""Interface for Ethereum client and Trustery contract."""

import json
import os

import eth_rpc_client
from rlp.utils import encode_hex

import trustery

# Trustery contract constants.
TRUSTERY_DEFAULT_ADDRESS = '0x61fdbb4a08e5b30a63ff3990e054eee99fad04e4'
TRUSTERY_ABI = json.load(open(os.path.join(os.path.dirname(trustery.__file__), 'trustery_abi.json')))

# Ethereum client interface.
ethclient = eth_rpc_client.Client(host='127.0.0.1', port='8545')


def encode_api_data(data, padding=None):
    """
    Prepare arbitrary data to be send to the Ethereum client via the API.

    data: the data.
    padding: padding length in bytes (default: no padding).

    Returns the encoded data.
    """
    if data is None:
        return None
    elif type(data) == str and data.startswith('0x'):
        if padding:
            data = data.ljust(padding*2+2, '0')
        # Return data if it is already hex-encoded.
        return data
    elif type(data) in [bool, int]:
        # Use native hex() to encode non-string data has encode_hex() does not support it.
        if padding and type(data) == int:
            return '0x' + hex(data)[2:].rjust(padding*2, '0')
        return hex(data)
    elif type(data) == long:
        # Use native hex() to encode long.
        encoded = hex(data)
        if encoded[-1:] == 'L':
            # Remove the trailing 'L' if found.
            encoded = encoded[:-1]
        if padding:
            encoded = '0x' + encoded[2:].rjust(padding*2, '0')
        return encoded
    else:
        # Encode data using encode_hex(), the recommended way to encode Ethereum data.
        if padding:
            data = data.ljust(padding, '0')
        return '0x' + encode_hex(data)
