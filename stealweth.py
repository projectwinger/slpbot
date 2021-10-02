import asyncio
import itertools as it
from utils.helper import check_balance, check_slp_balance
import time
import random

from entity.weth import produce_transaction, execute_signed_transaction


async def randsleep(caller=None) -> None:
    i = random.randint(0, 3)
    if caller:
        print(f"{caller} sleeping for {i} seconds.")
    await asyncio.sleep(i)


async def wproducer(name, q) -> None:
    n = random.randint(0, 5)
    for _ in it.repeat(None, n):
        await randsleep(caller=f"Producer {name}")
        i, t, txtype = await produce_transaction("WETH")
        await q.put((i, t, txtype))
        print(f"Weth Producer {name} added <{t} {txtype}> to queue.")


async def consumer(name, q) -> None:
    while True:
        await randsleep(caller=f"Consumer {name}")
        i, t, txtype = await q.get()
        now = time.perf_counter()
        print(f"Consumer {name} executing {txtype} contract"
              f" in {now - t:0.5f} seconds.")
        await execute_signed_transaction(i, t, txtype)
        q.task_done()


async def main():
    queue = asyncio.Queue()

    wproducers = [asyncio.create_task(wproducer(n, queue)) for n in range(50)]

    consumers = [asyncio.create_task(consumer(n, queue)) for n in range(100)]
    await asyncio.gather(*wproducers, *consumers)
    await queue.join()  # Implicitly awaits consumers, too
    for c in consumers:
        c.cancel()

asyncio.run(main())
