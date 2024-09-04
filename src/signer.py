from provider import get_provider  # Import your custom provider function

class Signer:
    def __init__(self, private_key):
        """
        Initialize the Signer class with a private key.
        CAUTION: Never expose your private keys (i.e., commit to a public repo).
        """
        self.private_key = private_key
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

