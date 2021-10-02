from web3 import Web3
import json
from utils.vars import *

w3 = Web3(Web3.HTTPProvider(RONIN_PROVIDER))
with open("entity/abis/slp_abi.json") as f:
    min_abi = json.load(f)


def check_slp_balance():
    slp_contract = w3.eth.contract(
        address=Web3.toChecksumAddress(SLP_CONTRACT),
        abi=min_abi
    )
    balance = slp_contract.functions.balanceOf(
        Web3.toChecksumAddress(FROM_ADDR.replace("ronin:", "0x"))
    ).call()
    return int(balance)


def check_balance():
    slp_contract = w3.eth.contract(
        address=Web3.toChecksumAddress(WETH_CONTRACT),
        abi=min_abi
    )
    balance = slp_contract.functions.balanceOf(
        Web3.toChecksumAddress(FROM_ADDR.replace("ronin:", "0x"))
    ).call()
    return int(balance)


def get_nonce(account):
    w3 = Web3(Web3.HTTPProvider(RONIN_PROVIDER_FREE))
    nonce = w3.eth.get_transaction_count(
        Web3.toChecksumAddress(account.replace("ronin:", "0x"))
    )
    return nonce
