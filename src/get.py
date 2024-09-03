import requests
from src.constants import AGGREGATOR_DOMAIN, ChainName, token_in, token_out

class SwapRoute:
    def __init__(self, chain_name=ChainName.BSC, token_in=token_in, token_out=token_out):
        self.chain_name = chain_name
        self.token_in = token_in
        self.token_out = token_out
        self.base_url = AGGREGATOR_DOMAIN
        self.amount_in = 150000000000000000000000

    def get_swap_route_v1(self):
        # Get the path to be called
        target_path = f"/{self.chain_name}/api/v1/routes"

        # Specify the call parameters
        target_path_config = {
            'params': {
                'tokenIn': self.token_in.address,
                'tokenOut': self.token_out.address,
                'amountIn': str(self.amount_in)
            }
        }

        # Call the API with requests to handle async calls
        try:
            print("\nCalling [V1] Get Swap Route...")
            response = requests.get(self.base_url + target_path, params=target_path_config['params'])

            print("[V1] GET Response:")
            print(response.json())
            return response.json().get('data')
        except requests.exceptions.RequestException as error:
            print(f"An error occurred: {error}")