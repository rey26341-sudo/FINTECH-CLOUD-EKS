from blockchain.ethereum.web3_client import get_web3
from blockchain.ethereum.wallet import get_account
from config import CHAIN_ID
def send_transaction(to_address, value_eth):
    w3 = get_web3()
    account = get_account()
    tx = {
        "from": account.address,
        "to": to_address,
        "value": w3.to_wei(value_eth, "ether"),
        "nonce": w3.eth.get_transaction_count(account.address),
        "gas": 21000,
        "gasPrice": w3.eth.gas_price,
        "chainId": CHAIN_ID,
    }
    signed_tx = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    return w3.to_hex(tx_hash)
