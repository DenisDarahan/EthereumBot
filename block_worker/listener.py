import asyncio
import json

from aio_pika import connect, Message
import websockets

from block_worker.config import INFURA_PROJECT_ID


request = {
    'new_heads': {
        'jsonrpc': '2.0',
        'id': 1,
        'method': 'eth_subscribe',
        'params': ['newHeads']
    }  # get hash
}


def get_block_hash(block):
    block_hash = json.dumps({
        'number': int(block['params']['result']['number'], 16),
        'hash': block['params']['result']['hash']
    })
    return block_hash.encode()


async def main():
    # RabbitMQ connection
    async with await connect("amqp://guest:guest@localhost/", loop=loop) as connection:
        # Create a channel
        channel = await connection.channel()
        # Declaring queue (if it's not declared yet)
        queue = await channel.declare_queue('block_hash_queue')

        # INFURA connection
        async with websockets.connect(f'wss://mainnet.infura.io/ws/v3/{INFURA_PROJECT_ID}') as ws_head:
            # Send hello message
            await ws_head.send(json.dumps(request['new_heads']))
            print((await ws_head.recv()))

            # Listen to new blocks
            while True:
                try:
                    # Get new block head
                    new_head = json.loads((await ws_head.recv()))

                    # Get block hash
                    block_hash = get_block_hash(new_head)
                    print(block_hash)

                    # Send block hash to process
                    await channel.default_exchange.publish(Message(block_hash), routing_key=queue.name)
                except websockets.exceptions.ConnectionClosed:
                    print('ConnectionClosed')
                    break


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
