"""
Ethereum Network Transaction Fee Analyzer

Collects and analyzes transaction fee data from Ethereum mainnet.
Compares your transaction fees with network averages.
"""

import requests
import time
import json
import logging
import os
import sys
from datetime import datetime
from collections import defaultdict
from tabulate import tabulate

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
from config import ETHERSCAN_API_KEY, ADDRESSES, TOKENS, SETTINGS, CHAIN_IDS, API_ENDPOINTS

log_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'ethereum.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

API_KEY = ETHERSCAN_API_KEY
MY_ADDRESS = ADDRESSES.get("ethereum", "")
BASE_API_URL = API_ENDPOINTS["ethereum"]
NETWORK_TOKENS = TOKENS.get("ethereum", {})
MAX_MY_TRANSACTIONS = SETTINGS["max_my_transactions"]
MAX_NETWORK_EXAMPLES = SETTINGS["max_network_examples"]
CHAIN_ID = CHAIN_IDS["ethereum"]

TOKEN_DISPLAY_NAMES = {
    "eth": "ETH",
    "usdt": "USDT",
    "usdc": "USDC"
}


def wei_to_eth(wei_value):
    """Convert wei to ETH."""
    return wei_value / 10**18


def get_transactions(address, contract_address=None, limit=5):
    """Get transaction list from Ethereum network."""
    action = "tokentx" if contract_address else "txlist"
    params = {
        "module": "account",
        "action": action,
        "address": address,
        "contractaddress": contract_address,
        "page": 1,
        "offset": limit,
        "sort": "desc",
        "apikey": API_KEY
    }
    
    try:
        response = requests.get(BASE_API_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if data["status"] == "1":
            logging.info(f"Retrieved {len(data['result'])} transactions for {contract_address or 'ETH'}")
            return data["result"]
        return []
    except Exception as e:
        logging.error(f"Error retrieving transactions: {str(e)}")
        return []


def get_block_transactions(block_number):
    """Get all transactions in an Ethereum block."""
    params = {
        "module": "proxy",
        "action": "eth_getBlockByNumber",
        "tag": hex(block_number),
        "boolean": "true",
        "apikey": API_KEY
    }
    
    try:
        response = requests.get(BASE_API_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("result", {}).get("transactions", [])
    except Exception as e:
        logging.error(f"Error retrieving block {block_number}: {str(e)}")
        return []


def get_transaction_receipt(tx_hash):
    """Get transaction receipt from Ethereum."""
    params = {
        "module": "proxy",
        "action": "eth_getTransactionReceipt",
        "txhash": tx_hash,
        "apikey": API_KEY
    }
    
    try:
        response = requests.get(BASE_API_URL, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("result")
    except Exception as e:
        logging.error(f"Error retrieving receipt {tx_hash}: {str(e)}")
        return None


def is_token_transfer(tx, token_address):
    """Check if transaction is a token transfer."""
    if token_address == "0x0000000000000000000000000000000000000000":
        return tx.get("to") and int(tx.get("value", "0"), 16) > 0
    else:
        return (tx.get("to") and 
                tx["to"].lower() == token_address.lower() and 
                tx.get("input", "").startswith("0xa9059cbb"))


def collect_my_transactions():
    """Collect user transactions from Ethereum network."""
    logging.info("Collecting user transactions from Ethereum...")
    my_transactions = []
    blocks_to_analyze = set()
    
    for token_name, token_address in NETWORK_TOKENS.items():
        logging.info(f"Collecting {MAX_MY_TRANSACTIONS} transactions for {token_name}")
        txs = get_transactions(MY_ADDRESS, None if token_name == "eth" else token_address, MAX_MY_TRANSACTIONS)
        
        for tx in txs:
            block_number = int(tx.get("blockNumber", "0"))
            if block_number > 0:
                transaction_data = {
                    "token": token_name,
                    "hash": tx.get("hash", ""),
                    "block": block_number,
                    "gas_used": int(tx.get("gasUsed", "0")),
                    "gas_price": int(tx.get("gasPrice", "0")),
                    "gas_limit": int(tx.get("gas", "0")),
                    "fee": int(tx.get("gasUsed", "0")) * int(tx.get("gasPrice", "0"))
                }
                my_transactions.append(transaction_data)
                blocks_to_analyze.add(block_number)
        
        time.sleep(0.3)
    
    logging.info(f"Collected {len(my_transactions)} user transactions in {len(blocks_to_analyze)} blocks")
    return my_transactions, list(blocks_to_analyze)


def collect_network_transfers(blocks, tokens_to_find):
    """Collect token transfers from specified blocks."""
    logging.info(f"Searching for transfers in {len(blocks)} blocks...")
    network_data = []
    
    for i, block in enumerate(blocks):
        logging.info(f"Analyzing block {block} ({i+1}/{len(blocks)})")
        txs_in_block = get_block_transactions(block)
        logging.info(f"Found {len(txs_in_block)} transactions in block {block}")
        
        token_counters = {token: 0 for token in tokens_to_find}
        
        for tx in txs_in_block:
            for token_name, token_address in NETWORK_TOKENS.items():
                if token_name not in tokens_to_find:
                    continue
                    
                if token_counters[token_name] >= MAX_NETWORK_EXAMPLES:
                    continue
                    
                if is_token_transfer(tx, token_address):
                    receipt = get_transaction_receipt(tx.get("hash", ""))
                    if receipt:
                        gas_used = int(receipt.get("gasUsed", "0"), 16)
                        gas_price = int(tx.get("gasPrice", "0"), 16)
                        gas_limit = int(tx.get("gas", "0"), 16)
                        fee = gas_used * gas_price
                        
                        transfer_data = {
                            "token": token_name,
                            "hash": tx.get("hash", ""),
                            "block": block,
                            "gas_used": gas_used,
                            "gas_price": gas_price,
                            "gas_limit": gas_limit,
                            "fee": fee
                        }
                        network_data.append(transfer_data)
                        token_counters[token_name] += 1
        
        found_in_block = sum(token_counters.values())
        logging.info(f"Found {found_in_block} transfers in block {block}")
        
        time.sleep(0.3)
    
    return network_data


def analyze_data(data):
    """Analyze collected transaction data."""
    my_stats = defaultdict(lambda: {
        "count": 0,
        "total_gas_used": 0,
        "total_gas_price": 0,
        "total_gas_limit": 0,
        "total_fee": 0
    })
    
    for tx in data["my_transactions"]:
        token = tx["token"]
        my_stats[token]["count"] += 1
        my_stats[token]["total_gas_used"] += tx["gas_used"]
        my_stats[token]["total_gas_price"] += tx["gas_price"]
        my_stats[token]["total_gas_limit"] += tx["gas_limit"]
        my_stats[token]["total_fee"] += tx["fee"]
    
    network_stats = defaultdict(lambda: {
        "count": 0,
        "total_gas_used": 0,
        "total_gas_price": 0,
        "total_gas_limit": 0,
        "total_fee": 0
    })
    
    for tx in data["network_transfers"]:
        token = tx["token"]
        network_stats[token]["count"] += 1
        network_stats[token]["total_gas_used"] += tx["gas_used"]
        network_stats[token]["total_gas_price"] += tx["gas_price"]
        network_stats[token]["total_gas_limit"] += tx["gas_limit"]
        network_stats[token]["total_fee"] += tx["fee"]
    
    for stats in [my_stats, network_stats]:
        for token in stats:
            if stats[token]["count"] > 0:
                stats[token]["avg_gas_used"] = stats[token]["total_gas_used"] / stats[token]["count"]
                stats[token]["avg_gas_price"] = stats[token]["total_gas_price"] / stats[token]["count"]
                stats[token]["avg_gas_limit"] = stats[token]["total_gas_limit"] / stats[token]["count"]
                stats[token]["avg_fee"] = stats[token]["total_fee"] / stats[token]["count"]
    
    return my_stats, network_stats


def generate_report(my_stats, network_stats, data):
    """Generate analysis report."""
    table_data = []
    
    for token_name in data["tokens_analyzed"]:
        my_data = my_stats.get(token_name, {})
        network_data = network_stats.get(token_name, {})
        
        if not my_data or not network_data:
            continue
        
        network_fee = network_data.get("avg_fee", 0)
        my_fee = my_data.get("avg_fee", 0)
        fee_diff_percent = ((my_fee - network_fee) / network_fee * 100) if network_fee > 0 else 0
        
        network_gas_limit = network_data.get("avg_gas_limit", 0)
        my_gas_limit = my_data.get("avg_gas_limit", 0)
        gas_limit_diff_percent = ((my_gas_limit - network_gas_limit) / network_gas_limit * 100) if network_gas_limit > 0 else 0
        
        table_data.append([
            TOKEN_DISPLAY_NAMES.get(token_name, token_name),
            my_data.get("count", 0),
            f"{my_data.get('avg_gas_used', 0):.0f}",
            f"{my_data.get('avg_gas_limit', 0):.0f}",
            f"{my_data.get('avg_gas_price', 0) / 10**9:.2f} Gwei",
            f"{wei_to_eth(my_data.get('avg_fee', 0)):.6f} ETH",
            network_data.get("count", 0),
            f"{network_data.get('avg_gas_used', 0):.0f}",
            f"{network_data.get('avg_gas_limit', 0):.0f}",
            f"{network_data.get('avg_gas_price', 0) / 10**9:.2f} Gwei",
            f"{wei_to_eth(network_data.get('avg_fee', 0)):.6f} ETH",
            f"{fee_diff_percent:+.2f}%",
            f"{gas_limit_diff_percent:+.2f}%"
        ])
    
    return table_data


def main():
    """Main execution function."""
    if not MY_ADDRESS:
        logging.error("Ethereum address not configured. Please set ADDRESSES['ethereum'] in config/config.py")
        return
    
    if not API_KEY or API_KEY == "YOUR_ETHERSCAN_API_KEY_HERE":
        logging.error("Etherscan API key not configured. Please set ETHERSCAN_API_KEY in config/config.py")
        return
    
    logging.info("Starting Ethereum transaction fee analyzer...")
    
    my_transactions, blocks = collect_my_transactions()
    
    if not my_transactions:
        logging.warning("No user transactions found. Analysis cannot proceed.")
        return
    
    tokens_in_my_txs = set(tx["token"] for tx in my_transactions)
    logging.info(f"Searching for token transfers: {list(tokens_in_my_txs)}")
    
    network_data = collect_network_transfers(blocks, tokens_in_my_txs)
    
    output_data = {
        "timestamp": datetime.now().isoformat(),
        "network": "Ethereum",
        "my_address": MY_ADDRESS,
        "settings": {
            "max_my_transactions": MAX_MY_TRANSACTIONS,
            "max_network_examples": MAX_NETWORK_EXAMPLES
        },
        "blocks_analyzed": blocks,
        "tokens_analyzed": list(tokens_in_my_txs),
        "my_transactions": my_transactions,
        "network_transfers": network_data
    }
    
    results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
    os.makedirs(results_dir, exist_ok=True)
    data_filename = os.path.join(results_dir, f"ethereum_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    
    with open(data_filename, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    logging.info(f"Data saved to {data_filename}")
    
    my_stats, network_stats = analyze_data(output_data)
    
    headers = [
        "Token", "My Tx", "Avg Gas Used", "Avg Gas Limit", "Avg Gas Price", "Avg Fee",
        "Network Tx", "Avg Gas Used", "Avg Gas Limit", "Avg Gas Price", "Avg Fee",
        "Fee Diff", "Gas Limit Diff"
    ]
    
    table_data = generate_report(my_stats, network_stats, output_data)
    
    print(f"\nEthereum Transaction Fee Analysis - {output_data['timestamp']}")
    print(f"Address: {output_data['my_address']}")
    print(f"Settings: {output_data['settings']['max_my_transactions']} user tx/token, {output_data['settings']['max_network_examples']} examples/token")
    print(f"Blocks analyzed: {len(output_data['blocks_analyzed'])}")
    print(f"Tokens analyzed: {', '.join([TOKEN_DISPLAY_NAMES.get(t, t) for t in output_data['tokens_analyzed']])}")
    print(f"User transactions: {len(output_data['my_transactions'])}")
    print(f"Network transfers: {len(output_data['network_transfers'])}")
    print()
    
    print("Transaction Fee Analysis Results:")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    report_filename = data_filename.replace('.json', '_report.txt')
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(f"Ethereum Transaction Fee Analysis - {output_data['timestamp']}\n")
        f.write(f"Address: {output_data['my_address']}\n")
        f.write(f"Settings: {output_data['settings']['max_my_transactions']} user tx/token, {output_data['settings']['max_network_examples']} examples/token\n")
        f.write(f"Blocks analyzed: {len(output_data['blocks_analyzed'])}\n")
        f.write(f"Tokens analyzed: {', '.join([TOKEN_DISPLAY_NAMES.get(t, t) for t in output_data['tokens_analyzed']])}\n")
        f.write(f"User transactions: {len(output_data['my_transactions'])}\n")
        f.write(f"Network transfers: {len(output_data['network_transfers'])}\n\n")
        f.write("Transaction Fee Analysis Results:\n")
        f.write(tabulate(table_data, headers=headers, tablefmt="grid"))
    
    logging.info(f"Report saved to {report_filename}")
    logging.info("Analysis complete!")


if __name__ == "__main__":
    main()

