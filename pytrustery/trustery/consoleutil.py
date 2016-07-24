"""Console utility functions."""

import click

from trustery import userconfig


def echo_attribute_block(attribute, signatures_status=None):
    """Echo a console block representing basic data about the attribute."""
    if signatures_status is None and 'signatures_status' in attribute:
        signatures_status = attribute['signatures_status']

    # Encode attribute identifier as hex if it contains non-ASCII characters.
    if 'identifer' in attribute and not all(ord(c) < 128 for c in attribute['identifier']):
        attribute['identifier'] = '0x' + attribute['identifier'].rstrip('\x00').encode('hex')

    if 'attributeID' in attribute:
        click.echo("Attribute ID #" + str(attribute['attributeID']) + ':')
    if 'blindedAttributeID' in attribute:
        click.echo("Blinded attribute ID #" + str(attribute['blindedAttributeID']) + ':')
    if 'signingAttributeID' in attribute:
        click.echo("\tSigning attribute ID: " + str(attribute['signingAttributeID']) + '.')
    click.echo("\tType: " + attribute['attributeType'])
    click.echo("\tOwner: " + attribute['owner']
        + (" [trusted]" if userconfig.is_trusted(attribute['owner']) else " [untrusted]"))
    if 'identifer' in attribute:
        click.echo("\tIdentifier: " + attribute['identifier'])

    if signatures_status is not None:
        valid_signatures = signatures_status['status']['valid']
        click.echo("\t[" + str(valid_signatures) + " valid signature"
            + ("]" if valid_signatures == 1 else "s]"))
