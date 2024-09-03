from web3 import Web3

def get_provider():
    """
    Returns a Web3 provider connected to the Binance Smart Chain.
    """
    bsc_rpc_url = "https://bsc-dataseed.binance.org/"  # Public BSC RPC URL
    return Web3(Web3.HTTPProvider(bsc_rpc_url))