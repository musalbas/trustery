"""API for making Trustery tranactions."""

from ethereum import abi

from ethapi import TRUSTERY_ABI
from ethapi import TRUSTERY_DEFAULT_ADDRESS
from ethapi import ethclient
from ethapi import encode_api_data


class Transactions(object):
    """API for making Trustery tranactions."""
    def __init__(self, from_address=None, to_address=TRUSTERY_DEFAULT_ADDRESS):
        """
        Initialise transactions.

        from_address: the Ethereum address transactions should be sent from.
        to_address: the Ethereum Trustery contract address.
        """
        if from_address is None:
            # Use the first Ethereum account address if no from address is specified.
            self.from_address = ethclient.get_accounts()[0]
        else:
            self.from_address = from_address
        self.to_address = to_address

        # Initialise contract ABI.
        self._contracttranslator = abi.ContractTranslator(TRUSTERY_ABI)

    def _send_transaction(self, data):
        """
        Send a transaction.

        data: the transactions data.
        """
        return ethclient.send_transaction(
            _from=self.from_address,
            to=self.to_address,
            data=encode_api_data(data),
            gas=2000000, # TODO deal with gas limit more sensibly
        )

    def add_attribute(self, attributetype, has_proof, identifier, data, datahash):
        """
        Send a transaction to add an identity attribute.

        attributetype: the type of address.
        has_proof: True if the attribute has a cryptographic proof, otherwise False.
        identifier: the indexable identifier of the attribute.
        data: the data of the attribute.
        datahash: the Keccak hash of the data of the attribute if it is stored off-blockchain.
        """
        args = [attributetype, has_proof, identifier, data, datahash]
        data = self._contracttranslator.encode('addAttribute', args)
        return self._send_transaction(data)

    def sign_attribute(self, attributeID, expiry):
        """
        Send a transaction to sign an identity attriute.

        attributeID: the ID of the attribute.
        expiry: the expiry time of the attriute.
        """
        args = [attributeID, expiry]
        data = self._contracttranslator.encode('signAttribute', args)
        return self._send_transaction(data)

    def revoke_signature(self, signatureID):
        """
        Send a transaction to revoke a signature.

        signatureID: the ID of the signature.
        """
        args = [signatureID]
        data = self._contracttranslator.encode('revokeSignature', args)
        return self._send_transaction(data)
