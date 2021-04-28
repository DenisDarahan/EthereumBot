from urllib.parse import urlencode

from web3 import Web3

from EthereumConfigs import ETHERSCAN_TOKEN
from .base import fetch_content_get, get_transactions


ETHERSCAN_ENDPOINT = 'https://api.etherscan.io/api'


async def get_user_balance(wallet: str) -> str:
    params = {
        'module': 'account',
        'action': 'balance',
        'address': wallet,
        'tag': 'latest',
        'apikey': ETHERSCAN_TOKEN
    }
    url = f'{ETHERSCAN_ENDPOINT}?{urlencode(params)}'
    response = await fetch_content_get(url)
    balance = f'{float(Web3.fromWei(int(response["result"]), "ether")):.10f}'.rstrip('0').rstrip('.')
    return balance


async def get_wallet_transactions(wallet: str, records_number: int = 5) -> list:
    params = {
        'module': 'account',
        'action': 'txlist',
        'address': wallet,
        'page': 1,
        'offset': records_number,
        'sort': 'desc',
        'apikey': ETHERSCAN_TOKEN
    }
    url = f'{ETHERSCAN_ENDPOINT}?{urlencode(params)}'
    transactions = await get_transactions(url)
    return transactions


async def get_wallet_internal_transactions(wallet: str, records_number: int = 5) -> list:
    params = {
        'module': 'account',
        'action': 'txlistinternal',
        'address': wallet,
        'page': 1,
        'offset': records_number,
        'sort': 'desc',
        'apikey': ETHERSCAN_TOKEN
    }
    url = f'{ETHERSCAN_ENDPOINT}?{urlencode(params)}'
    transactions = await get_transactions(url)
    return transactions


async def get_wallet_erc20_transactions(wallet: str, records_number: int = 5) -> list:
    params = {
        'module': 'account',
        'action': 'tokentx',
        'address': wallet,
        'page': 1,
        'offset': records_number,
        'sort': 'desc',
        'apikey': ETHERSCAN_TOKEN
    }
    url = f'{ETHERSCAN_ENDPOINT}?{urlencode(params)}'
    transactions = await get_transactions(url)
    return transactions


async def get_wallet_erc721_transactions(wallet: str, records_number: int = 5) -> list:
    params = {
        'module': 'account',
        'action': 'tokennfttx',
        'address': wallet,
        'page': 1,
        'offset': records_number,
        'sort': 'desc',
        'apikey': ETHERSCAN_TOKEN
    }
    url = f'{ETHERSCAN_ENDPOINT}?{urlencode(params)}'
    transactions = await get_transactions(url)
    return transactions


async def get_block_internal_transactions(block_number: int, tr_number: int) -> list:
    params = {
        'module': 'account',
        'action': 'txlistinternal',
        'startblock': block_number,
        'endblock': block_number,
        'page': 1,
        'offset': tr_number,
        'sort': 'asc',
        'apikey': ETHERSCAN_TOKEN
    }
    url = f'{ETHERSCAN_ENDPOINT}?{urlencode(params)}'
    response = await fetch_content_get(url)
    return response['result']
