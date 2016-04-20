contract Trustery {
    struct Signature {
        address signer;
    }

    uint public attributes;
    Signature[] public signatures;
    uint public revocations;

    event AttributeAdded(uint indexed attributeID, address indexed owner, string attributeType, bool has_proof, bytes32 indexed identifier, string data, string datahash);
    event AttributeSigned(uint indexed signatureID, address indexed signer, uint indexed attributeID, uint expiry);
    event SignatureRevoked(uint indexed revocationID, uint indexed signatureID);

    function addAttribute(string attributeType, bool has_proof, bytes32 identifier, string data, string datahash) returns (uint attributeID) {
        attributeID = attributes++;
        AttributeAdded(attributeID, msg.sender, attributeType, has_proof, identifier, data, datahash);
    }

    function signAttribute(uint attributeID, uint expiry) returns (uint signatureID) {
        signatureID = signatures.length++;
        Signature signature = signatures[signatureID];
        signature.signer = msg.sender;
        AttributeSigned(signatureID, msg.sender, attributeID, expiry);
    }

    function revokeSignature(uint signatureID) returns (uint revocationID) {
        if (signatures[signatureID].signer == msg.sender) {
            revocationID = revocations++;
            SignatureRevoked(revocationID, signatureID);
        }
    }
}
