"""
Litecoin Network Transaction Fee Analyzer

Collects and analyzes transaction fee data from Litecoin network.
Compares your transaction fees with network averages.
"""

import requests
import time
import json
import logging
import os
import sys
import statistics
from datetime import datetime
from collections import defaultdict
from tabulate import tabulate

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))
from config import ADDRESSES, SETTINGS, API_ENDPOINTS

log_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'litecoin.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

LTC_API_BASE = API_ENDPOINTS["litecoin"]
MY_ADDRESS = ADDRESSES.get("litecoin", "")
MAX_FEE = 8.0
OUR_TRANSACTIONS_LIMIT = 20
NETWORK_BLOCKS_LIMIT = 20


def calculate_fee_per_byte(tx):
    """Calculate fee per byte using vsize."""
    fee_litoshi = tx.get('fee', 0)
    weight = tx.get('weight', 0)
    vsize = weight / 4 if weight > 0 else tx.get('size', 1)
    fee_per_byte = fee_litoshi / vsize if vsize > 0 else 0
    return fee_per_byte, vsize


def is_cpfp_transaction(tx):
    """Check if transaction might be CPFP."""
    vin_count = len(tx.get('vin', []))
    if vin_count > 5:
        fee_litoshi = tx.get('fee', 0)
        vsize = tx.get('weight', 0) / 4 if tx.get('weight', 0) > 0 else tx.get('size', 1)
        fee_per_byte = fee_litoshi / vsize if vsize > 0 else 0
        if fee_per_byte < 2.0:
            return True
    return False


def get_blockchain_info():
    """Get current blockchain height."""
    url = f"{LTC_API_BASE}/blockchain/status"
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logging.error(f"Error retrieving blockchain info: {e}")
    return None


def get_recent_blocks(limit=20):
    """Get recent blocks."""
    blockchain_info = get_blockchain_info()
    if not blockchain_info:
        url = f"{LTC_API_BASE}/blocks"
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                blocks = response.json()
                return [block['height'] for block in blocks[:limit]]
        except Exception as e:
            logging.error(f"Error retrieving blocks: {e}")
        return []
    
    current_height = blockchain_info['blocks']
    start_height = max(1, current_height - limit + 1)
    return list(range(start_height, current_height + 1))


def get_block_transactions(block_height):
    """Get all transactions in a block."""
    hash_url = f"{LTC_API_BASE}/block-height/{block_height}"
    try:
        response = requests.get(hash_url, timeout=30)
        if response.status_code == 200:
            block_hash = response.text.strip()
            txs_url = f"{LTC_API_BASE}/block/{block_hash}/txs"
            response = requests.get(txs_url, timeout=30)
            if response.status_code == 200:
                return response.json()
    except Exception as e:
        logging.error(f"Error retrieving block {block_height}: {e}")
    return []


def get_our_transactions_stats():
    """Get statistics for user transactions."""
    logging.info("Analyzing user transactions...")
    
    if not MY_ADDRESS:
        logging.warning("Litecoin address not configured")
        return None
    
    url = f"{LTC_API_BASE}/address/{MY_ADDRESS}/txs"
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            our_txs = response.json()[:OUR_TRANSACTIONS_LIMIT]
            
            fees = []
            sizes = []
            weights = []
            inputs = []
            outputs = []
            
            for tx in our_txs:
                if not tx.get('status', {}).get('confirmed', False):
                    continue
                    
                fee_per_byte, vsize = calculate_fee_per_byte(tx)
                fees.append(fee_per_byte)
                sizes.append(tx.get('size', 0))
                weights.append(tx.get('weight', 0))
                inputs.append(len(tx.get('vin', [])))
                outputs.append(len(tx.get('vout', [])))
            
            if not fees:
                logging.warning("No confirmed transactions found")
                return None
            
            return {
                'avg_fee_per_byte': statistics.median(fees),
                'avg_size': statistics.median(sizes),
                'avg_weight': statistics.median(weights),
                'avg_inputs': statistics.median(inputs),
                'avg_outputs': statistics.median(outputs),
                'total_txs': len(fees)
            }
    except Exception as e:
        logging.error(f"Error retrieving user transactions: {e}")
    
    return None


def analyze_network_transactions():
    """Analyze network transactions."""
    logging.info("Analyzing network transactions...")
    
    recent_blocks = get_recent_blocks(NETWORK_BLOCKS_LIMIT)
    logging.info(f"Analyzing {len(recent_blocks)} blocks: from {min(recent_blocks)} to {max(recent_blocks)}")
    
    network_transactions = []
    total_blocks_processed = 0
    
    for i, block_height in enumerate(recent_blocks):
        transactions = get_block_transactions(block_height)
        
        if not transactions:
            continue
            
        for tx in transactions:
            if any(vin.get('is_coinbase', False) for vin in tx.get('vin', [])):
                continue
            
            if is_cpfp_transaction(tx):
                continue
            
            fee_per_byte, vsize = calculate_fee_per_byte(tx)
            
            if 0 < fee_per_byte <= MAX_FEE:
                network_transactions.append({
                    'fee_per_byte': fee_per_byte,
                    'size': tx.get('size', 0),
                    'weight': tx.get('weight', 0),
                    'inputs': len(tx.get('vin', [])),
                    'outputs': len(tx.get('vout', [])),
                    'vsize': vsize
                })
        
        total_blocks_processed += 1
        if total_blocks_processed % 5 == 0:
            logging.info(f"Processed {total_blocks_processed}/{len(recent_blocks)} blocks, found {len(network_transactions)} transactions")
        
        time.sleep(0.2)
    
    logging.info(f"Processed blocks: {total_blocks_processed}/{len(recent_blocks)}")
    return network_transactions


