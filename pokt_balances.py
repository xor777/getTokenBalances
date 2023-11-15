#POKT docs https://docs.pokt.network/api-docs/pokt/#/api-docs/pokt/
#POKT portal https://www.portal.pokt.network/

import requests
import csv
import math
import os
from dotenv import load_dotenv

load_dotenv()

portal_id = os.getenv("POKT_PORTAL_ID")

url = f'https://mainnet.gateway.pokt.network/v1/lb/{portal_id}/v1/query/balance'
headers = {'Content-Type': 'application/json'}

with open('pokt_balances.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Address', 'Balance'])

    with open('pokt_addresses.txt') as f:
        addresses = f.read().splitlines()

        counter = 0

        for address in addresses:

            row = [address]

            data = {
                "height": 0,
                "address": address
            }

            try:
                response = requests.post(url, headers = headers, json = data)
                balance = response.json()['balance'] / 1000000
                row.append(balance)
            except(e):
                print(f'Error in response: {e}, response: {response}')
                exit()

            writer.writerow(row)

            counter += 1
            if counter % 10 == 0:
                print(f'{math.floor(counter * 100 / len(addresses))}% completed')
                csvfile.flush()

print('done.')