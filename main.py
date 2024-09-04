from src.swap import V1Swap

class Manager:
    def __init__(self, private_key):
        self.v1_swap = V1Swap(private_key=private_key)

    async def buy(self, usdt, token, amount_in):
        await self.v1_swap.v1_swap(token_in=usdt, token_out=token, amount_in=amount_in)

    async def sell(self, token, usdt, amount_in):
        await self.v1_swap.v1_swap(token_in=token, token_out=usdt, amount_in=amount_in)