from eth_account import Account
from blockchain.ethereum.web3_client import get_web3
from config import WALLET_PRIVATE_KEY
def get_account():
    return Account.from_key(WALLET_PRIVATE_KEY)
def get_balance(address=None):
    w3 = get_web3()
    address = address or get_account().address
    balance_wei = w3.eth.get_balance(address)
    return w3.from_wei(balance_wei, "ether")
