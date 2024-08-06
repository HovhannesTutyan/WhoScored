import requests

# BlockCypher API endpoint for Bitcoin
base_url = "https://api.blockcypher.com/v1/btc/main"

def get_latest_block():
    # Fetch the latest block
    response = requests.get(f"{base_url}")
    latest_block = response.json().get('height')
    return latest_block

def get_block_transactions(block_height):
    # Fetch transactions in a specific block
    response = requests.get(f"{base_url}/blocks/{block_height}")
    block_data = response.json()
    return block_data.get('txids', [])

def get_transaction_details(txid):
    # Fetch details of a specific transaction
    response = requests.get(f"{base_url}/txs/{txid}")
    return response.json()

def is_large_transaction(transaction, threshold=10):
    # Check if the transaction involves a large amount (e.g., more than 10 BTC)
    total_btc = sum(output['value'] for output in transaction['outputs']) / 10**8
    return total_btc > threshold

def track_large_transactions():
    latest_block = get_latest_block()
    transactions = get_block_transactions(latest_block)

    print(f"Tracking transactions in block {latest_block}...")

    for txid in transactions:
        transaction = get_transaction_details(txid)
        if is_large_transaction(transaction):
            print(f"Large transaction detected: {txid}")
            print(f"Total BTC: {sum(output['value'] for output in transaction['outputs']) / 10**8}")

# Track large transactions in the latest block
track_large_transactions()
