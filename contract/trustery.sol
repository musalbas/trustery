contract Trustery {
    struct Attribute {
        address owner;
        string attributeType;
        bool has_proof;
        string identifier;
        string data;
        string datahash;
    }

    struct Signature {
        address signer;
        uint attributeID;
        uint expiry;
    }

    struct Revocation {
        uint signatureID;
    }

    Attribute[] public attributes;
    Signature[] public signatures;
    Revocation[] public revocations;

    event AttributeAdded(uint indexed attributeID, address indexed owner, string attributeType, bool has_proof, string indexed identifier, string data, string datahash);
    event AttributeSigned(uint indexed signatureID, address indexed signer, uint indexed attributeID, uint expiry);
    event SignatureRevoked(uint indexed revocationID, uint indexed signatureID);

    function addAttribute(string attributeType, bool has_proof, string identifier, string data) returns (uint attributeID) {
        attributeID = attributes.length++;
        Attribute attribute = attributes[attributeID];
        attribute.owner = msg.sender;
        attribute.attributeType = attributeType;
        attribute.has_proof = has_proof;
        attribute.identifier = identifier;
        attribute.data = data;
        attribute.datahash = datahash;
        AttributeAdded(attributeID, msg.sender, attributeType, has_proof, identifier, data, datahash);
    }

    function signAttribute(uint attributeID, uint expiry) returns (signatureID) {
        signatureID = signatures.length++;
        Signature signature = signatures[signatureID];
        signature.signer = msg.sender;
        signature.attributeID = attributeID;
        signature.expiry = expiry;
        AttributeSigned(signatureID, msg.sender, attributeID, expiry);
    }

    function revokeSignature(uint signatureID) returns (revocationID) {
        if (attributes[signatureID].owner == msg.sender) {
            revocationID = revocations.length++;
            Revocation revocation = revocations[revocationID];
            revocation.signatureID = signatureID;
            AttributeRevoked(revocationID, signatureID);
        }
    }
}
