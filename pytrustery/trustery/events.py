from ethereum import abi
from ethereum import processblock
from ethereum.utils import big_endian_to_int
from rlp.utils import decode_hex

from ethapi import TRUSTERY_ABI
from ethapi import TRUSTERY_DEFAULT_ADDRESS
from ethapi import ethclient
from ethapi import encode_api_data


class Events(object):
    def __init__(self, address=TRUSTERY_DEFAULT_ADDRESS):
        self.address = address

        self._contracttranslator = abi.ContractTranslator(TRUSTERY_ABI)

    def _get_logs(self, topics, event_name=None):
        if event_name is None:
            event_topic = ''
        else:
            event_topic = '' # TODO implement

        topics = [encode_api_data(topic) for topic in topics]
        topics = [event_topic] + topics

        logs = ethclient.get_logs({
            'fromBlock': 'earliest',
            'address': self.address,
            'topics': topics,
        })

        decoded_logs = []
        for log in logs:
            logobj = processblock.Log(
                log['address'][2:],
                [big_endian_to_int(decode_hex(topic[2:])) for topic in log['topics']],
                decode_hex(log['data'][2:])
            )
            decoded_log = self._contracttranslator.listen(logobj, noprint=True)
            decoded_logs.append(decoded_log)

        return decoded_logs

    def filter_attributes(self, attributeID=None, owner=None, identifier=None):
        return self._get_logs([attributeID, owner, identifier])
