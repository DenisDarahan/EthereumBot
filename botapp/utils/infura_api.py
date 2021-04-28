from json import dumps

from EthereumConfigs import INFURA_PROJECT_ID
from .base import fetch_content_post


INFURA_ENDPOINT = f'https://mainnet.infura.io/v3/{INFURA_PROJECT_ID}'


async def get_block_transactions(block_hash: str):
    data = {
        'jsonrpc': '2.0',
        'method': 'eth_getBlockByHash',
        'params': [block_hash, True],
        'id': 2
    }
    response = await fetch_content_post(INFURA_ENDPOINT, data=dumps(data))
    return response
