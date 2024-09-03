import requests
from src.constants import AGGREGATOR_DOMAIN, ChainName
from src.get import SwapRoute
from src.signer import Signer

class PostSwapRouteV1:
    def __init__(self):
        self.chain_name = ChainName.BSC
        self.target_path = f"/{self.chain_name}/api/v1/route/build"
        self.signer = Signer()
        self.swap_route = SwapRoute()
    
    async def post_swap_route_v1(self):
        # Get the route summary data to be encoded
        swap_route_data = self.swap_route.get_swap_route_v1()
        route_summary = swap_route_data['routeSummary']

        # Get the signer's address
        signer_address = self.signer.get_signer()

        # Configure the request body
        request_body = {
            "routeSummary": route_summary,
            "sender": signer_address.address,
            "recipient": signer_address.address,
            "slippageTolerance": 10  # 0.1%
        }

        # Call the API with requests to handle async calls
        try:
            print("\nCalling [V1] Post Swap Route For Encoded Data...")
            response = requests.post(AGGREGATOR_DOMAIN + self.target_path, json=request_body)

            print("[V1] POST Response:")
            print(response.json())
            return response.json().get('data')
        except requests.exceptions.RequestException as error:
            print(f"An error occurred: {error}")

