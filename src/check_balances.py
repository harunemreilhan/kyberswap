from provider import get_provider

def get_token_balance(wallet, token, in_ether: bool = False) -> int:
        provider = get_provider()
        token_contract = provider.eth.contract(address=token.address, abi=token.abi)
        """Get the balance of a token in a wallet."""
        balance: int = token_contract.functions.balanceOf(wallet).call()
        return provider.from_wei(balance, 'ether') if in_ether else balance