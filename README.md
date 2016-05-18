# trustery
**Note: this is a proof-of-concept prototype and shouldn't be used in production.**

Trustery is a Public Key Infrastructure (PKI) and identity management system on the Ethereum blockchain.

The aim of this project is to provide a PKI that has built-in certificate transparency to make it easy to detect rogue certificates, by building an alternative to decentralized PKI by using a public-ledgered web-of-trust model for fine-grained identity management.

[A full report is available here.](https://github.com/musalbas/trustery-report/blob/master/Report.pdf)

## Command-line options
<pre>Usage: trustery [OPTIONS] COMMAND [ARGS]...

  Ethereum-based identity system.

Options:
  --help  Show this message and exit.

Commands:
  add                 Add an attribute to your identity.
  ipfsadd             Add an attribute to your identity over IPFS.
  ipfsaddpgp          Add a PGP key attribute to your identity over IPFS.
  retrieve            Retrieve an attribute.
  revoke              Revoke one of your signatures.
  search              Search for attributes.
  sign                Sign an attribute.
  trust               Trust an Ethereum address.
  trusted             View the list of trusted Ethereum addresses.
  untrust             Untrust an Ethereum address.
</pre>

## Installation
```
git clone https://github.com/musalbas/trustery.git
cd trustery/pytrustery
pip install --user --editable .
```
