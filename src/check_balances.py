from provider import get_provider

def get_token_balance(wallet, token, formatted: bool = False) -> int:
        provider = get_provider()
        token_contract = provider.eth.contract(address=token.address, abi=token.abi)
        """Get the balance of a token in a wallet."""
        balance: int = token_contract.functions.balanceOf(wallet).call()
        return balance / token.decimals if formatted else balance