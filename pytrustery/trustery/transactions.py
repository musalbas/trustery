from pyethereum import abi
import rlp

from ethapi import TRUSTERY_ABI
from ethapi import ethrpc


class Transactions(object):
    def __init__(self, from_address, to_address):
        self.from_address = from_address
        self.to_address = to_address

        self.contract_translator = abi.ContractTranslator(TRUSTERY_ABI)

    def _sendTransaction(self, data):
        return ethrpc.eth_sendTransaction({
            'from': self.from_address,
            'to': self.to_address,
            'data': '0x' + rlp.utils.encode_hex(data),
        })

    def addattribute(self, attributetype, has_proof, identifier, data, datahash):
        args = [attributetype, has_proof, identifier, data, datahash]
        data = self.contract_translator.encode('addAttribute', args)
        return self._sendTransaction(data)
