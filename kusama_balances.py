from substrateinterface import SubstrateInterface
import math
import csv

substrate = SubstrateInterface(
    url = "wss://kusama-rpc.polkadot.io",
    ss58_format = 2,
    type_registry_preset = 'kusama'
)

with open('kusama_balances.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Address', 'Balance'])

    with open('kusama_addresses.txt') as f:
        addresses = f.read().splitlines()

        counter = 0

        for address in addresses:

            row = [address]

            try:
                result = substrate.query(module='System', storage_function='Account', params=[address])
                balance = result.value['data']['free'] / 10 ** 10
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