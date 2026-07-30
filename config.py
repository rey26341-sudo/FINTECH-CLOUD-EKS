import os
from dotenv import load_dotenv
load_dotenv()
SEPOLIA_RPC_URL = os.getenv("SEPOLIA_RPC_URL")
WALLET_PRIVATE_KEY = os.getenv("WALLET_PRIVATE_KEY")
CHAIN_ID = int(os.getenv("CHAIN_ID", 11155111))
