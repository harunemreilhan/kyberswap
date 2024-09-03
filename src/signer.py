from web3 import Web3
from src.provider import get_provider  # Import your custom provider function

class Signer:
    def __init__(self):
        """
        Initialize the Signer class with a private key.
        CAUTION: Never expose your private keys (i.e., commit to a public repo).
        """
        self.private_key = "01cd1c6dbc6510b43b6106100c51617c4a2b49e9464fd6878a425f08e48003c1"
        self.provider = get_provider()
        self.account = self._get_account()

    def _get_account(self):
        """
        Returns a Web3 account object for signing transactions.
        """
        return self.provider.eth.account.from_key(self.private_key)

    def get_signer(self):
        """
        Returns the account object which can be used to sign transactions.
        """
        return self.account

