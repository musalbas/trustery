from pyethereum import abi

from ethapi import TRUSTERY_ABI
from ethapi import TRUSTERY_ADDRESS
from ethapi import ethrpc
from ethapi import encode_api_data


class Events(object):
    def __init__(self, address=TRUSTERY_ADDRESS):
        self.address = address

        self._contracttranslator = abi.ContractTranslator(TRUSTERY_ABI)

    def _getlogs(self, topics, event_name=None):
        if event_name is None:
            event_topic = ''
        else:
            event_topic = '' # TODO implement

        topics = [encode_api_data(topic) for topic in topics]
        topics = [event_topic] + topics

        return ethrpc.eth_getLogs({
            'fromBlock': 'earliest',
            'address': self.address,
            'topics': topics,
        })

    def filterattributes(self, attributeID=None, owner=None, identifier=None):
        return self._getlogs([attributeID, owner, identifier])
