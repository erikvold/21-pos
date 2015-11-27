#!/usr/bin/python3

#
# Command line usage:
# $ python3 pos-client.py       # Get pos tagged article data
# $ python3 pos-client.py info  # Get server metadata
#

import json
import os
import sys
import click

# import from the 21 Developer Library
from two1.commands.config import Config
from two1.lib.wallet import Wallet
from two1.lib.bitrequests import BitTransferRequests

# set up bitrequest client for BitTransfer requests
wallet = Wallet()
username = Config().username
requests = BitTransferRequests(wallet, username)

DEFAULT_ENDPOINT = 'http://10.147.89.77:21349/'
DEFAULT_URL = 'https://bitcoinmagazine.com/articles/how-a-bitcoin-backbone-gives-small-miners-a-leg-up-matt-corrallo-s-relay-network-1447961203'

@click.group(invoke_without_command=True)
@click.option('--endpoint', '-e',
              default=DEFAULT_ENDPOINT,
              metavar='STRING',
              show_default=True,
              help='API endpoint URI')

@click.option('--url', '-u',
              default=DEFAULT_URL,
              metavar='STRING',
              show_default=True,
              help='Article URL')

@click.pass_context
def main(ctx, endpoint, url):
    """ Command-line Interface for the POS Tagger service
    """
    if ctx.obj is None:
        ctx.obj = {}

    ctx.obj['endpoint'] = endpoint
    ctx.obj['url'] = url
    
    if ctx.invoked_subcommand is None:
        cmd_article(ctx)

def cmd_article(ctx):
    sel_url = ctx.obj['endpoint'] + 'article'
    answer = requests.post(url=sel_url.format(), data=dict(url=(ctx.obj['url'])))
    print(answer.text)

@click.command(name='info')
@click.pass_context
def cmd_info(ctx):
    sel_url = ctx.obj['endpoint']
    answer = requests.get(url=sel_url.format())
    print(answer.text)

main.add_command(cmd_info)

if __name__ == "__main__":
    main()
