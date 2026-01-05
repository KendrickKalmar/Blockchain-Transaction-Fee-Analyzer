# Setup Instructions

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure the tool:**
   ```bash
   cp config/config.example.py config/config.py
   ```
   Then edit `config/config.py` and fill in your API keys and addresses.

3. **Run analysis:**
   ```bash
   python networks/ethereum.py
   ```

## Detailed Configuration

### Step 1: Get API Keys

#### Etherscan API (for Ethereum, Arbitrum, Polygon)
1. Go to [etherscan.io](https://etherscan.io/)
2. Create a free account
3. Navigate to API-KEYs section
4. Create a new API key
5. Copy the key to `config/config.py`

#### Litecoin
No API key required - uses public API.

### Step 2: Configure Addresses

Edit `config/config.py` and set your wallet addresses:

```python
ADDRESSES = {
    "ethereum": "0xYourEthereumAddress",
    "arbitrum": "0xYourArbitrumAddress",
    "polygon": "0xYourPolygonAddress",
    "litecoin": "LYourLitecoinAddress",
}
```

### Step 3: Adjust Settings (Optional)

You can modify analysis parameters in `config/config.py`:

```python
SETTINGS = {
    "max_my_transactions": 10,  # How many of your transactions to analyze
    "max_network_examples": 20   # How many network transactions to compare
}
```

## Running Analysis

Each network has its own script:

- `python networks/ethereum.py` - Analyze Ethereum mainnet
- `python networks/arbitrum.py` - Analyze Arbitrum
- `python networks/polygon.py` - Analyze Polygon
- `python networks/litecoin.py` - Analyze Litecoin

## Output Location

All results are saved in the `results/` directory:
- JSON files with raw data
- Text reports with analysis
- Log files with execution details

## Troubleshooting

### "Module not found" error
Make sure you're running from the project root directory and have installed dependencies:
```bash
pip install -r requirements.txt
```

### "Address not configured" error
Check that you've set the address in `config/config.py` for the network you're analyzing.

### "API key not configured" error
Make sure you've copied `config.example.py` to `config.py` and filled in your API key.

### No transactions found
- Verify your address has recent transactions
- Check that the address format is correct for the network
- Some networks only analyze confirmed transactions

