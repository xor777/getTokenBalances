# We have list of Ethereum addresses in file eth_addresses.txt
# We need to check Eth balance for each address alongside USDT and USDC
# Put the result into eth_balances.csv

import csv
import math
import json
import os
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

w3 = Web3(Web3.HTTPProvider(os.getenv('ETH_RPC_URL')))

# Tokens we'd like to check alongside Eth
tokens = {'USDT': '0xdac17f958d2ee523a2206206994597c13d831ec7',
          'USDC': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'}

# we need an ABI to call the token contracts to extract balances
with open('erc20_abi.json') as abi:
    erc20_abi = json.load(abi)

with open('eth_balances.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Address', 'Eth','Nonce'] + list(tokens.keys()))

    with open('eth_addresses.txt') as f:
        addresses = [w3.to_checksum_address(addr) for addr in f.read().splitlines()]

        counter = 0

        for address in addresses:

            row = [address]

            eth_balance = w3.eth.get_balance(address)
            eth_balance = w3.from_wei(eth_balance, 'ether')
            row.append(eth_balance)

            # Check nonce just to check whether there were any operations
            nonce = w3.eth.get_transaction_count(address)
            row.append(nonce)

            for token in tokens:
                contract = w3.eth.contract(address=w3.to_checksum_address(tokens[token]), abi=erc20_abi)
                balance = contract.functions.balanceOf(address).call()
                balance = balance / 10 ** contract.functions.decimals().call()
                row.append(balance)

            writer.writerow(row)

            if nonce > 0:
                print(f'nonce >0 here: {row}')

            if balance > 0 or eth_balance > 0:
                print(f'funds found: {row}')

            counter += 1
            if counter % 10 == 0:
                print(f'{math.floor(counter * 100 / len(addresses))}% completed')
                csvfile.flush()

print('done.')
