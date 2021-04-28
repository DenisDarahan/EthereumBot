from datetime import datetime

from botapp.middlewares import i18n


ETHERSCAN_MAIN = 'https://etherscan.io'
_ = i18n.gettext


async def get_transactions_repr(wallet: str, transactions: list, show_participants: int, counter: int = 1) -> str:
    trs_repr = ''
    for tr in transactions:
        if tr['from'] == wallet:
            sign = '➖'
            participant = f'\n<b>{_("to")}</b> <code>{tr["to"]}</code>'
        else:
            sign = '➕'
            participant = f'\n<b>{_("from")}</b> <code>{tr["from"]}</code>'

        trs_repr += (f'\n<b>{counter}</b>. <a href="{ETHERSCAN_MAIN}/tx/{tr["hash"]}">{sign}{tr["value"]} ETH</a> '
                     f'({datetime.utcfromtimestamp(int(tr["time"])).strftime("%H:%M %d.%m.%Y")})')

        trs_repr += participant * show_participants
        counter += 1

    return trs_repr
