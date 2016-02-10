from pyethereum import abi

from ethapi import TRUSTERY_ABI
from ethapi import TRUSTERY_ADDRESS
from ethapi import ethrpc
from ethapi import encode_api_data


class Events(object):
    def __init__(self, address=TRUSTERY_ADDRESS):
        self.address = address

        self._contract_translator = abi.ContractTranslator(TRUSTERY_ABI)

    def _getlogs(self, topics, eventname=None):
        if eventname is None:
            eventtopic = ''
        else:
            eventtopic = '' # TODO implement

        topics = [encode_api_data(topic) for topic in topics]
        topics = [eventtopic] + topics

        return ethrpc.eth_getLogs({
            'fromBlock': 'earliest',
            'address': self.address,
            'topics': topics,
        })

    def filterattributes(self, attributeID=None, owner=None, identifier=None):
        return self._getlogs([attributeID, owner, identifier])
