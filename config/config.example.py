"""
Configuration file template for blockchain transaction fee analyzer.
Copy this file to config.py and fill in your values.
"""

# Etherscan API configuration
ETHERSCAN_API_KEY = "YOUR_ETHERSCAN_API_KEY_HERE"

# Your wallet addresses for analysis
ADDRESSES = {
    "ethereum": "YOUR_ETHEREUM_ADDRESS_HERE",
    "arbitrum": "YOUR_ARBITRUM_ADDRESS_HERE",
    "polygon": "YOUR_POLYGON_ADDRESS_HERE",
    "solana": "YOUR_SOLANA_ADDRESS_HERE",
    "litecoin": "YOUR_LITECOIN_ADDRESS_HERE"
}

# Token configurations for each network
TOKENS = {
    "ethereum": {
        "eth": "0x0000000000000000000000000000000000000000",
        "usdt": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
        "usdc": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
    },
    "arbitrum": {
        "eth": "0x0000000000000000000000000000000000000000",
        "usdt": "0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9",
        "usdc": "0xaf88d065e77c8cc2239327c5edb3a432268e5831"
    },
    "polygon": {
        "pol": "0x0000000000000000000000000000000000000000",
        "usdt": "0xc2132d05d31c914a87c6611c10748aeb04b58e8f",
        "usdc": "0x3c499c542cef5e3811e1192ce70d8cc03d5c3359"
    },
    "solana": {
        "sol": "native",
        "usdc": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
        "usdt": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"
    }
}

# Analysis settings
SETTINGS = {
    "max_my_transactions": 10,
    "max_network_examples": 20
}

# Network chain IDs
CHAIN_IDS = {
    "ethereum": 1,
    "arbitrum": 42161,
    "polygon": 137
}

# API endpoints
API_ENDPOINTS = {
    "ethereum": "https://api.etherscan.io/api",
    "arbitrum": "https://api.etherscan.io/v2/api",
    "polygon": "https://api.etherscan.io/v2/api",
    "solana": [
        "https://api.mainnet-beta.solana.com",
        "https://solana-api.projectserum.com"
    ],
    "litecoin": "https://litecoinspace.org/api"
}

