from pyethereum import abi

from ethapi import TRUSTERY_ABI
from ethapi import TRUSTERY_ADDRESS
from ethapi import ethrpc
from ethapi import encode_api_data


class Transactions(object):
    def __init__(self, from_address=None, to_address=TRUSTERY_ADDRESS):
        if from_address is None:
            self.from_address = ethrpc.eth_accounts()[0]
        else:
            self.from_address = from_address
        self.to_address = to_address

        self._contract_translator = abi.ContractTranslator(TRUSTERY_ABI)

    def _sendtransaction(self, data):
        return ethrpc.eth_sendTransaction({
            'from': self.from_address,
            'to': self.to_address,
            'data': encode_api_data(data),
        })

    def addattribute(self, attributetype, has_proof, identifier, data, datahash):
        args = [attributetype, has_proof, identifier, data, datahash]
        data = self._contract_translator.encode('addAttribute', args)
        return self._sendtransaction(data)
