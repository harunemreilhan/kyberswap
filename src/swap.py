from src.post import PostSwapRouteV1
from src.approval import TokenApproval
from src.constants import token_in
from src.signer import Signer
from src.provider import get_provider

class V1Swap:
    def __init__(self):
        self.post_swap = PostSwapRouteV1()
        self.signerC = Signer()
        self.signer_address = self.signerC.get_signer().address
        self.signer = self.signerC.get_signer()
        self.provider = get_provider()
    async def v1_swap(self):
        # Get the swap data required to execute the transaction on-chain
        swap_data = await self.post_swap.post_swap_route_v1()
        encoded_swap_data = swap_data['data']
        router_contract = swap_data['routerAddress']

        # Use the configured signer to submit the on-chain transactions

        # Ensure that the router contract has sufficient allowance
        approval = TokenApproval()
        await approval.get_token_approval(token_in.address, self.signer_address, router_contract, swap_data['amountIn'])

        # Execute the swap transaction
        print("\nExecuting the swap tx on-chain...")
        print(f"Encoded data: {encoded_swap_data}")
        print(f"Router contract address: {router_contract}")
        try:
            execute_swap_tx = self.signer.sign_transaction({
                'data': encoded_swap_data,
                'from': self.signer_address,
                'to': router_contract,
                'gas': 3000000,
                'gasPrice': self.signerC.provider.eth.gas_price,
                'nonce': self.signerC.provider.eth.get_transaction_count(self.signer_address) + 1,
            })

            execute_swap_tx_receipt = self.provider.eth.send_raw_transaction(execute_swap_tx.rawTransaction)
            tx_hash_hex = str(self.provider.to_hex(execute_swap_tx_receipt))
            receipt = self.provider.eth.wait_for_transaction_receipt(tx_hash_hex)
            print(f"Swap tx executed with hash: {receipt}")
        except Exception as e:
            if "nonce too low" in str(e):
                print("Nonce too low, retrying...")
                await self.v1_swap()
