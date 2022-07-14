import requests
from web3 import Web3
import json

bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))
answer = True
value = input("enter value: ")


def take_info():
    privates = {}
    binance_addresses = {}

    with open('addresses.txt', 'r') as file:
        for line in file.readlines():
            address_info = line.split(':')
            privates[address_info[0]] = address_info[1]
            binance_addresses[address_info[0]] = address_info[2].replace("\n", "")

    return privates, binance_addresses


def send_tx(from_address: str, private_key: str, address_to: str):
    account_from = {
        "private_key": private_key,
        "address": from_address,
    }

    tx_create = web3.eth.account.sign_transaction(
        {
            "nonce": web3.eth.get_transaction_count(account_from["address"]),
            "gasPrice": web3.toWei(5, 'gwei'),
            "gas": 50000,
            "to": web3.toChecksumAddress(address_to),
            "value": web3.toWei(value, "ether"),
        },
        account_from["private_key"],
    )

    tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    web3.eth.wait_for_transaction_receipt(tx_receipt.transactionHash.hex())
    print(f'Transaction successful with hash: { tx_receipt.transactionHash.hex() }')
    return tx_receipt.transactionHash.hex()


def to_txt(hash_data):
    with open("Hashes.txt", "w") as file:
        for hash in hash_data:
            file.write(f"{hash}\n")


def main():
    hash_data = []
    privates, bin_addresses = take_info()
    for address, key in privates.items():
        hash_data.append(send_tx(address, key, bin_addresses.get(address)))
    to_txt(hash_data)


if __name__ == '__main__':
    main()
