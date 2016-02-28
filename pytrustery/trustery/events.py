"""API for retrieving Trustery events."""

from ethereum import abi
from ethereum import processblock
from ethereum.utils import big_endian_to_int
from rlp.utils import decode_hex

from ethapi import TRUSTERY_ABI
from ethapi import TRUSTERY_DEFAULT_ADDRESS
from ethapi import ethclient
from ethapi import encode_api_data


class Events(object):
    """API for retrieving Trustery events."""
    def __init__(self, address=TRUSTERY_DEFAULT_ADDRESS):
        """
        Initialise events retriever.

        address: the Ethereum Trustery contract address.
        """
        self.address = address

        # Initialise contract ABI.
        self._contracttranslator = abi.ContractTranslator(TRUSTERY_ABI)

    def _get_event_id_by_name(self, event_name):
        """
        Get the ID of an event given its name.

        event_name: the name of the event.
        """
        for event_id, event in self._contracttranslator.event_data.iteritems():
            if event['name'] == event_name:
                return event_id

    def _get_logs(self, topics, event_name=None):
        """
        Get logs (events).

        topics: a list of topics to search for.
        event_name: the name of the event.
        """
        # Set the event topic to the event ID if the event name is specified.
        if event_name is None:
            event_topic = None
        else:
            event_topic = self._get_event_id_by_name(event_name)

        # Prepent the event type to the topics.
        topics = [event_topic] + topics
        # Encode topics to be sent to the Ethereum client.
        topics = [encode_api_data(topic) for topic in topics]

        # Get logs from Ethereum client.
        logs = ethclient.get_logs(
            from_block='earliest',
            address=self.address,
            topics=topics,
        )

        # Decode logs using the contract ABI.
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
        """
        Filter and retrieve attributes.

        attributeID: the ID of the attribute.
        owner: the Ethereum address that owns the attributes.
        identifier: the identifier of the attribute.
        """
        return self._get_logs([attributeID, owner, identifier], event_name='AttributeAdded')
