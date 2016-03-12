"""Console application for Trustery."""

import logging
import time

import click

from trustery.events import Events
from trustery.transactions import Transactions


class StrParamType(click.ParamType):
    """Click parameter type that converts data using str()."""
    name = 'STR'

    def convert(self, value, param, ctx):
        return str(value)

STR = StrParamType()


@click.group()
def cli():
    """Ethereum-based identity system."""
    # Prevent the requests module from printing INFO logs to the console.
    logging.getLogger("requests").setLevel(logging.WARNING)


@cli.command()
@click.option('--attributetype', prompt=True, type=STR)
@click.option('--has_proof', prompt=True, type=bool)
@click.option('--identifier', prompt=True, type=STR)
@click.option('--data', prompt=True, type=STR)
@click.option('--datahash', prompt=True, type=STR)
def rawaddattribute(attributetype, has_proof, identifier, data, datahash):
    """(Advanced) Manually add an attribute to your identity."""
    transactions = Transactions()
    transactions.add_attribute(attributetype, has_proof, identifier, data, datahash)

    click.echo()
    click.echo("Transaction sent.")


@cli.command()
@click.option('--attributeid', prompt=True, type=int)
@click.option('--expiry', prompt=True, type=STR)
def rawsignattribute(attributeid, expiry):
    """(Advanced) Manually sign an attribute about an identity."""
    transactions = Transactions()
    transactions.sign_attribute(attributeid, expiry)

    click.echo()
    click.echo("Transaction sent.")


@cli.command()
@click.option('--signatureid', prompt=True, type=STR)
def rawrevokeattribute(signatureid):
    """(Advanced) Manaully revoke your signature of an attribute."""
    transactions = Transactions()
    transactions.revoke_signature(signatureid)

    click.echo()
    click.echo("Transaction sent.")


@cli.command()
@click.option('--attributetype', prompt='Attribute type', help='Attribute type', type=STR)
@click.option('--identifier', prompt='Attribute identifier', help='Attribute identifier', type=STR)
@click.option('--data', prompt='Attribute data', default='', help='Attribute data', type=STR)
def add(attributetype, identifier, data):
    """Add an attribute to your identity."""
    transactions = Transactions()
    transactions.add_attribute_with_hash(attributetype, False, identifier, data)

    click.echo()
    click.echo("Transaction sent.")


@cli.command()
@click.option('--attributeid', prompt='Attribute ID', help='Attribute ID', type=int)
@click.option('--expires', prompt='Signature days to expire', default=365, help='Signature days to expire', type=int)
def sign(attributeid, expires):
    """Sign an attribute."""
    transactions = Transactions()

    expiry = int(time.time()) + expires * 60 * 60 * 24
    transactions.sign_attribute(attributeid, expiry)

    click.echo()
    click.echo("Transaction sent.")


@cli.command()
@click.option('--signatureid', prompt='Signature ID', help='Signature ID', type=int)
def revoke(signatureid):
    """Revoke one of your signatures."""
    transactions = Transactions()
    transactions.revoke_signature(signatureid)

    click.echo()
    click.echo("Transaction sent.")


@cli.command()
@click.option('--attributeid', prompt='Attribute ID', help='Attribute ID', type=int)
def retrieve(attributeid):
    """Retrieve an attribute."""
    events = Events()
    attribute = events.retrieve_attribute(attributeid)

    if attribute is None:
        click.echo("No such attribute.")
        return

    click.echo()

    click.echo("Attribute ID #" + str(attribute['attributeID']) + ':')
    click.echo("\tType: " + attribute['attributeType'])
    click.echo("\tOwner: " + attribute['owner'])
    click.echo("\tIdentifier: " + attribute['identifier'])
    click.echo("\t[" + str(attribute['signatures_status']['status']['valid']) + " valid signatures]")
    click.echo()

    click.echo("Signatures for attribute ID #" + str(attribute['attributeID']) + ':')
    for signature in attribute['signatures_status']['signatures']:
        sig_line = "\t#" + str(signature['signatureID'])

        if signature['revocation']:
            sig_line += " [revoked]"
        elif signature['expired']:
            sig_line += " [expired]"
        elif signature['valid']:
            sig_line += " [valid]"

        sig_line += " by " + signature['signer']
        click.echo(sig_line)


@cli.command()
@click.option('--attributetype', help='Attribute type', type=STR)
@click.option('--identifier', help='Attribute identifier', type=STR)
@click.option('--owner', help='Attribute owner', type=STR)
def search(attributetype, identifier, owner):
    """Search for attributes."""
    events = Events()
    attributes = events.filter_attributes(None, identifier, owner)

    for attribute in attributes:
        if attributetype is not None and attributetype != attribute['attributeType']:
            continue

        signatures_status = events.get_attribute_signatures_status(attribute['attributeID'])

        click.echo("Attribute ID #" + str(attribute['attributeID']) + ':')
        click.echo("\tType: " + attribute['attributeType'])
        click.echo("\tOwner: " + attribute['owner'])
        click.echo("\tIdentifier: " + attribute['identifier'])
        click.echo("\t[" + str(signatures_status['status']['valid']) + " valid signatures]")
        click.echo()
