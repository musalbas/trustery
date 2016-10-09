"""Console utility functions."""

import click

from trustery import userconfig


def echo_attribute_block(attribute, signatures_status=None):
    """Echo a console block representing basic data about the attribute."""
    if signatures_status is None and 'signatures_status' in attribute:
        signatures_status = attribute['signatures_status']

    # Encode attribute identifier as hex if it contains non-ASCII characters.
    if not all(ord(c) < 128 for c in attribute['identifier']):
        attribute['identifier'] = '0x' + attribute['identifier'].rstrip('\x00').encode('hex')

    click.echo("Attribute ID #" + str(attribute['attributeID']) + ':')
    click.echo("\tType: " + attribute['attributeType'])
    click.echo("\tOwner: " + attribute['owner']
        + (" [trusted]" if userconfig.is_trusted(attribute['owner']) else " [untrusted]"))
    click.echo("\tIdentifier: " + attribute['identifier'])

    if signatures_status is not None:
        valid_signatures = signatures_status['status']['valid']
        click.echo("\t[" + str(valid_signatures) + " valid signature"
            + ("]" if valid_signatures == 1 else "s]"))
