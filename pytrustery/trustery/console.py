import logging

import click

from trustery.transactions import Transactions


class StrParamType(click.ParamType):
    name = 'STR'

    def convert(self, value, param, ctx):
        return str(value)

STR = StrParamType()


@click.group()
def cli():
    logging.getLogger("requests").setLevel(logging.WARNING)


@cli.command()
@click.option('--attributetype', prompt=True, type=STR)
@click.option('--has_proof', prompt=True, type=bool)
@click.option('--identifier', prompt=True, type=STR)
@click.option('--data', prompt=True, type=STR)
@click.option('--datahash', prompt=True, type=STR)
def rawaddattribute(attributetype, has_proof, identifier, data, datahash):
    transactions = Transactions()
    transactions.add_attribute(attributetype, has_proof, identifier, data, datahash)

    click.echo()
    click.echo("Transaction sent.")
