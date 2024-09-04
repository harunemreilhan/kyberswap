import random
import time
import inquirer
from termcolor import colored
from web3 import Web3
import datetime
import os
import logging
from src.check_balances import get_token_balance
from src.constants import usdt, token
from main import Manager



logging.basicConfig(filename='app.log', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize web3 connection
web3 = Web3(Web3.HTTPProvider('https://bsc-dataseed.binance.org/'))
GAS_PRICE = web3.eth.gas_price
GAS_LIMIT = 21000


def clear_screen():
    # Clear the terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')

def create_wallet():
    account = web3.eth.account.create()
    return account.address, account.privateKey.hex()

def save_wallets(wallets, filename):
    with open(f"wallets/{filename}", 'a') as file:
        for wallet in wallets:
            address = wallet['address']
            private_key = wallet['private_key']
            file.write(f"{address},{private_key}\n")

def load_wallets(filename):
    wallets = []
    with open(f"wallets/{filename}", 'r') as file:
        for line in file:
            address, private_key = line.strip().split(',')
            wallets.append({'address': address, 'private_key': private_key})
    return wallets

def check_wallets_balance(wallets):
    active_wallets = []
    tx_fee = web3.fromWei((GAS_PRICE * GAS_LIMIT) * 4, 'ether')
    for wallet in wallets:
        address = wallet['address']
        bnb_balance = get_token_balance(wallet=address, token=usdt, in_ether=True)
        token_balance = get_token_balance(wallet=address, token=token)
        if bnb_balance > tx_fee or token_balance > 1:
            active_wallets.append(wallet)
    return active_wallets

def distribute_funds(admin_address, admin_private_key, wallets, total_amount):
    usdt_contract = web3.eth.contract(address=usdt.address, abi=usdt.abi)  # Provide the correct ABI
    nonce = web3.eth.get_transaction_count(admin_address)
    gas_fee_per_tx = GAS_LIMIT * GAS_PRICE + 100
    amount_per_wallet = (total_amount - gas_fee_per_tx * len(wallets)) / len(wallets)

    for wallet in wallets:
        address = wallet['address']
        # Convert the amount to the correct decimals for USDT
        amount_in_usdt = int(amount_per_wallet * (10 ** usdt.decimals))

        # Prepare the transaction to transfer USDT
        tx = usdt_contract.functions.transfer(address, amount_in_usdt).buildTransaction({
            'chainId': web3.eth.chain_id,
            'gas': GAS_LIMIT,
            'gasPrice': GAS_PRICE,
            'nonce': nonce
        })

        # Sign the transaction
        signed_tx = web3.eth.account.sign_transaction(tx, admin_private_key)
        try:
            print(colored(f"Sending {web3.fromWei(amount_in_usdt, 'ether')} USDT to {address}...", 'yellow'))
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            web3.eth.wait_for_transaction_receipt(tx_hash)
            print(colored(f"Successfully sent {web3.fromWei(amount_in_usdt, 'ether')} USDT to {address}", 'green'))
            time.sleep(5)
        except Exception as e:
            logging.error(f"Failed to send USDT to {address}: {e}")
            print(colored(f"Failed to send USDT to {address}: {e}", 'red'))
        nonce += 1

def send_bnb(address_from, private_key, address_to, amount_in_bnb):
    amount_in_bnb = amount_in_bnb - GAS_LIMIT * GAS_PRICE
    tx = {
        'to': address_to,
        'value': amount_in_bnb,
        'gas': GAS_LIMIT,
        'gasPrice': GAS_PRICE,
        'nonce': web3.eth.get_transaction_count(address_from)
    }
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    try:
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        web3.eth.wait_for_transaction_receipt(tx_hash)
        print(colored(f"Successfully sent {web3.fromWei(amount_in_bnb, 'ether')} BNB to {address_to}", 'green'))
    except Exception as e:
        logging.error(f"Failed to send BNB from {address_from} to {address_to}: {e}")
        print(colored(f"Failed to send BNB from {address_from} to {address_to}: {e}", 'red'))
    time.sleep(5)

def generate_volume():
    while True:
        clear_screen()

        # Ask the user whether to create new wallets or use existing ones
        choices = ["Create New Wallets", "Continue with Existing Wallets", "Previous Menu"]
        questions = [
            inquirer.List('option', message=colored("Choose an option:", 'cyan'), choices=choices)
        ]
        answer = inquirer.prompt(questions)['option']

        if answer == "Previous Menu":
            break
        elif answer == "Create New Wallets":
            filename = f"wallets_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

            admin_address, admin_private_key = create_wallet()
            print(colored(f"Admin Wallet Created. Address: {admin_address}", 'green'))
            save_wallets([{'address': admin_address, 'private_key': admin_private_key}], filename)

            print(colored("Please deposit funds to the admin wallet...", 'yellow'))
            total_amount = web3.eth.get_balance(admin_address)
            while total_amount == 0:
                total_amount = web3.eth.get_balance(admin_address)
                time.sleep(2)
            
            print(colored(f"Admin Wallet Balance: {web3.fromWei(total_amount, 'ether')} BNB", 'green'))

            num_wallets = int(input(colored("Enter number of wallets to create: ", 'cyan')))
            wallets = [create_wallet() for _ in range(num_wallets)]
            wallets = [{'address': address, 'private_key': private_key} for address, private_key in wallets]

            save_wallets(wallets, filename)
            print(colored(f"Wallets created and saved to {filename}", 'green'))

            distribute_funds(admin_address, admin_private_key, wallets, total_amount)


        elif answer == "Continue with Existing Wallets":
            # List existing wallet files and let the user choose one
            files = [f for f in os.listdir('wallets') if f.startswith("wallets_") and f.endswith(".txt")]
            questions = [inquirer.List('file', message=colored("Choose a wallet file:", 'cyan'), choices=files)]
            selected_file = inquirer.prompt(questions)['file']

            filename = selected_file


        increase_holder = inquirer.confirm(colored("Increase holder?", 'cyan'), default=True)
        if increase_holder:
            print(colored("Option to increase holder selected. Implement this functionality...", 'green'))
        else:
            print(colored("Normal buy/sell operations will be performed...", 'green'))

    # Implement buying and selling logic here
        while True:
            cuurent_wallets = load_wallets(filename)
            active_wallets = check_wallets_balance(cuurent_wallets)
            for wallet in active_wallets:
                swap = Manager(wallet['private_key'])
                buyOrSell = random.choice([0, 1])
                token_balance = get_token_balance(wallet['address'], token)
                bnb_balance = get_token_balance(wallet['address'], usdt)
                gas_fee_per_tx = web3.fromWei((GAS_PRICE * GAS_LIMIT), 'ether')
                if bnb_balance <= gas_fee_per_tx  * 2:
                    continue

                if buyOrSell == 0: # Buy
                    if bnb_balance > gas_fee_per_tx:
                        amount_in_bnb = bnb_balance
                        try:
                            swap.buy(usdt, token, amount_in_bnb)
                        except Exception as e:
                            logging.error(f"Error during buy operation: {e}")
                            if "insufficient funds for" in str(e):
                                continue
                            elif "BNB balance is insufficient for" in str(e):
                                continue
                            else:
                                print(colored(f"Error: {e}", 'red'))
                        time.sleep(5)
                elif buyOrSell == 1: # Sell
                    if token_balance > 1 and increase_holder:
                        amount_in_tokens = token_balance - 1
                        try:
                            swap.sell(token, usdt, amount_in_tokens)
                        except Exception as e:
                            logging.error(f"Error during sell operation: {e}")
                            if "nonce too low" in str(e).lower():
                                print(colored("Nonce too low. Retrying...", 'yellow'))
                                swap.sell(token, usdt, amount_in_tokens)
                        time.sleep(5)
                        newBnbBalance = get_token_balance(wallet['address'], usdt)
                        newWallet = create_wallet()
                        newWallet = {
                            "address": newWallet[0],
                            "private_key": newWallet[1]
                        }
                        save_wallets([newWallet], filename)
                        send_bnb(wallet['address'], wallet['private_key'], newWallet['address'], newBnbBalance)
                        time.sleep(5)

                    elif token_balance > 0 and not increase_holder:
                        amount_in_tokens = token_balance
                        try:
                            swap.sell(token, usdt, amount_in_tokens)
                        except Exception as e:
                            logging.error(f"Error during sell operation: {e}")
                            if "nonce too low" in str(e).lower():
                                print(colored("Nonce too low. Retrying...", 'yellow'))
                                swap.sell(token, usdt, amount_in_tokens)
                            else:
                                print(colored(f"Error: {e}", 'red'))
                        time.sleep(5)
                        getTokenBalance = get_token_balance(wallet['address'], token)
                        if getTokenBalance > 0:
                            try:
                                swap.sell(token, usdt, getTokenBalance)
                            except Exception as e:
                                logging.error(f"Error during sell operation: {e}")
                                if "nonce too low" in str(e).lower():
                                    print(colored("Nonce too low. Retrying...", 'yellow'))
                                    swap.sell(token, usdt, getTokenBalance)
                                else:
                                    print(colored(f"Error: {e}", 'red'))
                        newBnbBalance = get_token_balance(wallet['address'], usdt)
                        newWallet = create_wallet()
                        newWallet = {
                            "address": newWallet[0],
                            "private_key": newWallet[1]
                        }
                        save_wallets([newWallet], filename)
                        send_bnb(wallet['address'], wallet['private_key'], newWallet['address'], newBnbBalance)
                        time.sleep(5)
                else:
                    pass

def clear_wallets_from_tokens():
    while True:
        clear_screen()    
        files = [f for f in os.listdir('wallets') if f.startswith("wallets_") and f.endswith(".txt")]
        files.append("Previous Menu")
        questions = [inquirer.List('file', message=colored("Choose a wallet file:", 'cyan'), choices=files)]
        answers = inquirer.prompt(questions)

        if answers['file'] == "Previous Menu":
            break

        wallets = load_wallets(answers['file'])

        for wallet in wallets:
            swap = Manager(wallet['private_key'])
            token_balance = get_token_balance(wallet['address'], token)
            if token_balance > 1:
                try:
                    swap.sell(token, usdt, token_balance - 1)
                except Exception as e:
                    logging.error(f"Error during sell operation: {e}")
                    if "nonce too low" in str(e).lower():
                        print(colored("Nonce too low. Retrying...", 'yellow'))
                        swap.sell(token, usdt, token_balance - 1)
        
        print(colored("Tokens in the selected wallets have been cleared.\n", 'green'))
        time.sleep(3)

def clear_wallets_from_bnb():
    while True:
        clear_screen()
        files = [f for f in os.listdir('wallets') if f.startswith("wallets_") and f.endswith(".txt")]
        files.append("Previous Menu")
        questions = [inquirer.List('file', message=colored("Choose a wallet file:", 'cyan'), choices=files)]
        answers = inquirer.prompt(questions)

        if answers['file'] == "Previous Menu":
            break

        wallets = load_wallets(answers['file'])

        dest_address = input(colored("Enter the destination wallet address to collect all BNB: ", 'cyan'))

        for wallet in wallets:
            balance = web3.eth.get_balance(wallet['address']) - GAS_LIMIT * GAS_PRICE
            if balance > 0:
                tx = {
                    'to': dest_address,
                    'value': balance,
                    'gas': GAS_LIMIT,
                    'gasPrice': GAS_PRICE,
                    'nonce': web3.eth.get_transaction_count(wallet['address'])
                }
                try:
                    signed_tx = web3.eth.account.sign_transaction(tx, wallet['private_key'])
                    print(colored(f"Sending {web3.fromWei(balance, 'ether')} BNB to {dest_address}...", 'yellow'))
                    web3.eth.send_raw_transaction(signed_tx.rawTransaction)
                    print(colored(f"Successfully sent {web3.fromWei(balance, 'ether')} BNB to {dest_address}", 'green'))
                except Exception as e:
                    logging.error(f"Failed to send BNB from {wallet['address']} to {dest_address}: {e}")
                    if "replacement transaction underpriced" in str(e).lower():
                        print(colored("Transaction underpriced. Retrying...", 'yellow'))
                        signed_tx = web3.eth.account.sign_transaction(tx, wallet['private_key'])
                        web3.eth.send_raw_transaction(signed_tx.rawTransaction)
                        print(colored(f"Successfully sent {web3.fromWei(balance, 'ether')} BNB to {dest_address}", 'green'))

        print(colored("All BNB in the selected wallets have been cleared.\n", 'green'))
        time.sleep(3)

def main_menu():
    clear_screen()
    choices = [
        "Generate Volume",
        "Clear Wallets from Tokens",
        "Clear Wallets From BNB",
        "Exit"  # Add Exit option to the main menu
    ]

    questions = [
        inquirer.List('option', message=colored("Choose an option:", 'cyan'), choices=choices, carousel=True)
    ]
    answers = inquirer.prompt(questions)
    return answers['option']

def main():
    while True:
        option = main_menu()
        if option == "Generate Volume":
            generate_volume()
        elif option == "Clear Wallets from Tokens":
            clear_wallets_from_tokens()
        elif option == "Clear Wallets From BNB":
            clear_wallets_from_bnb()
        elif option == "Exit":
            break

if __name__ == "__main__":
    main()