"""
Chain-agnostic interface. routes/ should only ever import from here,
never reach into blockchain/ethereum/, blockchain/polygon/, etc. directly.
"""
from blockchain.ethereum import wallet as eth_wallet
from blockchain.ethereum import transaction as eth_transaction

SUPPORTED_CHAINS = {"ethereum"}  # add "polygon", "solana" as you build them

def send_payment(chain: str, to_address: str, value: float):
    if chain == "ethereum":
        return eth_transaction.send_transaction(to_address, value)
    raise ValueError(f"Unsupported chain: {chain}")

def get_balance(chain: str, address: str = None):
    if chain == "ethereum":
        return eth_wallet.get_balance(address)
    raise ValueError(f"Unsupported chain: {chain}")
