# Aggregator Domain
AGGREGATOR_DOMAIN = "https://aggregator-api.kyberswap.com"

# Chain Names
class ChainName:
    MAINNET = "ethereum"
    BSC = "bsc"
    ARBITRUM = "arbitrum"
    MATIC = "polygon"
    OPTIMISM = "optimism"
    AVAX = "avalanche"
    BASE = "base"
    CRONOS = "cronos"
    ZKSYNC = "zksync"
    FANTOM = "fantom"
    LINEA = "linea"
    POLYGONZKEVM = "polygon-zkevm"
    AURORA = "aurora"
    BTTC = "bittorrent"
    SCROLL = "scroll"

# Chain IDs
class ChainId:
    MAINNET = 1
    BSC = 56
    ARBITRUM = 42161
    MATIC = 137
    OPTIMISM = 10
    AVAX = 43114
    BASE = 8453
    CRONOS = 25
    ZKSYNC = 324
    FANTOM = 250
    LINEA = 59144
    POLYGONZKEVM = 1101
    AURORA = 1313161554
    BTTC = 199
    ZKEVM = 1101
    SCROLL = 534352

# Token Interface
class Token:
    def __init__(self, address, chain_id, decimals, symbol=None, name=None):
        self.address = address
        self.chain_id = chain_id
        self.decimals = decimals
        self.symbol = symbol
        self.name = name

# Tokens
token_out = Token(
    address="0x55d398326f99059fF775485246999027B3197955",
    chain_id=str(ChainId.BSC),
    decimals=18,
    symbol="USDT",
    name="Tether USD"
)

token_in = Token(
    address="0x58B26C9b2d32dF1D0E505BCCa2D776698c9bE6B6",
    chain_id=str(ChainId.BSC),
    decimals=18,
    symbol="VOVO",
    name="VOVO Token"
)