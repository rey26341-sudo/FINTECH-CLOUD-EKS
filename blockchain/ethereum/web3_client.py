from web3 import Web3
from config import SEPOLIA_RPC_URL
def get_web3():
    w3 = Web3(Web3.HTTPProvider(SEPOLIA_RPC_URL))
    if not w3.is_connected():
        raise ConnectionError("Could not connect to Sepolia RPC")
    return w3