def main():
    """Main execution function."""
    if not MY_ADDRESS:
        logging.error("Litecoin address not configured. Please set ADDRESSES['litecoin'] in config/config.py")
        return
    
    logging.info("Starting Litecoin transaction fee analyzer...")
    
    our_stats = get_our_transactions_stats()
    if not our_stats:
        logging.warning("Could not retrieve user transaction statistics")
        return
    
    logging.info(f"Analyzed {our_stats['total_txs']} user transactions")
    
    network_txs = analyze_network_transactions()
    logging.info(f"Analyzed {len(network_txs)} network transactions")
    
    if not network_txs:
        logging.warning("No network transactions found for comparison")
        return
    
    network_fees = [tx['fee_per_byte'] for tx in network_txs]
    network_sizes = [tx['size'] for tx in network_txs]
    network_weights = [tx['weight'] for tx in network_txs]
    network_inputs = [tx['inputs'] for tx in network_txs]
    network_outputs = [tx['outputs'] for tx in network_txs]
    network_vsizes = [tx['vsize'] for tx in network_txs]
    
    network_stats = {
        'avg_fee_per_byte': statistics.median(network_fees),
        'avg_size': statistics.median(network_sizes),
        'avg_weight': statistics.median(network_weights),
        'avg_inputs': statistics.median(network_inputs),
        'avg_outputs': statistics.median(network_outputs),
        'avg_vsize': statistics.median(network_vsizes)
    }
    
    comparison_table = []
    
    fee_diff = our_stats['avg_fee_per_byte'] - network_stats['avg_fee_per_byte']
    fee_diff_percent = (fee_diff / network_stats['avg_fee_per_byte']) * 100 if network_stats['avg_fee_per_byte'] > 0 else 0
    
    comparison_table.append([
        "Fee (lit/vB)",
        f"{our_stats['avg_fee_per_byte']:.2f}",
        f"{network_stats['avg_fee_per_byte']:.2f}",
        f"{fee_diff:+.2f}",
        f"{fee_diff_percent:+.1f}%"
    ])
    
    size_diff = our_stats['avg_size'] - network_stats['avg_size']
    size_diff_percent = (size_diff / network_stats['avg_size']) * 100 if network_stats['avg_size'] > 0 else 0
    
    comparison_table.append([
        "Size (bytes)",
        f"{our_stats['avg_size']:.0f}",
        f"{network_stats['avg_size']:.0f}",
        f"{size_diff:+.0f}",
        f"{size_diff_percent:+.1f}%"
    ])
    
    our_vsize = our_stats['avg_weight'] / 4
    vsize_diff = our_vsize - network_stats['avg_vsize']
    vsize_diff_percent = (vsize_diff / network_stats['avg_vsize']) * 100 if network_stats['avg_vsize'] > 0 else 0
    
    comparison_table.append([
        "Virtual Size (vB)",
        f"{our_vsize:.1f}",
        f"{network_stats['avg_vsize']:.1f}",
        f"{vsize_diff:+.1f}",
        f"{vsize_diff_percent:+.1f}%"
    ])
    
    inputs_diff = our_stats['avg_inputs'] - network_stats['avg_inputs']
    inputs_diff_percent = (inputs_diff / network_stats['avg_inputs']) * 100 if network_stats['avg_inputs'] > 0 else 0
    
    comparison_table.append([
        "Inputs",
        f"{our_stats['avg_inputs']:.1f}",
        f"{network_stats['avg_inputs']:.1f}",
        f"{inputs_diff:+.1f}",
        f"{inputs_diff_percent:+.1f}%"
    ])
    
    outputs_diff = our_stats['avg_outputs'] - network_stats['avg_outputs']
    outputs_diff_percent = (outputs_diff / network_stats['avg_outputs']) * 100 if network_stats['avg_outputs'] > 0 else 0
    
    comparison_table.append([
        "Outputs",
        f"{our_stats['avg_outputs']:.1f}",
        f"{network_stats['avg_outputs']:.1f}",
        f"{outputs_diff:+.1f}",
        f"{outputs_diff_percent:+.1f}%"
    ])
    
    headers = ["Parameter", "User", "Network", "Diff", "Diff %"]
    print("\nLitecoin Transaction Fee Analysis")
    print(f"Address: {MY_ADDRESS}")
    print(f"User transactions analyzed: {our_stats['total_txs']}")
    print(f"Network transactions analyzed: {len(network_txs)}")
    print()
    print("Comparison Table:")
    print(tabulate(comparison_table, headers=headers, tablefmt="grid"))
    
    results_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
    os.makedirs(results_dir, exist_ok=True)
    report_filename = os.path.join(results_dir, f"litecoin_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(f"Litecoin Transaction Fee Analysis - {datetime.now().isoformat()}\n")
        f.write(f"Address: {MY_ADDRESS}\n")
        f.write(f"User transactions analyzed: {our_stats['total_txs']}\n")
        f.write(f"Network transactions analyzed: {len(network_txs)}\n\n")
        f.write("Comparison Table:\n")
        f.write(tabulate(comparison_table, headers=headers, tablefmt="grid"))
    
    logging.info(f"Report saved to {report_filename}")
    logging.info("Analysis complete!")


if __name__ == "__main__":
    main()

