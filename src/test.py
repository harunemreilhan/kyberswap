from constants import token, usdt
from check_balances import get_token_balance


print(get_token_balance(wallet="0x2a9dDbE48D40760e6885d9651ffa08b9C62d37b9", token=usdt, in_ether=True))