import asyncio
from utils.vars import *
from utils.helper import get_nonce
from web3 import Web3, exceptions
from utils.notification import send_notification
from utils.helper import check_balance, check_slp_balance
import json

w3 = Web3(Web3.HTTPProvider(RONIN_PROVIDER_FREE))
with open("entity/abis/slp_abi.json") as f:
    slb_abi = json.load(f)


async def produce_transaction(txtype):
    if txtype == 'SLP':
        use_contract = SLP_CONTRACT
        amount = check_slp_balance()
    else:
        use_contract = WETH_CONTRACT
        amount = check_balance()
    slp_contract = w3.eth.contract(
        address=Web3.toChecksumAddress(use_contract),
        abi=slb_abi
    )

    transaction = slp_contract.functions.transfer(
        Web3.toChecksumAddress(TO_ADDR),
        amount
    ).buildTransaction({
        "gas": 500000,
        "gasPrice": w3.toWei("0", "gwei"),
        "nonce": get_nonce(FROM_ADDR)
    })

    signed = w3.eth.account.sign_transaction(
        transaction,
        private_key=PRIV_KEY
    )
    try:
        w3.eth.send_raw_transaction(signed.rawTransaction)
        return signed, amount, txtype
    except Exception as e:
        send_notification(amount, txtype, failed=True, desc=str(e))


async def execute_signed_transaction(signed, amount, txtype):
    tx_hash = w3.toHex(w3.keccak(signed.rawTransaction))
    print("https://explorer.roninchain.com/txs/" + str(tx_hash))
    while True:
        try:
            recepit = w3.eth.get_transaction_receipt(tx_hash)
            if recepit["status"] == 1:
                success = True
                send_notification(amount, txtype, tx_hash=tx_hash, failed=False)
            else:
                success = False
            break
        except exceptions.TransactionNotFound:
            print(f"Waiting for transfer '{tx_hash}' to finish")
            await asyncio.sleep(5)



