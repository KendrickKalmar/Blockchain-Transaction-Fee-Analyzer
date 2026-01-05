# Configuration Guide

## Understanding Configuration Parameters

### CHAIN_ID

**What is CHAIN_ID?**
Chain ID is a unique numeric identifier for each blockchain network. It's used by APIs and wallets to distinguish between different networks, especially when multiple networks use the same address format (like EVM-compatible chains).

**Where to find Chain IDs?**
- Official documentation for each network
- [ChainList.org](https://chainlist.org/) - Comprehensive list of all chain IDs
- Block explorers (etherscan.io, polygonscan.com) often show chain ID in network info

**Common Chain IDs:**
- Ethereum Mainnet: `1`
- Arbitrum One: `42161`
- Polygon Mainnet: `137`
- BSC (Binance Smart Chain): `56`
- Avalanche C-Chain: `43114`
- Optimism: `10`

**Why it's needed:**
When using Etherscan API v2 (for Arbitrum, Polygon), you must specify the chain ID to tell the API which network to query. Without it, the API won't know if you want Ethereum, Arbitrum, or Polygon data.

### API Keys

#### Etherscan API Key
- **Required for:** Ethereum, Arbitrum, Polygon
- **Get it from:** [etherscan.io/apis](https://etherscan.io/apis)
- **Free tier:** 5 calls/second, 100,000 calls/day
- **How to get:**
  1. Create free account on etherscan.io
  2. Go to API-KEYs section
  3. Create new API key
  4. Copy and paste into `config/config.py`

#### Litecoin API
- **No API key required** - uses public blockchain explorer API
- Rate limits may apply, but no authentication needed

### Wallet Addresses

**Format requirements:**
- **Ethereum/Arbitrum/Polygon:** Must start with `0x` and be 42 characters
  - Example: `0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb`
- **Litecoin:** Must start with `L` or `M` (legacy) or `ltc1` (bech32)
  - Example: `LTC1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh`
- **Solana:** Base58 encoded, typically 32-44 characters
  - Example: `B2HxKAnUXA2h9Hxn9gzcSyyQkUVFQ7rdPsFtqbjpHTUi`

**Where to find your address:**
- Your wallet application (MetaMask, Trust Wallet, etc.)
- Block explorer after making a transaction
- Exchange withdrawal history

### Token Addresses

**Native tokens:**
- Always use zero address: `0x0000000000000000000000000000000000000000`
- This represents ETH on Ethereum/Arbitrum, POL on Polygon

**ERC-20 tokens:**
- Each token has a unique contract address on each network
- Same token (e.g., USDT) has different addresses on different networks
- Find addresses on:
  - [Etherscan Token Lists](https://etherscan.io/tokens)
  - [Polygonscan Tokens](https://polygonscan.com/tokens)
  - Token's official website/documentation

**Adding new tokens:**
1. Find the token contract address on the network's block explorer
2. Add it to the `TOKENS` dictionary in `config/config.py`
3. Use a descriptive key name (e.g., "usdt", "weth")

### Analysis Settings

**max_my_transactions:**
- How many of YOUR transactions to analyze per token
- Higher = more data, but slower analysis
- Recommended: 5-10 for quick analysis, 20+ for comprehensive

**max_network_examples:**
- How many network transactions to compare against
- Higher = more accurate comparison, but slower
- Recommended: 10-20 for balance of speed and accuracy

### API Endpoints

**Ethereum:**
- Uses Etherscan API v1: `https://api.etherscan.io/api`
- No chain ID needed (defaults to mainnet)

**Arbitrum/Polygon:**
- Uses Etherscan API v2: `https://api.etherscan.io/v2/api`
- Requires chain ID parameter in requests

**Solana:**
- Uses JSON-RPC endpoints
- Multiple endpoints provided for redundancy
- No API key required (public RPC)

**Litecoin:**
- Uses public blockchain explorer API
- No authentication required
- Base URL: `https://litecoinspace.org/api`

## Troubleshooting Configuration

### "Chain ID not found" error
- Check that the network name matches exactly (case-sensitive)
- Verify chain ID value is correct for the network
- See [ChainList.org](https://chainlist.org/) for reference

### "Invalid API key" error
- Verify API key is copied correctly (no extra spaces)
- Check API key is active on etherscan.io
- Ensure you're using the correct API key for the network

### "Address format invalid" error
- Verify address is correct for the network
- Check address format matches network requirements
- Ensure address has had transactions (empty addresses won't work)

### "Token not found" error
- Verify token address is correct for the network
- Check token contract exists on the network
- Some tokens may not be available on all networks

