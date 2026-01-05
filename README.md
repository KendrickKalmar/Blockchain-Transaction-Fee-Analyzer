# Blockchain Transaction Fee Analyzer

A comprehensive tool for analyzing and comparing transaction fees across multiple blockchain networks. This tool helps you understand how your transaction fees compare to network averages and identify potential optimization opportunities.

## Supported Networks

- **Ethereum** - Mainnet transaction fee analysis
- **Arbitrum** - Layer 2 transaction fee analysis
- **Polygon** - Polygon network transaction fee analysis
- **Litecoin** - UTXO-based transaction fee analysis

## Features

- Collects your transaction history from supported networks
- Analyzes network transaction patterns in the same blocks
- Compares your fees with network averages
- Generates detailed reports with statistics
- Supports multiple tokens per network
- Configurable analysis parameters

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd blockchain-fee-analyzer
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Test the installation:
```bash
python test_imports.py
```

4. Configure your settings:
   - Copy the example config: `cp config/config.example.py config/config.py`
   - Edit `config/config.py`
   - Set your API keys and wallet addresses
   - Adjust analysis parameters if needed
   
   See [CONFIGURATION.md](CONFIGURATION.md) for detailed configuration guide.

## Configuration

**For detailed configuration guide, see [CONFIGURATION.md](CONFIGURATION.md)**

Edit `config/config.py` to set up your environment:

```python
# Etherscan API key (required for Ethereum, Arbitrum, Polygon)
ETHERSCAN_API_KEY = "your_api_key_here"

# Your wallet addresses
ADDRESSES = {
    "ethereum": "0x...",
    "arbitrum": "0x...",
    "polygon": "0x...",
    "litecoin": "L...",
}

# Analysis settings
SETTINGS = {
    "max_my_transactions": 10,  # Number of your transactions to analyze per token
    "max_network_examples": 20   # Number of network transactions to compare
}
```

### Getting API Keys

- **Etherscan API**: Register at [etherscan.io](https://etherscan.io/apis) to get a free API key
- **Litecoin**: Uses public API, no key required

**Important Configuration Notes:**
- **CHAIN_ID**: Unique identifier for each network (see [CONFIGURATION.md](CONFIGURATION.md) for details)
  - Ethereum: 1, Arbitrum: 42161, Polygon: 137
  - Find all chain IDs at [chainlist.org](https://chainlist.org/)
- **Token Addresses**: Use zero address `0x0000...` for native tokens (ETH, POL)
- **Address Format**: Must match network requirements (0x for EVM, L/M for Litecoin)

## Usage

### Running Analysis for a Specific Network

Each network has its own analysis script:

```bash
# Ethereum
python networks/ethereum.py

# Arbitrum
python networks/arbitrum.py

# Polygon
python networks/polygon.py

# Litecoin
python networks/litecoin.py
```

### Output

Results are saved in the `results/` directory:

- **JSON files**: Raw transaction data (`*_data_*.json`)
- **Report files**: Human-readable analysis reports (`*_report_*.txt`)
- **Log files**: Execution logs (`*.log`)

## How It Works

1. **Data Collection**: 
   - Retrieves your recent transactions from the specified network
   - Identifies blocks containing your transactions
   - Collects similar transactions from those blocks

2. **Analysis**:
   - Calculates average gas usage, gas prices, and fees
   - Compares your transactions with network averages
   - Identifies differences in fee structures

3. **Reporting**:
   - Generates comparison tables
   - Shows percentage differences
   - Provides detailed statistics

## Project Structure

```
.
├── config/
│   └── config.py          # Configuration file
├── networks/
│   ├── ethereum.py        # Ethereum analyzer
│   ├── arbitrum.py        # Arbitrum analyzer
│   ├── polygon.py         # Polygon analyzer
│   └── litecoin.py        # Litecoin analyzer
├── results/               # Output directory (created automatically)
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Understanding the Results

The analysis reports include:

- **Token**: The token being analyzed
- **My Tx**: Number of your transactions
- **Avg Gas Used**: Average gas consumed
- **Avg Gas Limit**: Average gas limit set
- **Avg Gas Price**: Average gas price in Gwei
- **Avg Fee**: Average transaction fee
- **Network Tx**: Number of network transactions compared
- **Fee Diff**: Percentage difference in fees
- **Gas Limit Diff**: Percentage difference in gas limits

### Interpreting Results

- **Negative percentage**: You're paying less than network average (good)
- **Positive percentage**: You're paying more than network average (consider optimization)
- **Near zero**: Your fees are aligned with network average

## Limitations

- Analysis is based on recent transactions only
- Network comparison uses transactions from the same blocks
- Results may vary based on network conditions at the time of your transactions
- Some networks may have rate limits on API calls

## exp. of Result
```
+---------+--------------+----------------+-----------------+-----------------+----------------+---------------+----------------+-----------------+-----------------+----------------+--------------------+---------------------+--------------------+---------------------+
| Токен   |   Мои транз. |   Ср. gas used |   Ср. gas limit | Ср. gas price   | Ср. комиссия   |   Сеть транз. |   Ср. gas used |   Ср. gas limit | Ср. gas price   | Ср. комиссия   | Разница комиссий   | Разница gas limit   | Разница gas used   | Разница gas price   |
+=========+==============+================+=================+=================+================+===============+================+=================+=================+================+====================+=====================+====================+=====================+
| USDT    |           10 |          42270 |         1000000 | 0.03 Gwei       | 0.00000127 ETH |            12 |          40574 |         1223386 | 0.03 Gwei       | 0.00000139 ETH | -8.99%             | -18.26%             | +4.18%             | -12.93%             |
+---------+--------------+----------------+-----------------+-----------------+----------------+---------------+----------------+-----------------+-----------------+----------------+--------------------+---------------------+--------------------+---------------------+
| USDC    |           10 |          50102 |         1000000 | 0.03 Gwei       | 0.00000156 ETH |            10 |          49049 |          468669 | 0.02 Gwei       | 0.00000086 ETH | +80.62%            | +113.37%            | +2.15%             | +66.09%             |
+---------+--------------+----------------+-----------------+-----------------+----------------+---------------+----------------+-----------------+-----------------+----------------+--------------------+---------------------+--------------------+---------------------+
| ARB     |           10 |          51795 |         1000000 | 0.03 Gwei       | 0.00000165 ETH |             3 |          44870 |         1000000 | 0.03 Gwei       | 0.00000135 ETH | +22.84%            | +0.00%              | +15.43%            | +5.21%              |
+---------+--------------+----------------+-----------------+-----------------+----------------+---------------+----------------+-----------------+-----------------+----------------+--------------------+---------------------+--------------------+---------------------+
```

## Troubleshooting

### "Address not configured" error
- Make sure you've set the address in `config/config.py` for the network you're analyzing

### "API key not configured" error
- Set your Etherscan API key in `config/config.py`
- Ensure the API key is valid and has sufficient rate limits

### "No transactions found" warning
- Verify your address has recent transactions on the network
- Check that the address format is correct
- Some networks may require confirmed transactions only





