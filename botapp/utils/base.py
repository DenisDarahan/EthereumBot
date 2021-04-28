import json

from web3 import Web3

from botapp.misc import bot


async def fetch_content_get(url: str, **kwargs):
    async with bot.session.get(url, **kwargs) as response:
        return json.loads(await response.text())


async def fetch_content_post(url: str, **kwargs):
    async with bot.session.post(url, **kwargs) as response:
        return json.loads(await response.text())


async def get_transactions(url):
    response = await fetch_content_get(url)
    transactions = [{'hash': tr['hash'], 'from': tr['from'], 'to': tr['to'], 'time': tr['timeStamp'],
                     'value': f'{float(Web3.fromWei(int(tr["value"]), "ether")):.10f}'.rstrip('0').rstrip('.')}
                    for tr in response['result']]
    return transactions
