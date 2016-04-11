"""Interface for GPG."""

import shutil
import tempfile

import gnupg

# Initialise GPG interface.
gpgclient = gnupg.GPG()


class TempGPG(object):
    """A class for creating a temporary GPG instance seperate from the user's GPG home directory."""

    def __init__(self):
        """Initialise the temporary GPG instance."""
        # Securely create a temporary directory.
        self.tempdir = tempfile.mkdtemp()

        # Initialise temporary GPG interface.
        self.gpgclient = gnupg.GPG(gnupghome=self.tempdir)

    def destroy(self):
        """Destroy the temporary GPG instance."""
        shutil.rmtree(self.tempdir)


def generate_pgp_attribute_data(keyid, address):
    """
    Generate the data field (the PGP public key and cryptographic proof) for a PGP attribute.

    Returns a (fingerprint, data) tuple.

    keyid: the ID of the PGP key.
    address: Ethereum address to generate cryptographic proof for.
    """
    # Export public key.
    public_key = gpgclient.export_keys(keyid, minimal=True)

    # Use temporary GPG interface to check that only one key has been exported and to get its fingerprint.
    tempgpg = TempGPG()
    try:
        # Import public key.
        import_results = tempgpg.gpgclient.import_keys(public_key)

        # Check that only one key has been imported.
        if import_results.count != 1:
            raise ValueError("invalid PGP key ID specified")

        # Get key fingerprint.
        fingerprint = str(import_results.fingerprints[0])
    finally:
        # Destroy temporary GPG interface.
        tempgpg.destroy()

    # Generate cryptographic proof signature.
    proof = gpgclient.sign('Ethereum address: ' + address, keyid=fingerprint).data

    # Check that a proof was actually generated.
    if not proof:
        raise ValueError("a PGP key was specified that does not have a corresponding secret key")

    # Concatenate public key and cryptographic proof.
    data = public_key + '\n' + proof

    # Return data and fingerprint.
    return (fingerprint, data)


def process_proof(data):
    """
    Process cryptographic proof of PGP attribute data.

    Returns a (Ethereum address, PGP key fingerprint) tuple the proof is associated with if the signature is valid, otherwise False.

    data: the PGP attribute data.
    """
    # Extract key, signature and Ethereum address.
    key = ''
    signature = ''
    address = ''
    key_mode = False
    signature_mode = False
    for line in data.split('\n'):
        line = line.strip()
        if line == '-----END PGP PUBLIC KEY BLOCK-----':
            key_mode = False
            key += line + '\n'
        elif line == '-----BEGIN PGP PUBLIC KEY BLOCK-----' or key_mode:
            if not key_mode:
                key_mode = True
            key += line + '\n'
        elif line == '-----END PGP SIGNATURE-----':
            signature_mode = False
            signature += line + '\n'
        elif line == '-----BEGIN PGP SIGNED MESSAGE-----' or signature_mode:
            if not signature_mode:
                signature_mode = True
            if line.startswith('Ethereum address: '):
                address = line[len('Ethereum address: '):]
            signature += line + '\n'

    # Create temporary keychain and import key.
    tempgpg = TempGPG()
    import_results = tempgpg.gpgclient.import_keys(key)

    verified = tempgpg.gpgclient.verify(signature)

    tempgpg.destroy()

    if not verified:
        return False

    return (address, verified.fingerprint)
